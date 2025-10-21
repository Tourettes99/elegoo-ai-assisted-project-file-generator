"""
Configuration module for 3D AI Slicer Profile Generator
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Orca Slicer Configuration
ORCA_SLICER_PATH = os.getenv("ORCA_SLICER_PATH", r"C:\Program Files\OrcaSlicer\orca-slicer.exe")

# Model Configuration
GEMINI_MODEL = "gemini-2.5-flash"  # Using Gemini 2.5 Flash

# Slicer Configuration
SLICER_TYPE = "elegoo_orca"  # Only Elegoo Orca Slicer supported

# Paths
KNOWLEDGE_BASE_DIR = "knowledge_base"
PROFILES_OUTPUT_DIR = "generated_profiles"
MODELS_CACHE_DIR = "models_cache"

# Feature Extraction Settings
FEATURE_EXTRACTION = {
    "num_samples": 360,  # Number of rotation samples for analysis
    "resolution": 100,   # Resolution for feature detection
    "analyze_supports": True,
    "analyze_overhangs": True,
    "overhang_angle_threshold": 45,  # degrees
}

# ChromaDB Settings
CHROMA_COLLECTION_NAME = "model_features_memory"
CHROMA_PERSIST_DIR = "chroma_db"

# Create necessary directories
for directory in [KNOWLEDGE_BASE_DIR, PROFILES_OUTPUT_DIR, MODELS_CACHE_DIR, CHROMA_PERSIST_DIR]:
    os.makedirs(directory, exist_ok=True)

