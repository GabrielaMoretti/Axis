# VISIONFLOW - Reference Repositories

## 📚 Repositories to Study and Potentially Integrate

This document lists key open-source repositories that can serve as references, learning resources, or direct integration points for VISIONFLOW.

---

## 🎨 Professional Image Editors (Study for Architecture)

### 1. Darktable
**URL**: https://github.com/darktable-org/darktable
**Language**: C/C++
**License**: GPL-3.0

**What to Learn**:
- RAW processing pipeline
- Color management system
- Module architecture (processing nodes)
- Histogram and scopes implementation
- Non-destructive editing workflow
- LUT and color grading implementation

**Key Features**:
- Complete RAW workflow
- LAB color space processing
- Parametric masks
- OpenCL GPU acceleration
- Color profiles (ICC, LUT)

**Integration Potential**: Study the color science and processing pipeline architecture

---

### 2. RawTherapee
**URL**: https://github.com/Beep6581/RawTherapee
**Language**: C++
**License**: GPL-3.0

**What to Learn**:
- RAW demosaicing algorithms
- Detail enhancement (clarity, sharpening)
- Tone mapping
- Color correction workflows
- Batch processing architecture

**Key Features**:
- Advanced demosaicing
- Local adjustments
- Tone curves
- Film simulation
- Detail recovery

**Integration Potential**: Reference for RAW processing and tone mapping

---

### 3. GIMP
**URL**: https://github.com/GNOME/gimp
**Language**: C
**License**: GPL-3.0

**What to Learn**:
- Layer system architecture
- Selection and masking tools
- Filter and effect pipeline
- Plugin architecture
- Color management

**Integration Potential**: Study layer composition and masking systems

---

## 🔬 Computer Vision & Image Processing

### 4. OpenCV
**URL**: https://github.com/opencv/opencv
**Language**: C++
**License**: Apache-2.0

**What to Learn**:
- Image segmentation algorithms
- Edge detection (Canny, Sobel)
- Feature detection (SIFT, SURF, ORB)
- Object detection
- Image filtering

**Key Modules to Use**:
- `cv.GrabCut` - Foreground extraction
- `cv.Canny` - Edge detection
- `cv.bilateralFilter` - Edge-preserving smoothing
- `cv.watershed` - Image segmentation
- `cv.findContours` - Contour detection

**Integration**: Direct integration via opencv.js or native modules

---

### 5. MiDaS (Monocular Depth Estimation)
**URL**: https://github.com/isl-org/MiDaS
**Language**: Python (PyTorch)
**License**: MIT

**What to Learn**:
- Depth map generation from single images
- Model optimization for mobile
- Pre/post-processing for depth estimation

**Models Available**:
- MiDaS v2.1 Small (~30MB) - Good for mobile
- MiDaS v3.0 (~350MB) - Highest quality
- MiDaS v3.1 DPT (~1.3GB) - State-of-the-art

**Integration**: 
- Convert to ONNX or TensorFlow.js
- Use via API or local inference
- Consider WebAssembly compilation

---

### 6. U^2-Net (Salient Object Detection)
**URL**: https://github.com/xuebinqin/U-2-Net
**Language**: Python (PyTorch)
**License**: Apache-2.0

**What to Learn**:
- Automatic foreground/background separation
- Saliency detection
- Portrait segmentation

**Integration**:
- Convert model to TensorFlow.js or ONNX
- Use for automatic masking
- Lightweight model (~4MB) available

---

## 🌈 Color Science & Management

### 7. OpenColorIO (OCIO)
**URL**: https://github.com/AcademySoftwareFoundation/OpenColorIO
**Language**: C++
**License**: BSD-3-Clause

**What to Learn**:
- Color space transformations
- LUT application and creation
- ACES workflow implementation
- Display color management

**Key Features**:
- Industry-standard color pipeline
- 3D LUT support (Cube, VLT formats)
- GPU-accelerated transforms
- Config-based color management

**Integration**: 
- WebAssembly build for web
- Reference for LUT generation
- Study ACES implementation

---

### 8. ACES (Academy Color Encoding System)
**URL**: https://github.com/ampas/aces-dev
**Language**: Python, CTL
**License**: Academy's License

**What to Learn**:
- Professional color workflows
- Reference rendering transforms
- Look development
- Color space conversions

**Key Components**:
- ACES transforms (CTL files)
- LMT (Look Modification Transforms)
- ODT (Output Device Transforms)

**Integration**: Use ACES LUTs and implement transforms

---

