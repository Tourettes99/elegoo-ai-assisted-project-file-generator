"""
Dynamic Knowledge Base with Vector Storage
Stores and retrieves learned experiences from 3D printing profiles
"""
import chromadb
from chromadb.config import Settings
import json
import os
import numpy as np
from typing import Dict, Any, List, Optional
from datetime import datetime
from config import CHROMA_COLLECTION_NAME, CHROMA_PERSIST_DIR, KNOWLEDGE_BASE_DIR


def convert_to_json_serializable(obj):
    """Convert NumPy types to JSON-serializable Python types"""
    if isinstance(obj, (np.integer, np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64, np.float32)):
        return float(obj)
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_json_serializable(item) for item in obj]
    return obj


class KnowledgeBase:
    """Dynamic learning knowledge base for 3D printing profiles"""
    
    def __init__(self):
        """Initialize the knowledge base with ChromaDB"""
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=CHROMA_PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_or_create_collection(
                name=CHROMA_COLLECTION_NAME,
                metadata={"description": "3D model features and slicer profiles"}
            )
        except Exception as e:
            print(f"Warning: ChromaDB collection error: {e}")
            # Create new collection
            self.collection = self.client.create_collection(
                name=CHROMA_COLLECTION_NAME,
                metadata={"description": "3D model features and slicer profiles"}
            )
        
        # JSON storage for detailed cases
        self.cases_file = os.path.join(KNOWLEDGE_BASE_DIR, "cases.json")
        self._ensure_cases_file()
    
    def _ensure_cases_file(self):
        """Ensure the cases JSON file exists"""
        if not os.path.exists(self.cases_file):
            with open(self.cases_file, 'w') as f:
                json.dump([], f)
    
    def add_case(self, 
                 model_features: Dict[str, Any], 
                 profile: Dict[str, Any],
                 analysis: Dict[str, Any],
                 feedback: Optional[str] = None) -> str:
        """
        Add a new case to the knowledge base
        
        Args:
            model_features: Extracted features from the model
            profile: Generated slicer profile
            analysis: AI analysis results
            feedback: Optional user feedback
            
        Returns:
            Case ID
        """
        
        # Generate unique case ID
        case_id = f"case_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{model_features.get('model_hash', '')[:8]}"
        
        # Create case record and convert all NumPy types
        case = convert_to_json_serializable({
            "id": case_id,
            "timestamp": datetime.now().isoformat(),
            "model_features": model_features,
            "profile": profile,
            "analysis": analysis,
            "feedback": feedback,
            "success": self._determine_success(feedback) if feedback else None
        })
        
        # Create searchable text representation
        search_text = self._create_search_text(model_features, analysis)
        
        # Add to ChromaDB for vector search
        try:
            self.collection.add(
                ids=[case_id],
                documents=[search_text],
                metadatas=[{
                    "model_hash": str(model_features.get("model_hash", "")),
                    "volume": float(model_features.get("volume", 0)),
                    "has_overhangs": str(bool(model_features.get("overhangs", {}).get("has_overhangs", False))),
                    "detail_level": str(model_features.get("complexity", {}).get("detail_level", "medium")),
                    "timestamp": str(case["timestamp"])
                }]
            )
        except Exception as e:
            print(f"Warning: Failed to add to ChromaDB: {e}")
        
        # Add to JSON storage
        self._append_to_cases_file(case)
        
        return case_id
    
    def _create_search_text(self, features: Dict[str, Any], analysis: Dict[str, Any]) -> str:
        """Create searchable text representation of a case"""
        parts = []
        
        # Dimensions
        if "dimensions" in features:
            dims = features["dimensions"]
            parts.append(f"Dimensions: {float(dims.get('width', 0)):.1f}x{float(dims.get('depth', 0)):.1f}x{float(dims.get('height', 0)):.1f}mm")
        
        # Complexity
        if "complexity" in features:
            comp = features["complexity"]
            parts.append(f"Detail level: {comp.get('detail_level', 'unknown')}")
            parts.append(f"Watertight: {bool(comp.get('is_watertight', False))}")
        
        # Overhangs
        if "overhangs" in features:
            oh = features["overhangs"]
            if bool(oh.get("needs_supports")):
                parts.append(f"Needs supports: {float(oh.get('overhang_percentage', 0)):.1f}% overhangs")
        
        # Analysis
        if "analysis" in analysis:
            ana = analysis["analysis"]
            parts.append(f"Type: {ana.get('model_type', 'unknown')}")
            parts.append(f"Complexity: {ana.get('complexity_assessment', 'medium')}")
        
        # Profile summary
        if "profile" in analysis:
            prof = analysis["profile"]
            parts.append(f"Layer height: {prof.get('layer_height', 0.2)}mm")
            parts.append(f"Infill: {prof.get('infill_percentage', 20)}%")
            parts.append(f"Speed: {prof.get('print_speed', 60)}mm/s")
        
        return " | ".join(parts)
    
    def _determine_success(self, feedback: str) -> bool:
        """Determine if feedback indicates success"""
        if not feedback:
            return None
        
        feedback_lower = feedback.lower()
        positive_keywords = ["good", "great", "excellent", "perfect", "success", "worked", "nice"]
        negative_keywords = ["bad", "failed", "poor", "issue", "problem", "error", "terrible"]
        
        pos_count = sum(1 for kw in positive_keywords if kw in feedback_lower)
        neg_count = sum(1 for kw in negative_keywords if kw in feedback_lower)
        
        if pos_count > neg_count:
            return True
        elif neg_count > pos_count:
            return False
        else:
            return None
    
    def find_similar_cases(self, 
                          model_features: Dict[str, Any], 
                          limit: int = 5) -> List[Dict[str, Any]]:
        """
        Find similar cases from the knowledge base
        
        Args:
            model_features: Features of the current model
            limit: Maximum number of similar cases to return
            
        Returns:
            List of similar cases
        """
        
        # Create search query
        search_text = self._create_search_text(model_features, {})
        
        try:
            # Query ChromaDB
            results = self.collection.query(
                query_texts=[search_text],
                n_results=limit
            )
            
            # Load full case details from JSON
            if results and results["ids"] and len(results["ids"][0]) > 0:
                case_ids = results["ids"][0]
                return self._load_cases_by_ids(case_ids)
            else:
                return []
                
        except Exception as e:
            print(f"Warning: Similar case search failed: {e}")
            return []
    
    def _load_cases_by_ids(self, case_ids: List[str]) -> List[Dict[str, Any]]:
        """Load full case details from JSON file"""
        try:
            with open(self.cases_file, 'r') as f:
                all_cases = json.load(f)
            
            # Filter to requested IDs
            return [case for case in all_cases if case["id"] in case_ids]
            
        except Exception as e:
            print(f"Warning: Failed to load cases: {e}")
            return []
    
    def _append_to_cases_file(self, case: Dict[str, Any]):
        """Append a case to the JSON file"""
        try:
            # Load existing cases
            with open(self.cases_file, 'r') as f:
                cases = json.load(f)
            
            # Append new case
            cases.append(case)
            
            # Save back
            with open(self.cases_file, 'w') as f:
                json.dump(cases, indent=2, fp=f)
                
        except Exception as e:
            print(f"Warning: Failed to save case: {e}")
    
    def get_all_cases(self) -> List[Dict[str, Any]]:
        """Get all cases from the knowledge base"""
        try:
            with open(self.cases_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load cases: {e}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the knowledge base"""
        cases = self.get_all_cases()
        
        total_cases = len(cases)
        successful_cases = sum(1 for c in cases if c.get("success") is True)
        failed_cases = sum(1 for c in cases if c.get("success") is False)
        
        return {
            "total_cases": total_cases,
            "successful_cases": successful_cases,
            "failed_cases": failed_cases,
            "unknown_outcome": total_cases - successful_cases - failed_cases,
            "success_rate": (successful_cases / total_cases * 100) if total_cases > 0 else 0
        }
    
    def export_knowledge(self, output_path: str):
        """Export entire knowledge base to a file"""
        cases = self.get_all_cases()
        stats = self.get_statistics()
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "statistics": stats,
            "cases": cases
        }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        return output_path

