# VISIONFLOW - Implementation Guide

## 🚀 Getting Started

This guide provides step-by-step instructions to implement VISIONFLOW from scratch.

---

## Phase 1: Project Initialization

### Step 1: Initialize React Native + Expo Project

```bash
# Install Expo CLI globally
npm install -g expo-cli

# Create new Expo project
npx create-expo-app visionflow --template expo-template-blank-typescript

cd visionflow

# Install core dependencies
npm install @reduxjs/toolkit react-redux redux-persist
npm install @react-navigation/native @react-navigation/stack
npm install react-native-screens react-native-safe-area-context
npm install react-native-gesture-handler react-native-reanimated

# Install image processing libraries
npm install exifr culori
npm install jimp

# Install UI components
npm install react-native-paper
npm install react-native-vector-icons

# Development dependencies
npm install --save-dev @types/react @types/react-native
npm install --save-dev eslint prettier
npm install --save-dev jest @testing-library/react-native
```

### Step 2: Configure TypeScript

Create `tsconfig.json`:

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@core/*": ["src/core/*"],
      "@processing/*": ["src/processing/*"],
      "@io/*": ["src/io/*"],
      "@state/*": ["src/state/*"],
      "@ui/*": ["src/ui/*"],
      "@utils/*": ["src/utils/*"],
      "@types/*": ["src/types/*"],
      "@constants/*": ["src/constants/*"]
    }
  }
}
```

Update `package.json` to include path aliases for Metro bundler:

```json
{
  "expo": {
    "packagerOpts": {
      "config": "metro.config.js"
    }
  }
}
```

### Step 3: Create Folder Structure

```bash
mkdir -p src/{core,processing,io,state,ui,utils,types,constants}
mkdir -p src/core/{analysis,separation,color,depth,lens,texture,export}
mkdir -p src/processing/{shaders,webgl,workers}
mkdir -p src/ui/{screens,components,navigation,theme}
mkdir -p src/state/{slices,middleware}
mkdir -p assets/{luts,lens-profiles,icons}
mkdir -p tests/{unit,integration,e2e}
```

---

## Phase 2: Core Type Definitions

### Step 1: Create Base Types

Create `src/types/image.types.ts`:

```typescript
export interface ImageMetadata {
  width: number;
  height: number;
  format: string;
  colorSpace: string;
  exif?: EXIFData;
}

export interface EXIFData {
  make?: string;
  model?: string;
  lens?: string;
  focalLength?: number;
  aperture?: number;
  iso?: number;
  shutterSpeed?: string;
  dateTime?: string;
  gps?: GPSData;
}

export interface GPSData {
  latitude: number;
  longitude: number;
  altitude?: number;
}

export interface ImageData {
  data: Uint8ClampedArray;
  width: number;
  height: number;
  channels: number;
}

export interface ProcessingResult {
  imageData: ImageData;
  processingTime: number;
  metadata?: Record<string, any>;
}
```

Create `src/types/layer.types.ts`:

```typescript
export type LayerType = 
  | 'foreground' 
  | 'background' 
  | 'depth' 
  | 'material' 
  | 'illumination';

export interface Layer {
  id: string;
  name: string;
  type: LayerType;
  visible: boolean;
  opacity: number;
  mask?: ImageData;
  blendMode: BlendMode;
}

export type BlendMode = 
  | 'normal' 
  | 'multiply' 
  | 'screen' 
  | 'overlay' 
  | 'soft-light';

export interface LayerSeparationResult {
  foregroundMask: ImageData;
  depthMap: Float32Array;
  materialMap: MaterialType[];
  illuminationMap: Float32Array;
}

export type MaterialType = 
  | 'skin' 
  | 'fabric' 
  | 'metal' 
  | 'glass' 
  | 'plastic' 
  | 'organic' 
  | 'unknown';
```

Create `src/types/color.types.ts`:

```typescript
export interface ColorSpace {
  name: 'sRGB' | 'AdobeRGB' | 'ProPhotoRGB' | 'ACES' | 'LAB' | 'LCH';
  primaries?: [number, number][];
  whitePoint?: [number, number];
}

export interface ColorTemperature {
  kelvin: number;
  tint: number;
}

export interface CurvePoint {
  x: number;
  y: number;
}

export interface TonalCurve {
  points: CurvePoint[];
  channel: 'RGB' | 'R' | 'G' | 'B' | 'L';
}

export interface ColorGrading {
  shadows: HSL;
  midtones: HSL;
  highlights: HSL;
  globalSaturation: number;
  vibrance: number;
}

export interface HSL {
  h: number; // 0-360
  s: number; // 0-100
  l: number; // 0-100
}

export interface LUT3D {
  size: number; // typically 33 or 64
  data: Float32Array;
  format: 'cube' | 'vlt';
}
```

---

## Phase 3: State Management

### Step 1: Create Redux Store

Create `src/state/store.ts`:

```typescript
import { configureStore } from '@reduxjs/toolkit';
import { 
  persistStore, 
  persistReducer,
  FLUSH,
  REHYDRATE,
  PAUSE,
  PERSIST,
  PURGE,
  REGISTER,
} from 'redux-persist';
import AsyncStorage from '@react-native-async-storage/async-storage';

import imageReducer from './slices/imageSlice';
import editorReducer from './slices/editorSlice';
import layersReducer from './slices/layersSlice';
import historyReducer from './slices/historySlice';
import settingsReducer from './slices/settingsSlice';

const persistConfig = {
  key: 'root',
  storage: AsyncStorage,
  whitelist: ['settings'], // Only persist settings
};

const persistedSettingsReducer = persistReducer(persistConfig, settingsReducer);

export const store = configureStore({
  reducer: {
    image: imageReducer,
    editor: editorReducer,
    layers: layersReducer,
    history: historyReducer,
    settings: persistedSettingsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
      },
    }),
});

export const persistor = persistStore(store);

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### Step 2: Create Image Slice

Create `src/state/slices/imageSlice.ts`:

```typescript
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { ImageMetadata, ImageData } from '@types/image.types';

interface ImageState {
  original: ImageData | null;
  current: ImageData | null;
  preview: ImageData | null;
  metadata: ImageMetadata | null;
  isProcessing: boolean;
  error: string | null;
}

const initialState: ImageState = {
  original: null,
  current: null,
  preview: null,
  metadata: null,
  isProcessing: false,
  error: null,
};

const imageSlice = createSlice({
  name: 'image',
  initialState,
  reducers: {
    setOriginalImage: (state, action: PayloadAction<ImageData>) => {
      state.original = action.payload;
      state.current = action.payload;
      state.error = null;
    },
    setCurrentImage: (state, action: PayloadAction<ImageData>) => {
      state.current = action.payload;
    },
    setPreviewImage: (state, action: PayloadAction<ImageData>) => {
      state.preview = action.payload;
    },
    setMetadata: (state, action: PayloadAction<ImageMetadata>) => {
      state.metadata = action.payload;
    },
    setProcessing: (state, action: PayloadAction<boolean>) => {
      state.isProcessing = action.payload;
    },
    setError: (state, action: PayloadAction<string>) => {
      state.error = action.payload;
      state.isProcessing = false;
    },
    resetImage: (state) => {
      return initialState;
    },
  },
});

export const {
  setOriginalImage,
  setCurrentImage,
  setPreviewImage,
  setMetadata,
  setProcessing,
  setError,
  resetImage,
} = imageSlice.actions;

export default imageSlice.reducer;
```

---

## Phase 4: Core Modules - Image Analysis

### Step 1: EXIF Reader

Create `src/core/analysis/exifReader.ts`:

```typescript
import exifr from 'exifr';
import { EXIFData } from '@types/image.types';

export async function extractEXIF(imagePath: string): Promise<EXIFData | null> {
  try {
    const exifData = await exifr.parse(imagePath, {
      tiff: true,
      xmp: true,
      icc: true,
      gps: true,
    });

    if (!exifData) return null;

    return {
      make: exifData.Make,
      model: exifData.Model,
      lens: exifData.LensModel || exifData.Lens,
      focalLength: exifData.FocalLength,
      aperture: exifData.FNumber || exifData.ApertureValue,
      iso: exifData.ISO,
      shutterSpeed: exifData.ExposureTime,
      dateTime: exifData.DateTimeOriginal || exifData.DateTime,
      gps: exifData.latitude && exifData.longitude ? {
        latitude: exifData.latitude,
        longitude: exifData.longitude,
        altitude: exifData.GPSAltitude,
      } : undefined,
    };
  } catch (error) {
    console.error('Error extracting EXIF:', error);
    return null;
  }
}
```

### Step 2: Histogram Analyzer

Create `src/core/analysis/histogramAnalyzer.ts`:

```typescript
import { ImageData } from '@types/image.types';

export interface Histogram {
  red: Uint32Array;
  green: Uint32Array;
  blue: Uint32Array;
  luminance: Uint32Array;
}

export function calculateHistogram(imageData: ImageData): Histogram {
  const histogram: Histogram = {
    red: new Uint32Array(256),
    green: new Uint32Array(256),
    blue: new Uint32Array(256),
    luminance: new Uint32Array(256),
  };

  const { data, width, height } = imageData;
  const pixelCount = width * height;

  for (let i = 0; i < pixelCount * 4; i += 4) {
    const r = data[i];
    const g = data[i + 1];
    const b = data[i + 2];

    histogram.red[r]++;
    histogram.green[g]++;
    histogram.blue[b]++;

    // Calculate luminance using Rec. 709 coefficients
    const luma = Math.round(0.2126 * r + 0.7152 * g + 0.0722 * b);
    histogram.luminance[luma]++;
  }

  return histogram;
}

export function analyzeHistogram(histogram: Histogram) {
  const stats = {
    red: calculateChannelStats(histogram.red),
    green: calculateChannelStats(histogram.green),
    blue: calculateChannelStats(histogram.blue),
    luminance: calculateChannelStats(histogram.luminance),
  };

  return {
    stats,
    isClipped: detectClipping(histogram),
    dynamicRange: calculateDynamicRange(histogram.luminance),
  };
}

function calculateChannelStats(channel: Uint32Array) {
  let sum = 0;
  let count = 0;

  for (let i = 0; i < 256; i++) {
    sum += i * channel[i];
    count += channel[i];
  }

  const mean = sum / count;

  // Calculate standard deviation
  let variance = 0;
  for (let i = 0; i < 256; i++) {
    variance += channel[i] * Math.pow(i - mean, 2);
  }
  const stdDev = Math.sqrt(variance / count);

  return { mean, stdDev };
}

function detectClipping(histogram: Histogram): boolean {
  const threshold = 0.01; // 1% of pixels
  const totalPixels = Array.from(histogram.luminance).reduce((a, b) => a + b, 0);
  
  const blackClipping = histogram.luminance[0] / totalPixels > threshold;
  const whiteClipping = histogram.luminance[255] / totalPixels > threshold;

  return blackClipping || whiteClipping;
}

function calculateDynamicRange(luminance: Uint32Array): number {
  let min = 0;
  let max = 255;

  // Find first non-zero bin
  for (let i = 0; i < 256; i++) {
    if (luminance[i] > 0) {
      min = i;
      break;
    }
  }

  // Find last non-zero bin
  for (let i = 255; i >= 0; i--) {
    if (luminance[i] > 0) {
      max = i;
      break;
    }
  }

  return max - min;
}
```

---

## Phase 5: Color Correction Module

### Step 1: White Balance

Create `src/core/color/whiteBalance.ts`:

```typescript
import { ImageData, ColorTemperature } from '@types/image.types';

export function autoWhiteBalance(imageData: ImageData): ColorTemperature {
  const { data, width, height } = imageData;
  const pixelCount = width * height;

  let sumR = 0;
  let sumG = 0;
  let sumB = 0;

  // Calculate average color
  for (let i = 0; i < pixelCount * 4; i += 4) {
    sumR += data[i];
    sumG += data[i + 1];
    sumB += data[i + 2];
  }

  const avgR = sumR / pixelCount;
  const avgG = sumG / pixelCount;
  const avgB = sumB / pixelCount;

  // Calculate color temperature (simplified)
  const kelvin = estimateColorTemperature(avgR, avgG, avgB);
  const tint = calculateTint(avgR, avgG, avgB);

  return { kelvin, tint };
}

export function applyWhiteBalance(
  imageData: ImageData,
  temperature: ColorTemperature
): ImageData {
  const result = new ImageData(
    new Uint8ClampedArray(imageData.data),
    imageData.width,
    imageData.height
  );

  const { kelvin, tint } = temperature;
  const multipliers = getColorMultipliers(kelvin, tint);

  for (let i = 0; i < result.data.length; i += 4) {
    result.data[i] = clamp(result.data[i] * multipliers.r);
    result.data[i + 1] = clamp(result.data[i + 1] * multipliers.g);
    result.data[i + 2] = clamp(result.data[i + 2] * multipliers.b);
  }

  return result;
}

function estimateColorTemperature(r: number, g: number, b: number): number {
  // Simplified color temperature estimation
  // Real implementation would use Bradford chromatic adaptation
  const ratio = b / r;
  return Math.round(5500 + (ratio - 1) * 2000);
}

function calculateTint(r: number, g: number, b: number): number {
  return (g - (r + b) / 2) / 128;
}

function getColorMultipliers(kelvin: number, tint: number) {
  // Simplified conversion from Kelvin to RGB multipliers
  const normalized = (kelvin - 5500) / 1000;
  
  return {
    r: 1 + Math.max(-normalized * 0.2, 0),
    g: 1 + tint * 0.1,
    b: 1 + Math.max(normalized * 0.2, 0),
  };
}

function clamp(value: number): number {
  return Math.max(0, Math.min(255, Math.round(value)));
}
```

### Step 2: Curves

Create `src/core/color/curves.ts`:

```typescript
import { CurvePoint, TonalCurve } from '@types/color.types';
import { ImageData } from '@types/image.types';

export function applyCurve(
  imageData: ImageData,
  curve: TonalCurve
): ImageData {
  const lookupTable = generateCurveLUT(curve);
  const result = new ImageData(
    new Uint8ClampedArray(imageData.data),
    imageData.width,
    imageData.height
  );

  if (curve.channel === 'RGB') {
    for (let i = 0; i < result.data.length; i += 4) {
      result.data[i] = lookupTable[result.data[i]];
      result.data[i + 1] = lookupTable[result.data[i + 1]];
      result.data[i + 2] = lookupTable[result.data[i + 2]];
    }
  } else {
    const channelIndex = getChannelIndex(curve.channel);
    for (let i = 0; i < result.data.length; i += 4) {
      result.data[i + channelIndex] = lookupTable[result.data[i + channelIndex]];
    }
  }

  return result;
}

function generateCurveLUT(curve: TonalCurve): Uint8Array {
  const lut = new Uint8Array(256);
  const sortedPoints = [...curve.points].sort((a, b) => a.x - b.x);

  for (let i = 0; i < 256; i++) {
    const x = i / 255;
    const y = interpolateCurve(x, sortedPoints);
    lut[i] = Math.max(0, Math.min(255, Math.round(y * 255)));
  }

  return lut;
}

function interpolateCurve(x: number, points: CurvePoint[]): number {
  // Find surrounding points
  let i = 0;
  while (i < points.length && points[i].x < x) {
    i++;
  }

  if (i === 0) return points[0].y;
  if (i === points.length) return points[points.length - 1].y;

  const p1 = points[i - 1];
  const p2 = points[i];

  // Cubic interpolation
  const t = (x - p1.x) / (p2.x - p1.x);
  return cubicInterpolate(p1.y, p2.y, t);
}

function cubicInterpolate(y1: number, y2: number, t: number): number {
  const t2 = t * t;
  const t3 = t2 * t;
  return (2 * t3 - 3 * t2 + 1) * y1 + (-2 * t3 + 3 * t2) * y2;
}

function getChannelIndex(channel: string): number {
  switch (channel) {
    case 'R': return 0;
    case 'G': return 1;
    case 'B': return 2;
    default: return 0;
  }
}
```

---

## Phase 6: UI Components

### Step 1: Image Canvas

Create `src/ui/components/Canvas/ImageCanvas.tsx`:

```typescript
import React, { useRef, useEffect } from 'react';
import { View, Image, StyleSheet, Dimensions } from 'react-native';
import { useSelector } from 'react-redux';
import { RootState } from '@state/store';

const { width: SCREEN_WIDTH } = Dimensions.get('window');

export const ImageCanvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const currentImage = useSelector((state: RootState) => state.image.current);

  useEffect(() => {
    if (currentImage && canvasRef.current) {
      renderImageToCanvas(canvasRef.current, currentImage);
    }
  }, [currentImage]);

  if (!currentImage) {
    return (
      <View style={styles.placeholder}>
        {/* Placeholder UI */}
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <canvas
        ref={canvasRef}
        style={styles.canvas}
      />
    </View>
  );
};

