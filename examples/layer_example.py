"""
VISIONFLOW Layer Example
Demonstrates working with image layers.
"""

from PIL import Image
from visionflow.core.image import VisionFlowImage
from visionflow.modules import ColorCorrector, TextureRefiner

def main():
    # Load base image
    print("Loading base image...")
    vf_image = VisionFlowImage(image_path="input.jpg")
    
    # Get image info
    metadata = vf_image.get_metadata()
    print(f"\nImage: {metadata['width']}x{metadata['height']}")
    print(f"Mean brightness: {metadata['mean_brightness']:.2f}")
    
    # Work with the base image
    base = vf_image.base_image.copy()
    
    # Create adjustment layers
    print("\nCreating adjustment layers...")
    
    # Layer 1: Color correction
    color_adjusted = ColorCorrector.adjust_white_balance(base, temperature=0.1, tint=0.0)
    color_adjusted = ColorCorrector.adjust_saturation(color_adjusted, saturation=1.2)
    vf_image.add_layer(color_adjusted, "Color Correction", opacity=0.8)
    
    # Layer 2: Texture enhancement
    texture_enhanced = TextureRefiner.enhance_details(base, strength=1.0)
    vf_image.add_layer(texture_enhanced, "Texture Enhancement", opacity=0.5)
    
    # Layer 3: Clarity
    clarity_applied = TextureRefiner.apply_clarity(base, amount=0.8)
    vf_image.add_layer(clarity_applied, "Clarity", opacity=0.6)
    
    print(f"Total layers: {len(vf_image.layers)}")
    
    # Flatten and save
    print("\nFlattening layers...")
    result = vf_image.flatten()
    result.save("output_layered.jpg", quality=95)
    
    # Save with history
    vf_image.save("output_final.jpg", flatten=True)
    
    print("\nProcessing history:")
    for i, op in enumerate(vf_image.processing_history):
        print(f"  {i+1}. {op['operation']}")
    
    print("\nDone! Layered result saved.")

if __name__ == "__main__":
    main()
