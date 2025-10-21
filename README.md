# 🤖 AI 3D Print Profile Generator

An intelligent AI-powered system that automatically generates optimized Orca Slicer profiles for 3D models using Google's Gemini 2.5 Flash. The system learns from each print to continuously improve its recommendations.

## 🌟 Features

- **🔍 Intelligent Feature Extraction**: Analyzes 3D models to extract geometric features, overhangs, complexity, and more
- **🧠 AI-Powered Analysis**: Uses Google Gemini 2.5 Flash to generate optimal slicer parameters
- **📚 Dynamic Learning**: Builds a knowledge base from past prints and applies lessons to new models
- **🎯 Vector Search**: Finds similar past cases using ChromaDB for informed recommendations
- **📊 Beautiful UI**: Modern Gradio-based web interface
- **💾 Knowledge Export**: Export and share your learned printing knowledge
- **🔄 Continuous Improvement**: Success/failure feedback improves future predictions

## 🏗️ Architecture

```
┌─────────────┐
│  3D Model   │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ Feature Extractor   │ ─── Trimesh, NumPy
│ - Dimensions        │
│ - Overhangs         │
│ - Complexity        │
│ - Wall Analysis     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Knowledge Base     │ ─── ChromaDB
│ - Vector Search     │
│ - Similar Cases     │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   Gemini AI Agent   │ ─── Google Gemini 2.5 Flash
│ - Analyze Features  │
│ - Learn from Past   │
│ - Generate Profile  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│ Profile Generator   │
│ - Orca Slicer JSON  │
│ - Human Summary     │
└─────────────────────┘
```

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))
- Orca Slicer (optional, for direct profile import)

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd "AI AGENT"

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key_here
ORCA_SLICER_PATH=C:\Program Files\OrcaSlicer\orca-slicer.exe
```

### 3. Run the Application

#### Web UI (Recommended)

```bash
python app.py
```

Then open your browser to `http://localhost:7860`

#### Command Line

```bash
python cli.py path/to/your/model.stl --material PLA
```

## 📖 Usage Guide

### Web Interface

1. **Initialize the Agent**: Click "Initialize AI Agent" button
2. **Upload Model**: Select your 3D model file (.stl, .obj, .3mf)
3. **Choose Material**: Select your filament type (PLA, PETG, ABS, etc.)
4. **Analyze**: Click "Analyze Model" to generate the profile
5. **Download**: Get the JSON profile and import it into Orca Slicer
6. **Provide Feedback**: After printing, save feedback to help the AI learn!

### Command Line Interface

```bash
# Basic analysis
python cli.py model.stl

# With material specification
python cli.py model.stl --material PETG

# Disable knowledge base lookup
python cli.py model.stl --no-kb

# View statistics
python cli.py --stats

# Export knowledge base
python cli.py --export knowledge_backup.json
```

## 🧪 How It Works

### 1. Feature Extraction

The system analyzes your 3D model and extracts:
- **Dimensions**: Width, depth, height, volume
- **Overhangs**: Detects areas needing support (>45°)
- **Complexity**: Face density, detail level, watertightness
- **Wall Analysis**: Thin wall detection
- **Surface Characteristics**: Roughness, variation
- **Optimal Orientation**: Best print orientation suggestions

### 2. Knowledge Base Search

Before generating a profile, the system:
- Searches for similar models in the knowledge base
- Uses vector embeddings to find relevant past cases
- Considers geometric similarity and print outcomes
- Applies lessons learned from successful prints

### 3. AI Analysis

Google Gemini 2.5 Flash analyzes:
- Model features and characteristics
- Similar past cases (if found)
- Material properties and requirements
- Generates optimized slicer parameters
- Provides detailed reasoning for choices

### 4. Profile Generation

The system generates:
- **JSON Profile**: Orca Slicer-compatible configuration
- **Human Summary**: Readable explanation of settings
- **Parameter Reasoning**: Why each setting was chosen

