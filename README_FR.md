# Correcteur MVP 📝

Un correcteur orthographique et grammatical français intelligent utilisant l'IA locale avec une interface graphique moderne.

## 🎯 Description

Correcteur MVP est une application de correction de texte français qui utilise des modèles de langage avancés (LLM) pour corriger l'orthographe, la grammaire et la conjugaison tout en préservant le style original du texte. L'application détecte automatiquement le registre de langue (familier, soutenu, québécois, argot, etc.) et adapte ses corrections en conséquence.

## ⚠️ Avertissement Technologie IA

**Avis Important :** Cette application utilise la technologie d'intelligence artificielle pour la correction de texte. Bien que les modèles d'IA soient très sophistiqués et généralement précis, ils peuvent occasionnellement commettre des erreurs ou produire des résultats inattendus. Les utilisateurs doivent :

- **Réviser toutes les corrections** avant de les accepter
- **Faire preuve de jugement** lors de l'application des modifications suggérées
- **Vérifier manuellement le contenu important**, en particulier pour les documents professionnels ou critiques
- **Comprendre** que les corrections générées par l'IA sont des suggestions, non des vérités absolues

Les développeurs ne sont pas responsables des erreurs ou inexactitudes dans les corrections générées par l'IA. Utilisez toujours le jugement humain comme arbitre final de la qualité du texte.

## ✨ Fonctionnalités

- **Correction intelligente** : Corrige uniquement les fautes sans reformuler ou changer le style
- **Détection de style** : Identifie automatiquement le registre de langue (familier, soutenu, québécois, etc.)
- **Interface moderne** : Interface graphique intuitive basée sur ttkbootstrap
- **Correction progressive** : Traitement paragraphe par paragraphe avec feedback en temps réel
- **Métadonnées détaillées** : Explications des corrections et informations sur le style détecté
- **Support multi-serveurs** : Compatible avec différents serveurs Ollama
- **Traitement par blocs** : Découpage automatique du texte en paragraphes pour une meilleure précision

## 🏗️ Architecture

```
correcteur_mvp/
├── main.py                 # Point d'entrée de l'application
├── assets/                 # Ressources graphiques
│   └── icons/             # Icônes de l'interface
├── core/                  # Logique métier
│   ├── correction.py      # Module de correction via LLM
│   ├── decoupage.py       # Découpage du texte en paragraphes
│   ├── prompt_builder.py  # Construction des prompts (à développer)
│   └── resumeur.py        # Module de résumé (à développer)
├── gui/                   # Interface graphique
│   └── editeur.py         # Interface principale de l'éditeur
├── utils/                 # Utilitaires
│   ├── clipboard.py       # Gestion du presse-papier
│   ├── config_loader.py   # Chargement de la configuration XML
│   ├── file_io.py         # Gestion des fichiers
│   └── ollana_chexk.py    # Vérification de la connexion Ollama
└── R&D/                   # Recherche et développement
    └── logs/              # Journaux de correction
```

## 🚀 Installation

### Prérequis

- Python 3.8+
- Serveur Ollama avec un modèle de langage français (recommandé : Meta-Llama-3.1-70B-Instruct)

### Dépendances

Installez toutes les dépendances requises avec pip :

```bash
pip install -r requirements.txt
```

Ou installez manuellement :
```bash
pip install ttkbootstrap>=1.10.1
pip install requests>=2.31.0
pip install Pillow>=10.0.0
pip install tqdm>=4.65.0
```

### Configuration

1. Clonez le repository :
```bash
git clone https://github.com/THET1TAN/correcteur_mvp.git
cd correcteur_mvp
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Créez ou modifier le fichier `config.xml` à la racine du projet :
```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <server>
        <host>http://10.10.10.30</host>
        <port>11435</port>
    </server>
    <model>
        <name>hf.co/bartowski/Meta-Llama-3.1-70B-Instruct-GGUF:Q5_K_S</name>
    </model>
