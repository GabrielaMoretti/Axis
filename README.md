# VISIONFLOW

**Professional Image Editor with Optical Integrity Preservation**

VISIONFLOW é um editor de imagem profissional que preserva a integridade óptica das fotos. Voltado a criadores e estúdios, oferece um pipeline modular e reversível que une precisão técnica e fluidez no workflow de pós-produção.

## ✨ Core Features

### 1. **Import and Technical Analysis**
- Comprehensive image import with validation
- Detailed technical property analysis
- EXIF metadata extraction
- Sharpness and quality metrics
- Color channel analysis with histograms

### 2. **Layer Separation**
- Multi-layer image editing
- Blend modes (normal, multiply, screen, overlay)
- Layer opacity control
- Non-destructive editing workflow

### 3. **Physical Color Correction**
- White balance with temperature and tint controls
- Exposure adjustment with stops
- Contrast and saturation enhancement
- HSL (Hue, Saturation, Lightness) adjustments
- Tone curves for precise color grading

### 4. **Focus and Depth Control**
- Gaussian blur for depth simulation
- Depth of field effects with focus points
- Radial blur for motion effects
- Tilt-shift (miniature fake) effects
- Advanced sharpening with unsharp mask

### 5. **Lens Simulation**
- Vignette effects
- Chromatic aberration simulation
- Barrel and pincushion distortion
- Bokeh effects with shaped highlights
- Aperture simulation (f-stop control)

### 6. **Texture Refinement**
- Intelligent noise reduction
- Detail enhancement
- Film grain addition
- Skin smoothing for portraits
- Frequency separation (low/high)
- Clarity enhancement (midtone contrast)

### 7. **Visual Style Creation**
- Predefined styles (cinematic, vintage, dramatic, soft, high-key, low-key)
- Custom style creation
- LUT (Look-Up Table) support
- Color grading with shadows/midtones/highlights
- Style intensity control

## 🏗️ Architecture

VISIONFLOW is built on a **modular and reversible pipeline architecture**:

- **Modular Design**: Each feature is implemented as an independent module
- **Reversible Pipeline**: Track all operations with the ability to undo or modify
- **Non-Destructive Workflow**: Original images remain unchanged
- **Layer System**: Work with multiple layers and blend modes
- **Snapshot System**: Save intermediate results at any pipeline stage

## 📦 Installation

### Requirements
- Python 3.8 or higher
- PIL/Pillow for image processing
- NumPy for numerical operations
- SciPy for advanced filtering

### Install from source

```bash
# Clone the repository
git clone https://github.com/GabrielaMoretti/Axis.git
cd Axis

# Install dependencies
pip install -r requirements.txt

# Install VISIONFLOW
pip install -e .
```

## 🚀 Quick Start

### Command-Line Interface

#### 1. Analyze an Image

```bash
visionflow analyze input.jpg
```

This provides comprehensive technical analysis including:
- Dimensions and aspect ratio
- Color space and format
- Brightness statistics
- Channel analysis
- Sharpness metrics
- EXIF data

#### 2. Process an Image

Apply individual operations:

```bash
# Color correction
visionflow process input.jpg --temperature 0.2 --contrast 1.2 --saturation 1.1 -o output.jpg

# Add artistic effects
visionflow process input.jpg --vignette 0.3 --grain 0.1 --clarity 0.5 -o output.jpg

# Focus control
visionflow process input.jpg --sharpen 1.5 -o output.jpg
```

#### 3. Apply Style Presets

```bash
# List available styles
visionflow list-styles

# Apply a style
visionflow process input.jpg --style cinematic --style-intensity 0.8 -o output.jpg
```

#### 4. Use Pipeline Presets

```bash
# Portrait retouching
visionflow pipeline input.jpg portrait -o portrait_output.jpg

# Landscape enhancement
visionflow pipeline input.jpg landscape -o landscape_output.jpg

# Cinematic look
visionflow pipeline input.jpg cinematic -o cinematic_output.jpg
```

### Python API

```python
from visionflow.core.image import VisionFlowImage
from visionflow.modules import ColorCorrector, StyleCreator, TextureRefiner
from visionflow.pipeline import Pipeline

# Load and analyze image
img = VisionFlowImage(image_path="input.jpg")
metadata = img.get_metadata()
print(f"Image size: {metadata['width']}x{metadata['height']}")

# Apply operations
from PIL import Image
image = Image.open("input.jpg")

# Color correction
image = ColorCorrector.adjust_white_balance(image, temperature=0.1, tint=-0.05)
image = ColorCorrector.adjust_contrast(image, contrast=1.2)

# Apply style
style_creator = StyleCreator()
image = style_creator.apply_style(image, "cinematic", intensity=0.8)

# Save result
image.save("output.jpg")
```

