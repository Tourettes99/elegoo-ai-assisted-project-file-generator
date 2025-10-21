"""
Command-line interface for AI 3D Print Profile Generator
"""
import argparse
import sys
from ai_agent import AI3DPrintAgent
from config import GOOGLE_API_KEY
import os


def main():
    parser = argparse.ArgumentParser(
        description="AI 3D Print Profile Generator - Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s model.stl                                    # Analyze with default
  %(prog)s model.stl --material "Elegoo RAPID PETG"     # Elegoo filament
  %(prog)s model.stl --material "Generic PLA"           # Generic filament
  %(prog)s model.stl --build-plate 256                  # For 256mm build plate
  %(prog)s model.stl --no-kb                            # Don't use knowledge base
  %(prog)s --stats                                      # Show knowledge base stats
        """
    )
    
    # Model analysis arguments
    parser.add_argument(
        'model',
        nargs='?',
        help='Path to 3D model file (.stl, .obj, .3mf, etc.)'
    )
    
    parser.add_argument(
        '-m', '--material',
        default='Elegoo PLA',
        help='Filament type (e.g., "Elegoo PLA", "Elegoo RAPID PETG", "Generic PLA")'
    )
    
    parser.add_argument(
        '-b', '--build-plate',
        type=float,
        default=220.0,
        help='Build plate size in mm (default: 220.0)'
    )
    
    parser.add_argument(
        '--no-kb',
        action='store_true',
        help='Disable knowledge base lookup'
    )
    
    parser.add_argument(
        '-f', '--feedback',
        help='Save feedback with the analysis'
    )
    
    # Knowledge base operations
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show knowledge base statistics'
    )
    
    parser.add_argument(
        '--export',
        metavar='FILE',
        help='Export knowledge base to file'
    )
    
    parser.add_argument(
        '--api-key',
        help='Google Gemini API key (overrides .env)'
    )
    
    args = parser.parse_args()
    
    # Determine API key
    api_key = args.api_key or GOOGLE_API_KEY
    
    if not api_key and not args.stats and not args.export:
        print("❌ Error: GOOGLE_API_KEY not found!")
        print("   Please set it in .env file or use --api-key option")
        return 1
    
    # Initialize agent if needed
    agent = None
    
    # Handle knowledge base operations
    if args.stats:
        print("📊 Loading knowledge base statistics...\n")
        agent = AI3DPrintAgent(google_api_key=api_key)
        stats = agent.get_knowledge_stats()
        
        print("=" * 50)
        print("KNOWLEDGE BASE STATISTICS")
        print("=" * 50)
        print(f"Total Cases:       {stats['total_cases']}")
        print(f"Successful Prints: {stats['successful_cases']}")
        print(f"Failed Prints:     {stats['failed_cases']}")
        print(f"Unknown Outcome:   {stats['unknown_outcome']}")
        print(f"Success Rate:      {stats['success_rate']:.1f}%")
        print("=" * 50)
        return 0
    
    if args.export:
        print(f"💾 Exporting knowledge base to {args.export}...\n")
        agent = AI3DPrintAgent(google_api_key=api_key)
        path = agent.export_knowledge(args.export)
        print(f"✅ Exported to: {path}")
        return 0
    
    # Model analysis
    if not args.model:
        parser.print_help()
        return 1
    
    if not os.path.exists(args.model):
        print(f"❌ Error: Model file not found: {args.model}")
        return 1
    
    print("=" * 70)
    print("AI 3D PRINT PROFILE GENERATOR")
    print("=" * 70)
    print()
    
    # Initialize agent
    agent = AI3DPrintAgent(google_api_key=api_key)
    
    try:
        # Analyze the model (always Elegoo Orca Slicer)
        result = agent.analyze_model(
            model_path=args.model,
            material=args.material,
            use_knowledge_base=not args.no_kb,
            slicer_type="elegoo_orca",
            build_plate_size=args.build_plate
        )
        
        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)
        
        # Display key information
        analysis = result['analysis'].get('analysis', {})
        print(f"\nModel Type:    {analysis.get('model_type', 'Unknown')}")
        print(f"Complexity:    {analysis.get('complexity_assessment', 'Medium')}")
        print(f"Quality:       {result['analysis'].get('estimated_quality', 'Standard')}")
        print(f"Material:      {args.material}")
        
        # Display profile files
        print(f"\n📄 Generated Files:")
        if "3mf_profile" in result['profile_files']:
            print(f"   3MF PROJECT: {result['profile_files']['3mf_profile']}")
            print(f"   ✓ Just double-click to open in Orca Slicer!")
        print(f"   JSON Config (Backup): {result['profile_files']['json_config']}")
        print(f"   JSON Profile (Reference): {result['profile_files']['json_profile']}")
        print(f"   Summary: {result['profile_files']['summary']}")
        
        # Save to knowledge base if feedback provided
        if args.feedback:
            print(f"\n💾 Saving to knowledge base with feedback...")
            case_id = agent.save_to_knowledge_base(result, args.feedback)
            print(f"   ✅ Saved as: {case_id}")
        
        print("\n" + "=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print("\nNext steps:")
        print("1. Open the .3mf file in Orca Slicer (model + settings included!)")
        print("2. Review and adjust settings if needed")
        print("3. Slice and print")
        print("4. After printing, save feedback with --feedback option")
        print()
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

