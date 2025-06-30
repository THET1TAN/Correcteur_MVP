#!/usr/bin/env python3
import os
from tqdm import tqdm  # Import pour la barre de progression

def generate_tree(current_dir, prefix, out_file, progress_bar, ignored_files):
    entries = [e for e in sorted(os.listdir(current_dir)) if e not in ignored_files]
    count = len(entries)
    for i, entry in enumerate(entries):
        path = os.path.join(current_dir, entry)
        connector = "└── " if i == count - 1 else "├── "
        out_file.write(prefix + connector + entry + "\n")
        progress_bar.set_postfix({"Fichier": entry})
        progress_bar.update(1)
        if os.path.isdir(path):
            extension = "    " if i == count - 1 else "│   "
            generate_tree(path, prefix + extension, out_file, progress_bar, ignored_files)

if __name__ == "__main__":
    # Détermine le dossier où se trouve le script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_name = os.path.basename(__file__)
    output_file_name = "liste_fichiers.txt"
    print(f"📂 Répertoire de départ : {script_dir}")

    # Chemin complet du fichier de sortie dans le même dossier que le script
    output_file = os.path.join(script_dir, output_file_name)
    ignored_files = {script_name, output_file_name}  # Fichiers à ignorer
    all_files = sum([len(files) for _, _, files in os.walk(script_dir)]) - len(ignored_files)

    with open(output_file, "w", encoding="utf-8") as f:
        with tqdm(total=all_files, desc="Génération de la liste", unit="fichier") as pbar:
            generate_tree(script_dir, "", f, pbar, ignored_files)

    print(f"✅ Liste des fichiers générée dans : {output_file}")
    input("Appuyez sur Entrée pour quitter...")
