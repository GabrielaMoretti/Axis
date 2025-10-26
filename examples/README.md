# VISIONFLOW Examples

This directory contains example scripts demonstrating various VISIONFLOW features.

## Examples

### 1. basic_example.py
Demonstrates basic image processing operations:
- Color corrections (white balance, exposure, contrast, saturation)
- Lens effects (vignette)
- Texture refinement (clarity)

### 2. pipeline_example.py
Shows how to build and use custom pipelines:
- Creating a custom pipeline
- Adding multiple operations
- Executing with snapshots
- Saving intermediate results

### 3. style_example.py
Demonstrates style application:
- Applying predefined styles (cinematic, vintage, dramatic, soft)
- Creating custom styles
- Style intensity control

### 4. layer_example.py
Shows working with image layers:
- Loading images into layer system
- Creating adjustment layers
- Layer opacity control
- Flattening and saving

## Usage

To run an example:

```bash
# Make sure you have an input.jpg in the same directory
python3 basic_example.py
```

Or use the test image created during testing:

```bash
cp ../test_image.jpg input.jpg
python3 style_example.py
```
