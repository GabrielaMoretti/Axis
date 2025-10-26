# VISIONFLOW - Quick Reference

## 🚀 Quick Start Commands

```bash
# Initialize project
npx create-expo-app visionflow --template expo-template-blank-typescript
cd visionflow

# Install dependencies
npm install @reduxjs/toolkit react-redux
npm install @react-navigation/native @react-navigation/stack
npm install exifr culori jimp

# Start development
npm start

# Run on specific platform
npm run ios
npm run android
npm run web
```

---

## 📦 Essential Dependencies

### Core (Must Have)
```bash
npm install react-native expo
npm install @reduxjs/toolkit react-redux redux-persist
npm install @react-navigation/native @react-navigation/stack
npm install react-native-screens react-native-safe-area-context
npm install exifr culori
```

### Image Processing (Recommended)
```bash
npm install jimp                    # Pure JS image processing
npm install sharp                   # High-performance (Node.js)
npm install opencv.js               # Computer vision
```

### WebGL/GPU (For Advanced Features)
```bash
npm install three @react-three/fiber
npm install gpu.js
npm install gl-matrix
```

### Utilities
```bash
npm install comlink                 # Web Workers
npm install react-native-vector-icons
npm install react-native-paper      # UI components
```

---

## 🏗️ Project Setup Checklist

- [ ] Create Expo project with TypeScript template
- [ ] Set up folder structure (src/core, src/ui, etc.)
- [ ] Configure tsconfig.json with path aliases
- [ ] Set up Redux store with persistence
- [ ] Configure React Navigation
- [ ] Create .gitignore file
- [ ] Add ESLint and Prettier
- [ ] Set up testing framework (Jest)
- [ ] Create initial UI shell

---

## 📁 Folder Structure (Essential)

```
visionflow/
├── src/
│   ├── core/              # Image processing logic
│   ├── ui/                # React components
│   ├── state/             # Redux store
│   └── types/             # TypeScript types
├── assets/                # Static files
├── tests/                 # Test files
└── docs/                  # Documentation
```

---

## 🔑 Key TypeScript Types

```typescript
// Image data
interface ImageData {
  data: Uint8ClampedArray;
  width: number;
  height: number;
  channels: number;
}

// EXIF metadata
interface EXIFData {
  make?: string;
  model?: string;
  lens?: string;
  focalLength?: number;
  aperture?: number;
  iso?: number;
}

// Color temperature
interface ColorTemperature {
  kelvin: number;
  tint: number;
}

// Curve point
interface CurvePoint {
  x: number;  // 0-1
  y: number;  // 0-1
}

// Layer
interface Layer {
  id: string;
  name: string;
  type: LayerType;
  visible: boolean;
  opacity: number;
  mask?: ImageData;
}
```

---

## 🎨 Common Operations

### Load Image
```typescript
import Jimp from 'jimp';

const image = await Jimp.read('photo.jpg');
const imageData = {
  data: image.bitmap.data,
  width: image.bitmap.width,
  height: image.bitmap.height,
  channels: 4
};
```

### Extract EXIF
```typescript
import exifr from 'exifr';

const exif = await exifr.parse('photo.jpg', {
  tiff: true,
  gps: true
});
```

### White Balance
```typescript
function applyWhiteBalance(
  imageData: ImageData,
  kelvin: number
): ImageData {
  const multiplier = kelvinToRGB(kelvin);
  // Apply multiplier to RGB channels
}
```

### Histogram
```typescript
function calculateHistogram(imageData: ImageData) {
  const histogram = {
    red: new Uint32Array(256),
    green: new Uint32Array(256),
    blue: new Uint32Array(256)
  };
  
  for (let i = 0; i < imageData.data.length; i += 4) {
    histogram.red[imageData.data[i]]++;
    histogram.green[imageData.data[i + 1]]++;
    histogram.blue[imageData.data[i + 2]]++;
  }
  
  return histogram;
}
```

### Apply Curve
```typescript
function applyCurve(
  imageData: ImageData,
  points: CurvePoint[]
): ImageData {
  const lut = generateLUT(points);
  const result = new ImageData(
    new Uint8ClampedArray(imageData.data),
    imageData.width,
    imageData.height
  );
  
  for (let i = 0; i < result.data.length; i += 4) {
    result.data[i] = lut[result.data[i]];
    result.data[i + 1] = lut[result.data[i + 1]];
    result.data[i + 2] = lut[result.data[i + 2]];
  }
  
  return result;
}
```

---

## 🎯 Redux Setup

```typescript
// store.ts
import { configureStore } from '@reduxjs/toolkit';
import imageReducer from './slices/imageSlice';

export const store = configureStore({
  reducer: {
    image: imageReducer
  }
});

// slices/imageSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

const imageSlice = createSlice({
  name: 'image',
  initialState: {
    current: null,
    metadata: null
  },
  reducers: {
    setImage: (state, action: PayloadAction<ImageData>) => {
      state.current = action.payload;
    }
  }
});
```

---

## 🖼️ UI Components (Minimal)

