"""
Focus and Depth Control Module
Provides depth of field and focus manipulation.
"""

from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage
from typing import Optional, Tuple


class FocusDepthController:
    """Handles focus and depth of field operations."""
    
    @staticmethod
    def apply_gaussian_blur(image: Image.Image, radius: float = 2.0) -> Image.Image:
        """
        Apply Gaussian blur to simulate out-of-focus areas.
        
        Args:
            image: Input PIL Image
            radius: Blur radius (higher = more blur)
            
        Returns:
            Blurred image
        """
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
    
    @staticmethod
    def apply_depth_of_field(image: Image.Image, focus_point: Tuple[int, int],
                            focus_range: float = 0.3, max_blur: float = 5.0) -> Image.Image:
        """
        Apply depth of field effect with a focus point.
        
        Args:
            image: Input PIL Image
            focus_point: (x, y) coordinates of focus point
            focus_range: Range around focus point that stays sharp (0.0 to 1.0)
            max_blur: Maximum blur radius for out-of-focus areas
            
        Returns:
            Image with depth of field effect
        """
        width, height = image.size
        fx, fy = focus_point
        
        # Normalize focus point
        fx = np.clip(fx, 0, width - 1)
        fy = np.clip(fy, 0, height - 1)
        
        # Create distance map from focus point
        y, x = np.ogrid[:height, :width]
        distances = np.sqrt((x - fx)**2 + (y - fy)**2)
        max_distance = np.sqrt(width**2 + height**2)
        normalized_distances = distances / max_distance
        
        # Create blur map based on distance from focus point
        blur_map = np.clip((normalized_distances - focus_range) / (1.0 - focus_range), 0, 1)
        blur_map = blur_map * max_blur
        
        # Apply variable blur
        img_array = np.array(image)
        result = np.zeros_like(img_array)
        
        # Simple approximation: blend between sharp and blurred versions
        blurred = np.array(image.filter(ImageFilter.GaussianBlur(radius=max_blur)))
        
        for i in range(3):  # RGB channels
            for y in range(height):
                for x in range(width):
                    blur_amount = blur_map[y, x] / max_blur
                    result[y, x, i] = img_array[y, x, i] * (1 - blur_amount) + blurred[y, x, i] * blur_amount
        
        return Image.fromarray(result.astype(np.uint8))
    
    @staticmethod
    def apply_radial_blur(image: Image.Image, center: Optional[Tuple[int, int]] = None,
                         strength: float = 0.1) -> Image.Image:
        """
        Apply radial blur effect for motion or zoom effects.
        
        Args:
            image: Input PIL Image
            center: Center point for radial blur (defaults to image center)
            strength: Blur strength (0.0 to 1.0)
            
        Returns:
            Radially blurred image
        """
        width, height = image.size
        if center is None:
            center = (width // 2, height // 2)
        
        img_array = np.array(image).astype(float)
        result = img_array.copy()
        
        cx, cy = center
        y_coords, x_coords = np.ogrid[:height, :width]
        
        # Calculate angles and distances from center
        dx = x_coords - cx
        dy = y_coords - cy
        
        # Apply simple radial blur by averaging pixels along radial direction
        for _ in range(int(strength * 10) + 1):
            shifted = ndimage.shift(img_array, [dy * strength * 0.01, dx * strength * 0.01, 0], mode='nearest')
            result = result * 0.7 + shifted * 0.3
        
        return Image.fromarray(np.clip(result, 0, 255).astype(np.uint8))
    
    @staticmethod
    def apply_tilt_shift(image: Image.Image, focus_line_y: float = 0.5,
                        focus_width: float = 0.2, max_blur: float = 5.0) -> Image.Image:
        """
        Apply tilt-shift effect (miniature fake effect).
        
        Args:
            image: Input PIL Image
            focus_line_y: Vertical position of focus line (0.0 to 1.0)
            focus_width: Width of focus area (0.0 to 1.0)
            max_blur: Maximum blur radius
            
        Returns:
            Image with tilt-shift effect
        """
        width, height = image.size
        focus_y = int(focus_line_y * height)
        focus_half_width = int(focus_width * height / 2)
        
        # Create blur gradient map
        y_coords = np.arange(height)
        blur_map = np.abs(y_coords - focus_y) - focus_half_width
        blur_map = np.clip(blur_map, 0, None)
        blur_map = (blur_map / (height / 2)) * max_blur
        
        # Apply blur
        img_array = np.array(image)
        blurred = np.array(image.filter(ImageFilter.GaussianBlur(radius=max_blur)))
        
        result = np.zeros_like(img_array)
        for y in range(height):
            blur_amount = np.clip(blur_map[y] / max_blur, 0, 1)
            result[y] = img_array[y] * (1 - blur_amount) + blurred[y] * blur_amount
        
        return Image.fromarray(result.astype(np.uint8))
    
    @staticmethod
    def sharpen(image: Image.Image, strength: float = 1.0) -> Image.Image:
        """
        Sharpen image to enhance focus.
        
        Args:
            image: Input PIL Image
            strength: Sharpening strength (0.0 to 3.0)
            
        Returns:
            Sharpened image
        """
        # Apply unsharp mask
        blurred = image.filter(ImageFilter.GaussianBlur(radius=1))
        img_array = np.array(image).astype(float)
        blur_array = np.array(blurred).astype(float)
        
        sharpened = img_array + strength * (img_array - blur_array)
        return Image.fromarray(np.clip(sharpened, 0, 255).astype(np.uint8))
