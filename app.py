"""
Gradio Web Application for AI 3D Print Profile Generator
Modern UI for the AI agent system
"""
import gradio as gr
import os
from ai_agent import AI3DPrintAgent
from config import GOOGLE_API_KEY
import json


# Initialize the AI agent globally
agent = None


def initialize_agent():
    """Initialize the AI agent"""
    global agent
    if agent is None:
        try:
            agent = AI3DPrintAgent(google_api_key=GOOGLE_API_KEY)
            return "✅ AI Agent initialized successfully!"
        except Exception as e:
            return f"❌ Error initializing agent: {str(e)}"
    return "✅ Agent already initialized"


def analyze_3d_model(model_file, material, use_kb, build_plate_size):
    """
    Analyze a 3D model and generate profile
    
    Args:
        model_file: Uploaded 3D model file
        material: Selected material
        use_kb: Whether to use knowledge base
        slicer_type: Type of slicer (orca or elegoo_orca)
        build_plate_size: Build plate size in mm
        
    Returns:
        Tuple of (summary_text, profile_json, model_file, config_file, summary_file)
    """
    global agent
    
    if agent is None:
        return "❌ Please initialize the agent first!", "", None, None, None
    
    if model_file is None:
        return "❌ Please upload a 3D model file!", "", None, None, None
    
    try:
        # Get the file path
        model_path = model_file.name if hasattr(model_file, 'name') else model_file
        
        # Analyze the model (always Elegoo Orca Slicer)
        result = agent.analyze_model(
            model_path=model_path,
            material=material,
            use_knowledge_base=use_kb,
            slicer_type="elegoo_orca",
            build_plate_size=build_plate_size
        )
        
        # Build summary text
        summary_parts = [
            "# 🎯 Analysis Complete!\n",
            f"**Model:** {os.path.basename(model_path)}",
            f"**Material:** {material}",
            f"**Similar Cases Found:** {result['similar_cases_count']}\n",
            "## 📊 Feature Summary",
            "```",
            result['feature_summary'],
            "```\n",
            "## 🤖 AI Analysis",
        ]
        
        analysis = result['analysis'].get('analysis', {})
        summary_parts.extend([
            f"**Model Type:** {analysis.get('model_type', 'Unknown')}",
            f"**Complexity:** {analysis.get('complexity_assessment', 'Medium')}",
            f"**Quality Estimate:** {result['analysis'].get('estimated_quality', 'Standard')}\n",
        ])
        
        if 'print_challenges' in analysis and analysis['print_challenges']:
            summary_parts.append("**Print Challenges:**")
            for challenge in analysis['print_challenges']:
                summary_parts.append(f"- {challenge}")
            summary_parts.append("")
        
        summary_parts.append("## 💡 AI Reasoning")
        summary_parts.append(result['analysis'].get('reasoning', 'No reasoning provided'))
        
        summary_text = "\n".join(summary_parts)
        
        # Format profile JSON for display
        profile_json = json.dumps(result['analysis'].get('profile', {}), indent=2)
        
        # Get file paths - provide both 3MF and JSON config
        three_mf_file = result['profile_files'].get('3mf_profile', None)
        json_config_file = result['profile_files']['json_config']
        summary_file = result['profile_files']['summary']
        
        # Add import instructions to summary
        summary_text += f"\n\n---\n\n## How to Use in Elegoo Orca Slicer\n\n"
        
        prof = result['analysis'].get('profile', {})
        
        if "3mf_profile" in result['profile_files']:
            summary_text += "### RECOMMENDED: Open 3MF Project File\n"
            summary_text += f"1. **Double-click the .3mf file** (opens in Elegoo Orca Slicer)\n"
            summary_text += "2. **Model + ALL settings load automatically!**\n"
            if prof.get('support_material') and (prof.get('support_style') == 'tree' or 'tree' in str(prof.get('support_type', ''))):
                summary_text += "3. **Tree supports are included!**\n"
            summary_text += "4. **Slice and print!**\n"
            summary_text += "\n### Backup Method: Import JSON Config\n"
            summary_text += "1. Load your model manually\n"
            summary_text += "2. File -> Import -> Import Config\n"
            summary_text += "3. Select the _config.json file\n"
        else:
            summary_text += "1. Load your model in the slicer\n"
            summary_text += "2. File -> Import -> Import Config\n"
            summary_text += "3. Select the _config.json file\n"
        
        summary_text += f"\n**Note:** Generated for Elegoo Orca Slicer"
        
        return summary_text, profile_json, three_mf_file, json_config_file, summary_file
        
    except Exception as e:
        return f"❌ Error analyzing model: {str(e)}", "", None, None, None


