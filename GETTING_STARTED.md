# 🚀 Getting Started

Quick guide to get up and running with the AI 3D Print Profile Generator in 5 minutes!

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Dependencies (2 min)

```bash
pip install -r requirements.txt
```

### Step 2: Get API Key (1 min)

1. Visit https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Step 3: Configure (1 min)

Create a `.env` file:

```bash
# Windows
notepad .env

# Linux/Mac
nano .env
```

Add this line (paste your actual API key):
```
GOOGLE_API_KEY=your_actual_api_key_here
```

Save and close.

### Step 4: Verify Installation (1 min)

```bash
python quick_start.py
```

You should see all checks pass! ✅

### Step 5: Start Using It!

**Option A: Web Interface** (Easiest)
```bash
python app.py
```
Open http://localhost:7860 in your browser

**Option B: Command Line**
```bash
python cli.py your_model.stl
```

---

## 📖 First Time Usage

### Using the Web Interface

1. **Start the app:**
   ```bash
   python app.py
   ```

2. **In your browser** (http://localhost:7860):
   - Click "🚀 Initialize AI Agent"
   - Wait for "✅ AI Agent initialized successfully!"

3. **Analyze a model:**
   - Click "📂 Upload 3D Model"
   - Select your .stl file
   - Choose material (default: PLA)
   - Click "🔍 Analyze Model"

4. **Get your profile:**
   - Review the analysis
   - Download the JSON profile
   - Download the text summary

5. **Import to Orca Slicer:**
   - Open Orca Slicer
   - Import the downloaded JSON file
   - Slice and print!

### Using the Command Line

```bash
# Basic usage
python cli.py model.stl

# With material
python cli.py model.stl --material PETG

# After printing, save feedback
python cli.py model.stl --feedback "Great print!"

# View your learning progress
python cli.py --stats
```

---

## 🎯 Your First Analysis

Let's walk through a complete example:

### 1. Prepare a Model

Have a 3D model ready (e.g., `dragon.stl`)

### 2. Run the Analysis

**Via Web:**
```bash
python app.py
```
Then upload `dragon.stl` in the browser.

**Via CLI:**
```bash
python cli.py dragon.stl --material PLA
```

### 3. What Happens

The AI will:
1. ✅ Analyze the geometry (dimensions, overhangs, complexity)
2. 🔍 Search for similar past prints
3. 🧠 Generate optimal settings using Gemini AI
4. 📄 Create a profile file
5. 💡 Explain why it chose those settings

### 4. Review the Output

You'll get two files:
- **JSON Profile**: Import into Orca Slicer
- **Text Summary**: Human-readable explanation

Example summary:
```
Model Type: miniature
Complexity: high
Needs Supports: Yes (12.5% overhangs)

Recommended Settings:
- Layer Height: 0.12 mm (high detail for miniature)
- Infill: 15% (decorative piece)
- Supports: Yes (overhangs detected)
- Speed: 45 mm/s (slower for detail)
- Temperature: 210°C (PLA)
```

### 5. Use the Profile

1. Import JSON into Orca Slicer
2. Review settings (they're optimized but you can adjust)
3. Slice and print!

### 6. Provide Feedback

After printing:

**Via Web:**
- Go to "💾 Save with Feedback" tab
- Upload the same model
- Add feedback: "Perfect quality!" or "Supports were hard to remove"
- Click save

**Via CLI:**
```bash
python cli.py dragon.stl --feedback "Excellent detail, no issues"
```

The AI learns from this! Next time you print something similar, it'll be even better.

---

## 🎓 Learning the System

### How It Gets Smarter

1. **First Time**: AI analyzes fresh, uses general knowledge
2. **After Feedback**: Your experience is saved
3. **Next Similar Model**: AI applies what it learned
4. **Over Time**: Success rate improves

### Example Learning Journey

**Print #1: Small miniature**
```bash
python cli.py mini1.stl
# AI generates profile (no past data)
# Print succeeds
python cli.py mini1.stl --feedback "Perfect!"
```

**Print #5: Another miniature**
```bash
python cli.py mini5.stl
# AI finds 4 similar past cases
# Applies learned lessons
# Profile is better than #1!
```

**Print #20: Complex miniature**
```bash
python cli.py complex_mini.stl
# AI has extensive miniature experience
# Generates near-perfect profile
# You trust it!
```

---

## 💡 Tips for Success

### 1. Start Simple
- Use PLA for first few prints
- Start with proven models
- Build confidence in the system

### 2. Always Provide Feedback
- Even "good" or "bad" helps
- Specific feedback is better: "supports perfect" or "too fast"
- Both successes AND failures teach the AI

### 3. Check the Reasoning
- Read the AI's explanation
- Learn why it chose those settings
- Adjust if you disagree

### 4. Trust Improves Over Time
- First prints: Review carefully
- After 10+ successes: Trust more
- After 50+ cases: Very reliable

### 5. Material Matters
- Different materials = different profiles
- Build separate knowledge for each
- PLA first, then PETG, then others

---

## 🔧 Common First-Time Issues

### "Module not found"
**Fix:**
```bash
pip install -r requirements.txt
```

### "API key not found"
**Fix:** Create `.env` file with `GOOGLE_API_KEY=your_key`

### "No module named 'dotenv'"
**Fix:**
```bash
pip install python-dotenv
```

### "ChromaDB error"
**Fix (Windows):** Install Visual Studio Build Tools
**Fix (Linux/Mac):** `pip install --upgrade chromadb`

### Web UI won't start
**Fix:** Make sure port 7860 is free, or edit `app.py` to change port

---

## 📚 Next Steps

Now that you're set up:

1. ✅ **Read**: [README.md](README.md) for full documentation
2. 🎯 **Try**: [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for more scenarios
3. 🔧 **Test**: Run `python test_system.py` to verify everything
4. 📖 **Learn**: Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for advanced config
5. 🚀 **Use**: Start generating profiles for your prints!

---

## 🎯 Quick Reference

### Essential Commands

```bash
# Setup
pip install -r requirements.txt
python quick_start.py

# Web UI
python app.py

# CLI - Basic
python cli.py model.stl

# CLI - With options
python cli.py model.stl --material PETG --feedback "Great!"

# Statistics
python cli.py --stats

# Test system
python test_system.py
```

### File Locations

- **Profiles**: `generated_profiles/`
- **Knowledge**: `knowledge_base/cases.json`
- **Vector DB**: `chroma_db/`
- **Config**: `.env` and `config.py`

### Key Files

- `app.py` - Web interface
- `cli.py` - Command line
- `config.py` - Settings
- `.env` - Your API key (create this!)

---

## 🆘 Getting Help

1. **Check this guide** first
2. **Run quick_start.py** to diagnose issues
3. **Read error messages** carefully
4. **Review SETUP_GUIDE.md** for detailed troubleshooting

---

## 🎉 You're Ready!

You now have:
- ✅ Installation complete
- ✅ API configured
- ✅ Understanding of how it works
- ✅ Ready to generate your first profile

**Go print something awesome!** 🚀

---

*Need more help? Check [README.md](README.md) or [SETUP_GUIDE.md](SETUP_GUIDE.md)*

