# VISIONFLOW Quick Reference

## Installation

```bash
pip install -e .
```

## CLI Commands

### Analyze Image
```bash
visionflow analyze input.jpg
```
Returns: dimensions, brightness, channels, sharpness, EXIF data

### Process Image
```bash
# Color corrections
visionflow process input.jpg --temperature 0.1 --exposure 0.2 --contrast 1.2 --saturation 1.1 -o output.jpg

# Focus effects
visionflow process input.jpg --blur 3.0 --sharpen 1.5 -o output.jpg

# Lens effects
visionflow process input.jpg --vignette 0.3 -o output.jpg

# Texture
visionflow process input.jpg --denoise 1.0 --grain 0.1 --clarity 0.5 -o output.jpg

# Apply style
visionflow process input.jpg --style cinematic --style-intensity 0.8 -o output.jpg
```

### Apply Pipeline Preset
```bash
visionflow pipeline input.jpg portrait -o output.jpg
visionflow pipeline input.jpg landscape -o output.jpg
visionflow pipeline input.jpg cinematic -o output.jpg
```

### List Available Styles
```bash
visionflow list-styles
```
Returns: cinematic, vintage, dramatic, soft, high_key, low_key

## Python API

### Basic Usage
```python
from PIL import Image
from visionflow.modules import ColorCorrector, TextureRefiner, StyleCreator

# Load image
image = Image.open("input.jpg")

# Apply operations
image = ColorCorrector.adjust_contrast(image, 1.2)
image = TextureRefiner.apply_clarity(image, 0.5)

# Apply style
style_creator = StyleCreator()
image = style_creator.apply_style(image, "cinematic", intensity=0.8)

# Save
image.save("output.jpg")
```

### Using Layers
```python
from visionflow.core.image import VisionFlowImage
from visionflow.modules import ColorCorrector

# Load with layer support
vf_image = VisionFlowImage(image_path="input.jpg")

# Add adjustment layers
adjusted = ColorCorrector.adjust_saturation(vf_image.base_image, 1.2)
vf_image.add_layer(adjusted, "Color Adjustment", opacity=0.8)

# Flatten and save
result = vf_image.flatten()
result.save("output.jpg")
```

### Custom Pipeline
```python
from PIL import Image
from visionflow.pipeline import Pipeline
from visionflow.modules import ColorCorrector, LensSimulator

# Create pipeline
pipeline = Pipeline("My Workflow")
pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, {'contrast': 1.2})
pipeline.add_operation("Vignette", LensSimulator.apply_vignette, {'strength': 0.3})

# Execute
image = Image.open("input.jpg")
result = pipeline.execute(image, save_snapshots=True)
result.save("output.jpg")

# Get intermediate result
snapshot = pipeline.get_snapshot(1)  # After first operation
```

## Module Reference

### ColorCorrector
- `adjust_white_balance(image, temperature, tint)`
- `adjust_exposure(image, exposure)`
- `adjust_contrast(image, contrast)`
- `adjust_saturation(image, saturation)`
- `adjust_hsl(image, hue, saturation, lightness)`
- `apply_curves(image, curve_points)`

### FocusDepthController
- `apply_gaussian_blur(image, radius)`
- `apply_depth_of_field(image, focus_point, focus_range, max_blur)`
- `apply_radial_blur(image, center, strength)`
- `apply_tilt_shift(image, focus_line_y, focus_width, max_blur)`
- `sharpen(image, strength)`

### LensSimulator
- `apply_vignette(image, strength, center)`
- `apply_chromatic_aberration(image, strength)`
- `apply_lens_distortion(image, distortion)`
- `apply_bokeh(image, blur_amount, shape)`
- `simulate_aperture(image, f_stop)`

### TextureRefiner
- `denoise(image, strength)`
- `enhance_details(image, strength)`
- `apply_grain(image, intensity, size)`
- `smooth_skin(image, mask, smoothness)`
- `adjust_texture_frequency(image, low_freq, high_freq)`
- `apply_clarity(image, amount)`

### StyleCreator
- `apply_style(image, style_name, intensity)`
- `create_custom_style(name, parameters)`
- `get_available_styles()`
- `create_color_grade(image, shadows, midtones, highlights)`

## Parameter Ranges

- **temperature, tint**: -1.0 to 1.0
- **exposure**: -2.0 to 2.0 (stops)
- **contrast**: 0.0 to 2.0 (1.0 = original)
- **saturation**: 0.0 to 2.0 (1.0 = original)
- **blur radius**: 0.0 to 20.0 pixels
- **sharpen strength**: 0.0 to 3.0
- **vignette strength**: 0.0 to 1.0
- **grain intensity**: 0.0 to 1.0
- **clarity amount**: 0.0 to 2.0
- **style intensity**: 0.0 to 1.0

## Available Styles

- **cinematic**: Warm tones, controlled contrast, subtle vignette
- **vintage**: Warm yellows, faded colors, heavy grain
- **dramatic**: High contrast, boosted saturation, clarity
- **soft**: Gentle tones, reduced contrast, smooth
- **high_key**: Bright, airy, low contrast
- **low_key**: Dark, moody, high contrast

## Pipeline Presets

- **portrait**: Denoise → Smooth Skin → Enhance Details → Color Correction
- **landscape**: Clarity → Saturation → Contrast → Vignette
- **cinematic**: White Balance → Contrast → Saturation → Vignette → Grain