def save_with_feedback(model_file, material, use_kb, feedback):
    """Analyze model and save to knowledge base with feedback"""
    global agent
    
    if agent is None:
        return "❌ Please initialize the agent first!"
    
    if model_file is None:
        return "❌ Please upload a 3D model file!"
    
    try:
        model_path = model_file.name if hasattr(model_file, 'name') else model_file
        
        result = agent.process_with_feedback(
            model_path=model_path,
            material=material,
            feedback=feedback if feedback.strip() else None
        )
        
        return f"✅ Analysis complete and saved to knowledge base!\n**Case ID:** {result['case_id']}"
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def get_stats():
    """Get knowledge base statistics"""
    global agent
    
    if agent is None:
        return "❌ Agent not initialized"
    
    try:
        stats = agent.get_knowledge_stats()
        
        stats_text = f"""
# 📚 Knowledge Base Statistics

**Total Cases:** {stats['total_cases']}
**Successful Prints:** {stats['successful_cases']}
**Failed Prints:** {stats['failed_cases']}
**Unknown Outcome:** {stats['unknown_outcome']}
**Success Rate:** {stats['success_rate']:.1f}%
"""
        return stats_text
        
    except Exception as e:
        return f"❌ Error: {str(e)}"


def export_knowledge():
    """Export knowledge base"""
    global agent
    
    if agent is None:
        return "❌ Agent not initialized", None
    
    try:
        output_path = "knowledge_export.json"
        path = agent.export_knowledge(output_path)
        return f"✅ Knowledge base exported to: {output_path}", path
        
    except Exception as e:
        return f"❌ Error: {str(e)}", None


