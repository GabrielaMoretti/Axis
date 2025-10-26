"""
Import and Technical Analysis Module
Provides detailed analysis of image technical properties.
"""

from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
from typing import Dict, Any, Optional


class ImageImporter:
    """Handles image import and technical analysis."""
    
    @staticmethod
    def import_image(image_path: str) -> Image.Image:
        """
        Import an image with technical validation.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            PIL Image object
        """
        try:
            image = Image.open(image_path)
            return image
        except Exception as e:
            raise ValueError(f"Failed to import image: {str(e)}")
    
    @staticmethod
    def analyze_technical_properties(image: Image.Image) -> Dict[str, Any]:
        """
        Perform comprehensive technical analysis of an image.
        
        Args:
            image: PIL Image object
            
        Returns:
            Dictionary containing technical properties
        """
        img_array = np.array(image.convert('RGB'))
        
        analysis = {
            'dimensions': {
                'width': image.width,
                'height': image.height,
                'aspect_ratio': image.width / image.height
            },
            'color_space': image.mode,
            'format': getattr(image, 'format', 'Unknown'),
            'brightness': {
                'mean': float(np.mean(img_array)),
                'std': float(np.std(img_array)),
                'min': int(np.min(img_array)),
                'max': int(np.max(img_array))
            },
            'channels': {}
        }
        
        # Per-channel analysis
        if len(img_array.shape) == 3:
            channel_names = ['red', 'green', 'blue']
            for i, name in enumerate(channel_names):
                if i < img_array.shape[2]:
                    analysis['channels'][name] = {
                        'mean': float(np.mean(img_array[:, :, i])),
                        'std': float(np.std(img_array[:, :, i])),
                        'histogram': np.histogram(img_array[:, :, i], bins=256, range=(0, 256))[0].tolist()
                    }
        
        # Extract EXIF data if available
        analysis['exif'] = ImageImporter._extract_exif(image)
        
        # Calculate sharpness estimation
        analysis['sharpness'] = ImageImporter._estimate_sharpness(img_array)
        
        return analysis
    
    @staticmethod
    def _extract_exif(image: Image.Image) -> Dict[str, Any]:
        """Extract EXIF metadata from image."""
        exif_data = {}
        try:
            exif = image.getexif()
            if exif:
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    exif_data[tag] = str(value)
        except:
            pass
        return exif_data
    
    @staticmethod
    def _estimate_sharpness(img_array: np.ndarray) -> float:
        """
        Estimate image sharpness using variance of Laplacian.
        Higher values indicate sharper images.
        """
        from scipy import ndimage
        
        # Convert to grayscale if needed
        if len(img_array.shape) == 3:
            gray = np.mean(img_array, axis=2)
        else:
            gray = img_array
        
        # Apply Laplacian filter
        laplacian = ndimage.laplace(gray)
        sharpness = float(np.var(laplacian))
        
        return sharpness
