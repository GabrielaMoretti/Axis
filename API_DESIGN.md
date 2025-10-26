# VISIONFLOW - API Design

## 🔌 Core Module APIs

This document defines the public APIs for each core processing module.

---

## 1. Image Analysis Module

### 1.1 EXIF Reader

```typescript
interface EXIFReaderAPI {
  /**
   * Extract EXIF metadata from an image file
   * @param source - File path, URL, or Buffer
   * @returns Promise with EXIF data or null if not available
   */
  extractEXIF(source: string | Buffer): Promise<EXIFData | null>;

  /**
   * Get camera information from EXIF
   */
  getCameraInfo(exif: EXIFData): CameraInfo;

  /**
   * Get lens information from EXIF
   */
  getLensInfo(exif: EXIFData): LensInfo;

  /**
   * Get exposure settings from EXIF
   */
  getExposureInfo(exif: EXIFData): ExposureInfo;
}

interface CameraInfo {
  make: string;
  model: string;
  sensorSize?: string; // e.g., "APS-C", "Full Frame"
}

interface LensInfo {
  model: string;
  focalLength: number; // in mm
  minAperture: number;
  maxAperture: number;
}

interface ExposureInfo {
  aperture: number; // f-stop
  shutterSpeed: string; // e.g., "1/250"
  iso: number;
  exposureCompensation?: number;
}
```

### 1.2 Histogram Analyzer

```typescript
interface HistogramAPI {
  /**
   * Calculate RGB and luminance histograms
   */
  calculate(imageData: ImageData): Histogram;

  /**
   * Analyze histogram for statistics
   */
  analyze(histogram: Histogram): HistogramAnalysis;

  /**
   * Detect clipping in highlights or shadows
   */
  detectClipping(histogram: Histogram): ClippingInfo;

  /**
   * Calculate dynamic range
   */
  getDynamicRange(histogram: Histogram): number;
}

interface HistogramAnalysis {
  mean: number;
  median: number;
  stdDev: number;
  mode: number;
  dynamicRange: number;
}

interface ClippingInfo {
  shadows: boolean;
  highlights: boolean;
  percentage: {
    shadows: number;
    highlights: number;
  };
}
```

### 1.3 Structure Analyzer

```typescript
interface StructureAnalyzerAPI {
  /**
   * Analyze image structure
   */
  analyze(imageData: ImageData): ImageStructure;

  /**
   * Generate light map
   */
  generateLightMap(imageData: ImageData): Float32Array;

  /**
   * Generate contrast map
   */
  generateContrastMap(imageData: ImageData): Float32Array;
}

interface ImageStructure {
  lightMap: Float32Array;
  contrastMap: Float32Array;
  dominantColors: Color[];
  composition: CompositionInfo;
}

interface CompositionInfo {
  ruleOfThirds: {
    topLeft: Point;
    topRight: Point;
    bottomLeft: Point;
    bottomRight: Point;
  };
  centerOfMass: Point;
}
```

---

## 2. Layer Separation Module

```typescript
interface LayerSeparationAPI {
  /**
   * Separate image into layers
   */
  separate(imageData: ImageData, options?: SeparationOptions): Promise<LayerSet>;

  /**
   * Extract foreground mask
   */
  extractForeground(imageData: ImageData): Promise<ImageData>;

  /**
   * Generate depth map
   */
  generateDepthMap(imageData: ImageData, method?: 'frequency' | 'midas'): Promise<Float32Array>;

  /**
   * Detect materials
   */
  detectMaterials(imageData: ImageData): Promise<MaterialMap>;

  /**
   * Refine mask edges
   */
  refineMask(mask: ImageData, options: RefinementOptions): ImageData;
}

interface SeparationOptions {
  method: 'grabcut' | 'u2net' | 'frequency';
  iterations?: number;
  featherRadius?: number;
}

interface LayerSet {
  foreground: Layer;
  background: Layer;
  depth: Layer;
  material: Layer;
  illumination: Layer;
}

interface MaterialMap {
  width: number;
  height: number;
  data: MaterialType[]; // One per pixel
}

interface RefinementOptions {
  featherRadius: number;
  smoothness: number;
  edgeAwareness: number;
}
```

---

## 3. Color Correction Module

### 3.1 White Balance

