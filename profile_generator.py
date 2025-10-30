"""
Orca Slicer Profile Generator
Converts AI-generated parameters into 3MF files with embedded settings
"""
import json
import os
import zipfile
import shutil
from typing import Dict, Any
from datetime import datetime
from config import PROFILES_OUTPUT_DIR, ORCA_SLICER_PATH
import subprocess
import trimesh


class ProfileGenerator:
    """Generate Orca Slicer profiles from AI analysis"""
    
    def __init__(self):
        """Initialize profile generator"""
        self.output_dir = PROFILES_OUTPUT_DIR
        self.orca_path = ORCA_SLICER_PATH
    
    def generate_profile(self, 
                        analysis: Dict[str, Any], 
                        model_name: str = "model",
                        material: str = "PLA",
                        model_path: str = None,
                        slicer_type: str = "elegoo_orca",
                        build_plate_size: float = 220.0) -> Dict[str, str]:
        """
        Generate Orca Slicer profile files including 3MF with embedded settings
        
        Args:
            analysis: AI analysis with profile parameters
            model_name: Name of the model (for file naming)
            material: Printing material
            model_path: Optional path to original 3D model for 3MF generation
            slicer_type: Type of slicer (orca or elegoo_orca)
            build_plate_size: Build plate size in mm (default: 220)
            
        Returns:
            Dictionary with paths to generated files
        """
        
        print(f"\n{'='*70}")
        print(f"PROFILE GENERATION START")
        print(f"{'='*70}")
        print(f"   Model: {model_name}")
        print(f"   Material: {material}")
        print(f"   Slicer: {slicer_type}")
        print(f"   Build plate: {build_plate_size}mm")
        
        try:
            profile_data = analysis.get("profile", {})
            
            # Generate timestamp-based filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = self._sanitize_filename(model_name)
            base_filename = f"{safe_name}_{timestamp}"
            print(f"   Base filename: {base_filename}")
            
            # Generate 3MF project file with embedded settings (primary format)
            three_mf_path = None
            if model_path and os.path.exists(model_path):
                print(f"\n   🔍 Generating 3MF project file...")
                try:
                    three_mf_path = self._generate_3mf_with_settings(
                        model_path, profile_data, analysis, base_filename, material, slicer_type, build_plate_size
                    )
                    print(f"   ✓ 3MF generation complete")
                except Exception as e:
                    print(f"   ❌ 3MF GENERATION FAILED:")
                    print(f"      Error: {e}")
                    import traceback
                    traceback.print_exc()
                    # Continue without 3MF
            else:
                if not model_path:
                    print(f"   ⚠️  No model path provided - skipping 3MF generation")
                elif not os.path.exists(model_path):
                    print(f"   ⚠️  Model file not found: {model_path}")
            
            # Generate JSON config with slicer-specific format
            print(f"\n   🔍 Generating JSON config...")
            json_config_path = self._generate_json_config(profile_data, analysis, base_filename, material, slicer_type)
            
            # Generate JSON for reference
            print(f"\n   🔍 Generating JSON profile...")
            json_path = self._generate_json_profile(profile_data, analysis, base_filename, material)
            
            # Generate human-readable summary
            print(f"\n   🔍 Generating summary...")
            summary_path = self._generate_summary(analysis, base_filename)
            
            result = {
                "json_config": json_config_path,
                "json_profile": json_path,
                "summary": summary_path,
                "base_name": base_filename
            }
            
            if three_mf_path:
                result["3mf_profile"] = three_mf_path
            
            print(f"\n{'='*70}")
            print(f"PROFILE GENERATION COMPLETE")
            print(f"{'='*70}\n")
            
            return result
            
        except Exception as e:
            print(f"\n{'='*70}")
            print(f"❌ PROFILE GENERATION FAILED")
            print(f"{'='*70}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            import traceback
            print(f"Full traceback:")
            traceback.print_exc()
            print(f"{'='*70}\n")
            raise
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename"""
        # Remove extension if present
        name = os.path.splitext(os.path.basename(name))[0]
        # Remove invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            name = name.replace(char, '_')
        return name[:50]  # Limit length
    
    def _generate_json_profile(self, 
                               profile: Dict[str, Any], 
                               analysis: Dict[str, Any],
                               base_filename: str,
                               material: str) -> str:
        """Generate JSON profile file for Orca Slicer"""
        
        # Build complete profile structure
        orca_profile = {
            "version": "1.0",
            "generator": "AI Slicer Profile Generator",
            "generated_at": datetime.now().isoformat(),
            "material": material,
            "analysis": analysis.get("analysis", {}),
            "settings": {
                # Layer settings
                "layer_height": profile.get("layer_height", 0.2),
                "first_layer_height": profile.get("first_layer_height", 0.2),
                
                # Perimeters and shells
                "wall_loops": profile.get("perimeters", 3),
                "top_shell_layers": profile.get("top_solid_layers", 5),
                "bottom_shell_layers": profile.get("bottom_solid_layers", 5),
                
                # Infill
                "sparse_infill_density": f"{profile.get('infill_percentage', 20)}%",
                "sparse_infill_pattern": profile.get("infill_pattern", "cubic"),
                
                # Support
                "enable_support": profile.get("support_material", False),
                "support_type": profile.get("support_type", "normal"),
                "support_threshold_angle": profile.get("support_angle_threshold", 45),
                
                # Bed adhesion
                "brim_width": profile.get("brim_width", 0),
                "brim_type": "outer_only",
                
                # Speed settings (mm/s)
                "default_speed": profile.get("print_speed", 60),
                "initial_layer_speed": profile.get("first_layer_speed", 20),
                "outer_wall_speed": profile.get("perimeter_speed", 45),
                "inner_wall_speed": profile.get("perimeter_speed", 45),
                "sparse_infill_speed": profile.get("infill_speed", 80),
                "travel_speed": profile.get("travel_speed", 150),
                
                # Retraction
                "retraction_length": profile.get("retraction_length", 0.8),
                "retraction_speed": profile.get("retraction_speed", 35),
                
                # Temperature
                "nozzle_temperature": profile.get("temperature", 210),
                "bed_temperature": profile.get("bed_temperature", 60),
                "nozzle_temperature_initial_layer": profile.get("temperature", 210),
                
                # Cooling
                "fan_cooling_layer_time": 10,
                "slow_down_for_layer_cooling": True,
                "fan_max_speed": profile.get("cooling_fan_speed", 100),
                "fan_min_speed": profile.get("first_layer_fan_speed", 0),
                
                # Quality
                "resolution": 0.01,
                "detect_thin_wall": True,
            },
            "reasoning": analysis.get("reasoning", ""),
            "estimated_quality": analysis.get("estimated_quality", "standard")
        }
        
        # Save to file
        output_path = os.path.join(self.output_dir, f"{base_filename}.json")
        with open(output_path, 'w') as f:
            json.dump(orca_profile, f, indent=2)
        
        return output_path
    
    def _generate_3mf_with_settings(self,
                                     model_path: str,
                                     profile: Dict[str, Any],
                                     analysis: Dict[str, Any],
                                     base_filename: str,
                                     material: str,
                                     slicer_type: str = "elegoo_orca",
                                     build_plate_size: float = 220.0) -> str:
        """Generate a 3MF project file with embedded slicer settings for Elegoo/Orca Slicer"""
        
        output_path = os.path.join(self.output_dir, f"{base_filename}.3mf")
        temp_dir = os.path.join(self.output_dir, f"temp_{base_filename}")
        
        try:
            os.makedirs(temp_dir, exist_ok=True)
            
            # Load and convert model to STL for 3MF
            print(f"   🔍 Loading 3D model from: {model_path}")
            print(f"      File exists: {os.path.exists(model_path)}")
            print(f"      File size: {os.path.getsize(model_path) if os.path.exists(model_path) else 'N/A'} bytes")
            
            try:
                mesh = trimesh.load(model_path, force='mesh')
                print(f"   ✓ Model loaded successfully")
                print(f"      Type: {type(mesh)}")
                
                if isinstance(mesh, trimesh.Scene):
                    print(f"      Processing scene with {len(mesh.geometry)} geometries")
                    mesh = trimesh.util.concatenate([
                        geom for geom in mesh.geometry.values()
                        if isinstance(geom, trimesh.Trimesh)
                    ])
                    print(f"   ✓ Scene converted to single mesh")
                    
                print(f"      Vertices: {len(mesh.vertices)}")
                print(f"      Faces: {len(mesh.faces)}")
                print(f"      Bounds: {mesh.bounds}")
            except Exception as e:
                print(f"   ❌ MODEL LOADING ERROR:")
                print(f"      File: {os.path.abspath(model_path)}")
                print(f"      Error type: {type(e).__name__}")
                print(f"      Error message: {str(e)}")
                import traceback
                print(f"      Traceback:")
                traceback.print_exc()
                raise
            
            # Generate proper 3MF model XML with auto-positioning
            model_3d_dir = os.path.join(temp_dir, "3D")
            os.makedirs(model_3d_dir, exist_ok=True)
            
            # Create 3D model XML with mesh data and transform
            print(f"   📐 Build plate: {build_plate_size}mm - calculating optimal placement...")
            try:
                model_xml, transform_matrix = self._generate_3mf_model_xml(mesh, build_plate_size=build_plate_size)
                print(f"   ✓ Transform: {transform_matrix[:50]}...")
                print(f"   ✓ Generated 3MF model XML ({len(model_xml)} characters)")
            except Exception as e:
                print(f"   ❌ 3MF XML GENERATION ERROR:")
                print(f"      Error type: {type(e).__name__}")
                print(f"      Error message: {str(e)}")
                import traceback
                traceback.print_exc()
                raise
            
            # For Elegoo, create both main model and Objects subfolder
            if slicer_type == "elegoo_orca":
                # Main 3dmodel.model file
                model_file = os.path.join(model_3d_dir, "3dmodel.model")
                with open(model_file, 'w', encoding='utf-8') as f:
                    f.write(model_xml)
                
                # Also create 3D/Objects/Object_1_1.model (Elegoo specific)
                objects_dir = os.path.join(model_3d_dir, "Objects")
                os.makedirs(objects_dir, exist_ok=True)
                object_file = os.path.join(objects_dir, "Object_1_1.model")
                with open(object_file, 'w', encoding='utf-8') as f:
                    f.write(model_xml)
                
                # Create 3D/_rels/3dmodel.model.rels
                model_rels_dir = os.path.join(model_3d_dir, "_rels")
                os.makedirs(model_rels_dir, exist_ok=True)
                model_rels_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rel0" Target="/3D/Objects/Object_1_1.model" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>'''
                with open(os.path.join(model_rels_dir, "3dmodel.model.rels"), 'w', encoding='utf-8') as f:
                    f.write(model_rels_xml)
            else:
                # Standard Orca - just main model file
                model_file = os.path.join(model_3d_dir, "3dmodel.model")
                with open(model_file, 'w', encoding='utf-8') as f:
                    f.write(model_xml)
            
            # Create [Content_Types].xml with proper content type
            content_types_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
  <Override PartName="/3D/3dmodel.model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
</Types>'''
            
            with open(os.path.join(temp_dir, "[Content_Types].xml"), 'w', encoding='utf-8') as f:
                f.write(content_types_xml)
            
            # Create _rels/.rels with correct relationship type
            rels_dir = os.path.join(temp_dir, "_rels")
            os.makedirs(rels_dir, exist_ok=True)
            rels_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rel-1" Target="/3D/3dmodel.model" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>'''
            
            with open(os.path.join(rels_dir, ".rels"), 'w', encoding='utf-8') as f:
                f.write(rels_xml)
            
            # Create Metadata directory with slicer configs
            metadata_dir = os.path.join(temp_dir, "Metadata")
            os.makedirs(metadata_dir, exist_ok=True)
            
            # For Elegoo Orca Slicer (Bambu Studio based)
            if slicer_type == "elegoo_orca":
                # Calculate position on build plate (center)
                center_x = build_plate_size / 2
                center_y = build_plate_size / 2
                center_z = (mesh.bounds[1][2] - mesh.bounds[0][2]) / 2  # Model height center
                
                # Create project_settings.config (main config file for Elegoo)
                try:
                    print(f"   🔍 Generating project_settings.config...")
                    project_settings = self._generate_elegoo_project_settings(profile, analysis, material)
                    settings_path = os.path.join(metadata_dir, "project_settings.config")
                    with open(settings_path, 'w', encoding='utf-8') as f:
                        json.dump(project_settings, f, indent=2)
                    print(f"   ✓ project_settings.config written ({os.path.getsize(settings_path)} bytes)")
                except Exception as e:
                    print(f"   ❌ PROJECT SETTINGS ERROR:")
                    print(f"      Error type: {type(e).__name__}")
                    print(f"      Error message: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    raise
                
                # Create model_settings.config (XML with positioning!)
                # CRITICAL: source_offset should be 0,0,Z - transform handles positioning!
                model_settings_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<config>
  <object id="2">
    <metadata key="name" value="Object_1"/>
    <metadata key="extruder" value="1"/>
    <part id="1" subtype="normal_part">
      <metadata key="name" value="Object_1"/>
      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>
      <metadata key="source_file" value="AI_Generated_Model"/>
      <metadata key="source_object_id" value="0"/>
      <metadata key="source_volume_id" value="0"/>
      <metadata key="source_offset_x" value="0"/>
      <metadata key="source_offset_y" value="0"/>
      <metadata key="source_offset_z" value="{center_z}"/>
      <mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>
    </part>
  </object>
  <plate>
    <metadata key="plater_id" value="1"/>
    <metadata key="plater_name" value=""/>
    <metadata key="locked" value="false"/>
    <model_instance>
      <metadata key="object_id" value="2"/>
      <metadata key="instance_id" value="0"/>
      <metadata key="identify_id" value="1"/>
    </model_instance>
  </plate>
  <assemble>
   <assemble_item object_id="2" instance_id="0" transform="{transform_matrix}"/>
  </assemble>
</config>'''
                with open(os.path.join(metadata_dir, "model_settings.config"), 'w', encoding='utf-8') as f:
                    f.write(model_settings_xml)
                
                # Create plate_1.json (plate metadata)
                bounds = mesh.bounds
                plate_info = {
                    "bbox_objects": [{
                        "id": 1,
                        "name": "Object_1",
                        "bbox": [
                            float(center_x - (bounds[1][0] - bounds[0][0])/2),
                            float(center_y - (bounds[1][1] - bounds[0][1])/2),
                            float((bounds[1][0] - bounds[0][0])),
                            float((bounds[1][1] - bounds[0][1]))
                        ],
                        "layer_height": profile.get('layer_height', 0.2),
                        "area": float((bounds[1][0] - bounds[0][0]) * (bounds[1][1] - bounds[0][1]))
                    }],
                    "bed_type": "textured_plate",
                    "filament_colors": [],
                    "filament_ids": [],
                    "first_extruder": 0,
                    "is_seq_print": False,
                    "nozzle_diameter": 0.4,
                    "version": 2
                }
                with open(os.path.join(metadata_dir, "plate_1.json"), 'w', encoding='utf-8') as f:
                    json.dump(plate_info, f, indent=2)
                
                # Create slice_info.config (XML format)
                slice_info_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<config>
  <header>
    <header_item key="X-BBL-Client-Type" value="slicer"/>
    <header_item key="X-BBL-Client-Version" value="01.01.08.02"/>
  </header>
</config>'''
                with open(os.path.join(metadata_dir, "slice_info.config"), 'w', encoding='utf-8') as f:
                    f.write(slice_info_xml)
                
                # Create dummy thumbnail PNG files (Elegoo requires these!)
                # Without these, Elegoo won't load the settings!
                self._create_dummy_thumbnails(metadata_dir)
            
            # For standard Orca Slicer (PrusaSlicer based)
            else:
                config_json = self._generate_3mf_config_json(profile, analysis, material, slicer_type)
                
                with open(os.path.join(metadata_dir, "Slic3r_PE.json"), 'w', encoding='utf-8') as f:
                    json.dump(config_json, f, indent=2)
                
                with open(os.path.join(metadata_dir, "Slic3r_PE_model.json"), 'w', encoding='utf-8') as f:
                    json.dump(config_json, f, indent=2)
                
                with open(os.path.join(metadata_dir, "model_settings.json"), 'w', encoding='utf-8') as f:
                    json.dump(config_json, f, indent=2)
            
            # Create the 3MF file (it's a ZIP archive)
            print(f"   🔍 Creating 3MF ZIP archive...")
            try:
                file_count = 0
                with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, temp_dir)
                            zipf.write(file_path, arcname)
                            file_count += 1
                print(f"   ✓ 3MF archive created successfully ({file_count} files, {os.path.getsize(output_path)} bytes)")
                print(f"   ✓ 3MF file: {os.path.abspath(output_path)}")
            except Exception as e:
                print(f"   ❌ 3MF ZIP CREATION ERROR:")
                print(f"      Output path: {os.path.abspath(output_path)}")
                print(f"      Error type: {type(e).__name__}")
                print(f"      Error message: {str(e)}")
                import traceback
                traceback.print_exc()
                raise
            
            return output_path
            
        finally:
            # Clean up temp directory
            try:
                if os.path.exists(temp_dir):
                    print(f"   🔍 Cleaning up temp directory: {temp_dir}")
                    shutil.rmtree(temp_dir)
                    print(f"   ✓ Temp directory cleaned up")
            except Exception as e:
                print(f"   ⚠️  Cleanup warning: {e}")
                # Don't raise - cleanup errors are not critical
    
    def _generate_orca_config(self, profile: Dict[str, Any], analysis: Dict[str, Any], material: str, slicer_type: str = "elegoo_orca") -> str:
        """Generate slicer configuration embedded in 3MF for specific slicer type"""
        
        # Determine if using tree supports
        is_tree_support = profile.get('support_style') == 'tree' or 'tree' in str(profile.get('support_type', '')).lower()
        
        if slicer_type == "elegoo_orca":
            # Elegoo Orca Slicer / Bambu Studio format
            config_lines = [
                "# Generated by AI Slicer Profile Generator for Elegoo Orca Slicer",
                f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "[print]",
            ]
        else:
            # Standard Orca Slicer / PrusaSlicer format
            config_lines = [
                "# Generated by AI Slicer Profile Generator",
                f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"# Material: {material}",
                "",
                "[print]",
            ]
        
        config_lines.extend([
            f"layer_height = {profile.get('layer_height', 0.2)}",
            f"first_layer_height = {profile.get('first_layer_height', 0.2)}",
            f"wall_loops = {profile.get('perimeters', 3)}",
            f"top_shell_layers = {profile.get('top_solid_layers', 5)}",
            f"bottom_shell_layers = {profile.get('bottom_solid_layers', 5)}",
            f"sparse_infill_density = {profile.get('infill_percentage', 20)}%",
            f"sparse_infill_pattern = {profile.get('infill_pattern', 'cubic')}",
            "",
            "# Support Settings",
            f"enable_support = {'1' if profile.get('support_material', False) else '0'}",
            f"support_threshold_angle = {profile.get('support_angle_threshold', 45)}",
        ])
        
        # Add tree support specific settings if enabled
        if is_tree_support and profile.get('support_material', False):
            config_lines.extend([
                "# Tree Support Configuration",
                "support_type = tree",
                "support_style = tree",
                f"tree_support_branch_angle = {profile.get('tree_support_branch_angle', 45)}",
                f"tree_support_branch_distance = {profile.get('tree_support_branch_distance', 2.5)}",
                f"tree_support_wall_count = {profile.get('tree_support_wall_count', 0)}",
                "tree_support_auto_brim = 1",
                "tree_support_brim_width = 3",
            ])
        else:
            config_lines.extend([
                "support_type = normal",
                "support_style = default",
            ])
        
        config_lines.extend([
            "",
            f"brim_width = {profile.get('brim_width', 0)}",
            f"brim_type = outer_only",
            "",
            "# Speed settings",
            f"default_speed = {profile.get('print_speed', 60)}",
            f"initial_layer_speed = {profile.get('first_layer_speed', 20)}",
            f"outer_wall_speed = {profile.get('perimeter_speed', 45)}",
            f"inner_wall_speed = {profile.get('perimeter_speed', 45)}",
            f"sparse_infill_speed = {profile.get('infill_speed', 80)}",
            f"travel_speed = {profile.get('travel_speed', 150)}",
            "",
            "# Retraction",
            f"retraction_length = {profile.get('retraction_length', 0.8)}",
            f"retraction_speed = {profile.get('retraction_speed', 35)}",
            "",
            "# Quality",
            "resolution = 0.01",
            "detect_thin_wall = 1",
            "",
            "[filament]",
            f"filament_type = {material}",
            f"nozzle_temperature = {profile.get('temperature', 210)}",
            f"bed_temperature = {profile.get('bed_temperature', 60)}",
            f"nozzle_temperature_initial_layer = {profile.get('temperature', 210)}",
            "",
            "# Cooling",
            f"fan_max_speed = {profile.get('cooling_fan_speed', 100)}",
            f"fan_min_speed = {profile.get('first_layer_fan_speed', 0)}",
            "fan_cooling_layer_time = 10",
            "slow_down_for_layer_cooling = 1",
        ])
        
        return '\n'.join(config_lines)
    
    def _calculate_build_plate_transform(self, mesh: 'trimesh.Trimesh', build_plate_size: float = 220.0) -> tuple:
        """
        Calculate optimal positioning and scaling for build plate
        
        Returns: (scale_factor, offset_x, offset_y, offset_z)
        """
        bounds = mesh.bounds
        
        # Get model dimensions
        width = bounds[1][0] - bounds[0][0]
        depth = bounds[1][1] - bounds[0][1]
        height = bounds[1][2] - bounds[0][2]
        
        # Calculate scale factor to fit on build plate (with 5mm margin)
        max_dimension = max(width, depth)
        safe_build_size = build_plate_size - 10  # 5mm margin on each side
        
        scale_factor = 1.0
        if max_dimension > safe_build_size:
            scale_factor = safe_build_size / max_dimension
            print(f"   ⚠️  Model too large! Auto-scaling to {scale_factor*100:.1f}% to fit build plate")
        
        # After scaling, calculate the actual dimensions
        scaled_width = width * scale_factor
        scaled_depth = depth * scale_factor
        
        # Calculate offset to position model at bottom-left corner then center it
        # Transform moves the model's bounds[0] point to the target position
        # We want the model centered, so:
        # - Center X should be at build_plate_size/2
        # - Center Y should be at build_plate_size/2
        # - Bottom (Z min) should be at 0
        
        offset_x = (build_plate_size / 2) - (scaled_width / 2) - (bounds[0][0] * scale_factor)
        offset_y = (build_plate_size / 2) - (scaled_depth / 2) - (bounds[0][1] * scale_factor)
        offset_z = -(bounds[0][2] * scale_factor)  # Place bottom on Z=0
        
        # Log the transformation for debugging
        print(f"   Model bounds: X[{bounds[0][0]:.1f}, {bounds[1][0]:.1f}] Y[{bounds[0][1]:.1f}, {bounds[1][1]:.1f}] Z[{bounds[0][2]:.1f}, {bounds[1][2]:.1f}]")
        print(f"   Dimensions: {width:.1f} x {depth:.1f} x {height:.1f} mm")
        print(f"   Scale: {scale_factor*100:.1f}% | Offset: ({offset_x:.1f}, {offset_y:.1f}, {offset_z:.1f})")
        
        return (scale_factor, offset_x, offset_y, offset_z)
    
    def _generate_3mf_model_xml(self, mesh: 'trimesh.Trimesh', build_plate_size: float = 220.0) -> tuple:
        """
        Generate 3MF model XML with mesh geometry for Orca/Elegoo Slicer
        
        Returns: (model_xml, transform_matrix)
        """
        
        # Get vertices and faces
        vertices = mesh.vertices
        faces = mesh.faces
        bounds = mesh.bounds
        
        # CRITICAL: Normalize vertices to center at origin (0,0,0)
        # This is what Elegoo expects! Then we use transform to position it.
        center_x = (bounds[0][0] + bounds[1][0]) / 2
        center_y = (bounds[0][1] + bounds[1][1]) / 2
        center_z = bounds[0][2]  # Bottom at Z=0
        
        # Build vertices XML with NORMALIZED coordinates (centered at origin)
        vertices_xml = []
        for v in vertices:
            norm_x = float(v[0] - center_x)
            norm_y = float(v[1] - center_y)
            norm_z = float(v[2] - center_z)
            vertices_xml.append(f'     <vertex x="{norm_x}" y="{norm_y}" z="{norm_z}"/>')
        
        # Build triangles XML
        triangles_xml = []
        for f in faces:
            triangles_xml.append(f'     <triangle v1="{int(f[0])}" v2="{int(f[1])}" v3="{int(f[2])}"/>')
        
        # Now calculate transform to position the normalized model on build plate
        width = bounds[1][0] - bounds[0][0]
        depth = bounds[1][1] - bounds[0][1]
        
        # Calculate scale if needed
        max_dimension = max(width, depth)
        safe_build_size = build_plate_size - 10
        scale = 1.0
        if max_dimension > safe_build_size:
            scale = safe_build_size / max_dimension
            print(f"   ⚠️  Model too large! Auto-scaling to {scale*100:.1f}%")
        
        # Transform positions the center of the normalized model
        # at the center of the build plate
        offset_x = build_plate_size / 2
        offset_y = build_plate_size / 2
        offset_z = (bounds[1][2] - bounds[0][2]) / 2 * scale  # Half height for Z offset
        
        # Create transform matrix (no decimals on "1")
        scale_str = "1" if scale == 1.0 else f"{scale:.6f}".rstrip('0').rstrip('.')
        transform_matrix = f"{scale_str} 0 0 0 {scale_str} 0 0 0 {scale_str} {offset_x} {offset_y} {offset_z}"
        
        # Complete 3MF model XML with BambuStudio/Elegoo format and all required metadata
        model_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">
 <metadata name="Application">AI Slicer Profile Generator</metadata>
 <metadata name="BambuStudio:3mfVersion">1</metadata>
 <metadata name="Copyright"></metadata>
 <metadata name="CreationDate">{datetime.now().strftime('%Y-%m-%d')}</metadata>
 <metadata name="Description">AI Generated 3D Print Profile</metadata>
 <metadata name="Designer"></metadata>
 <metadata name="LicenseTerms"></metadata>
 <metadata name="ModificationDate">{datetime.now().strftime('%Y-%m-%d')}</metadata>
 <metadata name="Title">AI Generated Model</metadata>
 <resources>
  <object id="2" p:UUID="00010000-0000-0000-0000-000000000002" type="model">
   <mesh>
    <vertices>
{chr(10).join(vertices_xml)}
    </vertices>
    <triangles>
{chr(10).join(triangles_xml)}
    </triangles>
   </mesh>
  </object>
 </resources>
 <build p:UUID="00000000-0000-0000-0000-000000000000">
  <item objectid="2" p:UUID="00000002-0000-0000-0000-000000000002" transform="{transform_matrix}" printable="1"/>
 </build>
</model>'''
        
        return model_xml, transform_matrix
    
    def _generate_3mf_config_json(self, profile: Dict[str, Any], analysis: Dict[str, Any], material: str, slicer_type: str = "elegoo_orca") -> Dict[str, Any]:
        """Generate JSON configuration for embedding in 3MF file"""
        
        # Determine if using tree supports
        is_tree = profile.get('support_style') == 'tree' or 'tree' in str(profile.get('support_type', '')).lower()
        
        # Build configuration JSON
        config = {
            "version": "1.0.0",
            "generated_by": "AI Slicer Profile Generator",
            "generated_at": datetime.now().isoformat(),
            "material": material,
            "print": {
                "layer_height": profile.get('layer_height', 0.2),
                "initial_layer_height": profile.get('first_layer_height', 0.2),
                "wall_loops": profile.get('perimeters', 3),
                "top_shell_layers": profile.get('top_solid_layers', 5),
                "bottom_shell_layers": profile.get('bottom_solid_layers', 5),
                "sparse_infill_density": f"{profile.get('infill_percentage', 20)}%",
                "sparse_infill_pattern": profile.get('infill_pattern', 'cubic'),
                "enable_support": 1 if profile.get('support_material', False) else 0,
                "support_threshold_angle": profile.get('support_angle_threshold', 45),
                "brim_width": profile.get('brim_width', 0),
                "brim_type": "outer_only",
                "default_speed": profile.get('print_speed', 60),
                "initial_layer_speed": profile.get('first_layer_speed', 20),
                "outer_wall_speed": profile.get('perimeter_speed', 45),
                "inner_wall_speed": profile.get('perimeter_speed', 45),
                "sparse_infill_speed": profile.get('infill_speed', 80),
                "travel_speed": profile.get('travel_speed', 150),
                "retraction_length": profile.get('retraction_length', 0.8),
                "retraction_speed": profile.get('retraction_speed', 35),
            },
            "filament": {
                "filament_type": material,
                "nozzle_temperature": profile.get('temperature', 210),
                "nozzle_temperature_initial_layer": profile.get('temperature', 210),
                "fan_max_speed": profile.get('cooling_fan_speed', 100),
                "fan_min_speed": profile.get('first_layer_fan_speed', 0),
            }
        }
        
        # Add bed temperature with correct key for each slicer
        if slicer_type == "elegoo_orca":
            config["filament"]["hot_plate_temp"] = profile.get('bed_temperature', 60)
            config["filament"]["hot_plate_temp_initial_layer"] = profile.get('bed_temperature', 60)
        else:
            config["filament"]["bed_temperature"] = profile.get('bed_temperature', 60)
        
        # Add tree support settings if enabled
        if is_tree and profile.get('support_material', False):
            config["print"]["support_type"] = "tree"
            config["print"]["support_style"] = "tree"
            config["print"]["tree_support_branch_angle"] = profile.get('tree_support_branch_angle', 45)
            config["print"]["tree_support_branch_distance"] = profile.get('tree_support_branch_distance', 2.5)
            config["print"]["tree_support_wall_count"] = profile.get('tree_support_wall_count', 0)
        else:
            config["print"]["support_type"] = "normal"
            config["print"]["support_style"] = "default"
        
        return config
    
    def _load_elegoo_defaults(self) -> Dict[str, Any]:
        """Load default Elegoo settings template"""
        template_path = os.path.join(os.path.dirname(__file__), "elegoo_default_settings.json")
        
        print(f"   🔍 Loading Elegoo defaults from: {template_path}")
        
        if os.path.exists(template_path):
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    print(f"   ✓ Successfully loaded {len(data)} default settings")
                    return data
            except json.JSONDecodeError as e:
                print(f"   ❌ JSON PARSE ERROR in elegoo_default_settings.json:")
                print(f"      Line {e.lineno}, Column {e.colno}: {e.msg}")
                print(f"      Error at position {e.pos}")
                print(f"      Full path: {os.path.abspath(template_path)}")
                import traceback
                traceback.print_exc()
                return {}
            except Exception as e:
                print(f"   ❌ ERROR loading elegoo_default_settings.json: {e}")
                import traceback
                traceback.print_exc()
                return {}
        else:
            print(f"   ⚠️  Template not found at: {os.path.abspath(template_path)}")
            print(f"      Using minimal fallback settings")
        
        # Minimal fallback if template not found
        return {}
    
    def _generate_elegoo_project_settings(self, profile: Dict[str, Any], analysis: Dict[str, Any], material: str) -> Dict[str, Any]:
        """Generate complete project_settings.config for Elegoo Orca Slicer"""
        
        # Start with default Elegoo settings (all 493+ keys!)
        settings = self._load_elegoo_defaults()
        
        # Determine if using tree supports
        is_tree = profile.get('support_style') == 'tree' or 'tree' in str(profile.get('support_type', '')).lower()
        
        # Update ONLY AI-generated settings (override defaults)
        ai_settings = {
            # Layer settings
            "layer_height": str(profile.get('layer_height', 0.2)),
            "initial_layer_height": str(profile.get('first_layer_height', 0.2)),
            
            # Walls
            "wall_loops": str(profile.get('perimeters', 3)),
            "top_shell_layers": str(profile.get('top_solid_layers', 5)),
            "bottom_shell_layers": str(profile.get('bottom_solid_layers', 5)),
            
            # Infill
            "sparse_infill_density": f"{profile.get('infill_percentage', 20)}%",
            "sparse_infill_pattern": profile.get('infill_pattern', 'cubic'),
            
            # Support - THE CRITICAL PART!
            "enable_support": "1" if profile.get('support_material', False) else "0",
            "support_type": "tree(auto)" if is_tree else "normal(auto)",
            "support_style": "default",  # Elegoo uses "default" NOT "tree"!
            "support_threshold_angle": str(profile.get('support_angle_threshold', 45)),
            
            # Brim - DISABLED (per user request)
            # NOTE: Only brim_type matters! Other values can stay at defaults
            "brim_type": "no_brim",
            
            # Speed (strings!)
            "default_speed": str(profile.get('print_speed', 60)),
            "initial_layer_speed": str(profile.get('first_layer_speed', 20)),
            "outer_wall_speed": str(profile.get('perimeter_speed', 45)),
            "inner_wall_speed": str(profile.get('perimeter_speed', 45)),
            "sparse_infill_speed": str(profile.get('infill_speed', 80)),
            "travel_speed": str(profile.get('travel_speed', 150)),
            
            # Retraction
            "retraction_length": [str(profile.get('retraction_length', 0.8))],
            "retraction_speed": [str(profile.get('retraction_speed', 35))],
            
            # Temperature (arrays of strings!)
            "nozzle_temperature": [str(profile.get('temperature', 210))],
            "hot_plate_temp": [str(profile.get('bed_temperature', 60))],
            "hot_plate_temp_initial_layer": [str(profile.get('bed_temperature', 60))],
            
            # Cooling (arrays!)
            "fan_max_speed": [str(profile.get('cooling_fan_speed', 100))],
            "fan_min_speed": [str(profile.get('first_layer_fan_speed', 0))],
            
            # Filament - CRITICAL for Elegoo!
            "filament_type": [material],  # Use exact Elegoo filament name!
            "filament_settings_id": [f"{material} @ECC"],  # Settings profile ID
            
            # Track which settings were changed from system defaults
            # This tells Elegoo to actually USE these values!
            "different_settings_to_system": [
                "brim_type;enable_support;support_type;layer_height;wall_loops;"
                "sparse_infill_density;nozzle_temperature;hot_plate_temp"
            ],
            
            # Quality
            "resolution": "0.01",
            "detect_thin_wall": "1",
        }
        
        # Add tree support specific settings if enabled
        if is_tree and profile.get('support_material', False):
            ai_settings.update({
                "tree_support_branch_angle": str(profile.get('tree_support_branch_angle', 45)),
                "tree_support_branch_angle_organic": str(profile.get('tree_support_branch_angle', 45)),
                "tree_support_branch_distance": "5",
                "tree_support_branch_distance_organic": "5",
                "tree_support_branch_diameter": "2",
                "tree_support_branch_diameter_organic": "2",
                "tree_support_wall_count": str(profile.get('tree_support_wall_count', 0)),
                # Keep tree support brim at defaults - brim_type controls everything
                "tree_support_adaptive_layer_height": "1",
                "tree_support_tip_diameter": "2",
                "tree_support_top_rate": "30%",
            })
        
        # Merge AI settings into defaults (AI settings override)
        settings.update(ai_settings)
        
        return settings
    
    def _create_dummy_thumbnails(self, metadata_dir: str):
        """Create minimal PNG thumbnails required by Elegoo Orca Slicer"""
        try:
            from PIL import Image
            
            # Create a simple 1x1 transparent PNG
            # Elegoo checks for these files but doesn't strictly validate them
            img_small = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            img_medium = Image.new('RGBA', (1, 1), (0, 0, 0, 0))
            
            # Save thumbnails
            img_small.save(os.path.join(metadata_dir, "plate_1_small.png"))
            img_medium.save(os.path.join(metadata_dir, "plate_1.png"))
            img_medium.save(os.path.join(metadata_dir, "plate_no_light_1.png"))
            img_medium.save(os.path.join(metadata_dir, "top_1.png"))
            img_medium.save(os.path.join(metadata_dir, "pick_1.png"))
            
            print("   ✓ Created thumbnail files for Elegoo compatibility")
            
        except ImportError:
            print("   ⚠️  PIL/Pillow not available - thumbnails skipped (may affect settings loading)")
        except Exception as e:
            print(f"   ⚠️  Thumbnail creation failed: {e}")
    
    def _generate_json_config(self, profile: Dict[str, Any], analysis: Dict[str, Any], base_filename: str, material: str, slicer_type: str = "elegoo_orca") -> str:
        """Generate standalone JSON config file for manual import"""
        
        try:
            # For Elegoo, use the full project settings format
            if slicer_type == "elegoo_orca":
                print(f"   🔍 Generating Elegoo project settings...")
                config = self._generate_elegoo_project_settings(profile, analysis, material)
                print(f"   ✓ Generated {len(config)} config parameters")
            else:
                print(f"   🔍 Generating standard Orca config...")
                config = self._generate_3mf_config_json(profile, analysis, material, slicer_type)
            
            # Save to file
            output_path = os.path.join(self.output_dir, f"{base_filename}_config.json")
            print(f"   🔍 Writing JSON config to: {output_path}")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            
            print(f"   ✓ JSON config written successfully ({os.path.getsize(output_path)} bytes)")
            return output_path
            
        except Exception as e:
            print(f"   ❌ JSON CONFIG GENERATION ERROR:")
            print(f"      Error type: {type(e).__name__}")
            print(f"      Error message: {str(e)}")
            import traceback
            print(f"      Traceback:")
            traceback.print_exc()
            raise
    
    def _generate_ini_profile(self, 
                              profile: Dict[str, Any], 
                              analysis: Dict[str, Any],
                              base_filename: str,
                              material: str,
                              slicer_type: str = "elegoo_orca") -> str:
        """Generate INI profile file compatible with selected slicer"""
        
        # Determine if using tree supports
        is_tree = profile.get('support_style') == 'tree' or 'tree' in str(profile.get('support_type', '')).lower()
        
        if slicer_type == "elegoo_orca":
            # Build INI with Elegoo/Bambu Studio compatible format
            ini_lines = [
                "# generated by AI Slicer Profile Generator for Elegoo Orca Slicer",
                f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"# Material: {material}",
                "# Compatible with Elegoo Orca Slicer / Bambu Studio format",
                "",
                "[print:AI Generated Profile]",
                "compatible_printers = ",
            ]
        else:
            # Standard Orca Slicer format
            ini_lines = [
                "# generated by AI Slicer Profile Generator for Orca Slicer",
                f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                f"# Material: {material}",
                "",
                "[print]",
            ]
        
        ini_lines.extend([
            "",
            "# Quality",
            f"layer_height = {profile.get('layer_height', 0.2)}",
            f"initial_layer_height = {profile.get('first_layer_height', 0.2)}",
            "",
            "# Walls",
            f"wall_loops = {profile.get('perimeters', 3)}",
            f"top_shell_layers = {profile.get('top_solid_layers', 5)}",
            f"bottom_shell_layers = {profile.get('bottom_solid_layers', 5)}",
            "",
            "# Infill",
            f"sparse_infill_density = {profile.get('infill_percentage', 20)}%",
            f"sparse_infill_pattern = {profile.get('infill_pattern', 'cubic')}",
            "",
            "# Support",
            f"enable_support = {1 if profile.get('support_material', False) else 0}",
        ])
        
        # Add tree support settings if enabled
        if is_tree and profile.get('support_material', False):
            ini_lines.extend([
                f"support_type = tree(auto)",
                f"support_style = tree",
                f"support_threshold_angle = {profile.get('support_angle_threshold', 45)}",
                f"tree_support_branch_angle = {profile.get('tree_support_branch_angle', 45)}",
                f"tree_support_branch_distance = {profile.get('tree_support_branch_distance', 2.5)}",
                f"tree_support_wall_count = {profile.get('tree_support_wall_count', 0)}",
            ])
        else:
            ini_lines.extend([
                f"support_type = normal(auto)",
                f"support_style = default",
                f"support_threshold_angle = {profile.get('support_angle_threshold', 45)}",
            ])
        
        ini_lines.extend([
            "",
            "# Brim",
            f"brim_width = {profile.get('brim_width', 0)}",
            f"brim_type = outer_only",
            "",
            "# Speed (mm/s)",
            f"default_speed = {profile.get('print_speed', 60)}",
            f"initial_layer_speed = {profile.get('first_layer_speed', 20)}",
            f"outer_wall_speed = {profile.get('perimeter_speed', 45)}",
            f"inner_wall_speed = {profile.get('perimeter_speed', 45)}",
            f"sparse_infill_speed = {profile.get('infill_speed', 80)}",
            f"travel_speed = {profile.get('travel_speed', 150)}",
            "",
            "# Retraction",
            f"retraction_length = {profile.get('retraction_length', 0.8)}",
            f"retraction_speed = {profile.get('retraction_speed', 35)}",
            "",
            "# Quality",
            "resolution = 0.01",
            "detect_thin_wall = 1",
        ])
        
        # Add filament section header based on slicer type
        if slicer_type == "elegoo_orca":
            ini_lines.append("")
            ini_lines.append(f"[filament:{material}]")
        else:
            ini_lines.append("")
            ini_lines.append("[filament]")
        
        if slicer_type == "elegoo_orca":
            ini_lines.extend([
                "compatible_printers = ",
                f"filament_type = {material}",
                f"nozzle_temperature = {profile.get('temperature', 210)}",
                f"hot_plate_temp = {profile.get('bed_temperature', 60)}",
                f"nozzle_temperature_initial_layer = {profile.get('temperature', 210)}",
                f"hot_plate_temp_initial_layer = {profile.get('bed_temperature', 60)}",
            ])
        else:
            ini_lines.extend([
                f"filament_type = {material}",
                f"nozzle_temperature = {profile.get('temperature', 210)}",
                f"bed_temperature = {profile.get('bed_temperature', 60)}",
                f"nozzle_temperature_initial_layer = {profile.get('temperature', 210)}",
            ])
        
        ini_lines.extend([
            "",
            "# Cooling",
            f"fan_max_speed = {profile.get('cooling_fan_speed', 100)}",
            f"fan_min_speed = {profile.get('first_layer_fan_speed', 0)}",
            "overhang_fan_speed = 100",
            "reduce_fan_stop_start_freq = 1",
        ])
        
        # Add metadata section
        ini_lines.extend([
            "",
            "# Metadata",
            f"# Generated by: AI Slicer Profile Generator",
            f"# Model Type: {analysis.get('analysis', {}).get('model_type', 'unknown')}",
            f"# Complexity: {analysis.get('analysis', {}).get('complexity_assessment', 'medium')}",
            f"# Quality: {analysis.get('estimated_quality', 'standard')}",
        ])
        
        ini_lines
        
        # Save to file
        output_path = os.path.join(self.output_dir, f"{base_filename}.ini")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(ini_lines))
        
        return output_path
    
    def _generate_summary(self, analysis: Dict[str, Any], base_filename: str) -> str:
        """Generate human-readable summary file"""
        
        summary_lines = [
            "=" * 70,
            "3D PRINTING PROFILE SUMMARY",
            "Generated by AI Slicer Profile Generator",
            "=" * 70,
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            ""
        ]
        
        # Analysis section
        if "analysis" in analysis:
            ana = analysis["analysis"]
            summary_lines.extend([
                "ANALYSIS",
                "-" * 70,
                f"Model Type: {ana.get('model_type', 'Unknown')}",
                f"Complexity: {ana.get('complexity_assessment', 'Medium')}",
                ""
            ])
            
            if "print_challenges" in ana and ana["print_challenges"]:
                summary_lines.append("Print Challenges:")
                for challenge in ana["print_challenges"]:
                    summary_lines.append(f"  • {challenge}")
                summary_lines.append("")
            
            if "key_considerations" in ana and ana["key_considerations"]:
                summary_lines.append("Key Considerations:")
                for consideration in ana["key_considerations"]:
                    summary_lines.append(f"  • {consideration}")
                summary_lines.append("")
        
        # Profile settings
        if "profile" in analysis:
            prof = analysis["profile"]
            summary_lines.extend([
                "PROFILE SETTINGS",
                "-" * 70,
                "",
                "Layer Settings:",
                f"  Layer Height: {prof.get('layer_height', 0.2)} mm",
                f"  First Layer Height: {prof.get('first_layer_height', 0.2)} mm",
                "",
                "Walls and Shells:",
                f"  Perimeters: {prof.get('perimeters', 3)}",
                f"  Top Solid Layers: {prof.get('top_solid_layers', 5)}",
                f"  Bottom Solid Layers: {prof.get('bottom_solid_layers', 5)}",
                "",
                "Infill:",
                f"  Density: {prof.get('infill_percentage', 20)}%",
                f"  Pattern: {prof.get('infill_pattern', 'cubic')}",
                "",
                "Support:",
                f"  Enable Support: {prof.get('support_material', False)}",
                f"  Support Type: {prof.get('support_type', 'normal')}",
                f"  Support Style: {prof.get('support_style', 'default')}",
                f"  Angle Threshold: {prof.get('support_angle_threshold', 45)}°",
                "",
                "Speed (mm/s):",
                f"  Print Speed: {prof.get('print_speed', 60)}",
                f"  First Layer Speed: {prof.get('first_layer_speed', 20)}",
                f"  Perimeter Speed: {prof.get('perimeter_speed', 45)}",
                f"  Infill Speed: {prof.get('infill_speed', 80)}",
                f"  Travel Speed: {prof.get('travel_speed', 150)}",
                "",
                "Temperature:",
                f"  Nozzle: {prof.get('temperature', 210)}°C",
                f"  Bed: {prof.get('bed_temperature', 60)}°C",
                "",
                "Cooling:",
                f"  Fan Speed: {prof.get('cooling_fan_speed', 100)}%",
                f"  First Layer Fan: {prof.get('first_layer_fan_speed', 0)}%",
                ""
            ])
        
        # Reasoning
        if "reasoning" in analysis:
            summary_lines.extend([
                "AI REASONING",
                "-" * 70,
                analysis["reasoning"],
                ""
            ])
        
        # Recommendations
        summary_lines.extend([
            "RECOMMENDATIONS",
            "-" * 70,
            f"Material: {analysis.get('material_suggestion', 'PLA')}",
            f"Expected Quality: {analysis.get('estimated_quality', 'Standard')}",
            ""
        ])
        
        summary_lines.append("=" * 70)
        
        # Save to file
        output_path = os.path.join(self.output_dir, f"{base_filename}_summary.txt")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(summary_lines))
        
        return output_path
    
    def open_in_orca_slicer(self, profile_path: str) -> bool:
        """
        Attempt to open the profile in Orca Slicer
        
        Args:
            profile_path: Path to the profile file
            
        Returns:
            True if successful, False otherwise
        """
        
        if not os.path.exists(self.orca_path):
            print(f"Orca Slicer not found at: {self.orca_path}")
            return False
        
        try:
            subprocess.Popen([self.orca_path, profile_path])
            return True
        except Exception as e:
            print(f"Failed to open Orca Slicer: {e}")
            return False

