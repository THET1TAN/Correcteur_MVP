import os  # Import os for directory and file handling
import requests
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
import threading
import time
from datetime import datetime  # Import datetime for timestamps

# Paramètres globaux
SERVER_HOST = "http://10.10.10.30"
SERVER_PORT = 11435
MODEL_NAME = "hf.co/bartowski/Meta-Llama-3.1-70B-Instruct-GGUF:Q5_K_S"

def get_server_url(host=SERVER_HOST, port=SERVER_PORT):
    return f"{host}:{port}" if port else host
SERVER_URL = get_server_url()

def get_ollama_token_count(prompt, model=MODEL_NAME, server=SERVER_URL):
    """Obtenir le nombre de tokens en utilisant le système de tokenisation d'Ollama."""
    url = f"{server}/api/tokenize"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("token_count", 0)
    except requests.RequestException:
        return 0

def send_to_ollama(prompt, model=MODEL_NAME, server=SERVER_URL):
    url = f"{server}/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        start_time = time.time()  # Start the timer
        response = requests.post(url, json=payload, headers=headers, timeout=600)
        response.raise_for_status()
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        print(f"Temps écoulé pour la réponse du modèle : {elapsed_time:.2f} secondes")  # Log the time
        json_data = response.json()
        model_response = json_data.get("response", "")
        usage_info = json_data.get("usage", {})
        return model_response, usage_info
    except requests.RequestException as e:
        return f"Erreur de requête : {e}", {}

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
    start_time = time.time()  # Start the timer
    while not loading_event.is_set():
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        lbl.config(
            text=f"Traitement en cours... {spinner[i % len(spinner)]} ({elapsed_time:.1f}s)",
            bootstyle="warning"
        )
        i += 1
        time.sleep(0.15)
    lbl.config(text="")

def advanced_token_count(text):
    """
    Placeholder for an advanced token counting function,
    similar to how an LLM might tokenize text.
    """
    # Here you could integrate a real tokenizer (e.g., GPT2Tokenizer).
    # For demonstration, let's split on any whitespace characters and punctuation.
    import re
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
    return len(tokens)

def evaluate_tokenization(text, token_counting_mode="naive"):
    """Evaluate tokenization based on a chosen mode: naive or advanced."""
    if token_counting_mode == "advanced":
        return advanced_token_count(text)
    return len(text.split())  # Naive method

LOG_DIR = "./logs"
LOG_FILE = os.path.join(LOG_DIR, "correction_logs.txt")

def ensure_log_directory():
    """Ensure the log directory exists."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

def log_correction(input_text, result, elapsed_time, input_token_count, output_token_count, real_model_token_count=0):
    """Log the correction details to a file."""
    ensure_log_directory()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time
    with open(LOG_FILE, "a", encoding="utf-8") as log_file:
        log_file.write(f"Date et heure : {timestamp}\n")  # Log the timestamp
        log_file.write(f"Texte original : {input_text}\n")
        log_file.write(f"Résultat : {result}\n")
        log_file.write(f"Temps écoulé : {elapsed_time:.2f} secondes\n")
        log_file.write(f"Nombre de tokens (entrée) : {input_token_count}\n")
        log_file.write(f"Nombre de tokens (sortie) : {output_token_count}\n")
        log_file.write("-" * 50 + "\n")

def start_loading_animation(lbl, token_lbl, text, token_counting_mode="naive"):
    loading_event.clear()
    token_count = evaluate_tokenization(text, token_counting_mode)  # Evaluate tokenization
    token_lbl.config(text=f"Tokens : {token_count}", bootstyle="info")  # Display token count
    threading.Thread(target=lambda: loading_animation(lbl), daemon=True).start()

def open_text_input():
    def on_submit():
        texte = text_widget.get("1.0", tk.END).strip()
        if not texte:
            result_label.config(text="Aucun texte fourni. Veuillez réessayer.", bootstyle="danger")
            return

        result_label.config(text="Vérification du serveur...", bootstyle="secondary")
        root.update()  # Force a UI update

        start_loading_animation(result_label, token_label, texte, "advanced")  # Example usage
        
        def ping_and_process():
            if not ping_server():
                loading_event.set()  # Stop the loading animation
                root.after(0, lambda: result_label.config(
                    text="Erreur : Serveur de correction injoignable.", bootstyle="danger"
                ))
                return
            root.after(0, lambda: result_label.config(text="Correction en cours...", bootstyle="info"))
            def worker():
                full_prompt = template.replace("{texte}", texte)
                start_time = time.time()  # Start the timer for correction
                model_response, usage_info = send_to_ollama(full_prompt)
                elapsed_time = time.time() - start_time
                input_token_count = evaluate_tokenization(texte, "advanced")
                output_token_count = evaluate_tokenization(model_response, "advanced")
                real_model_token_count = (
                    usage_info.get("prompt_tokens", 0)
                    + usage_info.get("completion_tokens", 0)
                )
                log_correction(
                    texte,
                    model_response,
                    elapsed_time,
                    input_token_count,
                    output_token_count,
                    real_model_token_count
                )
                loading_event.set()  # Stop the loading animation
                root.after(0, lambda: show_result_window(model_response))
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

    token_label = tb.Label(root, text="", font=("Segoe UI", 10))  # Token count label
    token_label.pack(pady=5)

    global loading_event
    loading_event = threading.Event()

    root.mainloop()

if __name__ == "__main__":
    ensure_log_directory()  # Ensure the log directory and file are created
    get_server_url()
    open_text_input()