```typescript
interface WhiteBalanceAPI {
  /**
   * Automatically detect white balance
   */
  auto(imageData: ImageData): ColorTemperature;

  /**
   * Apply white balance adjustment
   */
  apply(imageData: ImageData, temperature: ColorTemperature): ImageData;

  /**
   * Get preset color temperatures
   */
  getPresets(): Record<string, ColorTemperature>;
}

// Presets
const WB_PRESETS = {
  daylight: { kelvin: 5500, tint: 0 },
  cloudy: { kelvin: 6500, tint: 0 },
  shade: { kelvin: 7500, tint: 0 },
  tungsten: { kelvin: 3200, tint: 0 },
  fluorescent: { kelvin: 4000, tint: 0 },
  flash: { kelvin: 5500, tint: 0 },
};
```

### 3.2 Curves

```typescript
interface CurvesAPI {
  /**
   * Apply tonal curve to image
   */
  apply(imageData: ImageData, curve: TonalCurve): ImageData;

  /**
   * Create curve from points
   */
  createCurve(points: CurvePoint[], channel: Channel): TonalCurve;

  /**
   * Generate lookup table from curve
   */
  generateLUT(curve: TonalCurve): Uint8Array;

  /**
   * Get preset curves
   */
  getPresets(): Record<string, TonalCurve>;
}

type Channel = 'RGB' | 'R' | 'G' | 'B' | 'L';

// Presets
const CURVE_PRESETS = {
  linear: { points: [{x: 0, y: 0}, {x: 1, y: 1}] },
  sRGB: { points: /* sRGB curve points */ },
  contrast: { points: /* S-curve points */ },
};
```

### 3.3 Color Grading

```typescript
interface ColorGradingAPI {
  /**
   * Apply color grading
   */
  apply(imageData: ImageData, grading: ColorGrading): ImageData;

  /**
   * Adjust shadows/midtones/highlights
   */
  adjustToneRange(
    imageData: ImageData,
    range: 'shadows' | 'midtones' | 'highlights',
    adjustment: HSL
  ): ImageData;

  /**
   * Apply LUT
   */
  applyLUT(imageData: ImageData, lut: LUT3D): ImageData;

  /**
   * Calculate color difference (ΔE2000)
   */
  deltaE(color1: Color, color2: Color): number;
}
```

---

## 4. Depth Control Module

```typescript
interface DepthControlAPI {
  /**
   * Generate depth map
   */
  generateDepthMap(imageData: ImageData, options?: DepthOptions): Promise<Float32Array>;

  /**
   * Apply depth-based blur (bokeh)
   */
  applyBokeh(
    imageData: ImageData,
    depthMap: Float32Array,
    options: BokehOptions
  ): Promise<ImageData>;

  /**
   * Set focus plane
   */
  setFocusPlane(depthMap: Float32Array, depth: number): Float32Array;

  /**
   * Calculate circle of confusion
   */
  calculateCoC(
    focalLength: number,
    aperture: number,
    focusDistance: number,
    subjectDistance: number
  ): number;
}

interface DepthOptions {
  method: 'frequency' | 'midas' | 'stereo';
  quality: 'low' | 'medium' | 'high';
}

interface BokehOptions {
  aperture: number; // f-stop (e.g., 1.8, 2.8, 5.6)
  focalLength: number; // in mm
  focusDistance: number; // in meters
  bokehShape: 'circular' | 'hexagonal' | 'octagonal';
  rotation: number; // in degrees
  quality: 'low' | 'medium' | 'high';
}
```

---

## 5. Lens Simulation Module

