# 🎥 VISIONFLOW

**Professional Image Editor by Physical Control and Intuitive Flow**

> Transform mobile captures into cinematographic quality images through physical-based optical processing — without AI generation.

---

## 📋 Overview

**VISIONFLOW** is a professional post-production image editor designed for contemporary creators, photographers, visual artists, and producers. It bridges the gap between professional studio pipelines and accessible mobile editing.

### Core Philosophy

> "The image is not recreated — it is revealed."

VISIONFLOW reads, separates, calibrates, and refines the original photograph while respecting its optical integrity. Unlike AI-driven editors that regenerate images, VISIONFLOW manipulates the actual physical properties of light, color, and lens characteristics.

---

## ✨ Key Features

### 🔬 **Technical Analysis**
- Automatic EXIF metadata extraction (camera, lens, settings)
- Histogram and light map generation
- Image structure analysis (foreground, background, lighting)

### 🎨 **Physical-Based Processing**
- **Layer Separation**: Non-destructive masks for foreground, depth, materials
- **Colorimetry**: Perceptual color correction using LAB/LCH spaces
- **Depth Control**: Physically accurate bokeh simulation
- **Lens Simulation**: Real optical characteristics (vignette, flare, distortion)
- **Texture Refinement**: Frequency separation, grain, microcontrast

### 🎬 **Professional Workflow**
- ACES-compatible color pipeline
- 3D LUT generation and export
- Non-destructive editing
- RAW format support (CR2, NEF, DNG, etc.)
- HEIC/HEIF support

---

## 🗂️ Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture and technology stack
- **[PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md)** - Folder organization and module design
- **[IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md)** - Step-by-step implementation instructions
- **[LIBRARIES.md](./LIBRARIES.md)** - Detailed library integration guide
- **[REFERENCE_REPOSITORIES.md](./REFERENCE_REPOSITORIES.md)** - Open-source references to study

---

## 🛠️ Technology Stack

### Frontend
- **React Native** + **Expo** - Cross-platform (iOS, Android, Web, Desktop)
- **Redux Toolkit** - State management
- **React Navigation** - Navigation

### Image Processing
- **OpenCV.js** - Computer vision and segmentation
- **Sharp** / **Jimp** - High-performance image manipulation
- **exifr** - EXIF metadata extraction
- **Culori** / **Color.js** - Color science and conversions

### GPU Acceleration
- **Three.js** - WebGL-based processing
- **gpu.js** - GPU computing
- **Custom GLSL shaders** - Real-time effects

### Advanced Features
- **libraw** - RAW image processing
- **OpenColorIO** - Professional color management
- **MiDaS** (optional) - Depth estimation
- **U^2-Net** (optional) - Object segmentation

---

## 🚀 Quick Start

### Prerequisites

```bash
node >= 18.0.0
npm >= 9.0.0
expo-cli
```

### Installation

```bash
# Clone the repository
git clone https://github.com/GabrielaMoretti/Axis.git
cd Axis

# Initialize the project (see IMPLEMENTATION_GUIDE.md for detailed steps)
npx create-expo-app visionflow --template expo-template-blank-typescript

# Install dependencies
npm install

# Start development server
npm start
```

### Development

```bash
# Run on iOS
npm run ios

# Run on Android
npm run android

# Run on Web
npm run web

# Run tests
npm test

# Lint code
npm run lint
```

---

## 📐 Project Structure

```
visionflow/
├── src/
│   ├── core/              # Image processing modules
│   │   ├── analysis/      # EXIF, histogram, structure
│   │   ├── separation/    # Layer separation engine
│   │   ├── color/         # Colorimetry and grading
│   │   ├── depth/         # Depth control and bokeh
│   │   ├── lens/          # Lens simulation
│   │   ├── texture/       # Refinement and grain
│   │   └── export/        # LUT generation
│   ├── processing/        # WebGL/GPU processing
│   ├── ui/                # React components
│   ├── state/             # Redux state management
│   └── utils/             # Utilities
├── assets/                # LUTs, lens profiles
├── tests/                 # Unit and integration tests
└── docs/                  # Additional documentation
```

---

## 🎯 Roadmap

### Phase 1: Foundation (Weeks 1-4) ✅
- [x] Architecture documentation
- [ ] Project initialization
- [ ] Basic UI shell
- [ ] Image import (JPEG, PNG)
- [ ] EXIF metadata reading

### Phase 2: Core Processing (Weeks 5-10)
- [ ] Histogram and analysis tools
- [ ] Color correction (curves, white balance)
- [ ] Layer separation prototype
- [ ] RAW and HEIC support

### Phase 3: Advanced Features (Weeks 11-16)
- [ ] Depth map generation
- [ ] Bokeh simulation
- [ ] Lens profiles
- [ ] Texture refinement

### Phase 4: Look Builder (Weeks 17-20)
- [ ] LUT generation
- [ ] Color grading tools
- [ ] Preset system
- [ ] ACES integration

### Phase 5: Polish (Weeks 21-24)
- [ ] Performance optimization
- [ ] WebAssembly compilation
- [ ] UI/UX refinement
- [ ] Testing and bug fixes

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

### Development Guidelines

1. Follow the TypeScript style guide
2. Write tests for new features
3. Document public APIs
4. Keep modules focused and single-purpose
5. Optimize for performance

---

## 📖 Core Concepts

### Non-Destructive Editing
All edits are applied as parametric adjustments that can be modified or removed at any time without degrading the original image.

### Physical-Based Processing
Instead of applying digital filters, VISIONFLOW simulates the physics of light, lenses, and color to achieve natural, professional results.

### Layer Separation
The engine analyzes the image structure and creates separate layers for foreground, background, depth, materials, and illumination — enabling precise, isolated adjustments.

### Colorimetry
Uses perceptual color spaces (LAB, LCH, OKLCH) and industry-standard tools (ΔE2000, ACES) to ensure accurate color representation across devices.

---

## 🎓 Learning Resources

- [Image Processing Basics](./docs/learning/image-processing.md)
- [Color Science Fundamentals](./docs/learning/color-science.md)
- [WebGL for Image Processing](./docs/learning/webgl-guide.md)
- [RAW Processing Pipeline](./docs/learning/raw-processing.md)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

VISIONFLOW builds upon the work of many open-source projects:
- OpenCV - Computer vision
- Three.js - WebGL rendering
- Color.js - Color science
- The Academy (ACES) - Color management standards
- And many more (see [REFERENCE_REPOSITORIES.md](./REFERENCE_REPOSITORIES.md))

---

## 📬 Contact

- **Issues**: [GitHub Issues](https://github.com/GabrielaMoretti/Axis/issues)
- **Discussions**: [GitHub Discussions](https://github.com/GabrielaMoretti/Axis/discussions)

---

## 🌟 Support

If you find this project useful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting features
- 🤝 Contributing code

---

**Built with ❤️ for creators who demand professional quality**