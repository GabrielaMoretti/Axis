"""
Physical Color Correction Module
Provides scientifically accurate color correction operations.
"""

from PIL import Image, ImageEnhance
import numpy as np
from typing import Tuple, Optional


class ColorCorrector:
    """Handles physical color correction operations."""
    
    @staticmethod
    def adjust_white_balance(image: Image.Image, temperature: float = 0.0, 
                            tint: float = 0.0) -> Image.Image:
        """
        Adjust white balance with temperature and tint controls.
        
        Args:
            image: Input PIL Image
            temperature: Temperature shift (-1.0 to 1.0, negative = cooler, positive = warmer)
            tint: Tint shift (-1.0 to 1.0, negative = green, positive = magenta)
            
        Returns:
            Color corrected image
        """
        img_array = np.array(image).astype(float)
        
        # Temperature adjustment (affects red-blue balance)
        if temperature != 0:
            temp_factor = 1.0 + temperature * 0.3
            img_array[:, :, 0] = np.clip(img_array[:, :, 0] * temp_factor, 0, 255)  # Red
            img_array[:, :, 2] = np.clip(img_array[:, :, 2] / temp_factor, 0, 255)  # Blue
        
        # Tint adjustment (affects green-magenta balance)
        if tint != 0:
            tint_factor = 1.0 + tint * 0.3
            img_array[:, :, 1] = np.clip(img_array[:, :, 1] * tint_factor, 0, 255)  # Green
        
        return Image.fromarray(img_array.astype(np.uint8))
    
    @staticmethod
    def adjust_exposure(image: Image.Image, exposure: float = 0.0) -> Image.Image:
        """
        Adjust exposure (brightness) of the image.
        
        Args:
            image: Input PIL Image
            exposure: Exposure adjustment (-2.0 to 2.0 stops)
            
        Returns:
            Exposure-adjusted image
        """
        factor = 2.0 ** exposure
        img_array = np.array(image).astype(float)
        img_array = np.clip(img_array * factor, 0, 255)
        return Image.fromarray(img_array.astype(np.uint8))
    
    @staticmethod
    def adjust_contrast(image: Image.Image, contrast: float = 1.0) -> Image.Image:
        """
        Adjust image contrast.
        
        Args:
            image: Input PIL Image
            contrast: Contrast factor (0.0 = gray, 1.0 = original, >1.0 = increased)
            
        Returns:
            Contrast-adjusted image
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(contrast)
    
    @staticmethod
    def adjust_saturation(image: Image.Image, saturation: float = 1.0) -> Image.Image:
        """
        Adjust color saturation.
        
        Args:
            image: Input PIL Image
            saturation: Saturation factor (0.0 = grayscale, 1.0 = original, >1.0 = increased)
            
        Returns:
            Saturation-adjusted image
        """
        enhancer = ImageEnhance.Color(image)
        return enhancer.enhance(saturation)
    
    @staticmethod
    def adjust_hsl(image: Image.Image, hue: float = 0.0, 
                   saturation: float = 0.0, lightness: float = 0.0) -> Image.Image:
        """
        Adjust Hue, Saturation, and Lightness.
        
        Args:
            image: Input PIL Image
            hue: Hue rotation in degrees (-180 to 180)
            saturation: Saturation adjustment (-1.0 to 1.0)
            lightness: Lightness adjustment (-1.0 to 1.0)
            
        Returns:
            HSL-adjusted image
        """
        import colorsys
        
        img_array = np.array(image).astype(float) / 255.0
        h, w, c = img_array.shape
        
        # Convert RGB to HSL
        result = np.zeros_like(img_array)
        for i in range(h):
            for j in range(w):
                r, g, b = img_array[i, j]
                h_val, l_val, s_val = colorsys.rgb_to_hls(r, g, b)
                
                # Apply adjustments
                h_val = (h_val + hue / 360.0) % 1.0
                s_val = np.clip(s_val + saturation, 0, 1)
                l_val = np.clip(l_val + lightness, 0, 1)
                
                r, g, b = colorsys.hls_to_rgb(h_val, l_val, s_val)
                result[i, j] = [r, g, b]
        
        return Image.fromarray((result * 255).astype(np.uint8))
    
    @staticmethod
    def apply_curves(image: Image.Image, curve_points: list) -> Image.Image:
        """
        Apply tone curve adjustment.
        
        Args:
            image: Input PIL Image
            curve_points: List of (input, output) points for the curve
            
        Returns:
            Curve-adjusted image
        """
        if not curve_points:
            return image.copy()
        
        # Create lookup table
        lut = np.arange(256, dtype=np.float32)
        
        # Interpolate curve
        for i in range(len(curve_points) - 1):
            x1, y1 = curve_points[i]
            x2, y2 = curve_points[i + 1]
            
            for x in range(int(x1), int(x2) + 1):
                if x2 != x1:
                    t = (x - x1) / (x2 - x1)
                    lut[x] = y1 + t * (y2 - y1)
        
        lut = np.clip(lut, 0, 255).astype(np.uint8)
        
        # Apply LUT to image
        return image.point(lut.tolist())