```typescript
interface LensSimulationAPI {
  /**
   * Apply lens profile
   */
  applyProfile(imageData: ImageData, profile: LensProfile): ImageData;

  /**
   * Get lens profile by name
   */
  getProfile(name: string): LensProfile | null;

  /**
   * List available profiles
   */
  listProfiles(): string[];

  /**
   * Create custom profile
   */
  createProfile(params: LensParams): LensProfile;

  /**
   * Apply distortion
   */
  applyDistortion(imageData: ImageData, params: DistortionParams): ImageData;

  /**
   * Apply chromatic aberration
   */
  applyChromaticAberration(imageData: ImageData, params: CAParams): ImageData;

  /**
   * Apply vignette
   */
  applyVignette(imageData: ImageData, params: VignetteParams): ImageData;

  /**
   * Apply lens flare
   */
  applyFlare(imageData: ImageData, params: FlareParams): ImageData;
}

interface LensProfile {
  name: string;
  manufacturer: string;
  focalLength: number;
  maxAperture: number;
  distortion: DistortionParams;
  chromaticAberration: CAParams;
  vignette: VignetteParams;
}

interface DistortionParams {
  type: 'barrel' | 'pincushion' | 'mustache';
  k1: number; // radial distortion coefficient
  k2: number;
  k3: number;
  p1: number; // tangential distortion coefficient
  p2: number;
}

interface CAParams {
  red: number;
  blue: number;
  intensity: number;
}

interface VignetteParams {
  intensity: number;
  radius: number;
  softness: number;
}

interface FlareParams {
  intensity: number;
  position: Point;
  color: Color;
  type: 'ghosting' | 'starburst' | 'haze';
}
```

---

## 6. Texture & Refinement Module

```typescript
interface TextureAPI {
  /**
   * Apply frequency separation
   */
  frequencySeparation(
    imageData: ImageData,
    radius: number
  ): { low: ImageData; high: ImageData };

  /**
   * Apply sharpening
   */
  sharpen(imageData: ImageData, options: SharpenOptions): ImageData;

  /**
   * Adjust microcontrast
   */
  adjustMicrocontrast(imageData: ImageData, amount: number): ImageData;

  /**
   * Apply film grain
   */
  applyGrain(imageData: ImageData, options: GrainOptions): ImageData;

  /**
   * Apply clarity
   */
  applyClarity(imageData: ImageData, amount: number): ImageData;
}

interface SharpenOptions {
  amount: number; // 0-100
  radius: number; // in pixels
  threshold: number; // 0-255
  method: 'unsharp' | 'high-pass' | 'deconvolution';
}

interface GrainOptions {
  amount: number; // 0-100
  size: number; // grain size
  type: 'uniform' | 'gaussian' | 'film';
  roughness: number; // 0-1
}
```

---

## 7. Look Builder & Export Module

```typescript
interface LookBuilderAPI {
  /**
   * Create look from current adjustments
   */
  createLook(name: string, adjustments: Adjustments): Look;

  /**
   * Apply look to image
   */
  applyLook(imageData: ImageData, look: Look): ImageData;

  /**
   * Generate 3D LUT
   */
  generateLUT(look: Look, size?: number): LUT3D;

  /**
   * Export LUT to file
   */
  exportLUT(lut: LUT3D, format: 'cube' | 'vlt'): Promise<Blob>;

  /**
   * Import LUT from file
   */
  importLUT(file: Blob): Promise<LUT3D>;

  /**
   * List available looks
   */
  listLooks(): Look[];

  /**
   * Save look preset
   */
  saveLook(look: Look): Promise<void>;
}

interface Look {
  id: string;
  name: string;
  category: 'cinematic' | 'analog' | 'editorial' | 'natural' | 'custom';
  adjustments: Adjustments;
  thumbnail?: string;
}

interface Adjustments {
  whiteBalance?: ColorTemperature;
  curves?: TonalCurve[];
  colorGrading?: ColorGrading;
  texture?: TextureAdjustments;
  lens?: LensProfile;
  depth?: BokehOptions;
}
```

---

## 8. Export Module

```typescript
interface ExportAPI {
  /**
   * Export image
   */
  export(
    imageData: ImageData,
    options: ExportOptions
  ): Promise<Blob>;

  /**
   * Export with metadata
   */
  exportWithMetadata(
    imageData: ImageData,
    metadata: EXIFData,
    options: ExportOptions
  ): Promise<Blob>;

  /**
   * Get supported formats
   */
  getSupportedFormats(): ExportFormat[];
}

interface ExportOptions {
  format: 'jpeg' | 'png' | 'tiff' | 'webp' | 'heic';
  quality: number; // 0-100
  colorSpace: 'sRGB' | 'AdobeRGB' | 'ProPhotoRGB';
  embedProfile: boolean;
  preserveMetadata: boolean;
  resize?: {
    width: number;
    height: number;
    fit: 'contain' | 'cover' | 'fill';
  };
}

interface ExportFormat {
  extension: string;
  mimeType: string;
  supportsQuality: boolean;
  supportsTransparency: boolean;
  maxDimensions: number;
}
```

