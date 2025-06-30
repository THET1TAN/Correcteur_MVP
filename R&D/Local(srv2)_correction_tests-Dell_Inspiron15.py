import requests
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
import threading
import time

# Paramètres globaux
SERVER_HOST = "http://10.10.10.30"
SERVER_PORT = 11435
MODEL_NAME = "hf.co/bartowski/Meta-Llama-3.1-70B-Instruct-GGUF:Q5_K_S"

def get_server_url(host=SERVER_HOST, port=SERVER_PORT):
    return f"{host}:{port}" if port else host
SERVER_URL = get_server_url()

def send_to_ollama(prompt, model=MODEL_NAME, server=SERVER_URL):
    url = f"{server}/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=600)
        response.raise_for_status()
        return response.json().get("response", "")
    except requests.RequestException as e:
        return f"Erreur de requête : {e}"

def ping_server(server=SERVER_URL):
    try:
        response = requests.get(server, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Prompt modèle
template = """ATTENTION : Tu es un correcteur orthographique et grammatical expert en langue française.

Règles ABSOLUES :
- Corrige UNIQUEMENT les fautes d'orthographe, grammaire, accord ou conjugaison.
- NE PAS reformuler, NE PAS améliorer le style, NE PAS changer les mots ou les sujets ("on" reste "on").
- Respecte les expressions familières, régionales, orales ou populaires.
- Si une phrase est cassée → Corrige uniquement les mots nécessaires sans changer la structure.
- Identifie automatiquement le style et la région (ou nature) du texte francophone : familier, québécois, soutenu, argot, etc.

IMPORTANT :
→ Tu dois OBLIGATOIREMENT répondre sous la forme d'un JSON STRICT.
→ Même si tu ne comprends pas, même si le texte est vide, même si tu rencontres une difficulté → réponds quand même avec un JSON VALIDE ou PARTIEL contenant les clés attendues.

Structure de réponse :
{
  "style": "<nature du texte détecté : familier, standard, soutenu, québécois, argot, mélange, inconnu, etc.>",
  "correction": "<texte corrigé uniquement pour les fautes>",
  "explication": "<explication très rapide des corrections (orthographe, accord, conjugaison, grammaire uniquement)>"
}

ATTENTION :
- NE JAMAIS sortir de cette structure.
- En cas de doute, mets : "inconnu" dans "style".
- Si aucune correction : copie le texte original dans "correction" et écris "aucune correction nécessaire" dans "explication".
- SI UNE ERREUR SURVIENT : Fournis quand même un JSON vide mais propre comme :
{
  "style": "inconnu",
  "correction": "",
  "explication": "Erreur interne, veuillez réessayer."
}

Voici le texte à corriger :
{texte}
"""

def loading_animation(lbl):
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not loading_event.is_set():
        lbl.config(text=f"Traitement en cours... {spinner[i % len(spinner)]}", bootstyle="warning")
        i += 1
        time.sleep(0.15)
    lbl.config(text="")

def start_loading_animation(lbl):
    loading_event.clear()
    threading.Thread(target=lambda: loading_animation(lbl), daemon=True).start()

def open_text_input():
    def on_submit():
        texte = text_widget.get("1.0", tk.END).strip()
        if not texte:
            result_label.config(text="Aucun texte fourni. Veuillez réessayer.", bootstyle="danger")
            return

        result_label.config(text="Vérification du serveur...", bootstyle="secondary")
        root.update()  # Force une mise à jour de l'interface utilisateur

        start_loading_animation(result_label)

        def ping_and_process():
            if not ping_server():
                loading_event.set()  # Arrête l'animation de chargement
                root.after(0, lambda: result_label.config(
                    text="Erreur : Serveur de correction injoignable.", bootstyle="danger"
                ))
                return
            root.after(0, lambda: result_label.config(text="Correction en cours...", bootstyle="info"))
            def worker():
                full_prompt = template.replace("{texte}", texte)
                result = send_to_ollama(full_prompt)
                loading_event.set()  # Arrête l'animation de chargement
                root.after(0, lambda: show_result_window(result))
            threading.Thread(target=worker, daemon=True).start()

        threading.Thread(target=ping_and_process, daemon=True).start()

    def show_result_window(result):
        result_win = tb.Toplevel(root)
        result_win.title("Résultat de la correction")
        result_win.geometry("700x400")
        result_label = tb.Label(result_win, text="Réponse du modèle :", font=("Segoe UI", 12, "bold"))
        result_label.pack(pady=10)
        result_text = tk.Text(result_win, wrap="word", font=("Segoe UI", 11), height=18)
        result_text.pack(fill="both", expand=True, padx=10, pady=5)
        result_text.insert("1.0", result)
        result_text.config(state="disabled")

    root = tb.Window(themename="flatly")
    root.title("Correcteur - Saisie du texte")
    root.geometry("700x500")

    label = tb.Label(root, text="Collez ou saisissez votre texte à corriger :", font=("Segoe UI", 12, "bold"))
    label.pack(pady=10)

    text_widget = tk.Text(root, wrap="word", font=("Segoe UI", 11), height=15)
    text_widget.pack(fill="both", expand=True, padx=10)

    submit_btn = tb.Button(root, text="Corriger", command=on_submit, bootstyle=PRIMARY)
    submit_btn.pack(pady=10)

    result_label = tb.Label(root, text="", wraplength=650, font=("Segoe UI", 10))
    result_label.pack(pady=10)

    global loading_event
    loading_event = threading.Event()

    root.mainloop()

if __name__ == "__main__":
    get_server_url()
    open_text_input()