### 9. Color.js
**URL**: https://github.com/LeaVerou/color.js
**Language**: JavaScript
**License**: MIT

**What to Learn**:
- Modern color space implementations
- Color difference calculations (ΔE2000)
- Gamut mapping
- CSS Color Level 4 support

**Integration**: Direct use for color science operations

---

## 🎮 WebGL & GPU Processing

### 10. Three.js
**URL**: https://github.com/mrdoob/three.js
**Language**: JavaScript
**License**: MIT

**What to Learn**:
- WebGL rendering pipeline
- Shader material system
- Post-processing effects
- Texture management

**Key Examples to Study**:
- `/examples/webgl_postprocessing_*` - Post-processing effects
- `/examples/webgl_depth_texture.html` - Depth rendering
- `/examples/webgl_shader_lensflares.html` - Lens effects

**Integration**: Core dependency for GPU-accelerated processing

---

### 11. gpu.js
**URL**: https://github.com/gpujs/gpu.js
**Language**: JavaScript
**License**: MIT

**What to Learn**:
- GPU kernel programming in JavaScript
- Parallel processing patterns
- GPU/CPU fallback strategies

**Integration**: Use for heavy image processing operations

---

### 12. WebGL Fundamentals Examples
**URL**: https://github.com/gfxfundamentals/webgl-fundamentals
**Language**: JavaScript
**License**: MIT

**What to Learn**:
- WebGL basics
- Shader programming
- Image processing with WebGL
- Texture manipulation

**Integration**: Educational resource for custom shader development

---

## 📸 RAW Processing & File Formats

### 13. LibRaw
**URL**: https://github.com/LibRaw/LibRaw
**Language**: C++
**License**: LGPL-2.1 or CDDL-1.0

**What to Learn**:
- RAW file parsing (700+ formats)
- Demosaicing algorithms
- White balance from RAW data
- Metadata extraction

**Integration**:
- Use via WebAssembly
- Reference for RAW processing pipeline

---

### 14. libheif
**URL**: https://github.com/strukturag/libheif
**Language**: C++
**License**: LGPL-3.0

**What to Learn**:
- HEIC/HEIF file format handling
- iOS image format support
- Compression and decompression

**Integration**: Via heic-convert npm package

---

### 15. ExifTool
**URL**: https://github.com/exiftool/exiftool
**Language**: Perl
**License**: GPL-1.0 or Artistic-1.0

**What to Learn**:
- Comprehensive metadata reading/writing
- Lens database
- Camera profiles

**Integration**: Reference for metadata handling (use exifr in JS)

---

## 🎬 Video Processing (Future Reference)

### 16. FFmpeg
**URL**: https://github.com/FFmpeg/FFmpeg
**Language**: C
**License**: LGPL-2.1

**What to Learn** (for future video support):
- Video decoding/encoding
- Frame extraction
- Color space conversions
- Filter graphs

**Integration**: Via ffmpeg.wasm for web-based video processing

---

## 🖼️ Web-Based Image Editors (Architecture Study)

### 17. Photopea (Closed Source - Study Only)
**URL**: https://www.photopea.com
**Note**: Not open source, but excellent for UX study

**What to Study**:
- Web-based editor performance
- UI/UX patterns
- Non-destructive workflow
- Layer system

---

### 18. Pixelmator Pro (Closed Source - Study Only)
**URL**: https://www.pixelmator.com/pro/
**Note**: Not open source

**What to Study**:
- Modern UI design
- Color adjustment workflow
- Machine learning integration
- Performance optimization

---

## 🔧 JavaScript Image Processing

### 19. Sharp
**URL**: https://github.com/lovell/sharp
**Language**: JavaScript (bindings to libvips)
**License**: Apache-2.0

**What to Learn**:
- High-performance image processing
- Format conversions
- Efficient resize algorithms

**Integration**: Core dependency for server-side processing

---

### 20. Jimp
**URL**: https://github.com/jimp-dev/jimp
**Language**: JavaScript
**License**: MIT

**What to Learn**:
- Pure JavaScript image processing
- Cross-platform compatibility
- Plugin architecture

**Integration**: Fallback for environments without native modules

---

### 21. Fabric.js
**URL**: https://github.com/fabricjs/fabric.js
**Language**: JavaScript
**License**: MIT

**What to Learn**:
- Canvas manipulation
- Object transforms
- Interactive editing tools

**Integration**: Potential use for UI canvas interactions

---

## 📱 React Native Image Processing

### 22. react-native-opencv3
**URL**: https://github.com/adamgf/react-native-opencv3
**Language**: JavaScript/Native
**License**: MIT