function renderImageToCanvas(
  canvas: HTMLCanvasElement,
  imageData: ImageData
) {
  const ctx = canvas.getContext('2d');
  if (!ctx) return;

  canvas.width = imageData.width;
  canvas.height = imageData.height;
  ctx.putImageData(imageData, 0, 0);
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a1a',
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholder: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  canvas: {
    maxWidth: SCREEN_WIDTH,
    maxHeight: '100%',
  },
});
```

---

## Phase 7: Testing Setup

### Step 1: Create Unit Tests

Create `tests/unit/core/analysis/histogramAnalyzer.test.ts`:

```typescript
import { calculateHistogram, analyzeHistogram } from '@core/analysis/histogramAnalyzer';

describe('histogramAnalyzer', () => {
  it('should calculate histogram correctly', () => {
    const imageData = {
      data: new Uint8ClampedArray([
        255, 0, 0, 255,
        0, 255, 0, 255,
        0, 0, 255, 255,
      ]),
      width: 3,
      height: 1,
    };

    const histogram = calculateHistogram(imageData as any);

    expect(histogram.red[255]).toBe(1);
    expect(histogram.green[255]).toBe(1);
    expect(histogram.blue[255]).toBe(1);
  });

  it('should analyze histogram statistics', () => {
    const histogram = {
      red: new Uint32Array(256),
      green: new Uint32Array(256),
      blue: new Uint32Array(256),
      luminance: new Uint32Array(256),
    };

    histogram.red[128] = 100;
    histogram.green[128] = 100;
    histogram.blue[128] = 100;
    histogram.luminance[128] = 100;

    const analysis = analyzeHistogram(histogram);

    expect(analysis.stats.red.mean).toBe(128);
  });
});
```

---

## 🎯 Implementation Priority

1. **Week 1-2**: Setup + EXIF + Basic UI
2. **Week 3-4**: Histogram + White Balance + Curves
3. **Week 5-6**: Layer Separation (OpenCV integration)
4. **Week 7-8**: Depth Map + Bokeh
5. **Week 9-10**: Lens Profiles + Optical Effects
6. **Week 11-12**: Texture + Grain
7. **Week 13-14**: Look Builder + LUT Export
8. **Week 15-16**: Performance Optimization + Testing

---

## 📚 Next Steps

1. Start with Phase 1-2 to set up the foundation
2. Implement one module at a time
3. Test each module independently
4. Integrate modules progressively
5. Optimize performance as needed

See `LIBRARIES.md` for detailed library integration guides.
