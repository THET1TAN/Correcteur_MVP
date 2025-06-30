import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip  # Ajout de l'import pour les tooltips
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageOps, ImageTk
from core.decoupage import decouper_texte_en_paragraphes
from core.correction import corriger_paragraphe
import threading
import time
import re  # Import re module for regular expression operations

# Version globale de mettre_a_jour_texte_corrige qui sera redéfinie dans lancer_application
def mettre_a_jour_texte_corrige(texte_corrige):
    pass

def extraire_numero_paragraphe(pid):
    """
    Extrait le numéro d'un ID de paragraphe (ex: 'P10' -> 10)
    """
    match = re.search(r'(\d+)', pid)
    if match:
        return int(match.group(1))
    return 0  # Fallback, though this shouldn't happen

def afficher_correction_progressive(paragraphes, app_vars):
    """
    Corrige les paragraphes un par un de façon séquentielle et les affiche avec une icône d'information
    qui permettra d'accéder aux détails de correction (style, explication).
    
    Args:
        paragraphes (dict): Dictionnaire des paragraphes à corriger
        app_vars (dict): Variables de l'application
    """
    # Récupérer les variables de l'application
    zone_texte_corrige = app_vars.get('zone_texte_corrige')
    statut = app_vars.get('statut')
    info_icon = app_vars.get('info_icon')
    
    # Dictionnaire pour stocker les corrections et leurs métadonnées
    corrections = {}
    meta_info = {}
    
    # Trier les IDs de paragraphes numériquement
    pids_ordonnes = sorted(paragraphes.keys(), key=extraire_numero_paragraphe)
    
    # Dictionnaire pour stocker les tooltips actifs
    tooltip_windows = {}
    
    # -----------------------------------
    #  GESTION DES TOOLTIPS
    # -----------------------------------
    def hide_all_tooltips():
        for pid, win in list(tooltip_windows.items()):
            if win is not None:
                win.destroy()
                tooltip_windows[pid] = None
        
    def show_tooltip(event, pid):
        hide_all_tooltips()
        data = meta_info.get(pid)
        if not data:
            return
        style = data.get("style", "inconnu")
        expl = data.get("explication", "Aucune explication fournie")
        expl = (expl[:150] + "…") if len(expl) > 150 else expl
        tooltip_text = f"Style : {style}\n\nExplication : {expl}"
        
        tooltip = ttk.Toplevel()
        tooltip.overrideredirect(True)  # Retire la bordure de fenêtre
        tooltip.attributes('-topmost', True)  # Place au dessus des autres fenêtres
        
        # Calculer la position du tooltip près du curseur
        x, y = event.x_root + 15, event.y_root + 10
        tooltip.geometry(f"+{x}+{y}")
        
        # Ajouter le contenu du tooltip
        ttk.Label(tooltip, text=tooltip_text, wraplength=300, 
                  padding=5, justify="left", bootstyle="info").pack()
        
        # Stocker la référence au tooltip
        tooltip_windows[pid] = tooltip
    
    def hide_tooltip(event, pid):
        win = tooltip_windows.get(pid)
        if win is not None:
            win.destroy()
            tooltip_windows[pid] = None
    
    zone_texte_corrige.bind("<Button-1>", lambda e: hide_all_tooltips())
    
    # Helper : insertion d'icône info comme widget réel
    def inserer_widget_info(pid):
        """Insère l'icône info pour un paragraphe et connecte tous les bindings."""
        lbl = ttk.Label(zone_texte_corrige, image=info_icon, cursor="hand2")
        lbl.bind("<Enter>", lambda e, p=pid: (zone_texte_corrige.config(cursor="hand2"), show_tooltip(e, p)))
        lbl.bind("<Leave>", lambda e, p=pid: (zone_texte_corrige.config(cursor=""), hide_tooltip(e, p)))
        lbl.bind("<Button-1>", lambda e, p=pid: afficher_info_paragraphe(p, meta_info[p]))
        zone_texte_corrige.window_create(tk.END, window=lbl, padx=0)
        zone_texte_corrige.insert(tk.END, " ")  # espace après l'icône pour respirer
    
    # Afficher tous les paragraphes comme "En attente..." au début
    zone_texte_corrige.config(state="normal")
    zone_texte_corrige.bind("<Key>", lambda e: "break")  # Bloque l’édition, mais l'état reste normal
    zone_texte_corrige.delete("1.0", tk.END)
    
    for pid in pids_ordonnes:
        zone_texte_corrige.insert(tk.END, f"[{pid}] En attente de correction...\n\n")
    
    zone_texte_corrige.config(state="disabled")
    
    # Traitement séquentiel des paragraphes
    def traitement_sequentiel():
        total_paragraphes = len(pids_ordonnes)
        
        for index, pid in enumerate(pids_ordonnes):
            texte = paragraphes[pid]
            statut.set(f"Correction du paragraphe {pid} ({index+1}/{total_paragraphes})...")
            
            try:
                # Correction du paragraphe actuel
                correction, info = corriger_paragraphe(texte)
                
                # Stocker la correction et les métadonnées
                corrections[pid] = correction
                meta_info[pid] = {
                    "style": info.get("style", "inconnu"),
                    "explication": info.get("explication", "Aucune explication fournie")
                }
                
            except Exception as e:
                # En cas d'erreur, mettre à jour avec un message d'erreur
                corrections[pid] = f"Erreur: {str(e)}"
                meta_info[pid] = {
                    "style": "erreur",
                    "explication": f"Une erreur s'est produite: {str(e)}"
                }
            
            # Mise à jour de l'interface graphique - Rafraîchir tout l'affichage
            zone_texte_corrige.config(state="normal")
            zone_texte_corrige.delete("1.0", tk.END)
            
            # Parcourir les paragraphes traités jusqu'à présent
            for j, pid_j in enumerate(pids_ordonnes):
                if pid_j in corrections:
                    # Paragraphe déjà corrigé - insérer l'icône comme widget
                    inserer_widget_info(pid_j)
                    zone_texte_corrige.insert(tk.END, corrections[pid_j])
                else:
                    # Paragraphe en attente
                    zone_texte_corrige.insert(tk.END, f"[{pid_j}] En attente de correction...")
                
                # Ajouter deux sauts de ligne après chaque paragraphe sauf le dernier
                if j < total_paragraphes - 1:
                    zone_texte_corrige.insert(tk.END, "\n\n")
            
            zone_texte_corrige.config(state="disabled")
        
        statut.set(f"Correction terminée - {total_paragraphes} paragraphes traités")
    
    # Lancer le traitement dans un thread séparé
    threading.Thread(target=traitement_sequentiel, daemon=True).start()

