# 🚀 Setup Guide

Complete setup instructions for the AI 3D Print Profile Generator.

## Prerequisites

- **Python 3.8 or higher**
- **Google Gemini API Key** ([Get free API key](https://makersuite.google.com/app/apikey))
- **Internet connection** (for API access)
- **Orca Slicer** (optional, for direct profile import)

## Step-by-Step Setup

### 1. Python Installation

Check if Python is installed:
```bash
python --version
```

If not installed, download from [python.org](https://www.python.org/downloads/)

### 2. Install Dependencies

Open a terminal/command prompt in the project directory:

```bash
# Windows
cd "C:\Users\isman\Documents\AI AGENT"
pip install -r requirements.txt

# Linux/Mac
cd ~/Documents/AI\ AGENT
pip install -r requirements.txt
```

### 3. Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

### 4. Configure Environment

Create a file named `.env` in the project root directory:

**Windows:**
```bash
# Create the file
notepad .env
```

**Linux/Mac:**
```bash
nano .env
```

Add this content (replace with your actual API key):
```env
GOOGLE_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ORCA_SLICER_PATH=C:\Program Files\OrcaSlicer\orca-slicer.exe
```

Save and close the file.

### 5. Verify Installation

Test the setup:

```bash
python cli.py --stats
```

You should see:
```
🤖 Initializing AI 3D Print Agent...
✓ Feature Extractor ready
✓ Gemini AI connected
✓ Knowledge Base loaded
✓ Profile Generator ready

📚 Knowledge Base: 0 cases

✅ AI Agent ready!
```

## Common Issues

### "Module not found" Error

**Solution:** Install missing packages
```bash
pip install -r requirements.txt
```

### "API Key not found" Error

**Solution:** Create `.env` file with your `GOOGLE_API_KEY`

### "ChromaDB error"

**Solution 1:** Install C++ build tools (Windows)
- Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2022)
- Install "Desktop development with C++"

**Solution 2:** Use alternative ChromaDB installation
```bash
pip install chromadb --no-binary chromadb
```

### "Trimesh import error"

**Solution:** Install dependencies
```bash
pip install trimesh[easy]
```

### Permission Errors

**Windows:** Run as Administrator
```bash
# Right-click Command Prompt → "Run as Administrator"
```

**Linux/Mac:** Use sudo
```bash
sudo pip install -r requirements.txt
```

## Testing the Installation

### 1. Test with Web UI

```bash
python app.py
```

Open browser to: `http://localhost:7860`

### 2. Test with CLI (if you have a test model)

```bash
python cli.py path/to/test_model.stl
```

## Optional: Orca Slicer Integration

### Windows
1. Download [Orca Slicer](https://github.com/SoftFever/OrcaSlicer/releases)
2. Install to default location
3. Update `.env` with correct path:
```env
ORCA_SLICER_PATH=C:\Program Files\OrcaSlicer\orca-slicer.exe
```

### Linux
```bash
# Install Orca Slicer (AppImage)
chmod +x OrcaSlicer.AppImage

# Update .env
ORCA_SLICER_PATH=/home/username/OrcaSlicer.AppImage
```

### Mac
```bash
# Install via Homebrew
brew install --cask orcaslicer

# Update .env
ORCA_SLICER_PATH=/Applications/OrcaSlicer.app/Contents/MacOS/OrcaSlicer
```

## Next Steps

1. ✅ Installation complete
2. 📖 Read the [README.md](README.md) for usage instructions
3. 🎯 Try analyzing your first 3D model
4. 💾 Provide feedback to build your knowledge base
5. 🚀 Watch the AI improve over time!

## Getting Help

If you encounter issues:

1. **Check this guide** for common solutions
2. **Review error messages** carefully
3. **Verify API key** is correct in `.env`
4. **Test internet connection** (required for Gemini API)
5. **Check Python version** (3.8+ required)

## System Requirements

### Minimum
- Python 3.8+
- 4 GB RAM
- 500 MB disk space
- Internet connection

### Recommended
- Python 3.10+
- 8 GB RAM
- 1 GB disk space (for knowledge base growth)
- Stable internet connection

## Security Notes

🔒 **Important:**
- Never commit `.env` file to version control
- Keep your API key private
- Don't share your API key publicly
- Google Gemini has free tier limits

## API Usage Limits

Google Gemini 2.5 Flash (free tier):
- 15 requests per minute
- 1,500 requests per day
- 1 million tokens per minute

For heavy usage, consider:
- [Google AI Studio pricing](https://ai.google.dev/pricing)
- Upgrading to paid tier

---

**Setup Complete! 🎉**

You're ready to start generating intelligent 3D print profiles!