---

## 9. Worker Thread API

```typescript
interface WorkerAPI {
  /**
   * Process image in worker thread
   */
  processInWorker<T>(
    operation: string,
    data: ImageData,
    params: any
  ): Promise<T>;

  /**
   * Batch process multiple images
   */
  batchProcess(
    operations: ProcessOperation[]
  ): Promise<ProcessResult[]>;

  /**
   * Cancel processing
   */
  cancel(operationId: string): void;
}

interface ProcessOperation {
  id: string;
  type: string;
  imageData: ImageData;
  params: any;
}

interface ProcessResult {
  id: string;
  success: boolean;
  data?: any;
  error?: string;
  processingTime: number;
}
```

---

## 10. State Management API (Redux)

```typescript
// Actions
interface ImageActions {
  loadImage(source: string | File): AsyncThunk;
  setOriginalImage(imageData: ImageData): Action;
  setCurrentImage(imageData: ImageData): Action;
  applyAdjustment(adjustment: Adjustment): AsyncThunk;
  undoAdjustment(): Action;
  redoAdjustment(): Action;
  resetImage(): Action;
}

// Selectors
interface ImageSelectors {
  selectOriginalImage(state: RootState): ImageData | null;
  selectCurrentImage(state: RootState): ImageData | null;
  selectMetadata(state: RootState): ImageMetadata | null;
  selectAdjustments(state: RootState): Adjustment[];
  selectHistogram(state: RootState): Histogram | null;
  selectIsProcessing(state: RootState): boolean;
}
```

---

## Usage Examples

### Basic Image Load and Process

```typescript
import { ImageLoader, WhiteBalance, Curves } from '@core';

// Load image
const imageData = await ImageLoader.load('photo.jpg');

// Extract EXIF
const exif = await EXIFReader.extractEXIF('photo.jpg');

// Auto white balance
const wb = WhiteBalance.auto(imageData);
const balanced = WhiteBalance.apply(imageData, wb);

// Apply curve
const curve = Curves.createCurve([
  { x: 0, y: 0 },
  { x: 0.5, y: 0.6 },
  { x: 1, y: 1 }
], 'RGB');
const result = Curves.apply(balanced, curve);

// Export
await Exporter.export(result, {
  format: 'jpeg',
  quality: 95,
  colorSpace: 'sRGB'
});
```

### Advanced Depth Processing

```typescript
import { DepthControl, LayerSeparation } from '@core';

// Generate depth map
const depthMap = await DepthControl.generateDepthMap(imageData, {
  method: 'midas',
  quality: 'high'
});

// Apply bokeh
const bokehResult = await DepthControl.applyBokeh(imageData, depthMap, {
  aperture: 1.8,
  focalLength: 50,
  focusDistance: 2,
  bokehShape: 'circular',
  quality: 'high'
});
```

### Complete Workflow

```typescript
import { Pipeline } from '@core';

const pipeline = new Pipeline()
  .load('photo.jpg')
  .extractMetadata()
  .autoWhiteBalance()
  .applyCurve('contrast')
  .separateLayers()
  .generateDepthMap()
  .applyBokeh({ aperture: 2.8 })
  .applyLensProfile('Zeiss Planar 50mm')
  .applyGrain({ amount: 30, type: 'film' })
  .createLook('Cinematic Portrait')
  .export({ format: 'jpeg', quality: 95 });

const result = await pipeline.execute();
```

---

## Error Handling

All async operations return Promises that should be handled with try/catch:

```typescript
try {
  const result = await ImageLoader.load('invalid.jpg');
} catch (error) {
  if (error instanceof UnsupportedFormatError) {
    console.error('Format not supported');
  } else if (error instanceof CorruptedFileError) {
    console.error('File is corrupted');
  } else {
    console.error('Unknown error:', error);
  }
}
```

---

## Performance Considerations

- Use Web Workers for heavy operations
- Implement progressive rendering for previews
- Cache intermediate results
- Use WebGL for real-time effects
- Batch similar operations together

---

See `IMPLEMENTATION_GUIDE.md` for implementation details.
