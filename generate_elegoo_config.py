"""
Generate a standalone Elegoo Orca Slicer configuration from analysis results
This creates a config that can be manually pasted into Elegoo Orca Slicer
"""
import sys
import json
import os


def create_elegoo_instructions(profile, analysis, material="PLA"):
    """Create manual configuration instructions for Elegoo Orca Slicer"""
    
    is_tree = profile.get('support_style') == 'tree' or 'tree' in str(profile.get('support_type', '')).lower()
    
    instructions = f"""
╔════════════════════════════════════════════════════════════════════════╗
║          ELEGOO ORCA SLICER - MANUAL CONFIGURATION GUIDE               ║
╚════════════════════════════════════════════════════════════════════════╝

Material: {material}
Model Type: {analysis.get('analysis', {}).get('model_type', 'Unknown')}
Complexity: {analysis.get('analysis', {}).get('complexity_assessment', 'Medium')}

═══════════════════════════════════════════════════════════════════════════

📋 PRINT SETTINGS - Copy these values into Elegoo Orca Slicer:

┌─ Quality ─────────────────────────────────────────────────────────────┐
│ Layer Height:              {profile.get('layer_height', 0.2)} mm
│ Initial Layer Height:      {profile.get('first_layer_height', 0.2)} mm
└───────────────────────────────────────────────────────────────────────┘

┌─ Strength ────────────────────────────────────────────────────────────┐
│ Wall Loops:                {profile.get('perimeters', 3)}
│ Top Shell Layers:          {profile.get('top_solid_layers', 5)}
│ Bottom Shell Layers:       {profile.get('bottom_solid_layers', 5)}
└───────────────────────────────────────────────────────────────────────┘

┌─ Infill ──────────────────────────────────────────────────────────────┐
│ Sparse Infill Density:     {profile.get('infill_percentage', 20)}%
│ Sparse Infill Pattern:     {profile.get('infill_pattern', 'cubic')}
└───────────────────────────────────────────────────────────────────────┘

┌─ Support ─────────────────────────────────────────────────────────────┐
│ Enable Support:            {'YES ✓' if profile.get('support_material', False) else 'NO'}
"""
    
    if profile.get('support_material', False):
        if is_tree:
            instructions += f"""│ Support Type:              tree(auto)  🌳 TREE SUPPORTS
│ Support Style:             tree
│ Tree Branch Angle:         {profile.get('tree_support_branch_angle', 45)}°
│ Tree Branch Distance:      {profile.get('tree_support_branch_distance', 2.5)} mm
"""
        else:
            instructions += f"""│ Support Type:              normal(auto)
│ Support Style:             default
"""
        instructions += f"""│ Support Threshold Angle:   {profile.get('support_angle_threshold', 45)}°
"""
    
    instructions += f"""└───────────────────────────────────────────────────────────────────────┘

┌─ Speed (mm/s) ────────────────────────────────────────────────────────┐
│ Default Speed:             {profile.get('print_speed', 60)}
│ Initial Layer Speed:       {profile.get('first_layer_speed', 20)}
│ Outer Wall Speed:          {profile.get('perimeter_speed', 45)}
│ Inner Wall Speed:          {profile.get('perimeter_speed', 45)}
│ Sparse Infill Speed:       {profile.get('infill_speed', 80)}
│ Travel Speed:              {profile.get('travel_speed', 150)}
└───────────────────────────────────────────────────────────────────────┘

┌─ Temperature (°C) ────────────────────────────────────────────────────┐
│ Nozzle Temperature:        {profile.get('temperature', 210)}
│ Bed Temperature:           {profile.get('bed_temperature', 60)}
└───────────────────────────────────────────────────────────────────────┘

┌─ Cooling ─────────────────────────────────────────────────────────────┐
│ Fan Max Speed:             {profile.get('cooling_fan_speed', 100)}%
│ Fan Min Speed:             {profile.get('first_layer_fan_speed', 0)}%
└───────────────────────────────────────────────────────────────────────┘

┌─ Other ───────────────────────────────────────────────────────────────┐
│ Brim Width:                {profile.get('brim_width', 0)} mm
│ Retraction Length:         {profile.get('retraction_length', 0.8)} mm
│ Retraction Speed:          {profile.get('retraction_speed', 35)} mm/s
└───────────────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════════════════

🎯 HOW TO APPLY IN ELEGOO ORCA SLICER:

1. Open Elegoo Orca Slicer
2. Load your 3D model
3. Manually enter each value from above into the corresponding field
4. Pay special attention to:
"""
    
    if is_tree and profile.get('support_material'):
        instructions += """   ⚠️  SUPPORT TYPE: Set to "tree(auto)" or "tree"
   ⚠️  SUPPORT STYLE: Set to "tree"
"""
    
    instructions += """
5. Save your profile with a custom name (e.g., "AI - High Detail")
6. Slice and print!

═══════════════════════════════════════════════════════════════════════════

💡 AI REASONING:

"""
    instructions += analysis.get('reasoning', 'No reasoning provided.')
    instructions += """

═══════════════════════════════════════════════════════════════════════════
Generated by AI 3D Print Profile Generator
"""
    
    return instructions


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_elegoo_config.py <json_profile_file>")
        print("\nOr use 'latest' to process the most recent profile:")
        print("  python generate_elegoo_config.py latest")
        return
    
    file_path = sys.argv[1]
    
    if file_path == "latest":
        # Find latest JSON in generated_profiles
        import glob
        profiles_dir = "generated_profiles"
        if not os.path.exists(profiles_dir):
            print(f"❌ Directory not found: {profiles_dir}")
            return
        
        files = glob.glob(os.path.join(profiles_dir, "*.json"))
        if not files:
            print(f"❌ No .json files found in {profiles_dir}/")
            return
        
        file_path = max(files, key=os.path.getmtime)
        print(f"Found latest: {os.path.basename(file_path)}\n")
    
    # Load the JSON profile
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        profile = data.get('settings', data.get('profile', {}))
        material = data.get('material', 'PLA')
        analysis = data
        
        # Generate instructions
        instructions = create_elegoo_instructions(profile, analysis, material)
        
        # Save to file
        output_path = file_path.replace('.json', '_ELEGOO_MANUAL.txt')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        # Also print to console
        print(instructions)
        print(f"\n📄 Instructions saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

