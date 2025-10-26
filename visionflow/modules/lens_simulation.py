"""
Lens Simulation Module
Simulates various lens characteristics and optical effects.
"""

from PIL import Image, ImageFilter
import numpy as np
from typing import Tuple


class LensSimulator:
    """Simulates lens characteristics and optical effects."""
    
    @staticmethod
    def apply_vignette(image: Image.Image, strength: float = 0.5,
                      center: Tuple[float, float] = (0.5, 0.5)) -> Image.Image:
        """
        Apply vignette effect (darkening at edges).
        
        Args:
            image: Input PIL Image
            strength: Vignette strength (0.0 to 1.0)
            center: Center point as fraction of image dimensions
            
        Returns:
            Image with vignette effect
        """
        width, height = image.size
        img_array = np.array(image).astype(float)
        
        # Create vignette mask
        cx = width * center[0]
        cy = height * center[1]
        
        y, x = np.ogrid[:height, :width]
        distances = np.sqrt((x - cx)**2 + (y - cy)**2)
        max_distance = np.sqrt((width/2)**2 + (height/2)**2)
        
        vignette_mask = 1 - (distances / max_distance) * strength
        vignette_mask = np.clip(vignette_mask, 0, 1)
        
        # Apply vignette
        for i in range(3):  # RGB channels
            img_array[:, :, i] *= vignette_mask
        
        return Image.fromarray(np.clip(img_array, 0, 255).astype(np.uint8))
    
    @staticmethod
    def apply_chromatic_aberration(image: Image.Image, strength: float = 2.0) -> Image.Image:
        """
        Apply chromatic aberration effect (color fringing at edges).
        
        Args:
            image: Input PIL Image
            strength: Aberration strength in pixels
            
        Returns:
            Image with chromatic aberration
        """
        from scipy import ndimage
        
        img_array = np.array(image).astype(float)
        width, height = image.size
        
        # Apply simple uniform shift to simulate chromatic aberration
        # Red channel shifts outward, blue channel shifts inward
        result = np.zeros_like(img_array)
        result[:, :, 0] = ndimage.shift(img_array[:, :, 0], [strength, strength], mode='nearest')  # Red outward
        result[:, :, 1] = img_array[:, :, 1]  # Green unchanged
        result[:, :, 2] = ndimage.shift(img_array[:, :, 2], [-strength, -strength], mode='nearest')  # Blue inward
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def apply_lens_distortion(image: Image.Image, distortion: float = 0.0) -> Image.Image:
        """
        Apply barrel or pincushion distortion.
        
        Args:
            image: Input PIL Image
            distortion: Distortion amount (-1.0 = barrel, 0.0 = none, 1.0 = pincushion)
            
        Returns:
            Distorted image
        """
        if abs(distortion) < 0.01:
            return image.copy()
        
        width, height = image.size
        img_array = np.array(image)
        
        # Create meshgrid
        cx, cy = width / 2, height / 2
        y, x = np.mgrid[0:height, 0:width]
        
        # Normalize coordinates
        x_norm = (x - cx) / width
        y_norm = (y - cy) / height
        
        # Calculate radius
        r = np.sqrt(x_norm**2 + y_norm**2)
        
        # Apply distortion
        r_distorted = r * (1 + distortion * r**2)
        
        # Convert back to pixel coordinates
        theta = np.arctan2(y_norm, x_norm)
        x_new = cx + r_distorted * width * np.cos(theta)
        y_new = cy + r_distorted * height * np.sin(theta)
        
        # Clamp coordinates
        x_new = np.clip(x_new, 0, width - 1)
        y_new = np.clip(y_new, 0, height - 1)
        
        # Sample from original image
        from scipy.ndimage import map_coordinates
        result = np.zeros_like(img_array)
        for i in range(3):
            result[:, :, i] = map_coordinates(img_array[:, :, i], [y_new, x_new], order=1)
        
        return Image.fromarray(result.astype(np.uint8))
    
    @staticmethod
    def apply_bokeh(image: Image.Image, blur_amount: float = 5.0,
                   shape: str = 'circle') -> Image.Image:
        """
        Apply bokeh effect (artistic blur with shaped highlights).
        
        Args:
            image: Input PIL Image
            blur_amount: Amount of blur
            shape: Bokeh shape ('circle', 'hexagon')
            
        Returns:
            Image with bokeh effect
        """
        # Simple bokeh approximation using Gaussian blur
        # In a full implementation, this would use custom kernels
        blurred = image.filter(ImageFilter.GaussianBlur(radius=blur_amount))
        
        # Enhance highlights in blurred areas
        img_array = np.array(image).astype(float)
        blur_array = np.array(blurred).astype(float)
        
        # Identify bright areas
        brightness = np.mean(img_array, axis=2)
        highlight_mask = (brightness > 200).astype(float)
        highlight_mask = np.stack([highlight_mask] * 3, axis=2)
        
        # Enhance highlights in bokeh
        result = blur_array + highlight_mask * 30
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def simulate_aperture(image: Image.Image, f_stop: float = 2.8) -> Image.Image:
        """
        Simulate different aperture settings affecting depth of field.
        
        Args:
            image: Input PIL Image
            f_stop: F-stop value (lower = shallower DOF, more blur)
            
        Returns:
            Image with simulated aperture effect
        """
        # Map f-stop to blur radius (inverse relationship)
        blur_radius = max(0, 20 / f_stop - 2)
        
        if blur_radius < 0.5:
            return image.copy()
        
        return image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