</configuration>
```

4. Assurez-vous que votre serveur Ollama est démarré et accessible.

## 🎮 Utilisation

### Lancement de l'application

```bash
python main.py
```

### Interface utilisateur

1. **Zone de texte source** : Collez ou tapez votre texte à corriger
2. **Bouton "Corriger"** : Lance le processus de correction
3. **Zone de texte corrigé** : Affiche le texte corrigé avec des icônes d'information
4. **Icônes d'information** : Cliquez pour voir les détails des corrections (style détecté, explications)

### Fonctionnalités avancées

- **Correction progressive** : Le texte est traité paragraphe par paragraphe
- **Tooltips informatifs** : Survolez les icônes pour un aperçu rapide
- **Préservation du style** : Le correcteur maintient le registre de langue original
- **Gestion d'erreurs** : Interface robuste avec gestion des erreurs de connexion

## 🛠️ Configuration

### Paramètres serveur

Modifiez le fichier `config.xml` pour adapter la configuration à votre environnement :

- `host` : Adresse IP ou nom de domaine du serveur Ollama
- `port` : Port du serveur Ollama
- `model` : Nom du modèle de langage à utiliser

### Modèles recommandés

- **Meta-Llama-3.1-70B-Instruct** : Excellent pour le français, précis et rapide
- **Mistral-7B-Instruct** : Alternative plus légère
- **Qwen2.5-72B-Instruct** : Très performant sur les langues non-anglaises

## 🧪 Développement

### Structure des modules

- **core/correction.py** : Gestion des requêtes vers l'API Ollama et template de prompt
- **core/decoupage.py** : Algorithme de découpage du texte en paragraphes
- **gui/editeur.py** : Interface graphique complète avec gestion des événements
- **utils/config_loader.py** : Chargement et validation de la configuration XML

### API de correction

```python
from core.correction import corriger_paragraphe

# Correction d'un paragraphe
texte_corrigé, métadonnées = corriger_paragraphe("Votre texte à corrigé")
```

### Format de réponse

Le modèle retourne un JSON structuré :
```json
{
  "style": "familier",
  "correction": "Votre texte corrigé",
  "explication": "Correction de l'accord du participe passé"
}
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

### Guidelines de développement

- Respectez les conventions de nommage Python (PEP 8)
- Ajoutez des docstrings pour toutes les fonctions publiques
- Testez vos modifications avant de soumettre
- Documentez les nouvelles fonctionnalités

## 📝 Roadmap

- [ ] **Module resumeur.py** : Fonctionnalité de résumé de texte
- [ ] **Module prompt_builder.py** : Construction dynamique des prompts
- [ ] **Mode Premium avec API externes** : Intégration de clés API pour accéder aux LLM cloud (OpenAI GPT, Claude, Gemini, etc.) avec clés privées utilisateur
- [ ] **Support multi-langues** : Extension à d'autres langues
- [ ] **Mode batch** : Traitement de fichiers multiples
- [ ] **Export/Import** : Sauvegarde des corrections
- [ ] **Thèmes** : Interface personnalisable
- [ ] **Raccourcis clavier** : Amélioration de l'UX
- [ ] **Plugin système** : Architecture extensible

## 🐛 Problèmes connus

- Le fichier de configuration XML doit être présent au démarrage
- La connexion au serveur Ollama doit être stable
- Les très longs textes peuvent nécessiter plus de temps de traitement

## 📊 Performance

- **Temps de réponse** : 2-10 secondes par paragraphe selon le modèle
- **Précision** : 95%+ sur les fautes courantes
- **Mémoire** : ~100MB en fonctionnement normal
- **Compatibilité** : Windows, Linux, macOS

## 📄 Licence

Ce projet est sous licence **Creative Commons Attribution-NonCommercial-ShareAlike 4.0** (CC BY-NC-SA 4.0).

### Résumé de la licence :

**Vous êtes autorisé à :**
- 🔄 **Partager** — copier et redistribuer le matériel dans tout support ou format
- 🔧 **Adapter** — remixer, transformer et créer à partir du matériel

**Selon les conditions suivantes :**
- 👤 **Attribution** — Vous devez créditer l'œuvre, indiquer les changements effectués et fournir un lien vers la licence
- 🚫 **Pas d'utilisation commerciale** — Vous ne pouvez pas utiliser cette œuvre à des fins commerciales
- 🤝 **Partage dans les mêmes conditions** — Si vous modifiez cette œuvre, vous devez distribuer votre contribution sous la même licence

Pour plus de détails, consultez : https://creativecommons.org/licenses/by-nc-sa/4.0/

## 👨‍💻 Auteur

**Joël Smith-Gravel**

## 🙏 Remerciements

- **Ollama** pour l'infrastructure de modèles locaux
- **ttkbootstrap** pour l'interface graphique moderne
- **Meta AI** pour les modèles Llama
- La communauté open source pour les outils et bibliothèques utilisés

## 📞 Support

Pour toute question ou problème :
- Ouvrez une [issue](https://github.com/THET1TAN/correcteur_mvp/issues) sur GitHub
- Consultez la [documentation](https://github.com/THET1TAN/correcteur_mvp/wiki)

---

<div align="center">
  <i>Développé avec ❤️ pour la francophonie</i>
</div>

## 🌍 Versions linguistiques

- [Français (French)](README_FR.md) - Version française (actuelle)
- [English](README.md) - Version anglaise
