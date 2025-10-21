# 📖 How to Import AI-Generated Profiles in Orca Slicer

## 🎯 Quick Method (Recommended)

### Step 1: Open the Model
1. Open Orca Slicer
2. Drag and drop the `.3mf` file OR click "Add" and select your `.stl` file

### Step 2: Import the Config
1. In Orca Slicer, go to: **File → Import → Import Config...**
2. Select the `.ini` file (same name as your 3MF, but with `.ini` extension)
3. Click "Open"

### Step 3: Verify Tree Supports (if applicable)
1. Check the **Support** panel on the right
2. If tree supports were recommended, you should see:
   - **Type**: `tree` or `tree(auto)`
   - **Style**: `tree`
   - **Enable support**: ✓ checked

### Step 4: Slice and Print!
1. Click "Slice Plate"
2. Review the preview
3. Export G-code and print

---

## 🌳 Tree Support Verification

If your model had complex overhangs, the AI should have enabled tree supports.

**Check if tree supports are active:**
- Look at the **Support** section (usually on the right panel)
- **Type** should show: `tree` or `tree(auto)`
- **Style** should show: `tree`

**If tree supports are NOT enabled but should be:**
1. Manually change **Type** to: `tree(auto)`
2. Change **Style** to: `tree`
3. Set **Threshold angle** to: `45°`

---

## 📁 Generated Files Explanation

After analysis, you get:

| File | Purpose | How to Use |
|------|---------|------------|
| `model_xxx.3mf` | 3D model | Open in Orca Slicer |
| `model_xxx.ini` | **Config file** | **Import this!** (File → Import → Import Config) |
| `model_xxx.json` | Reference data | For your records |
| `model_xxx_summary.txt` | Human-readable explanation | Read to understand why AI chose those settings |

---

## 🔧 Manual Import (Alternative)

If automatic import doesn't work:

### For Print Settings:
1. Open the `.ini` file in a text editor
2. Look at the `[print]` section
3. Manually enter values in Orca Slicer

### For Support Settings:
Look for these lines in the `.ini` file:
```ini
enable_support = 1
support_type = tree
support_style = tree
support_threshold_angle = 45
tree_support_branch_angle = 45
tree_support_branch_distance = 2.5
```

Then in Orca Slicer:
- Enable support: ✓
- Type: tree(auto)
- Style: tree
- Threshold angle: 45°

---

## ❓ Troubleshooting

### Tree Supports Not Showing Up?
**Solution:** Import the `.ini` config file:
1. File → Import → Import Config...
2. Select the `.ini` file
3. Check Support panel again

### Config Import Does Nothing?
**Solution:** Orca Slicer might not import all settings. Manually check:
- Layer height
- Support type
- Infill percentage
- Print speeds

### Want to Save This Profile?
After importing:
1. Click the **save** icon next to the profile dropdown
2. Give it a name like "AI - High Detail" or "AI - Tree Supports"
3. Reuse it for similar models!

---

## 💡 Pro Tips

1. **Read the Summary**: The `_summary.txt` file explains WHY the AI chose specific settings
2. **Trust but Verify**: Always preview the slice before printing
3. **Provide Feedback**: After printing, use the feedback feature so the AI learns!
4. **Save Good Profiles**: If a profile works great, save it in Orca Slicer for reuse

---

## 🚀 Expected Results

**For models with complex overhangs:**
- Tree supports will be enabled automatically
- You'll see organic tree-like support structures
- Less material used than normal supports
- Easier to remove after printing

**For simple models:**
- Normal supports (if needed)
- Standard settings optimized for the model
- Balanced quality vs speed

---

Need help? Run: `python cli.py --help`

