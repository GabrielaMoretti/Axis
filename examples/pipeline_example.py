"""
VISIONFLOW Pipeline Example
Demonstrates building and using custom pipelines.
"""

from PIL import Image
from visionflow.pipeline import Pipeline
from visionflow.modules import ColorCorrector, LensSimulator, TextureRefiner

def main():
    # Load image
    print("Loading image...")
    image = Image.open("input.jpg")
    
    # Create custom pipeline
    print("Building custom pipeline...")
    pipeline = Pipeline("Portrait Enhancement")
    
    # Add operations to pipeline
    pipeline.add_operation("Denoise", TextureRefiner.denoise, {'strength': 1.5})
    pipeline.add_operation("Smooth Skin", TextureRefiner.smooth_skin, {'smoothness': 0.3})
    pipeline.add_operation("White Balance", ColorCorrector.adjust_white_balance, 
                          {'temperature': 0.05, 'tint': 0.0})
    pipeline.add_operation("Exposure", ColorCorrector.adjust_exposure, {'exposure': 0.2})
    pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, {'contrast': 1.15})
    pipeline.add_operation("Saturation", ColorCorrector.adjust_saturation, {'saturation': 1.1})
    pipeline.add_operation("Enhance Details", TextureRefiner.enhance_details, {'strength': 0.5})
    pipeline.add_operation("Vignette", LensSimulator.apply_vignette, {'strength': 0.2})
    
    # Execute pipeline with snapshots
    print("Executing pipeline...")
    result = pipeline.execute(image, save_snapshots=True)
    
    # Save final result
    print("Saving final result...")
    result.save("output_pipeline.jpg", quality=95)
    
    # Save intermediate snapshots
    print("Saving intermediate results...")
    for i in range(0, len(pipeline.operations) + 1, 2):
        snapshot = pipeline.get_snapshot(i)
        if snapshot:
            snapshot.save(f"output_step_{i}.jpg", quality=95)
    
    # Print pipeline summary
    print("\nPipeline Operations:")
    for i, op in enumerate(pipeline.get_operation_list()):
        print(f"  {i+1}. {op['name']}")
    
    print("\nDone! Results saved.")

if __name__ == "__main__":
    main()