### Building Custom Pipelines

```python
from visionflow.pipeline import Pipeline
from visionflow.modules import ColorCorrector, LensSimulator, TextureRefiner

# Create custom pipeline
pipeline = Pipeline("My Custom Workflow")

# Add operations
pipeline.add_operation("White Balance", ColorCorrector.adjust_white_balance, 
                      {'temperature': 0.15, 'tint': 0.0})
pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, 
                      {'contrast': 1.25})
pipeline.add_operation("Clarity", TextureRefiner.apply_clarity, 
                      {'amount': 0.6})
pipeline.add_operation("Vignette", LensSimulator.apply_vignette, 
                      {'strength': 0.25})

# Execute pipeline
from PIL import Image
input_image = Image.open("input.jpg")
result = pipeline.execute(input_image, save_snapshots=True)

# Get intermediate results
intermediate = pipeline.get_snapshot(2)  # After second operation

# Save result
result.save("output.jpg")
```

## 📚 Available Operations

### Color Correction
- `adjust_white_balance(temperature, tint)` - White balance control
- `adjust_exposure(exposure)` - Exposure in stops
- `adjust_contrast(contrast)` - Contrast adjustment
- `adjust_saturation(saturation)` - Saturation control
- `adjust_hsl(hue, saturation, lightness)` - HSL adjustments
- `apply_curves(curve_points)` - Tone curves

### Focus and Depth
- `apply_gaussian_blur(radius)` - Blur effect
- `apply_depth_of_field(focus_point, focus_range, max_blur)` - DOF simulation
- `apply_radial_blur(center, strength)` - Radial/zoom blur
- `apply_tilt_shift(focus_line_y, focus_width, max_blur)` - Tilt-shift effect
- `sharpen(strength)` - Sharpening

### Lens Simulation
- `apply_vignette(strength, center)` - Vignette effect
- `apply_chromatic_aberration(strength)` - Color fringing
- `apply_lens_distortion(distortion)` - Barrel/pincushion distortion
- `apply_bokeh(blur_amount, shape)` - Bokeh effect
- `simulate_aperture(f_stop)` - Aperture simulation

### Texture Refinement
- `denoise(strength)` - Noise reduction
- `enhance_details(strength)` - Detail enhancement
- `apply_grain(intensity, size)` - Film grain
- `smooth_skin(mask, smoothness)` - Portrait smoothing
- `adjust_texture_frequency(low_freq, high_freq)` - Frequency separation
- `apply_clarity(amount)` - Clarity/midtone contrast

### Visual Styles
- `apply_style(style_name, intensity)` - Apply preset style
- `create_custom_style(name, parameters)` - Create custom style
- `apply_lut(lut_file/array)` - Apply LUT
- `create_color_grade(shadows, midtones, highlights)` - Color grading

## 🎨 Available Styles

- **cinematic**: Warm tones, controlled contrast, subtle vignette
- **vintage**: Warm yellows, faded colors, heavy grain
- **dramatic**: High contrast, boosted saturation, clarity
- **soft**: Gentle tones, reduced contrast, smooth
- **high_key**: Bright, airy, low contrast
- **low_key**: Dark, moody, high contrast

## 🔧 Pipeline Presets

### Portrait Retouch
1. Denoise (strength: 1.5)
2. Smooth Skin (smoothness: 0.4)
3. Enhance Details (strength: 0.5)
4. Color Correction (saturation: 1.1)

### Landscape Enhancement
1. Clarity (amount: 0.7)
2. Saturation (1.2)
3. Contrast (1.15)
4. Vignette (0.2)

### Cinematic Look
1. White Balance (temp: 0.1, tint: -0.05)
2. Contrast (1.2)
3. Saturation (0.9)
4. Vignette (0.3)
5. Grain (0.05)

## 🎯 Use Cases

- **Professional Photography**: Post-processing workflow for studios
- **Portrait Retouching**: Skin smoothing, blemish removal, color correction
- **Landscape Photography**: Enhance details, control atmosphere
- **Cinematic Grading**: Film-like color grading and visual styles
- **Product Photography**: Precise color accuracy and detail enhancement
- **Creative Projects**: Artistic effects and style creation

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with:
- [Pillow (PIL)](https://python-pillow.org/) - Image processing
- [NumPy](https://numpy.org/) - Numerical computing
- [SciPy](https://scipy.org/) - Scientific computing

---

**VISIONFLOW** - Preserving optical integrity with professional precision.