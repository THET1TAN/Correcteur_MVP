def decouper_texte_en_paragraphes(texte):
    """
    Découpe un texte en paragraphes et les stocke dans un dictionnaire.
    
    Args:
        texte (str): Le texte à découper en paragraphes
        
    Returns:
        dict: Un dictionnaire avec les IDs des paragraphes comme clés et les paragraphes comme valeurs
              Les paragraphes ne contiennent pas de sauts de ligne.
    """
    # Divise le texte en paragraphes (les paragraphes sont séparés par une ou plusieurs lignes vides)
    paragraphes_bruts = [p for p in texte.split('\n\n') if p.strip()]
    
    # Crée un dictionnaire pour stocker les paragraphes avec leurs IDs
    paragraphes = {}
    
    # Pour chaque paragraphe, créer une entrée dans le dictionnaire avec un ID unique
    for i, paragraphe in enumerate(paragraphes_bruts, 1):
        # Remplacer tous les sauts de ligne par des espaces
        paragraphe_sans_saut = paragraphe.replace('\n', ' ').strip()
        # Normaliser les espaces multiples en un seul espace
        paragraphe_sans_saut = ' '.join(paragraphe_sans_saut.split())
        
        # Ajouter au dictionnaire avec un ID de type "P1", "P2", etc.
        paragraphes[f"P{i}"] = paragraphe_sans_saut
    
    return paragraphes