**What to Learn**:
- OpenCV integration in React Native
- Native module architecture
- Performance optimization

**Integration**: Direct integration for mobile OpenCV support

---

### 23. react-native-vision-camera
**URL**: https://github.com/mrousavy/react-native-vision-camera
**Language**: TypeScript/Native
**License**: MIT

**What to Learn**:
- Camera integration
- Real-time frame processing
- Native performance optimization

**Integration**: For future camera features

---

## 🎓 Educational Repositories

### 24. Image Processing Playground
**URL**: https://github.com/processing/p5.js
**Language**: JavaScript
**License**: LGPL-2.1

**What to Learn**:
- Creative coding patterns
- Visual effects
- Interactive graphics

---

### 25. WebGL Image Processing
**URL**: https://github.com/evanw/webgl-filter
**Language**: JavaScript
**License**: MIT

**What to Learn**:
- WebGL-based image filters
- Shader implementations
- Real-time processing

---

## 🔬 Academic & Research

### 26. Scikit-image
**URL**: https://github.com/scikit-image/scikit-image
**Language**: Python
**License**: BSD-3-Clause

**What to Learn**:
- Image processing algorithms
- Filter implementations
- Segmentation techniques

**Note**: Python-based, reference for algorithm implementation

---

### 27. ImageJ/Fiji
**URL**: https://github.com/imagej/ImageJ
**Language**: Java
**License**: Public Domain

**What to Learn**:
- Scientific image processing
- Plugin architecture
- Measurement and analysis tools

---

## 🛠️ Utilities & Tools

### 28. Comlink
**URL**: https://github.com/GoogleChromeLabs/comlink
**Language**: JavaScript
**License**: Apache-2.0

**What to Learn**:
- Web Worker communication
- RPC patterns
- Async processing

**Integration**: Core dependency for worker threads

---

### 29. pica
**URL**: https://github.com/nodeca/pica
**Language**: JavaScript
**License**: MIT

**What to Learn**:
- High-quality image resizing
- Canvas optimization
- Web Worker usage

**Integration**: Alternative for image resizing

---

## 📊 Priority Matrix

### Must Study (High Priority)
1. **OpenCV** - Core computer vision
2. **OpenColorIO** - Color management
3. **Darktable** - Overall architecture
4. **Three.js** - WebGL processing
5. **Color.js** - Color science

### Should Study (Medium Priority)
6. **MiDaS** - Depth estimation
7. **U^2-Net** - Segmentation
8. **RawTherapee** - RAW processing
9. **Sharp** - Performance optimization
10. **LibRaw** - RAW format support

### Nice to Study (Lower Priority)
11. **FFmpeg** - Future video support
12. **Fabric.js** - Canvas interaction
13. **WebGL Fundamentals** - Educational
14. **Scikit-image** - Algorithm reference
15. **Photopea** - UX inspiration

---

## 🚀 Integration Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Clone and study: Sharp, Jimp, exifr
- Reference: Color.js documentation
- Set up: React Native project

### Phase 2: Core Processing (Weeks 5-10)
- Integrate: OpenCV.js
- Study: Darktable color pipeline
- Reference: OpenColorIO transforms

### Phase 3: Advanced Features (Weeks 11-16)
- Integrate: Three.js for WebGL
- Study: MiDaS depth estimation
- Reference: U^2-Net for segmentation

### Phase 4: Optimization (Weeks 17-24)
- Study: gpu.js patterns
- Reference: Sharp performance techniques
- Optimize: Worker thread architecture

---

## 📝 How to Use This List

1. **Clone for Study**: Clone repos to understand architecture
2. **Reference Implementation**: Look at specific algorithms
3. **Direct Integration**: Add as dependencies when possible
4. **Inspiration**: Study UI/UX patterns
5. **Algorithm Port**: Adapt algorithms to JavaScript/TypeScript

---

## 🔗 Quick Access Links

### Essential
- [OpenCV Tutorial](https://docs.opencv.org/4.x/d5/d10/tutorial_js_root.html)
- [Three.js Examples](https://threejs.org/examples/)
- [WebGL Fundamentals](https://webglfundamentals.org/)
- [Color.js Docs](https://colorjs.io/)

### Advanced
- [ACES Documentation](https://www.oscars.org/science-technology/aces)
- [OpenColorIO Config](https://opencolorio.readthedocs.io/)
- [MiDaS Paper](https://arxiv.org/abs/1907.01341)

---

See `ARCHITECTURE.md` for how these integrate into the overall system.
