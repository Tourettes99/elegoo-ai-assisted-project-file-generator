"""
Main AI Agent Orchestrator
Coordinates all components: feature extraction, AI analysis, knowledge base, and profile generation
"""
from typing import Dict, Any, Optional, Tuple
import os
from feature_extractor import FeatureExtractor
from gemini_agent import GeminiAgent
from knowledge_base import KnowledgeBase
from profile_generator import ProfileGenerator


class AI3DPrintAgent:
    """
    Main AI Agent for 3D Print Profile Generation
    
    This agent:
    1. Analyzes 3D models and extracts features
    2. Searches for similar past cases in the knowledge base
    3. Uses Gemini AI to generate optimal slicer profiles
    4. Learns from each case to improve future predictions
    """
    
    def __init__(self, google_api_key: Optional[str] = None):
        """Initialize the AI agent with all components"""
        
        print("🤖 Initializing AI 3D Print Agent...")
        
        # Initialize components
        self.feature_extractor = FeatureExtractor()
        self.gemini_agent = GeminiAgent(api_key=google_api_key)
        self.knowledge_base = KnowledgeBase()
        self.profile_generator = ProfileGenerator()
        
        print("✓ Feature Extractor ready")
        print("✓ Gemini AI connected")
        print("✓ Knowledge Base loaded")
        print("✓ Profile Generator ready")
        
        # Load knowledge base stats
        stats = self.knowledge_base.get_statistics()
        print(f"\n📚 Knowledge Base: {stats['total_cases']} cases")
        if stats['total_cases'] > 0:
            print(f"   Success Rate: {stats['success_rate']:.1f}%")
        
        print("\n✅ AI Agent ready!\n")
    
    def analyze_model(self, 
                     model_path: str,
                     material: str = "PLA",
                     use_knowledge_base: bool = True,
                     slicer_type: str = "elegoo_orca",
                     build_plate_size: float = 220.0) -> Dict[str, Any]:
        """
        Complete analysis pipeline for a 3D model
        
        Args:
            model_path: Path to the 3D model file
            material: Printing material (PLA, PETG, ABS, etc.)
            use_knowledge_base: Whether to use past cases for reference
            slicer_type: Type of slicer (orca or elegoo_orca)
            build_plate_size: Build plate size in mm (e.g., 220, 256, 300)
            
        Returns:
            Complete analysis results with generated profile
        """
        
        print(f"📂 Loading model: {os.path.basename(model_path)}")
        print(f"   Full path: {os.path.abspath(model_path)}")
        print(f"   File exists: {os.path.exists(model_path)}")
        if os.path.exists(model_path):
            print(f"   File size: {os.path.getsize(model_path)} bytes")
        
        # Step 1: Extract features from the 3D model
        print("🔍 Extracting geometric features...")
        try:
            features = self.feature_extractor.extract_from_file(model_path)
            print("✓ Feature extraction complete")
        except Exception as e:
            print(f"❌ FEATURE EXTRACTION ERROR:")
            print(f"   Error type: {type(e).__name__}")
            print(f"   Error message: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        
        # Generate feature summary
        feature_summary = self.feature_extractor.generate_summary(features)
        print("\n" + feature_summary + "\n")
        
        # Step 2: Search knowledge base for similar cases
        similar_cases = []
        if use_knowledge_base:
            print("🔎 Searching for similar past cases...")
            similar_cases = self.knowledge_base.find_similar_cases(features, limit=3)
            
            if similar_cases:
                print(f"   Found {len(similar_cases)} similar case(s)")
                for i, case in enumerate(similar_cases, 1):
                    case_analysis = case.get("analysis", {}).get("analysis", {})
                    print(f"   {i}. {case_analysis.get('model_type', 'Unknown')} - "
                          f"{case_analysis.get('complexity_assessment', 'medium')} complexity")
            else:
                print("   No similar cases found - generating from scratch")
        
        # Step 3: AI analysis with Gemini
        print("\n🧠 Analyzing with Gemini AI...")
        analysis = self.gemini_agent.analyze_features(features, similar_cases)
        
        ana = analysis.get('analysis', {})
        prof = analysis.get('profile', {})
        print(f"   Model Type: {ana.get('model_type', 'Unknown')}")
        print(f"   Complexity: {ana.get('complexity_assessment', 'Medium')}")
        print(f"   Quality Estimate: {analysis.get('estimated_quality', 'Standard')}")
        
        # Show support selection
        if prof.get('support_material'):
            support_style = prof.get('support_style', 'default')
            support_type = prof.get('support_type', 'normal')
            if support_style == 'tree' or 'tree' in support_type:
                print(f"   🌳 Tree Supports: ENABLED (style: {support_style})")
            else:
                print(f"   📌 Normal Supports: enabled")
        
        # Step 4: Generate slicer profile
        slicer_name = "Elegoo Orca Slicer" if slicer_type == "elegoo_orca" else "Orca Slicer"
        print(f"\n📝 Generating {slicer_name} profile (build plate: {build_plate_size}mm)...")
        profile_files = self.profile_generator.generate_profile(
            analysis,
            model_name=os.path.basename(model_path),
            material=material,
            model_path=model_path,  # Pass model path for 3MF generation
            slicer_type=slicer_type,
            build_plate_size=build_plate_size
        )
        
        if "3mf_profile" in profile_files:
            print(f"   ✓ 3MF PROJECT saved: {os.path.basename(profile_files['3mf_profile'])} ⭐ USE THIS!")
        print(f"   ✓ JSON config saved: {os.path.basename(profile_files['json_config'])} (backup)")
        print(f"   ✓ Summary saved: {os.path.basename(profile_files['summary'])}")
        
        # Important user instructions
        print(f"\n💡 How to use in {slicer_name.upper()}:")
        if "3mf_profile" in profile_files:
            print(f"   METHOD 1 (RECOMMENDED): Open 3MF Project File")
            print(f"   1. Double-click: {os.path.basename(profile_files['3mf_profile'])}")
            print(f"      OR drag it into {slicer_name}")
            print("   2. Model + ALL settings load automatically!")
            if prof.get('support_material') and (prof.get('support_style') == 'tree' or 'tree' in str(prof.get('support_type', ''))):
                print("   3. Tree supports included!")
            print("   4. Slice and print!")
            print(f"\n   METHOD 2 (Backup): Import JSON config")
        else:
            print(f"   1. Open {slicer_name}")
            print("   2. Load your 3D model")
        print("   3. Go to: File -> Import -> Import Config...")
        print(f"   4. Select: {os.path.basename(profile_files['json_config'])}")
        if prof.get('support_material') and (prof.get('support_style') == 'tree' or 'tree' in str(prof.get('support_type', ''))):
            print("   5. Tree supports will be active!")
        print("   6. Slice and print!")
        
        # Combine results
        result = {
            "model_path": model_path,
            "material": material,
            "features": features,
            "similar_cases_count": len(similar_cases),
            "analysis": analysis,
            "profile_files": profile_files,
            "feature_summary": feature_summary
        }
        
        return result
    
    def save_to_knowledge_base(self,
                               result: Dict[str, Any],
                               feedback: Optional[str] = None) -> str:
        """
        Save analysis result to knowledge base for future learning
        
        Args:
            result: Result from analyze_model()
            feedback: Optional user feedback on print quality
            
        Returns:
            Case ID
        """
        
        print("\n💾 Saving to knowledge base...")
        
        case_id = self.knowledge_base.add_case(
            model_features=result["features"],
            profile=result["analysis"].get("profile", {}),
            analysis=result["analysis"],
            feedback=feedback
        )
        
        print(f"   ✓ Case saved: {case_id}")
        
        # Update stats
        stats = self.knowledge_base.get_statistics()
        print(f"   📚 Total cases: {stats['total_cases']}")
        
        return case_id
    
    def process_with_feedback(self,
                            model_path: str,
                            material: str = "PLA",
                            feedback: Optional[str] = None) -> Dict[str, Any]:
        """
        Complete workflow: analyze model and save to knowledge base
        
        Args:
            model_path: Path to 3D model
            material: Printing material
            feedback: Optional feedback to save with the case
            
        Returns:
            Analysis result
        """
        
        # Analyze the model
        result = self.analyze_model(model_path, material)
        
        # Save to knowledge base
        case_id = self.save_to_knowledge_base(result, feedback)
        result["case_id"] = case_id
        
        return result
    
    def get_knowledge_stats(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        return self.knowledge_base.get_statistics()
    
    def export_knowledge(self, output_path: str) -> str:
        """Export knowledge base to file"""
        return self.knowledge_base.export_knowledge(output_path)
    
    def open_profile_in_slicer(self, profile_path: str) -> bool:
        """Open a profile in Orca Slicer"""
        return self.profile_generator.open_in_orca_slicer(profile_path)

