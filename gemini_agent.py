"""
Google Gemini AI Agent Integration
Handles communication with Gemini 2.5 Flash for intelligent slicer profile generation
"""
import google.generativeai as genai
from typing import Dict, Any, List, Optional
import json
from config import GOOGLE_API_KEY, GEMINI_MODEL


class GeminiAgent:
    """AI Agent powered by Google Gemini for 3D printing profile generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Gemini agent"""
        self.api_key = api_key or GOOGLE_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "Google API key not found. Please set GOOGLE_API_KEY in .env file or pass it to constructor."
            )
        
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        
        # System context for the agent
        self.system_context = self._build_system_context()
    
    def _build_system_context(self) -> str:
        """Build the system context/prompt for the Gemini agent"""
        return """You are an expert 3D printing AI assistant specialized in generating optimal slicer profiles for Orca Slicer.

Your role is to:
1. Analyze 3D model features and geometric properties
2. Generate optimal printing parameters based on model characteristics
3. Learn from past successful prints and apply that knowledge to new models
4. Create detailed, safe, and high-quality slicer configurations

Key considerations:
- Layer height: Balance between quality (0.12-0.2mm) and speed (0.2-0.32mm)
- Print speed: Adjust based on detail level and overhang complexity
- Supports: Required for overhangs > 45 degrees
  * Tree supports (organic/hybrid): Best for complex overhangs, miniatures, organic shapes
  * Normal supports: Simpler models with basic overhangs
- Infill: 10-20% for decorative, 40-100% for functional parts
- Wall count: Minimum 2-3 for strength, more for functional parts
- Temperature: Material-dependent (PLA: 200-220°C, PETG: 230-250°C, ABS: 240-260°C)

Support Type Selection:
- Use "tree_auto" or "tree_hybrid" when severe overhangs (>60°) detected or overhang complexity is high
- Use "normal" for simple overhangs
- Tree supports save material and are easier to remove

Always respond with valid JSON slicer profiles and detailed reasoning for your parameter choices."""
    
    def analyze_features(self, features: Dict[str, Any], similar_cases: List[Dict] = None) -> Dict[str, Any]:
        """
        Analyze 3D model features and generate slicer profile recommendations
        
        Args:
            features: Extracted features from the 3D model
            similar_cases: Optional list of similar past cases for reference
            
        Returns:
            Analysis with recommended slicer parameters
        """
        # Build the prompt
        prompt = self._build_analysis_prompt(features, similar_cases)
        
        try:
            # Generate response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis = self._parse_analysis_response(response.text, features)
            
            return analysis
            
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def _build_analysis_prompt(self, features: Dict[str, Any], similar_cases: List[Dict] = None) -> str:
        """Build the prompt for model analysis"""
        
        prompt_parts = [
            "Analyze this 3D model and generate an optimal Orca Slicer profile.\n",
            "\n## Model Features:",
            json.dumps(features, indent=2),
        ]
        
        if similar_cases:
            prompt_parts.append("\n## Similar Past Cases (for reference):")
            for i, case in enumerate(similar_cases[:3], 1):  # Limit to top 3
                prompt_parts.append(f"\n### Similar Case {i}:")
                prompt_parts.append(json.dumps(case, indent=2))
        
        prompt_parts.append("""

## Instructions:
Generate a complete slicer profile with the following structure:

```json
{
  "analysis": {
    "model_type": "descriptive category (e.g., 'miniature', 'functional_part', 'decorative')",
    "complexity_assessment": "low/medium/high",
    "print_challenges": ["list", "of", "challenges"],
    "key_considerations": ["important", "factors"]
  },
  "profile": {
    "layer_height": 0.2,
    "first_layer_height": 0.2,
    "perimeters": 3,
    "top_solid_layers": 5,
    "bottom_solid_layers": 5,
    "infill_percentage": 20,
    "infill_pattern": "cubic",
    "support_material": true,
    "support_type": "tree_auto",
    "support_style": "tree",
    "tree_support_branch_angle": 45,
    "tree_support_branch_distance": 2.5,
    "support_angle_threshold": 45,
    "brim_width": 0,
    "brim_type": "no_brim",
    "print_speed": 60,
    "first_layer_speed": 20,
    "perimeter_speed": 45,
    "infill_speed": 80,
    "travel_speed": 150,
    "retraction_length": 0.8,
    "retraction_speed": 35,
    "temperature": 210,
    "bed_temperature": 60,
    "cooling_fan_speed": 100,
    "first_layer_fan_speed": 0
  },
  "reasoning": "Detailed explanation of why these parameters were chosen",
  "material_suggestion": "PLA/PETG/ABS",
  "estimated_quality": "high/medium/standard",
  "estimated_print_time_factor": 1.0
}
```

Provide your response as valid JSON only.""")
        
        return "\n".join(prompt_parts)
    
    def _parse_analysis_response(self, response_text: str, features: Dict[str, Any]) -> Dict[str, Any]:
        """Parse and validate Gemini's response"""
        
        # Extract JSON from response (handle markdown code blocks)
        response_text = response_text.strip()
        
        if "```json" in response_text:
            start = response_text.find("```json") + 7
            end = response_text.rfind("```")
            response_text = response_text[start:end].strip()
        elif "```" in response_text:
            start = response_text.find("```") + 3
            end = response_text.rfind("```")
            response_text = response_text[start:end].strip()
        
        try:
            analysis = json.loads(response_text)
            
            # Add metadata
            analysis["model_hash"] = features.get("model_hash", "")
            analysis["source"] = "gemini_ai"
            
            return analysis
            
        except json.JSONDecodeError as e:
            # Fallback: return a basic analysis
            return self._generate_fallback_analysis(features, response_text)
    
    def _generate_fallback_analysis(self, features: Dict[str, Any], raw_response: str) -> Dict[str, Any]:
        """Generate a fallback analysis if JSON parsing fails"""
        
        # Basic rule-based fallback
        dims = features.get("dimensions", {})
        overhangs = features.get("overhangs", {})
        complexity = features.get("complexity", {})
        
        return {
            "analysis": {
                "model_type": "unknown",
                "complexity_assessment": complexity.get("detail_level", "medium"),
                "print_challenges": ["automatic_analysis_failed"],
                "key_considerations": ["using_fallback_profile"],
                "raw_ai_response": raw_response[:500]  # Store partial response
            },
            "profile": {
                "layer_height": 0.2,
                "first_layer_height": 0.2,
                "perimeters": 3,
                "top_solid_layers": 5,
                "bottom_solid_layers": 5,
                "infill_percentage": 20,
                "infill_pattern": "cubic",
                "support_material": overhangs.get("needs_supports", False),
                "support_type": "tree_auto" if overhangs.get("recommend_tree_support", False) else "normal",
                "support_style": "tree" if overhangs.get("recommend_tree_support", False) else "default",
                "tree_support_branch_angle": 45,
                "tree_support_branch_distance": 2.5,
                "support_angle_threshold": 45,
                "brim_width": 0,  # Always disabled per user request
                "brim_type": "no_brim",
                "print_speed": 60,
                "first_layer_speed": 20,
                "perimeter_speed": 45,
                "infill_speed": 80,
                "travel_speed": 150,
                "retraction_length": 0.8,
                "retraction_speed": 35,
                "temperature": 210,
                "bed_temperature": 60,
                "cooling_fan_speed": 100,
                "first_layer_fan_speed": 0
            },
            "reasoning": "Fallback profile generated due to AI parsing error. Using safe default parameters.",
            "material_suggestion": "PLA",
            "estimated_quality": "standard",
            "estimated_print_time_factor": 1.0,
            "model_hash": features.get("model_hash", ""),
            "source": "fallback"
        }
    
    def generate_learning_summary(self, model_features: Dict, profile_result: Dict, user_feedback: str) -> str:
        """
        Generate a learning summary from a completed print
        
        Args:
            model_features: Original model features
            profile_result: The profile that was used
            user_feedback: User's feedback on the print quality
            
        Returns:
            Learning summary to be stored in knowledge base
        """
        prompt = f"""Based on this 3D printing case, generate a concise learning summary:

## Model Features:
{json.dumps(model_features, indent=2)}

## Profile Used:
{json.dumps(profile_result, indent=2)}

## User Feedback:
{user_feedback}

Generate a brief learning summary (2-3 sentences) that captures:
1. What worked well or what failed
2. Key parameter insights
3. Recommendations for similar future models

Respond with plain text only."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Learning summary generation failed: {str(e)}"

