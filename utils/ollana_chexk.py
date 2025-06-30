import subprocess
from utils.installe_ollama import installer_ollama
from utils.installe_modele import installer_modele

def ollama_est_installe() -> bool:
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False

def modele_est_present(nom_modele: str) -> bool:
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        return nom_modele.lower() in result.stdout.lower()
    except Exception:
        return False

def verifier_ollama_et_modele(nom_modele: str) -> bool:
    if not ollama_est_installe():
        print("❌ Ollama non installé.")
        installer_ollama()
        return False

    if not modele_est_present(nom_modele):
        print(f"⚠️ Modèle '{nom_modele}' non installé.")
        installer_modele(nom_modele)
        return False

    return True