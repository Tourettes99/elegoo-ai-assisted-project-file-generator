# 📚 Usage Examples

Practical examples of using the AI 3D Print Profile Generator.

## Table of Contents
- [Quick Start Examples](#quick-start-examples)
- [Web Interface Examples](#web-interface-examples)
- [Command Line Examples](#command-line-examples)
- [Python API Examples](#python-api-examples)
- [Advanced Usage](#advanced-usage)

---

## Quick Start Examples

### 1. First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
python quick_start.py

# Start web interface
python app.py
```

### 2. Analyze Your First Model

```bash
# Simple analysis
python cli.py my_model.stl

# With specific material
python cli.py my_model.stl --material PETG

# Save with feedback
python cli.py my_model.stl --feedback "Great print quality!"
```

---

## Web Interface Examples

### Example 1: Basic Model Analysis

1. Start the web server:
   ```bash
   python app.py
   ```

2. Open browser to `http://localhost:7860`

3. Click "🚀 Initialize AI Agent"

4. Upload a 3D model (.stl file)

5. Select material (e.g., PLA)

6. Click "🔍 Analyze Model"

7. Download the generated profile

8. Import into Orca Slicer

### Example 2: Learning from Prints

1. Go to "💾 Save with Feedback" tab

2. Upload your model

3. Add feedback in the text box:
   - **Good print**: "Excellent quality, no issues"
   - **Bad print**: "Supports failed, too much stringing"
   - **Mediocre**: "OK quality but slow"

4. Click "💾 Analyze & Save"

5. The AI will learn from this case!

### Example 3: View Progress

1. Go to "📚 Knowledge Base" tab

2. Click "📊 View Statistics"

3. See your success rate improve over time

4. Export your knowledge for backup

---

## Command Line Examples

### Example 1: Quick Analysis

```bash
python cli.py dragon_miniature.stl
```

**Output:**
```
🤖 Initializing AI 3D Print Agent...
✓ Feature Extractor ready
✓ Gemini AI connected
✓ Knowledge Base loaded
✓ Profile Generator ready

📂 Loading model: dragon_miniature.stl
🔍 Extracting geometric features...

Dimensions: 30.0mm × 25.0mm × 80.0mm
Volume: 15000.00 mm³
Detail Level: high
Watertight: Yes
⚠️ Needs Supports (12.5% overhangs)
Wall Type: thin

🧠 Analyzing with Gemini AI...
   Model Type: miniature
   Complexity: high
   Quality Estimate: high

📝 Generating Orca Slicer profile...
   ✓ Profile saved: dragon_miniature_20251021_143022.json
   ✓ Summary saved: dragon_miniature_20251021_143022_summary.txt
```

### Example 2: Material-Specific Analysis

```bash
# For flexible materials
python cli.py phone_case.stl --material TPU

# For high-temp materials
python cli.py gear.stl --material ABS

# For strength
python cli.py bracket.stl --material PETG
```

### Example 3: With Feedback Loop

```bash
# After successful print
python cli.py model.stl --material PLA --feedback "Perfect quality, great layer adhesion"

# After failed print
python cli.py model.stl --material PLA --feedback "Failed - supports broke during print"
```

### Example 4: Disable Knowledge Base

```bash
# Fresh analysis without past cases
python cli.py new_design.stl --no-kb
```

### Example 5: Knowledge Base Management

```bash
# View statistics
python cli.py --stats

# Export knowledge base
python cli.py --export my_backup.json
```

---

## Python API Examples

### Example 1: Basic Integration

```python
from ai_agent import AI3DPrintAgent

# Initialize agent
agent = AI3DPrintAgent()

# Analyze a model
result = agent.analyze_model(
    model_path="my_model.stl",
    material="PLA",
    use_knowledge_base=True
)

# Access results
print(f"Model Type: {result['analysis']['analysis']['model_type']}")
print(f"Profile saved to: {result['profile_files']['json_profile']}")
```

### Example 2: Batch Processing

```python
import os
from ai_agent import AI3DPrintAgent

agent = AI3DPrintAgent()

# Process all STL files in a directory
stl_dir = "my_models/"
for filename in os.listdir(stl_dir):
    if filename.endswith('.stl'):
        print(f"Processing {filename}...")
        
        result = agent.analyze_model(
            model_path=os.path.join(stl_dir, filename),
            material="PLA"
        )
        
        # Save to knowledge base
        agent.save_to_knowledge_base(result)
        
        print(f"✓ {filename} complete!")
```

### Example 3: Custom Workflow

```python
from feature_extractor import FeatureExtractor
from gemini_agent import GeminiAgent

# Extract features manually
extractor = FeatureExtractor()
features = extractor.extract_from_file("model.stl")

# Get feature summary
summary = extractor.generate_summary(features)
print(summary)

# Custom AI analysis
ai = GeminiAgent()
analysis = ai.analyze_features(features)

print(f"Recommended infill: {analysis['profile']['infill_percentage']}%")
print(f"Reasoning: {analysis['reasoning']}")
```

### Example 4: Knowledge Base Queries

```python
from knowledge_base import KnowledgeBase

kb = KnowledgeBase()

# Get all cases
cases = kb.get_all_cases()
print(f"Total cases: {len(cases)}")

# Get statistics
stats = kb.get_statistics()
print(f"Success rate: {stats['success_rate']:.1f}%")

# Export
kb.export_knowledge("backup.json")
```

---

## Advanced Usage

### Example 1: Custom Feature Analysis

```python
from feature_extractor import FeatureExtractor
import trimesh

# Load model with trimesh directly
mesh = trimesh.load("complex_model.stl")

# Apply transformations
mesh.apply_scale(2.0)  # Scale 2x
mesh.apply_transform(trimesh.transformations.rotation_matrix(
    angle=1.57,  # 90 degrees
    direction=[1, 0, 0]
))

# Analyze transformed model
extractor = FeatureExtractor(overhang_threshold=50)  # Custom threshold
features = extractor.extract_features(mesh)

print(f"Volume: {features['volume']}")
print(f"Overhangs: {features['overhangs']['overhang_percentage']}%")
```

### Example 2: Multi-Material Comparison

```python
from ai_agent import AI3DPrintAgent

agent = AI3DPrintAgent()
materials = ["PLA", "PETG", "ABS"]

results = {}
for material in materials:
    result = agent.analyze_model(
        model_path="functional_part.stl",
        material=material
    )
    
    profile = result['analysis']['profile']
    results[material] = {
        'temp': profile['temperature'],
        'speed': profile['print_speed'],
        'quality': result['analysis']['estimated_quality']
    }

# Compare
for material, params in results.items():
    print(f"{material}: {params['temp']}°C, {params['speed']}mm/s, {params['quality']}")
```

### Example 3: Integration with Slicer Automation

```python
from ai_agent import AI3DPrintAgent
import subprocess

agent = AI3DPrintAgent()

# Analyze model
result = agent.analyze_model("part.stl", material="PETG")

# Get profile path
profile_path = result['profile_files']['json_profile']

# Auto-open in Orca Slicer
agent.open_profile_in_slicer(profile_path)

# Or use custom command
subprocess.run([
    "orca-slicer",
    "--load-config", profile_path,
    "--export-gcode",
    "--output", "output.gcode",
    "part.stl"
])
```

### Example 4: Learning from User Feedback

```python
from ai_agent import AI3DPrintAgent

agent = AI3DPrintAgent()

# Analyze and get user input
result = agent.analyze_model("model.stl", material="PLA")

print("Profile generated! Please print and provide feedback.")
print("After printing, run this script again with feedback.")

# After printing...
feedback = input("How was the print? (good/bad/notes): ")

# Save with feedback
agent.save_to_knowledge_base(result, feedback=feedback)

print("✓ Feedback saved! AI will learn from this.")
```

---

## Workflow Scenarios

### Scenario 1: New to 3D Printing

**Goal**: Get safe, reliable profiles

```bash
# Start with defaults
python cli.py model.stl

# Review the generated summary file
cat generated_profiles/*_summary.txt

# Use the profile
# Import JSON into Orca Slicer

# After first successful print
python cli.py model.stl --feedback "Good result"
```

### Scenario 2: Experienced User Optimization

**Goal**: Fine-tune profiles based on experience

```python
from ai_agent import AI3DPrintAgent

agent = AI3DPrintAgent()

# Analyze with knowledge base
result = agent.analyze_model("advanced_part.stl", material="PETG")

# Review AI suggestions
print(result['analysis']['reasoning'])

# After testing
feedback = """
Layer height 0.2mm was good
Needed more top layers (used 7 instead of 5)
Speed was perfect
"""

agent.save_to_knowledge_base(result, feedback=feedback)
```

### Scenario 3: Print Farm Automation

**Goal**: Batch process multiple models

```python
import os
from ai_agent import AI3DPrintAgent

agent = AI3DPrintAgent()
queue_dir = "print_queue/"

for model_file in sorted(os.listdir(queue_dir)):
    if not model_file.endswith('.stl'):
        continue
    
    print(f"Processing {model_file}...")
    
    result = agent.process_with_feedback(
        model_path=os.path.join(queue_dir, model_file),
        material="PLA"
    )
    
    # Export to specific location
    profile_path = result['profile_files']['json_profile']
    print(f"  → Profile: {profile_path}")
    
    # Queue for printing...
```

---

## Tips and Tricks

### Tip 1: Improving AI Accuracy

- Provide detailed feedback after each print
- Be specific: "supports broke" vs "print failed"
- Include successes and failures
- The more cases, the better the AI learns

### Tip 2: Material Profiles

Different materials need different approaches:

- **PLA**: Balanced settings, good for learning
- **PETG**: Slower speeds, higher temp
- **ABS**: Heated chamber, warping prevention
- **TPU**: Slow speed, minimal retraction

### Tip 3: Model Preparation

Before analysis:
- Ensure model is watertight
- Correct orientation matters
- Scale appropriately
- Check for errors in mesh

### Tip 4: Knowledge Base Management

```bash
# Regular backups
python cli.py --export "backup_$(date +%Y%m%d).json"

# Review statistics periodically
python cli.py --stats

# Clean start if needed (delete chroma_db/ and knowledge_base/)
```

---

**Need more examples? Check the [README.md](README.md) or run `python cli.py --help`**

