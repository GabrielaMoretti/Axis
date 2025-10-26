"""
Command-Line Interface for VISIONFLOW
Professional image editor with modular workflow.
"""

import argparse
import sys
from pathlib import Path
from PIL import Image

from visionflow.core.image import VisionFlowImage
from visionflow.modules import (
    ImageImporter, ColorCorrector, FocusDepthController,
    LensSimulator, TextureRefiner, StyleCreator
)
from visionflow.pipeline import Pipeline, PipelinePreset


def print_banner():
    """Print VISIONFLOW banner."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                        VISIONFLOW                            ║
║          Professional Image Editor with Optical Integrity    ║
║                     Version 0.1.0                           ║
╚═══════════════════════════════════════════════════════════════╝
    """)


def analyze_command(args):
    """Handle image analysis command."""
    print(f"\n📊 Analyzing image: {args.input}")
    
    try:
        image = ImageImporter.import_image(args.input)
        analysis = ImageImporter.analyze_technical_properties(image)
        
        print("\n=== Image Technical Analysis ===")
        print(f"\nDimensions: {analysis['dimensions']['width']}x{analysis['dimensions']['height']}")
        print(f"Aspect Ratio: {analysis['dimensions']['aspect_ratio']:.2f}")
        print(f"Color Space: {analysis['color_space']}")
        print(f"Format: {analysis['format']}")
        
        print(f"\n--- Brightness ---")
        print(f"Mean: {analysis['brightness']['mean']:.2f}")
        print(f"Std Dev: {analysis['brightness']['std']:.2f}")
        print(f"Range: {analysis['brightness']['min']} - {analysis['brightness']['max']}")
        
        print(f"\n--- Channels ---")
        for channel, data in analysis['channels'].items():
            print(f"{channel.capitalize()}: Mean={data['mean']:.2f}, Std={data['std']:.2f}")
        
        print(f"\n--- Quality Metrics ---")
        print(f"Sharpness Score: {analysis['sharpness']:.2f}")
        
        if analysis['exif']:
            print(f"\n--- EXIF Data ---")
            for key, value in list(analysis['exif'].items())[:10]:
                print(f"{key}: {value}")
        
        print("\n✅ Analysis complete!\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def process_command(args):
    """Handle image processing command."""
    print(f"\n🎨 Processing image: {args.input}")
    
    try:
        # Load image
        vf_image = VisionFlowImage(image_path=args.input)
        current_image = vf_image.base_image
        
        # Apply operations based on arguments
        operations_applied = []
        
        # Color corrections
        if args.temperature or args.tint:
            temp = args.temperature if args.temperature else 0.0
            tint = args.tint if args.tint else 0.0
            current_image = ColorCorrector.adjust_white_balance(current_image, temp, tint)
            operations_applied.append(f"White Balance (temp={temp}, tint={tint})")
        
        if args.exposure:
            current_image = ColorCorrector.adjust_exposure(current_image, args.exposure)
            operations_applied.append(f"Exposure ({args.exposure})")
        
        if args.contrast:
            current_image = ColorCorrector.adjust_contrast(current_image, args.contrast)
            operations_applied.append(f"Contrast ({args.contrast})")
        
        if args.saturation:
            current_image = ColorCorrector.adjust_saturation(current_image, args.saturation)
            operations_applied.append(f"Saturation ({args.saturation})")
        
        # Focus and depth
        if args.blur:
            current_image = FocusDepthController.apply_gaussian_blur(current_image, args.blur)
            operations_applied.append(f"Blur ({args.blur})")
        
        if args.sharpen:
            current_image = FocusDepthController.sharpen(current_image, args.sharpen)
            operations_applied.append(f"Sharpen ({args.sharpen})")
        
        # Lens effects
        if args.vignette:
            current_image = LensSimulator.apply_vignette(current_image, args.vignette)
            operations_applied.append(f"Vignette ({args.vignette})")
        
        # Texture
        if args.denoise:
            current_image = TextureRefiner.denoise(current_image, args.denoise)
            operations_applied.append(f"Denoise ({args.denoise})")
        
        if args.grain:
            current_image = TextureRefiner.apply_grain(current_image, args.grain)
            operations_applied.append(f"Grain ({args.grain})")
        
        if args.clarity:
            current_image = TextureRefiner.apply_clarity(current_image, args.clarity)
            operations_applied.append(f"Clarity ({args.clarity})")
        
        # Style
        if args.style:
            style_creator = StyleCreator()
            current_image = style_creator.apply_style(current_image, args.style, 
                                                     args.style_intensity if args.style_intensity else 1.0)
            operations_applied.append(f"Style: {args.style}")
        
        # Save output
        output_path = args.output if args.output else args.input.replace('.', '_processed.')
        current_image.save(output_path)
        
        print(f"\n✅ Processing complete!")
        print(f"\nOperations applied:")
        for op in operations_applied:
            print(f"  • {op}")
        print(f"\n💾 Saved to: {output_path}\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def pipeline_command(args):
    """Handle pipeline preset command."""
    print(f"\n🔧 Applying pipeline preset: {args.preset}")
    print(f"   Input: {args.input}")
    
    try:
        # Load image
        image = Image.open(args.input)
        
        # Select preset
        if args.preset == 'portrait':
            pipeline = PipelinePreset.portrait_retouch()
        elif args.preset == 'landscape':
            pipeline = PipelinePreset.landscape_enhancement()
        elif args.preset == 'cinematic':
            pipeline = PipelinePreset.cinematic_look()
        else:
            print(f"❌ Unknown preset: {args.preset}")
            print("Available presets: portrait, landscape, cinematic")
            sys.exit(1)
        
        # Execute pipeline
        result = pipeline.execute(image)
        
        # Save output
        output_path = args.output if args.output else args.input.replace('.', f'_{args.preset}.')
        result.save(output_path)
        
        print(f"\n✅ Pipeline complete!")
        print(f"\nOperations:")
        for op in pipeline.get_operation_list():
            print(f"  • {op['name']}")
        print(f"\n💾 Saved to: {output_path}\n")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def list_styles_command(args):
    """List available styles."""
    print("\n📋 Available Styles:\n")
    
    style_creator = StyleCreator()
    styles = style_creator.get_available_styles()
    
    for style in styles:
        print(f"  • {style}")
    
    print("\n")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="VISIONFLOW - Professional Image Editor",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze image technical properties')
    analyze_parser.add_argument('input', help='Input image path')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process image with operations')
    process_parser.add_argument('input', help='Input image path')
    process_parser.add_argument('-o', '--output', help='Output image path')
    
    # Color correction
    process_parser.add_argument('--temperature', type=float, help='White balance temperature (-1.0 to 1.0)')
    process_parser.add_argument('--tint', type=float, help='White balance tint (-1.0 to 1.0)')
    process_parser.add_argument('--exposure', type=float, help='Exposure adjustment (-2.0 to 2.0)')
    process_parser.add_argument('--contrast', type=float, help='Contrast (0.0 to 2.0)')
    process_parser.add_argument('--saturation', type=float, help='Saturation (0.0 to 2.0)')
    
    # Focus and depth
    process_parser.add_argument('--blur', type=float, help='Blur radius')
    process_parser.add_argument('--sharpen', type=float, help='Sharpen strength')
    
    # Lens effects
    process_parser.add_argument('--vignette', type=float, help='Vignette strength (0.0 to 1.0)')
    
    # Texture
    process_parser.add_argument('--denoise', type=float, help='Denoise strength')
    process_parser.add_argument('--grain', type=float, help='Grain intensity')
    process_parser.add_argument('--clarity', type=float, help='Clarity amount')
    
    # Style
    process_parser.add_argument('--style', help='Apply predefined style')
    process_parser.add_argument('--style-intensity', type=float, help='Style intensity (0.0 to 1.0)')
    
    # Pipeline command
    pipeline_parser = subparsers.add_parser('pipeline', help='Apply preset pipeline')
    pipeline_parser.add_argument('input', help='Input image path')
    pipeline_parser.add_argument('preset', choices=['portrait', 'landscape', 'cinematic'],
                                help='Pipeline preset to apply')
    pipeline_parser.add_argument('-o', '--output', help='Output image path')
    
    # List styles command
    list_parser = subparsers.add_parser('list-styles', help='List available styles')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    # Execute command
    if args.command == 'analyze':
        analyze_command(args)
    elif args.command == 'process':
        process_command(args)
    elif args.command == 'pipeline':
        pipeline_command(args)
    elif args.command == 'list-styles':
        list_styles_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
