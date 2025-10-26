"""
Core image class that represents an image with its layers and processing history.
Provides a reversible pipeline for professional image editing.
"""

from PIL import Image
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import copy


class ImageLayer:
    """Represents a single layer in the image with blend mode and opacity."""
    
    def __init__(self, image: Image.Image, name: str = "Layer", 
                 opacity: float = 1.0, blend_mode: str = "normal"):
        """
        Initialize an image layer.
        
        Args:
            image: PIL Image object
            name: Layer name
            opacity: Layer opacity (0.0 to 1.0)
            blend_mode: Blend mode (normal, multiply, screen, overlay)
        """
        self.image = image
        self.name = name
        self.opacity = opacity
        self.blend_mode = blend_mode
        self.visible = True
    
    def copy(self):
        """Create a deep copy of the layer."""
        return ImageLayer(
            self.image.copy(),
            self.name,
            self.opacity,
            self.blend_mode
        )


class VisionFlowImage:
    """
    Core image class with layer support and processing history.
    Implements a reversible pipeline for professional editing.
    """
    
    def __init__(self, image_path: Optional[str] = None, 
                 image: Optional[Image.Image] = None):
        """
        Initialize VisionFlow image.
        
        Args:
            image_path: Path to image file
            image: PIL Image object (alternative to image_path)
        """
        if image_path:
            self.base_image = Image.open(image_path).convert('RGB')
        elif image:
            self.base_image = image.convert('RGB')
        else:
            raise ValueError("Either image_path or image must be provided")
        
        self.layers: List[ImageLayer] = [
            ImageLayer(self.base_image.copy(), "Background")
        ]
        self.processing_history: List[Dict[str, Any]] = []
        self.metadata = self._analyze_image()
    
    def _analyze_image(self) -> Dict[str, Any]:
        """Analyze technical properties of the image."""
        img_array = np.array(self.base_image)
        
        return {
            'width': self.base_image.width,
            'height': self.base_image.height,
            'mode': self.base_image.mode,
            'format': getattr(self.base_image, 'format', 'Unknown'),
            'mean_brightness': float(np.mean(img_array)),
            'std_brightness': float(np.std(img_array)),
            'aspect_ratio': self.base_image.width / self.base_image.height,
        }
    
    def add_layer(self, image: Image.Image, name: str = "New Layer", 
                  opacity: float = 1.0, blend_mode: str = "normal") -> ImageLayer:
        """Add a new layer to the image."""
        layer = ImageLayer(image, name, opacity, blend_mode)
        self.layers.append(layer)
        self._record_operation('add_layer', {'name': name})
        return layer
    
    def remove_layer(self, layer_index: int):
        """Remove a layer by index."""
        if 0 <= layer_index < len(self.layers):
            removed = self.layers.pop(layer_index)
            self._record_operation('remove_layer', {'name': removed.name})
    
    def get_layer(self, layer_index: int) -> Optional[ImageLayer]:
        """Get a layer by index."""
        if 0 <= layer_index < len(self.layers):
            return self.layers[layer_index]
        return None
    
    def flatten(self) -> Image.Image:
        """Flatten all visible layers into a single image."""
        if not self.layers:
            return self.base_image.copy()
        
        # Start with the first visible layer
        result = None
        for layer in self.layers:
            if not layer.visible:
                continue
            
            if result is None:
                result = layer.image.copy()
            else:
                # Simple blend - could be extended with more blend modes
                layer_array = np.array(layer.image).astype(float)
                result_array = np.array(result).astype(float)
                
                if layer.blend_mode == "normal":
                    blended = result_array * (1 - layer.opacity) + layer_array * layer.opacity
                elif layer.blend_mode == "multiply":
                    blended = (result_array * layer_array / 255.0) * layer.opacity + result_array * (1 - layer.opacity)
                else:  # Default to normal
                    blended = result_array * (1 - layer.opacity) + layer_array * layer.opacity
                
                result = Image.fromarray(np.clip(blended, 0, 255).astype(np.uint8))
        
        return result if result else self.base_image.copy()
    
    def _record_operation(self, operation: str, params: Dict[str, Any]):
        """Record an operation in the processing history for reversibility."""
        self.processing_history.append({
            'operation': operation,
            'params': params,
            'layer_count': len(self.layers)
        })
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get image metadata and technical analysis."""
        return self.metadata.copy()
    
    def save(self, output_path: str, flatten: bool = True):
        """
        Save the image.
        
        Args:
            output_path: Path to save the image
            flatten: Whether to flatten layers before saving
        """
        if flatten:
            image_to_save = self.flatten()
        else:
            image_to_save = self.base_image
        
        image_to_save.save(output_path)
        self._record_operation('save', {'path': output_path, 'flatten': flatten})