### 5. Learning Loop

After each print:
- Save feedback (success/failure/notes)
- System stores the case with outcomes
- Future similar models benefit from this experience
- Success rate improves over time

## 📁 Project Structure

```
AI AGENT/
├── app.py                  # Gradio web interface
├── cli.py                  # Command-line interface
├── ai_agent.py            # Main orchestrator
├── feature_extractor.py   # 3D model analysis
├── gemini_agent.py        # Google Gemini integration
├── knowledge_base.py      # ChromaDB learning system
├── profile_generator.py   # Orca Slicer profile output
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .env.example           # Environment template
├── knowledge_base/        # Stored learning cases
├── generated_profiles/    # Output profiles
├── chroma_db/            # Vector database
└── models_cache/         # Temporary model storage
```

## 🎓 Learning System

The AI improves through:

### Positive Feedback
- Reinforces parameter choices that worked
- Increases confidence in similar recommendations
- Builds patterns for successful prints

### Negative Feedback
- Identifies what to avoid
- Adjusts parameters for similar future cases
- Prevents repeated mistakes

### Similar Model Recognition
- Matches new models to past experiences
- Applies successful strategies
- Adapts to model-specific challenges

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Feature extraction settings
FEATURE_EXTRACTION = {
    "num_samples": 360,              # Rotation samples
    "overhang_angle_threshold": 45,  # Support threshold
    "analyze_supports": True,
    "analyze_overhangs": True,
}

# Model selection
GEMINI_MODEL = "gemini-2.0-flash-exp"

# Paths
KNOWLEDGE_BASE_DIR = "knowledge_base"
PROFILES_OUTPUT_DIR = "generated_profiles"
```

## 📊 Example Output

### Analysis Summary
```
Dimensions: 50.0mm × 50.0mm × 100.0mm
Volume: 125000.00 mm³
Detail Level: high
Watertight: Yes
⚠️ Needs Supports (15.3% overhangs)
Wall Type: thick
```

### Generated Profile
- Layer Height: 0.2mm (balanced quality/speed)
- Supports: Enabled (15% overhangs detected)
- Infill: 20% cubic (decorative part)
- Print Speed: 60mm/s (high detail requires precision)
- Temperature: 210°C (PLA optimal)

## 🤝 Contributing

Contributions are welcome! This project demonstrates:
- AI agent architecture
- LLM integration (Google Gemini)
- Vector databases (ChromaDB)
- 3D geometry processing (Trimesh)
- Modern web UIs (Gradio)

## 📝 License

MIT License - Feel free to use and modify!

## 🙏 Credits

Built with:
- [Google Gemini 2.5 Flash](https://ai.google.dev/) - AI analysis
- [Trimesh](https://trimsh.org/) - 3D geometry processing
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Gradio](https://gradio.app/) - Web interface
- [Orca Slicer](https://github.com/SoftFever/OrcaSlicer) - Target slicer

## 🐛 Troubleshooting

### "API Key not found"
Create a `.env` file with your `GOOGLE_API_KEY`

### "ChromaDB error"
Delete the `chroma_db` folder and restart (will rebuild)

### "Model loading failed"
Ensure your 3D model is valid and in a supported format (.stl, .obj, .3mf)

### "Orca Slicer not opening"
Update `ORCA_SLICER_PATH` in `.env` or `config.py`

## 🚀 Future Enhancements

- [ ] Support for more slicers (Cura, PrusaSlicer)
- [ ] Multi-material profiles
- [ ] Print time estimation
- [ ] Cost calculation
- [ ] Web-based 3D model viewer
- [ ] API endpoint for automation
- [ ] Fine-tuned model on 3D printing data

## 📧 Support

For issues or questions, please check:
1. This README
2. Configuration in `config.py`
3. Example usage in `cli.py`

---

**Made with ❤️ for the 3D printing community**

