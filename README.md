# 🤖 AI 3D Print Profile Generator for Elegoo Orca Slicer

An intelligent AI-powered system that automatically generates optimized 3D printing profiles for **Elegoo Orca Slicer** using Google's Gemini 2.5 Flash. The system learns from each print to continuously improve its recommendations.

## 🌟 Key Features

- **🔍 Intelligent 3D Analysis**: Extracts geometric features, overhangs, complexity, wall thickness
- **🧠 AI-Powered**: Uses Google Gemini 2.5 Flash for optimal parameter selection
- **🌳 Smart Tree Supports**: Automatically enables tree supports when detecting complex overhangs
- **📏 Build Plate Auto-Fit**: Automatically centers and scales models for your build plate
- **📚 Learning System**: Builds knowledge base from past prints to improve over time
- **🎨 Beautiful UI**: Modern Gradio web interface
- **🎯 Elegoo-Specific**: Generates perfect 3MF project files for Elegoo Orca Slicer

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup API Key

1. Get a FREE Google Gemini API key: https://makersuite.google.com/app/apikey
2. Copy `.env.template` to `.env`
3. Add your API key to `.env`

```env
GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the Application

**Web Interface:**
```bash
python app.py
```
Then open http://localhost:7860

**Command Line:**
```bash
python cli.py your_model.stl --material "Elegoo PLA" --build-plate 256
```

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key (free)
- Elegoo Orca Slicer

## 🎯 Supported Filaments

- Elegoo PLA
- Elegoo RAPID PLA+
- Elegoo RAPID PETG
- Elegoo PETG PRO
- Elegoo PLA Matte
- Elegoo PLA PRO
- Elegoo PLA Silk
- Elegoo ASA
- Elegoo TPU 95A
- Generic PLA/PETG/ABS

## 🏗️ How It Works

1. **Upload** your 3D model (.stl, .obj, .3mf)
2. **Select** filament type (e.g., "Elegoo PLA")
3. **Set** build plate size (220mm, 256mm, etc.)
4. **AI analyzes** geometry, overhangs, complexity
5. **Generates** optimized 3MF project file
6. **Open** in Elegoo Orca Slicer - all settings loaded!
7. **Slice** and print!

## 🌳 Automatic Tree Supports

The AI automatically enables tree supports when detecting:
- Severe overhangs (>60°)
- Complex overhang patterns
- High overhang percentage

Tree supports use less material and are easier to remove!

## 📁 Output Files

For each analysis you get:
1. **`.3mf` file** - Open directly in Elegoo Orca Slicer (model + all settings!)
2. **`_config.json`** - Backup config for manual import
3. **`_summary.txt`** - Human-readable explanation of settings

## 💾 Learning System

- Save feedback after each print
- AI learns what works and what doesn't
- Future similar models benefit from experience
- Export/import knowledge base

## 📖 Documentation

- `README.md` - Full documentation
- `GETTING_STARTED.md` - Quick start guide
- `SETUP_GUIDE.md` - Detailed installation
- `USAGE_EXAMPLES.md` - Practical examples
- `FILAMENT_GUIDE.md` - Filament type reference

## 🔒 Security

- `.env` file contains your API key (never committed)
- All sensitive files are in `.gitignore`
- Local storage only - nothing uploaded except to Gemini API

## 📝 License

MIT License - Free to use and modify

## 🙏 Credits

- Google Gemini 2.5 Flash - AI analysis
- Trimesh - 3D geometry processing
- ChromaDB - Vector database
- Gradio - Web interface
- Elegoo Orca Slicer - Target slicer

---

**Made for the Elegoo 3D printing community** ❤️

