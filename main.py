from gui.editeur import lancer_application
from utils.config_loader import charger_config_xml
import traceback
import time

def config_loading():
    try:
        config = charger_config_xml()
        print("Configuration chargée avec succès :", config)
        return config
    except Exception as e:
        print("Erreur lors du chargement de la configuration :", e)
        return None  # Ensure None is returned on failure

if __name__ == "__main__":
    print("Starting main script...")
    try:
        config = config_loading()
        print("Config loading done, launching application...")
        if config:
            lancer_application(config)
        else:
            print("No valid configuration found.")
    except Exception as e:
        print("Une erreur inattendue s'est produite :")
        traceback.print_exc()
        time.sleep(5)  # Delay to observe the error
        input("Appuyez sur Entrée pour continuer...")
    finally:
        input("Appuyez sur Entrée pour quitter...")