"""
3D Model Feature Extraction Module
Extracts geometric features from 3D models for AI analysis
"""
import trimesh
import numpy as np
from typing import Dict, Any, List
import hashlib
import os


class FeatureExtractor:
    """Extract features from 3D models for slicer profile generation"""
    
    def __init__(self, overhang_threshold: float = 45.0):
        self.overhang_threshold = overhang_threshold
    
    def load_model(self, file_path: str) -> trimesh.Trimesh:
        """Load a 3D model from file"""
        print(f"   🔍 FeatureExtractor loading model: {file_path}")
        print(f"      File exists: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            print(f"      File size: {os.path.getsize(file_path)} bytes")
            print(f"      File extension: {os.path.splitext(file_path)[1]}")
        
        try:
            mesh = trimesh.load(file_path, force='mesh')
            print(f"   ✓ Model loaded by trimesh")
            print(f"      Type: {type(mesh)}")
            
            if isinstance(mesh, trimesh.Scene):
                print(f"      Scene detected with {len(mesh.geometry)} geometries")
                # If it's a scene, combine all geometries
                geometries = [
                    geom for geom in mesh.geometry.values()
                    if isinstance(geom, trimesh.Trimesh)
                ]
                print(f"      Combining {len(geometries)} mesh geometries")
                mesh = trimesh.util.concatenate(geometries)
                print(f"   ✓ Scene combined into single mesh")
            
            print(f"      Vertices: {len(mesh.vertices)}")
            print(f"      Faces: {len(mesh.faces)}")
            print(f"      Volume: {mesh.volume:.2f}")
            print(f"      Area: {mesh.area:.2f}")
            
            return mesh
        except Exception as e:
            print(f"   ❌ MODEL LOADING ERROR in FeatureExtractor:")
            print(f"      File: {os.path.abspath(file_path)}")
            print(f"      Error type: {type(e).__name__}")
            print(f"      Error message: {str(e)}")
            import traceback
            print(f"      Traceback:")
            traceback.print_exc()
            raise ValueError(f"Failed to load 3D model: {str(e)}")
    
    def extract_features(self, mesh: trimesh.Trimesh) -> Dict[str, Any]:
        """Extract comprehensive features from a 3D mesh"""
        
        # Basic geometric properties
        features = {
            "model_hash": self._compute_model_hash(mesh),
            "volume": float(mesh.volume),
            "surface_area": float(mesh.area),
            "bounding_box": {
                "dimensions": mesh.bounding_box.extents.tolist(),
                "center": mesh.centroid.tolist(),
            },
            "vertex_count": int(len(mesh.vertices)),
            "face_count": int(len(mesh.faces)),
        }
        
        # Dimensional analysis
        dims = mesh.bounding_box.extents
        features["dimensions"] = {
            "width": float(dims[0]),
            "depth": float(dims[1]),
            "height": float(dims[2]),
            "max_dimension": float(np.max(dims)),
            "min_dimension": float(np.min(dims)),
        }
        
        # Complexity metrics
        features["complexity"] = self._analyze_complexity(mesh)
        
        # Overhang analysis
        features["overhangs"] = self._detect_overhangs(mesh)
        
        # Wall thickness estimation
        features["wall_analysis"] = self._analyze_walls(mesh)
        
        # Surface characteristics
        features["surface"] = self._analyze_surface(mesh)
        
        # Orientation suggestions
        features["orientation"] = self._suggest_orientation(mesh)
        
        return features
    
    def _compute_model_hash(self, mesh: trimesh.Trimesh) -> str:
        """Compute a hash of the model for identification"""
        # Use vertices and faces to create a hash
        data = np.concatenate([mesh.vertices.flatten(), mesh.faces.flatten()])
        return hashlib.md5(data.tobytes()).hexdigest()
    
    def _analyze_complexity(self, mesh: trimesh.Trimesh) -> Dict[str, Any]:
        """Analyze model complexity"""
        return {
            "face_density": float(len(mesh.faces) / mesh.area if mesh.area > 0 else 0),
            "is_watertight": bool(mesh.is_watertight),
            "has_holes": bool(not mesh.is_watertight),
            "euler_number": int(mesh.euler_number),
            "detail_level": self._calculate_detail_level(mesh),
        }
    
    def _calculate_detail_level(self, mesh: trimesh.Trimesh) -> str:
        """Categorize model detail level"""
        face_density = len(mesh.faces) / mesh.area if mesh.area > 0 else 0
        
        if face_density > 100:
            return "very_high"
        elif face_density > 50:
            return "high"
        elif face_density > 20:
            return "medium"
        else:
            return "low"
    
    def _detect_overhangs(self, mesh: trimesh.Trimesh) -> Dict[str, Any]:
        """Detect overhanging surfaces and analyze support requirements"""
        face_normals = mesh.face_normals
        
        # Calculate angle from vertical (Z-axis)
        z_axis = np.array([0, 0, -1])
        angles = np.arccos(np.clip(np.dot(face_normals, z_axis), -1.0, 1.0))
        angles_deg = np.degrees(angles)
        
        # Find overhangs at different thresholds
        overhang_mask = angles_deg > self.overhang_threshold
        severe_overhang_mask = angles_deg > 60  # Severe overhangs
        extreme_overhang_mask = angles_deg > 75  # Nearly horizontal
        
        overhang_faces = np.sum(overhang_mask)
        severe_overhang_faces = np.sum(severe_overhang_mask)
        extreme_overhang_faces = np.sum(extreme_overhang_mask)
        total_faces = len(mesh.faces)
        
        overhang_percentage = (overhang_faces / total_faces * 100) if total_faces > 0 else 0
        severe_percentage = (severe_overhang_faces / total_faces * 100) if total_faces > 0 else 0
        extreme_percentage = (extreme_overhang_faces / total_faces * 100) if total_faces > 0 else 0
        
        # Determine if tree supports are recommended
        # Tree supports are better for: complex overhangs, organic shapes, miniatures
        needs_tree_support = (
            severe_percentage > 5 or  # Many severe overhangs
            (overhang_percentage > 15 and extreme_percentage > 2) or  # Complex overhang pattern
            (overhang_percentage > 20)  # Very high overhang content
        )
        
        return {
            "has_overhangs": bool(overhang_percentage > 5),
            "overhang_percentage": float(overhang_percentage),
            "severe_overhang_percentage": float(severe_percentage),
            "extreme_overhang_percentage": float(extreme_percentage),
            "overhang_face_count": int(overhang_faces),
            "needs_supports": bool(overhang_percentage > 10),
            "recommend_tree_support": bool(needs_tree_support),
            "max_overhang_angle": float(np.max(angles_deg)),
            "support_complexity": "high" if needs_tree_support else "medium" if overhang_percentage > 10 else "low"
        }
    
    def _analyze_walls(self, mesh: trimesh.Trimesh) -> Dict[str, Any]:
        """Analyze wall characteristics"""
        # Sample rays to estimate thickness
        # This is a simplified approach
        dims = mesh.bounding_box.extents
        avg_dimension = np.mean(dims)
        
        return {
            "estimated_min_wall_thickness": float(avg_dimension * 0.01),  # Rough estimate
            "has_thin_walls": bool(avg_dimension < 10),  # mm
            "wall_type": "thin" if avg_dimension < 10 else "thick",
        }
    
    def _analyze_surface(self, mesh: trimesh.Trimesh) -> Dict[str, Any]:
        """Analyze surface characteristics"""
        # Calculate surface roughness indicators
        face_areas = mesh.area_faces
        mean_face_area = np.mean(face_areas)
        std_face_area = np.std(face_areas)
        
        return {
            "mean_face_area": float(mean_face_area),
            "surface_variation": float(std_face_area / mean_face_area) if mean_face_area > 0 else 0,
            "surface_type": "smooth" if std_face_area / mean_face_area < 0.5 else "detailed",
        }
    
    def _suggest_orientation(self, mesh: trimesh.Trimesh) -> Dict[str, Any]:
        """Suggest optimal print orientation"""
        dims = mesh.bounding_box.extents
        
        # Find the most stable orientation (largest face down)
        sorted_indices = np.argsort(dims)
        
        return {
            "suggested_up_axis": int(sorted_indices[2]),  # Tallest dimension
            "suggested_base_axis": int(sorted_indices[0]),  # Shortest dimension
            "current_height": float(dims[2]),
            "optimal_rotation": "model_positioned_optimally" if sorted_indices[2] == 2 else "rotation_recommended",
        }
    
    def extract_from_file(self, file_path: str) -> Dict[str, Any]:
        """Complete feature extraction pipeline from file"""
        mesh = self.load_model(file_path)
        features = self.extract_features(mesh)
        features["file_name"] = file_path
        return features
    
    def generate_summary(self, features: Dict[str, Any]) -> str:
        """Generate human-readable summary of features"""
        summary_parts = []
        
        # Dimensions
        dims = features["dimensions"]
        summary_parts.append(
            f"Dimensions: {dims['width']:.1f}mm × {dims['depth']:.1f}mm × {dims['height']:.1f}mm"
        )
        
        # Volume and complexity
        summary_parts.append(f"Volume: {features['volume']:.2f} mm³")
        summary_parts.append(f"Detail Level: {features['complexity']['detail_level']}")
        summary_parts.append(f"Watertight: {'Yes' if features['complexity']['is_watertight'] else 'No'}")
        
        # Overhangs
        oh = features["overhangs"]
        if oh["needs_supports"]:
            support_type = "Tree Supports recommended" if oh.get("recommend_tree_support") else "Normal Supports"
            summary_parts.append(f"⚠️ Needs Supports ({oh['overhang_percentage']:.1f}% overhangs)")
            summary_parts.append(f"   → {support_type} (complexity: {oh.get('support_complexity', 'medium')})")
        else:
            summary_parts.append("✓ No significant overhangs")
        
        # Walls
        wall = features["wall_analysis"]
        summary_parts.append(f"Wall Type: {wall['wall_type']}")
        
        return "\n".join(summary_parts)

