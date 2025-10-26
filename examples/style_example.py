"""
VISIONFLOW Style Example
Demonstrates applying predefined and custom styles.
"""

from PIL import Image
from visionflow.modules import StyleCreator

def main():
    # Load image
    print("Loading image...")
    image = Image.open("input.jpg")
    
    # Create style creator
    style_creator = StyleCreator()
    
    # List available styles
    print("\nAvailable styles:")
    for style in style_creator.get_available_styles():
        print(f"  • {style}")
    
    # Apply predefined styles
    print("\nApplying styles...")
    
    styles_to_apply = ['cinematic', 'vintage', 'dramatic', 'soft']
    
    for style_name in styles_to_apply:
        print(f"  Applying {style_name} style...")
        styled = style_creator.apply_style(image, style_name, intensity=0.8)
        styled.save(f"output_{style_name}.jpg", quality=95)
    
    # Create and apply custom style
    print("\nCreating custom style...")
    custom_params = {
        'temperature': 0.15,
        'tint': -0.1,
        'contrast': 1.25,
        'saturation': 1.15,
        'clarity': 0.8,
        'vignette': 0.25,
        'grain': 0.08
    }
    
    style_creator.create_custom_style('my_custom_style', custom_params)
    
    print("Applying custom style...")
    custom_styled = style_creator.apply_style(image, 'my_custom_style', intensity=1.0)
    custom_styled.save("output_custom.jpg", quality=95)
    
    print("\nDone! All styled images saved.")

if __name__ == "__main__":
    main()
