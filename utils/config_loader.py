import xml.etree.ElementTree as ET

def charger_config_xml(chemin="config.xml"):
    config = {}
    try:
        tree = ET.parse(chemin)
        root = tree.getroot()

        for section in root:
            config[section.tag] = {}
            for param in section:
                # Tentative de conversion en int ou float, sinon texte brut
                val = param.text
                if val.isdigit():
                    val = int(val)
                else:
                    try:
                        val = float(val)
                    except:
                        pass
                config[section.tag][param.tag] = val

        return config

    except FileNotFoundError:
        raise FileNotFoundError(f"Fichier de configuration introuvable : {chemin}")
    except ET.ParseError as e:
        raise ValueError(f"Erreur de parsing XML : {e}")
