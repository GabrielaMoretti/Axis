"""
VISIONFLOW Basic Example
Demonstrates basic image processing operations.
"""

from PIL import Image
from visionflow.modules import ColorCorrector, TextureRefiner, LensSimulator

def main():
    # Load image
    print("Loading image...")
    image = Image.open("input.jpg")
    
    # Apply color corrections
    print("Applying color corrections...")
    image = ColorCorrector.adjust_white_balance(image, temperature=0.1, tint=-0.05)
    image = ColorCorrector.adjust_exposure(image, exposure=0.2)
    image = ColorCorrector.adjust_contrast(image, contrast=1.2)
    image = ColorCorrector.adjust_saturation(image, saturation=1.1)
    
    # Apply lens effects
    print("Applying lens effects...")
    image = LensSimulator.apply_vignette(image, strength=0.3)
    
    # Apply texture refinement
    print("Applying texture refinement...")
    image = TextureRefiner.apply_clarity(image, amount=0.5)
    
    # Save result
    print("Saving result...")
    image.save("output_basic.jpg", quality=95)
    print("Done! Saved to output_basic.jpg")

if __name__ == "__main__":
    main()
