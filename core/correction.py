import requests
import time
import json

# Paramètres globaux
SERVER_HOST = "http://10.10.10.30"
SERVER_PORT = 11435
MODEL_NAME = "hf.co/bartowski/Meta-Llama-3.1-70B-Instruct-GGUF:Q5_K_S"

def get_server_url(host=SERVER_HOST, port=SERVER_PORT):
    """Construire l'URL du serveur."""
    return f"{host}:{port}" if port else host

def ping_server(server=None):
    """Vérifier si le serveur est accessible."""
    if server is None:
        server = get_server_url()
    try:
        response = requests.get(server, timeout=3)
        return response.status_code == 200
    except requests.RequestException:
        return False

def send_to_ollama(prompt, model=MODEL_NAME, server=None):
    """Envoyer une requête au modèle via l'API Ollama."""
    if server is None:
        server = get_server_url()
    
    url = f"{server}/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, headers=headers, timeout=600)
        response.raise_for_status()
        elapsed_time = time.time() - start_time
        print(f"Temps écoulé pour la réponse du modèle : {elapsed_time:.2f} secondes")
        
        json_data = response.json()
        model_response = json_data.get("response", "")
        usage_info = json_data.get("usage", {})
        return model_response, usage_info
    except requests.RequestException as e:
        return f"Erreur de requête : {e}", {}

# Template de prompt pour la correction
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

def corriger_paragraphe(paragraphe, model=MODEL_NAME, server=None):
    """
    Corrige un paragraphe de texte en utilisant le modèle de correction.
    
    Args:
        paragraphe (str): Le texte à corriger
        model (str): Le nom du modèle à utiliser
        server (str): L'URL du serveur Ollama
        
    Returns:
        tuple: (texte_corrigé, informations supplémentaires incluant la réponse JSON brute)
    """
    if server is None:
        server = get_server_url()
    
    # Vérifier que le serveur est disponible
    if not ping_server(server):
        return paragraphe, {"erreur": "Serveur de correction indisponible"}
    
    # Construire le prompt complet
    prompt = template.replace("{texte}", paragraphe)
    
    # Envoyer au modèle
    response, usage_info = send_to_ollama(prompt, model, server)
    
    # Traiter la réponse
    try:
        # Tentative de parsing du JSON
        json_response = json.loads(response)
        
        # Extraire la correction pour le retour mais garder la réponse brute
        texte_corrige = json_response.get("correction", paragraphe)
        info_supplementaires = {
            "style": json_response.get("style", "inconnu"),
            "explication": json_response.get("explication", ""),
            "usage": usage_info,
            "json_brut": response  # Ajouter la réponse JSON brute
        }
        
        return texte_corrige, info_supplementaires
    except json.JSONDecodeError:
        # En cas d'erreur de décodage JSON, retourner le texte original
        return paragraphe, {
            "erreur": "Réponse invalide du modèle", 
            "json_brut": response  # Ajouter quand même la réponse brute
        }
