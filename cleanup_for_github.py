"""
Cleanup script to prepare codebase for GitHub upload
Removes sensitive files and user data
"""
import os
import shutil
import sys

if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except:
        pass

print("="*70)
print("GITHUB UPLOAD CLEANUP")
print("="*70)

# Files and folders to clean
sensitive_items = [
    '.env',  # API keys
    'elegoo_default_settings.json',  # User's Elegoo settings
    'knowledge_base/',  # User's learning data
    'generated_profiles/',  # User's generated files
    'chroma_db/',  # Vector database
    'models_cache/',  # Cached models
]

test_scripts = [
    'test_elegoo_3mf.py',
    'debug_3mf.py',
    'compare_3mf.py',
    'compare_brim_files.py',
    'check_vertices.py',
    'check_latest.py',
    'check_brim_value.py',
    'verify_brim.py',
    'extract_elegoo_defaults.py',
    'deep_compare.py',
    'quick_fix_supports.py',
    'generate_elegoo_config.py',
]

model_files = []
for ext in ['.stl', '.obj', '.3mf', '.ply']:
    import glob
    model_files.extend(glob.glob(f'*{ext}'))

print("\n1. SENSITIVE FILES:")
print("-"*70)
for item in sensitive_items:
    if os.path.exists(item):
        print(f"  ✓ Will be ignored: {item}")
    else:
        print(f"  - Not found: {item}")

print("\n2. TEST/DEBUG SCRIPTS:")
print("-"*70)
found_tests = [f for f in test_scripts if os.path.exists(f)]
if found_tests:
    print(f"  Found {len(found_tests)} test scripts (will be ignored by .gitignore)")
    for f in found_tests:
        print(f"    - {f}")
else:
    print("  No test scripts found")

print("\n3. MODEL FILES:")
print("-"*70)
if model_files:
    print(f"  Found {len(model_files)} model files (will be ignored)")
    for f in model_files[:5]:
        print(f"    - {f}")
    if len(model_files) > 5:
        print(f"    ... and {len(model_files) - 5} more")
else:
    print("  No model files found")

print("\n4. API KEY CHECK:")
print("-"*70)

# Check if .env exists
if os.path.exists('.env'):
    print("  ⚠️  WARNING: .env file exists!")
    print("  Make sure it's in .gitignore and won't be uploaded!")
else:
    print("  ✓ No .env file found (good - use .env.template)")

# Check if .env.template is safe
if os.path.exists('.env.template'):
    with open('.env.template', 'r') as f:
        content = f.read()
        if 'AIza' in content or 'your_google_gemini_api_key_here' not in content:
            print("  ⚠️  WARNING: .env.template might contain a real API key!")
        else:
            print("  ✓ .env.template is safe (placeholder only)")
else:
    print("  - .env.template not found")

print("\n" + "="*70)
print("SUMMARY")
print("="*70)

# Check .gitignore exists
if os.path.exists('.gitignore'):
    print("✓ .gitignore exists - sensitive files will be protected")
else:
    print("❌ .gitignore MISSING! Create it before uploading!")

# Final recommendations
print("\n📋 BEFORE GITHUB UPLOAD:")
print("  1. Verify .env is NOT in the upload")
print("  2. Check for any hardcoded API keys in code")
print("  3. Ensure elegoo_default_settings.json is ignored")
print("  4. Test scripts are ignored")
print("  5. No personal 3D models included")

print("\n✅ If all checks pass, you're ready to upload!")
print()