def afficher_info_paragraphe(pid, info):
    """
    Affiche une fenêtre pop-up avec les informations supplémentaires sur la correction
    
    Args:
        pid (str): ID du paragraphe
        info (dict): Informations sur la correction (style, explication)
    """
    popup = ttk.Toplevel(title=f"Informations sur le paragraphe {pid}")
    popup.geometry("400x300")
    
    # Cadre pour le contenu
    frame = ttk.Frame(popup, padding=10)
    frame.pack(fill=BOTH, expand=True)
    
    # Titre
    ttk.Label(frame, text=f"Détails de correction - Paragraphe {pid}", 
              font=("TkDefaultFont", 12, "bold")).pack(pady=(0, 10))
    
    # Style détecté
    style_frame = ttk.Frame(frame)
    style_frame.pack(fill=X, pady=5)
    ttk.Label(style_frame, text="Style détecté:", font=("TkDefaultFont", 10, "bold")).pack(side=LEFT, padx=(0, 5))
    ttk.Label(style_frame, text=info.get("style", "Inconnu")).pack(side=LEFT)
    
    # Explication des corrections
    expl_frame = ttk.Frame(frame)
    expl_frame.pack(fill=BOTH, expand=True, pady=5)
    ttk.Label(expl_frame, text="Explications:", font=("TkDefaultFont", 10, "bold")).pack(anchor=W)
    
    expl_text = tk.Text(expl_frame, wrap=tk.WORD, height=8)
    expl_text.pack(fill=BOTH, expand=True, pady=(5, 0))
    expl_text.insert("1.0", info.get("explication", "Aucune explication disponible"))
    expl_text.config(state="disabled")
    
    # Scrollbar pour les explications
    scrollbar = ttk.Scrollbar(expl_text, command=expl_text.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    expl_text.config(yscrollcommand=scrollbar.set)
    
    # Bouton fermer
    ttk.Button(frame, text="Fermer", command=popup.destroy).pack(pady=(10, 0))

def lancer_application(config):
    try:
        print("Launching the GUI application...")
        # Récupération des paramètres depuis la configuration
        theme = config.get("app", {}).get("theme", "superhero")
        window_width = config.get("app", {}).get("window_width", 800)
        window_height = config.get("app", {}).get("window_height", 600)

        app = ttk.Window(
            title="Correcteur IA local",
            themename=theme,
            size=(window_width, window_height),
            minsize=(640, 260)
        )

        font_size = tk.IntVar(value=12)

        def update_font_size(delta):
            new_size = font_size.get() + delta
            if new_size >= 8:
                font_size.set(new_size)
                zone_texte_original.config(font=("TkDefaultFont", font_size.get()))
                zone_texte_corrige.config(font=("TkDefaultFont", font_size.get()))

        def reset_font_size():
            font_size.set(12)
            zone_texte_original.config(font=("TkDefaultFont", font_size.get()))
            zone_texte_corrige.config(font=("TkDefaultFont", font_size.get()))

        app.bind("<Control-plus>", lambda e: update_font_size(2))
        app.bind("<Control-minus>", lambda e: update_font_size(-2))
        app.bind("<Control-0>", lambda e: reset_font_size())

        toolbar = ttk.Frame(app)
        toolbar.pack(fill=X, padx=10, pady=5)

        def load_icon_with_theme(file_path, invert_colors=False, size=None):
            image = Image.open(file_path).convert("RGBA")
            if invert_colors:
                r, g, b, a = image.split()
                rgb = Image.merge("RGB", (r, g, b))
                inverted_rgb = ImageOps.invert(rgb)
                image = Image.merge("RGBA", (*inverted_rgb.split(), a))
            if size:
                image = image.resize(size, Image.LANCZOS)
            return ImageTk.PhotoImage(image)

        enlarge_icon = load_icon_with_theme("assets/icons/zoom-in.png", invert_colors=True, size=(24, 24))
        reduce_icon = load_icon_with_theme("assets/icons/zoom-out.png", invert_colors=True, size=(24, 24))
        reset_icon = load_icon_with_theme("assets/icons/arrow-clockwise.png", invert_colors=True, size=(24, 24))

        enlarge_button = ttk.Button(
            toolbar, 
            image=enlarge_icon, 
            command=lambda: update_font_size(2), 
            bootstyle="primary"
        )
        enlarge_button.pack(side=LEFT, padx=5)
        enlarge_button.bind("<Enter>", lambda e: enlarge_button.config(text="Agrandir"))
        enlarge_button.bind("<Leave>", lambda e: enlarge_button.config(text=""))

        reduce_button = ttk.Button(
            toolbar, 
            image=reduce_icon, 
            command=lambda: update_font_size(-2), 
            bootstyle="primary"
        )
        reduce_button.pack(side=LEFT, padx=5)
        reduce_button.bind("<Enter>", lambda e: reduce_button.config(text="Réduire"))
        reduce_button.bind("<Leave>", lambda e: reduce_button.config(text=""))

        reset_button = ttk.Button(
            toolbar, 
            image=reset_icon, 
            command=reset_font_size, 
            bootstyle="info"
        )
        reset_button.pack(side=LEFT, padx=5)
        reset_button.bind("<Enter>", lambda e: reset_button.config(text="Réinitialiser"))
        reset_button.bind("<Leave>", lambda e: reset_button.config(text=""))

        app.enlarge_icon = enlarge_icon
        app.reduce_icon = reduce_icon
        app.reset_icon = reset_icon

        labels_frame = ttk.Frame(app)
        labels_frame.pack(fill=X, padx=10, pady=(5, 0))
        
        ttk.Label(labels_frame, text="Texte original", font=("TkDefaultFont", 10, "bold")).pack(side=LEFT, padx=(0, 5))
        ttk.Label(labels_frame, text="Texte corrigé", font=("TkDefaultFont", 10, "bold")).pack(side=RIGHT, padx=(5, 0))

        text_frame = ttk.Frame(app)
        text_frame.pack_propagate(False)
        text_frame.pack(padx=10, pady=5, expand=True, fill=BOTH)

        text_frame.grid_propagate(False)
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_columnconfigure(1, weight=0)
        text_frame.grid_columnconfigure(2, weight=1)
        text_frame.grid_columnconfigure(3, weight=0)

        zone_texte_original = tk.Text(
            text_frame, 
            wrap=tk.WORD,
            font=("TkDefaultFont", font_size.get())
        )
        zone_texte_original.grid(row=0, column=0, sticky="nsew")

        v_scrollbar_original = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=zone_texte_original.yview)
        v_scrollbar_original.grid(row=0, column=1, sticky="ns")
        zone_texte_original.config(yscrollcommand=v_scrollbar_original.set)

        zone_texte_corrige = tk.Text(
            text_frame, 
            wrap=tk.WORD,
            font=("TkDefaultFont", font_size.get()),
            state="disabled"
        )
        zone_texte_corrige.grid(row=0, column=2, sticky="nsew")

        v_scrollbar_corrige = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=zone_texte_corrige.yview)
        v_scrollbar_corrige.grid(row=0, column=3, sticky="ns")
        zone_texte_corrige.config(yscrollcommand=v_scrollbar_corrige.set)

        def mettre_a_jour_texte_corrige(texte_corrige):
            zone_texte_corrige.config(state="normal")
            zone_texte_corrige.delete("1.0", tk.END)
            zone_texte_corrige.insert("1.0", texte_corrige)
            zone_texte_corrige.config(state="disabled")

        globals()['mettre_a_jour_texte_corrige'] = mettre_a_jour_texte_corrige

        is_dark_theme = theme in ['superhero', 'darkly', 'cyborg']

        couper_icon = load_icon_with_theme("assets/icons/scissors.png", is_dark_theme, size=(16, 16))
        copier_icon = load_icon_with_theme("assets/icons/copy.png", is_dark_theme, size=(16, 16))
        coller_icon = load_icon_with_theme("assets/icons/clipboard.png", is_dark_theme, size=(16, 16))

        menu_contextuel_original = tk.Menu(zone_texte_original, tearoff=0)
        menu_contextuel_original.add_command(
            label="Couper", 
            command=lambda: zone_texte_original.event_generate("<<Cut>>"), 
            image=couper_icon, 
            compound=LEFT
        )
        menu_contextuel_original.add_command(
            label="Copier", 
            command=lambda: zone_texte_original.event_generate("<<Copy>>"), 
            image=copier_icon, 
            compound=LEFT
        )
        menu_contextuel_original.add_command(
            label="Coller", 
            command=lambda: zone_texte_original.event_generate("<<Paste>>"), 
            image=coller_icon, 
            compound=LEFT
        )

        menu_contextuel_corrige = tk.Menu(zone_texte_corrige, tearoff=0)
        menu_contextuel_corrige.add_command(
            label="Copier", 
            command=lambda: zone_texte_corrige.event_generate("<<Copy>>"), 
            image=copier_icon, 
            compound=LEFT
        )

        def afficher_menu_contextuel_original(event):
            menu_contextuel_original.tk_popup(event.x_root, event.y_root)

        def afficher_menu_contextuel_corrige(event):
            menu_contextuel_corrige.tk_popup(event.x_root, event.y_root)

        zone_texte_original.bind("<Button-3>", afficher_menu_contextuel_original)
        zone_texte_corrige.bind("<Button-3>", afficher_menu_contextuel_corrige)

        cadre_boutons = ttk.Frame(app)
        cadre_boutons.pack(pady=5)

        def quitter_application():
            if zone_texte_original.get("1.0", tk.END).strip():
                if messagebox.askyesno("Confirmation", "Du texte est présent. Voulez-vous vraiment quitter ?"):
                    app.destroy()
            else:
                app.destroy()

        def corriger_texte():
            texte = zone_texte_original.get("1.0", tk.END).replace("\r\n", "\n").strip()
            if not texte:
                messagebox.showinfo("Information", "La zone de texte est vide.")
                return
            
            paragraphes = decouper_texte_en_paragraphes(texte)
            print(f"Paragraphes découpés : {len(paragraphes)} paragraphes")
            
            if not paragraphes:
                messagebox.showinfo("Information", "Aucun paragraphe détecté dans le texte.")
                return
                
            statut.set("Préparation de la correction...")
            
            app_vars = {
                'zone_texte_corrige': zone_texte_corrige,
                'statut': statut,
                'info_icon': app.info_icon
            }
            
            threading.Thread(
                target=afficher_correction_progressive, 
                args=(paragraphes, app_vars),
                daemon=True
            ).start()

        corriger_icon = load_icon_with_theme("assets/icons/check-circle.png", invert_colors=True)
        quitter_icon = load_icon_with_theme("assets/icons/x-circle.png", invert_colors=True)
        info_icon = load_icon_with_theme("assets/icons/info-circle.png", is_dark_theme, size=(16, 16))
        app.info_icon = info_icon  # Garder une référence pour éviter le garbage collection
        
        ttk.Button(
            cadre_boutons, 
            text="Corriger le texte", 
            image=corriger_icon, 
            compound=LEFT, 
            command=corriger_texte
        ).pack(side=LEFT, padx=5)
        
        ttk.Button(
            cadre_boutons, 
            text="Quitter", 
            image=quitter_icon, 
            compound=LEFT, 
            command=quitter_application
        ).pack(side=LEFT, padx=5)

        app.corriger_icon = corriger_icon
        app.quitter_icon = quitter_icon
        app.couper_icon = couper_icon
        app.copier_icon = copier_icon
        app.coller_icon = coller_icon

        statut = ttk.StringVar(value="En attente")
        ttk.Label(app, textvariable=statut, bootstyle="info").pack(pady=5)

        app.mainloop()
    except Exception as e:
        print("Une erreur s'est produite dans l'application :", e)
        import traceback
        traceback.print_exc()