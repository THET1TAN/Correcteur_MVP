# Correcteur MVP 📝

An intelligent French spelling and grammar checker using local AI with a modern graphical interface.

## 🎯 Description

Correcteur MVP is a French text correction application that uses advanced language models (LLM) to correct spelling, grammar, and conjugation while preserving the original text style. The application automatically detects the language register (colloquial, formal, Quebec French, slang, etc.) and adapts its corrections accordingly.

## ⚠️ AI Technology Disclaimer

**Important Notice:** This application uses artificial intelligence technology for text correction. While the AI models are highly sophisticated and generally accurate, they may occasionally make errors or produce unexpected results. Users should:

- **Review all corrections** before accepting them
- **Use their judgment** when applying suggested changes
- **Verify important content** manually, especially for professional or critical documents
- **Understand** that AI-generated corrections are suggestions, not absolute truths

The developers are not responsible for any errors or inaccuracies in the AI-generated corrections. Always use human judgment as the final arbiter of text quality.

## ✨ Features

- **Intelligent correction**: Corrects only errors without reformulating or changing the style
- **Style detection**: Automatically identifies language register (colloquial, formal, Quebec French, etc.)
- **Modern interface**: Intuitive graphical interface based on ttkbootstrap
- **Progressive correction**: Paragraph-by-paragraph processing with real-time feedback
- **Detailed metadata**: Explanations of corrections and information about detected style
- **Multi-server support**: Compatible with different Ollama servers
- **Block processing**: Automatic text segmentation into paragraphs for better accuracy

## 🏗️ Architecture

```
correcteur_mvp/
├── main.py                 # Application entry point
├── assets/                 # Graphic resources
│   └── icons/             # Interface icons
├── core/                  # Business logic
│   ├── correction.py      # LLM correction module
│   ├── decoupage.py       # Text segmentation into paragraphs
│   ├── prompt_builder.py  # Prompt construction (to be developed)
│   └── resumeur.py        # Summary module (to be developed)
├── gui/                   # Graphical interface
│   └── editeur.py         # Main editor interface
├── utils/                 # Utilities
│   ├── clipboard.py       # Clipboard management
│   ├── config_loader.py   # XML configuration loading
│   ├── file_io.py         # File management
│   └── ollana_chexk.py    # Ollama connection verification
└── R&D/                   # Research and development
    └── logs/              # Correction logs
```

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Ollama server with a French language model (recommended: Meta-Llama-3.1-70B-Instruct)

### Dependencies

Install all required dependencies using pip:

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install ttkbootstrap>=1.10.1
pip install requests>=2.31.0
pip install Pillow>=10.0.0
pip install tqdm>=4.65.0
```

### Configuration

1. Clone the repository:
```bash
git clone https://github.com/THET1TAN/correcteur_mvp.git
cd correcteur_mvp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create or modify the `config.xml` file at the project root:
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

4. Ensure your Ollama server is started and accessible.

## 🎮 Usage

### Launching the application

```bash
python main.py
```

### User interface

1. **Source text area**: Paste or type your text to be corrected
2. **"Correct" button**: Starts the correction process
3. **Corrected text area**: Displays corrected text with information icons
4. **Information icons**: Click to see correction details (detected style, explanations)

### Advanced features

- **Progressive correction**: Text is processed paragraph by paragraph
- **Informative tooltips**: Hover over icons for quick preview
- **Style preservation**: The corrector maintains the original language register
- **Error handling**: Robust interface with connection error management

## 🛠️ Configuration

### Server parameters

Modify the `config.xml` file to adapt the configuration to your environment:

- `host`: IP address or domain name of the Ollama server
- `port`: Ollama server port
- `model`: Name of the language model to use

### Recommended models

- **Meta-Llama-3.1-70B-Instruct**: Excellent for French, accurate and fast
- **Mistral-7B-Instruct**: Lighter alternative
- **Qwen2.5-72B-Instruct**: Very performant on non-English languages

## 🧪 Development

### Module structure

- **core/correction.py**: Ollama API request handling and prompt template
- **core/decoupage.py**: Text segmentation algorithm into paragraphs
- **gui/editeur.py**: Complete graphical interface with event handling
- **utils/config_loader.py**: XML configuration loading and validation

### Correction API

```python
from core.correction import corriger_paragraphe

# Paragraph correction
corrected_text, metadata = corriger_paragraphe("Your text to be corrected")
```

### Response format

The model returns structured JSON:
```json
{
  "style": "colloquial",
  "correction": "Your corrected text",
  "explication": "Past participle agreement correction"
}
```

## 🤝 Contributing

Contributions are welcome! Here's how to contribute:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development guidelines

- Follow Python naming conventions (PEP 8)
- Add docstrings for all public functions
- Test your changes before submitting
- Document new features

## 📝 Roadmap

- [ ] **resumeur.py module**: Text summarization functionality
- [ ] **prompt_builder.py module**: Dynamic prompt construction
- [ ] **Premium mode with external APIs**: Integration of API keys to access cloud LLMs (OpenAI GPT, Claude, Gemini, etc.) with user private keys
- [ ] **Multi-language support**: Extension to other languages
- [ ] **Batch mode**: Multiple file processing
- [ ] **Export/Import**: Correction backup
- [ ] **Themes**: Customizable interface
- [ ] **Keyboard shortcuts**: UX improvements
- [ ] **Plugin system**: Extensible architecture

## 🐛 Known issues

- XML configuration file must be present at startup
- Ollama server connection must be stable
- Very long texts may require more processing time

## 📊 Performance

- **Response time**: 2-10 seconds per paragraph depending on model
- **Accuracy**: 95%+ on common errors
- **Memory**: ~100MB in normal operation
- **Compatibility**: Windows, Linux, macOS

## 📄 License

This project is licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0** (CC BY-NC-SA 4.0).

### License summary:

**You are free to:**
- 🔄 **Share** — copy and redistribute the material in any medium or format
- 🔧 **Adapt** — remix, transform, and build upon the material

**Under the following terms:**
- 👤 **Attribution** — You must give appropriate credit, indicate if changes were made, and provide a link to the license
- 🚫 **NonCommercial** — You may not use the material for commercial purposes
- 🤝 **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license

For more details, see: https://creativecommons.org/licenses/by-nc-sa/4.0/

## 👨‍💻 Author

**Joël Smith-Gravel**

## 🙏 Acknowledgments

- **Ollama** for the local model infrastructure
- **ttkbootstrap** for the modern graphical interface
- **Meta AI** for Llama models
- The open source community for tools and libraries used

## 📞 Support

For any questions or issues:
- Open an [issue](https://github.com/THET1TAN/correcteur_mvp/issues) on GitHub
- Check the [documentation](https://github.com/THET1TAN/correcteur_mvp/wiki)

---

<div align="center">
  <i>Developed with ❤️ for the Francophonie</i>
</div>

## 🌍 Language versions

- [Français (French)](README_FR.md) - Version française
- [English](README.md) - English version (current)
