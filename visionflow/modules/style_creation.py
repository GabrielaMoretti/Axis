"""
Visual Style Creation Module
Creates and applies artistic visual styles to images.
"""

from PIL import Image
import numpy as np
from typing import Dict, Any, Optional


class StyleCreator:
    """Creates and applies visual styles to images."""
    
    def __init__(self):
        """Initialize style creator with predefined styles."""
        self.styles = {
            'cinematic': {
                'temperature': 0.1,
                'tint': -0.05,
                'contrast': 1.2,
                'saturation': 0.9,
                'vignette': 0.3,
                'grain': 0.05
            },
            'vintage': {
                'temperature': 0.2,
                'tint': 0.1,
                'contrast': 0.9,
                'saturation': 0.8,
                'vignette': 0.5,
                'grain': 0.15
            },
            'dramatic': {
                'temperature': 0.0,
                'tint': 0.0,
                'contrast': 1.5,
                'saturation': 1.2,
                'clarity': 1.0,
                'vignette': 0.2
            },
            'soft': {
                'temperature': 0.05,
                'tint': 0.05,
                'contrast': 0.85,
                'saturation': 0.95,
                'smoothness': 0.3,
                'glow': 0.2
            },
            'high_key': {
                'exposure': 0.5,
                'contrast': 0.8,
                'saturation': 0.9,
                'brightness_lift': 20
            },
            'low_key': {
                'exposure': -0.3,
                'contrast': 1.3,
                'saturation': 1.1,
                'shadows_crush': 15
            }
        }
    
    def apply_style(self, image: Image.Image, style_name: str,
                   intensity: float = 1.0) -> Image.Image:
        """
        Apply a predefined style to an image.
        
        Args:
            image: Input PIL Image
            style_name: Name of the style to apply
            intensity: Style intensity (0.0 to 1.0)
            
        Returns:
            Styled image
        """
        if style_name not in self.styles:
            return image.copy()
        
        style_params = self.styles[style_name]
        result = image.copy()
        
        # Apply style parameters
        from visionflow.modules.color_correction import ColorCorrector
        from visionflow.modules.lens_simulation import LensSimulator
        from visionflow.modules.texture_refinement import TextureRefiner
        
        # Temperature and tint
        if 'temperature' in style_params or 'tint' in style_params:
            temp = style_params.get('temperature', 0.0) * intensity
            tint = style_params.get('tint', 0.0) * intensity
            result = ColorCorrector.adjust_white_balance(result, temp, tint)
        
        # Exposure
        if 'exposure' in style_params:
            exp = style_params['exposure'] * intensity
            result = ColorCorrector.adjust_exposure(result, exp)
        
        # Contrast
        if 'contrast' in style_params:
            contrast = 1.0 + (style_params['contrast'] - 1.0) * intensity
            result = ColorCorrector.adjust_contrast(result, contrast)
        
        # Saturation
        if 'saturation' in style_params:
            sat = 1.0 + (style_params['saturation'] - 1.0) * intensity
            result = ColorCorrector.adjust_saturation(result, sat)
        
        # Clarity
        if 'clarity' in style_params:
            clarity = style_params['clarity'] * intensity
            result = TextureRefiner.apply_clarity(result, clarity)
        
        # Vignette
        if 'vignette' in style_params:
            vignette = style_params['vignette'] * intensity
            result = LensSimulator.apply_vignette(result, vignette)
        
        # Grain
        if 'grain' in style_params:
            grain = style_params['grain'] * intensity
            result = TextureRefiner.apply_grain(result, grain)
        
        return result
    
    def create_custom_style(self, name: str, parameters: Dict[str, Any]):
        """
        Create a custom style with specified parameters.
        
        Args:
            name: Name for the custom style
            parameters: Dictionary of style parameters
        """
        self.styles[name] = parameters
    
    def get_available_styles(self) -> list:
        """Get list of available style names."""
        return list(self.styles.keys())
    
    def apply_lut(self, image: Image.Image, lut_file: Optional[str] = None,
                 lut_array: Optional[np.ndarray] = None) -> Image.Image:
        """
        Apply a Look-Up Table (LUT) for color grading.
        
        Args:
            image: Input PIL Image
            lut_file: Path to LUT file (cube format)
            lut_array: 3D numpy array representing the LUT
            
        Returns:
            Color-graded image
        """
        if lut_array is None:
            return image.copy()
        
        img_array = np.array(image)
        result = np.zeros_like(img_array)
        
        # Apply LUT
        # This is a simplified version - full implementation would support .cube files
        for i in range(3):
            result[:, :, i] = np.interp(img_array[:, :, i], 
                                       np.arange(256), 
                                       lut_array[:, i] if len(lut_array.shape) == 2 else np.arange(256))
        
        return Image.fromarray(result.astype(np.uint8))
    
    @staticmethod
    def create_color_grade(image: Image.Image, shadows: tuple = (0, 0, 0),
                          midtones: tuple = (0, 0, 0),
                          highlights: tuple = (0, 0, 0)) -> Image.Image:
        """
        Apply color grading to shadows, midtones, and highlights separately.
        
        Args:
            image: Input PIL Image
            shadows: RGB adjustment for shadows (-50 to 50 for each channel)
            midtones: RGB adjustment for midtones (-50 to 50 for each channel)
            highlights: RGB adjustment for highlights (-50 to 50 for each channel)
            
        Returns:
            Color-graded image
        """
        img_array = np.array(image).astype(float)
        
        # Calculate luminance
        luminance = 0.299 * img_array[:, :, 0] + 0.587 * img_array[:, :, 1] + 0.114 * img_array[:, :, 2]
        
        # Create masks for shadows, midtones, highlights
        shadow_mask = np.clip(1 - luminance / 85, 0, 1)
        highlight_mask = np.clip((luminance - 170) / 85, 0, 1)
        midtone_mask = 1 - shadow_mask - highlight_mask
        
        # Apply adjustments
        result = img_array.copy()
        for i in range(3):
            result[:, :, i] += shadow_mask * shadows[i]
            result[:, :, i] += midtone_mask * midtones[i]
            result[:, :, i] += highlight_mask * highlights[i]
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
