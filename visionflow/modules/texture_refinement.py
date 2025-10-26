"""
Texture Refinement Module
Provides advanced texture processing and refinement operations.
"""

from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from scipy import ndimage


class TextureRefiner:
    """Handles texture refinement operations."""
    
    @staticmethod
    def denoise(image: Image.Image, strength: float = 1.0) -> Image.Image:
        """
        Apply noise reduction while preserving details.
        
        Args:
            image: Input PIL Image
            strength: Denoising strength (0.0 to 3.0)
            
        Returns:
            Denoised image
        """
        img_array = np.array(image).astype(float)
        
        # Apply bilateral filter approximation
        result = np.zeros_like(img_array)
        kernel_size = int(strength * 3) + 1
        
        for i in range(3):  # RGB channels
            # Simple averaging with edge preservation
            smoothed = ndimage.gaussian_filter(img_array[:, :, i], sigma=strength)
            result[:, :, i] = smoothed
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def enhance_details(image: Image.Image, strength: float = 1.0) -> Image.Image:
        """
        Enhance fine details and texture.
        
        Args:
            image: Input PIL Image
            strength: Enhancement strength (0.0 to 3.0)
            
        Returns:
            Detail-enhanced image
        """
        img_array = np.array(image).astype(float)
        
        # Apply high-pass filter
        blurred = np.array(image.filter(ImageFilter.GaussianBlur(radius=2))).astype(float)
        high_pass = img_array - blurred
        
        # Add back scaled details
        result = img_array + high_pass * strength
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def apply_grain(image: Image.Image, intensity: float = 0.1,
                   size: float = 1.0) -> Image.Image:
        """
        Add film grain texture.
        
        Args:
            image: Input PIL Image
            intensity: Grain intensity (0.0 to 1.0)
            size: Grain size (0.5 to 3.0)
            
        Returns:
            Image with grain texture
        """
        img_array = np.array(image).astype(float)
        height, width = img_array.shape[:2]
        
        # Generate noise
        noise = np.random.normal(0, intensity * 30, (height, width))
        
        # Blur noise for grain size
        if size > 1.0:
            noise = ndimage.gaussian_filter(noise, sigma=size)
        
        # Add noise to all channels
        result = img_array.copy()
        for i in range(3):
            result[:, :, i] += noise
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def smooth_skin(image: Image.Image, mask: np.ndarray = None,
                   smoothness: float = 0.5) -> Image.Image:
        """
        Apply skin smoothing (portrait retouching).
        
        Args:
            image: Input PIL Image
            mask: Optional mask for areas to smooth
            smoothness: Smoothing amount (0.0 to 1.0)
            
        Returns:
            Skin-smoothed image
        """
        img_array = np.array(image).astype(float)
        
        # Apply strong blur
        blurred = np.array(image.filter(ImageFilter.GaussianBlur(radius=10))).astype(float)
        
        # Preserve details by mixing original and blurred
        detail = img_array - np.array(image.filter(ImageFilter.GaussianBlur(radius=2))).astype(float)
        smoothed = blurred + detail * 0.5
        
        # Blend based on smoothness
        if mask is not None:
            mask_3d = np.stack([mask] * 3, axis=2)
            result = img_array * (1 - mask_3d * smoothness) + smoothed * mask_3d * smoothness
        else:
            result = img_array * (1 - smoothness) + smoothed * smoothness
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def adjust_texture_frequency(image: Image.Image, low_freq: float = 1.0,
                                 high_freq: float = 1.0) -> Image.Image:
        """
        Separately adjust low and high frequency texture components.
        
        Args:
            image: Input PIL Image
            low_freq: Low frequency multiplier (0.0 to 2.0)
            high_freq: High frequency multiplier (0.0 to 2.0)
            
        Returns:
            Frequency-adjusted image
        """
        img_array = np.array(image).astype(float)
        
        # Separate frequencies
        low = np.array(image.filter(ImageFilter.GaussianBlur(radius=5))).astype(float)
        high = img_array - low
        
        # Adjust frequencies
        result = low * low_freq + high * high_freq
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def apply_clarity(image: Image.Image, amount: float = 0.5) -> Image.Image:
        """
        Apply clarity enhancement (midtone contrast).
        
        Args:
            image: Input PIL Image
            amount: Clarity amount (0.0 to 2.0)
            
        Returns:
            Clarity-enhanced image
        """
        img_array = np.array(image).astype(float)
        
        # Apply local contrast enhancement
        blurred = np.array(image.filter(ImageFilter.GaussianBlur(radius=20))).astype(float)
        local_contrast = img_array - blurred
        
        # Apply midtone mask
        brightness = np.mean(img_array, axis=2, keepdims=True)
        midtone_mask = 1 - np.abs(brightness - 128) / 128
        midtone_mask = np.repeat(midtone_mask, 3, axis=2)
        
        # Apply clarity
        result = img_array + local_contrast * amount * midtone_mask
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