```typescript
// ImageCanvas.tsx
import React from 'react';
import { View } from 'react-native';

export const ImageCanvas: React.FC<{ imageData: ImageData }> = ({ imageData }) => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  
  useEffect(() => {
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      ctx?.putImageData(imageData, 0, 0);
    }
  }, [imageData]);
  
  return <canvas ref={canvasRef} />;
};

// SliderControl.tsx
export const SliderControl: React.FC<{
  label: string;
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
}> = ({ label, value, onChange, min = 0, max = 100 }) => {
  return (
    <View>
      <Text>{label}: {value}</Text>
      <Slider
        value={value}
        onValueChange={onChange}
        minimumValue={min}
        maximumValue={max}
      />
    </View>
  );
};
```

---

## 🔧 WebGL Setup (Basic)

```typescript
import * as THREE from 'three';

// Create scene
const scene = new THREE.Scene();
const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0, 1);
const renderer = new THREE.WebGLRenderer();

// Create shader material
const material = new THREE.ShaderMaterial({
  uniforms: {
    tDiffuse: { value: texture }
  },
  vertexShader: `
    varying vec2 vUv;
    void main() {
      vUv = uv;
      gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
    }
  `,
  fragmentShader: `
    uniform sampler2D tDiffuse;
    varying vec2 vUv;
    void main() {
      gl_FragColor = texture2D(tDiffuse, vUv);
    }
  `
});

// Render
const mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
renderer.render(scene, camera);
```

---

## 🧪 Testing Setup

```typescript
// imageProcessor.test.ts
import { calculateHistogram } from '../core/analysis/histogram';

describe('Histogram', () => {
  it('should calculate correctly', () => {
    const imageData = createTestImage();
    const histogram = calculateHistogram(imageData);
    expect(histogram.red[255]).toBeGreaterThan(0);
  });
});
```

---

## 🚀 Performance Tips

### 1. Use Web Workers
```typescript
import { wrap } from 'comlink';

const worker = new Worker('./processor.worker.ts');
const api = wrap(worker);
const result = await api.processImage(imageData);
```

### 2. Progressive Rendering
```typescript
// Render low-res preview first
const preview = resizeImage(imageData, 0.25);
renderPreview(preview);

// Then render full resolution
const full = processImage(imageData);
renderFull(full);
```

### 3. Canvas Optimization
```typescript
// Use offscreen canvas for processing
const offscreen = new OffscreenCanvas(width, height);
const ctx = offscreen.getContext('2d');
// Process in offscreen, then transfer
```

### 4. Batch Operations
```typescript
// Instead of multiple passes
imageData = whiteBalance(imageData);
imageData = curves(imageData);
imageData = sharpen(imageData);

// Combine into one pass
imageData = processAll(imageData, {
  whiteBalance: wb,
  curves: curve,
  sharpen: amount
});
```

---

## 📊 Common Algorithms

### Bilateral Filter (Edge-Preserving)
```typescript
function bilateralFilter(
  imageData: ImageData,
  spatialSigma: number,
  rangeSigma: number
): ImageData {
  // Implementation
}
```

### Gaussian Blur
```typescript
function gaussianBlur(
  imageData: ImageData,
  radius: number
): ImageData {
  const kernel = createGaussianKernel(radius);
  return convolve(imageData, kernel);
}
```

### Unsharp Mask
```typescript
function unsharpMask(
  imageData: ImageData,
  amount: number,
  radius: number
): ImageData {
  const blurred = gaussianBlur(imageData, radius);
  return blend(imageData, blurred, amount);
}
```

---

## 🔗 Useful Resources

### Documentation
- [OpenCV.js Docs](https://docs.opencv.org/4.x/d5/d10/tutorial_js_root.html)
- [Three.js Examples](https://threejs.org/examples/)
- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [Redux Toolkit](https://redux-toolkit.js.org/)

### Tutorials
- [WebGL Fundamentals](https://webglfundamentals.org/)
- [Color Science](https://www.color.org/)
- [Image Processing](https://www.imageprocessingplace.com/)

### Tools
- [LUT Generator](https://www.colour-science.org/)
- [Color Picker](https://colorjs.io/apps/picker/)
- [Shader Editor](https://thebookofshaders.com/edit.php)

---

## 🐛 Common Issues & Solutions

### Issue: Image too large for canvas
```typescript
// Solution: Resize for display
const maxDimension = 2048;
const scale = Math.min(1, maxDimension / Math.max(width, height));
const displayWidth = width * scale;
const displayHeight = height * scale;
```

### Issue: Processing too slow
```typescript
// Solution: Use Web Workers
const worker = new Worker('./processor.worker.ts');
worker.postMessage({ imageData, operation: 'blur' });
```

### Issue: Memory errors with large images
```typescript
// Solution: Process in tiles
function processTiles(imageData: ImageData) {
  const tileSize = 512;
  for (let y = 0; y < height; y += tileSize) {
    for (let x = 0; x < width; x += tileSize) {
      const tile = extractTile(imageData, x, y, tileSize);
      processTile(tile);
    }
  }
}
```

---

## 🎯 Next Steps

1. ✅ Read ARCHITECTURE.md
2. ✅ Review PROJECT_STRUCTURE.md
3. 📝 Follow IMPLEMENTATION_GUIDE.md
4. 🔧 Check LIBRARIES.md for integration details
5. 📚 Study REFERENCE_REPOSITORIES.md
6. 🚀 Start coding!

---

**Happy coding! 🎨**