# Build Gradio Interface
with gr.Blocks(title="AI 3D Print Profile Generator", theme=gr.themes.Soft()) as demo:
    
    gr.Markdown("""
    # 🤖 AI 3D Print Profile Generator for Elegoo Orca Slicer
    ### Intelligent Slicer Profile Generation with Dynamic Learning
    
    Upload a 3D model, and the AI will analyze it and generate an optimized Elegoo Orca Slicer profile.
    The system learns from each print to improve future recommendations!
    """)
    
    # Initialization section
    with gr.Row():
        with gr.Column():
            init_btn = gr.Button("🚀 Initialize AI Agent", variant="primary", size="lg")
            init_output = gr.Textbox(label="Status", interactive=False)
    
    init_btn.click(fn=initialize_agent, outputs=init_output)
    
    gr.Markdown("---")
    
    # Main analysis interface
    with gr.Tabs():
        
        # Tab 1: Quick Analysis
        with gr.Tab("🎯 Quick Analysis"):
            gr.Markdown("Upload a 3D model for instant analysis and profile generation")
            
            with gr.Row():
                with gr.Column(scale=1):
                    model_input = gr.File(
                        label="📂 Upload 3D Model",
                        file_types=[".stl", ".obj", ".3mf", ".ply"],
                        type="filepath"
                    )
                    material_input = gr.Dropdown(
                        choices=[
                            "Elegoo PLA",
                            "Elegoo RAPID PLA+",
                            "Elegoo RAPID PETG",
                            "Elegoo PETG PRO",
                            "Elegoo PLA Matte",
                            "Elegoo PLA PRO",
                            "Elegoo PLA Silk",
                            "Elegoo PLA+",
                            "Elegoo ASA",
                            "Elegoo TPU 95A",
                            "Generic PLA",
                            "Generic PETG",
                            "Generic ABS"
                        ],
                        value="Elegoo PLA",
                        label="🧪 Filament Type"
                    )
                    build_plate_input = gr.Number(
                        value=220,
                        label="📏 Build Plate Size (mm)",
                        info="Common sizes: 220 (Neptune), 256 (Neptune 4), 300 (large printers)"
                    )
                    use_kb_input = gr.Checkbox(
                        value=True,
                        label="📚 Use Knowledge Base (learn from past prints)"
                    )
                    analyze_btn = gr.Button("🔍 Analyze Model", variant="primary")
                
                with gr.Column(scale=2):
                    analysis_output = gr.Markdown(label="Analysis Results")
            
            with gr.Row():
                with gr.Column():
                    profile_json_output = gr.Code(
                        label="Generated Profile (JSON Preview)",
                        language="json"
                    )
                with gr.Column():
                    gr.Markdown("### Download Files")
                    model_file_output = gr.File(label="1. PROJECT (.3mf) - Double-click to open!")
                    config_file_output = gr.File(label="2. Config (.json) - Backup import")
                    summary_file_output = gr.File(label="3. Summary (.txt) - Read explanation")
            
            analyze_btn.click(
                fn=analyze_3d_model,
                inputs=[model_input, material_input, use_kb_input, build_plate_input],
                outputs=[analysis_output, profile_json_output, model_file_output, config_file_output, summary_file_output]
            )
        
        # Tab 2: Analysis + Feedback
        with gr.Tab("💾 Save with Feedback"):
            gr.Markdown("""
            Analyze a model and save it to the knowledge base with your feedback.
            This helps the AI learn and improve!
            """)
            
            with gr.Row():
                with gr.Column():
                    model_input_2 = gr.File(
                        label="📂 Upload 3D Model",
                        file_types=[".stl", ".obj", ".3mf", ".ply"],
                        type="filepath"
                    )
                    material_input_2 = gr.Dropdown(
                        choices=["PLA", "PETG", "ABS", "TPU", "ASA"],
                        value="PLA",
                        label="🧪 Material"
                    )
                    use_kb_input_2 = gr.Checkbox(
                        value=True,
                        label="📚 Use Knowledge Base"
                    )
                    feedback_input = gr.Textbox(
                        label="💬 Feedback (Optional)",
                        placeholder="e.g., 'Print was excellent!' or 'Had some issues with supports'",
                        lines=3
                    )
                    save_btn = gr.Button("💾 Analyze & Save", variant="primary")
                    
                with gr.Column():
                    save_output = gr.Markdown(label="Result")
            
            save_btn.click(
                fn=save_with_feedback,
                inputs=[model_input_2, material_input_2, use_kb_input_2, feedback_input],
                outputs=save_output
            )
        
        # Tab 3: Knowledge Base
        with gr.Tab("📚 Knowledge Base"):
            gr.Markdown("View statistics and export the knowledge base")
            
            with gr.Row():
                stats_btn = gr.Button("📊 View Statistics")
                export_btn = gr.Button("💾 Export Knowledge Base")
            
            stats_output = gr.Markdown(label="Statistics")
            export_output = gr.Textbox(label="Export Status")
            export_file = gr.File(label="Download Export")
            
            stats_btn.click(fn=get_stats, outputs=stats_output)
            export_btn.click(fn=export_knowledge, outputs=[export_output, export_file])
    
    gr.Markdown("""
    ---
    ### 📖 How to Use
    
    1. **Initialize** the AI agent first
    2. **Upload** a 3D model (.stl, .obj, etc.)
    3. **Select** your printing material
    4. **Analyze** to generate an optimized profile
    5. **Download** the profile and import it into Orca Slicer
    6. **Save feedback** after printing to help the AI learn!
    
    ### 🎓 Learning System
    
    The AI learns from every print:
    - Successful prints reinforce good parameter choices
    - Failed prints help identify what to avoid
    - Similar models benefit from past experience
    
    ### ⚙️ Setup
    
    Make sure you have set your `GOOGLE_API_KEY` in a `.env` file or environment variable.
    """)


if __name__ == "__main__":
    # Set UTF-8 encoding for Windows console
    import sys
    if sys.platform == 'win32':
        try:
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        except:
            pass
    
    print("\n" + "="*70)
    print("Starting AI 3D Print Profile Generator")
    print("="*70)
    print("\nAccess the web interface at:")
    print("   -> http://localhost:7860")
    print("   -> http://127.0.0.1:7860")
    print("\nPress Ctrl+C to stop the server\n")
    print("="*70 + "\n")
    
    demo.launch(
        server_name="127.0.0.1",  # Changed from 0.0.0.0 for Windows compatibility
        server_port=7860,
        share=False,
        show_error=True,
        inbrowser=True  # Automatically open browser
    )

