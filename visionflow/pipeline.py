"""
Modular and Reversible Pipeline
Provides a structured workflow for image editing operations.
"""

from typing import List, Dict, Any, Optional, Callable
from PIL import Image
import copy
from visionflow.core.image import VisionFlowImage


class PipelineOperation:
    """Represents a single operation in the pipeline."""
    
    def __init__(self, name: str, function: Callable, params: Dict[str, Any]):
        """
        Initialize a pipeline operation.
        
        Args:
            name: Operation name
            function: Function to execute
            params: Parameters for the function
        """
        self.name = name
        self.function = function
        self.params = params
        self.result_image = None
    
    def execute(self, image: Image.Image) -> Image.Image:
        """Execute the operation on an image."""
        self.result_image = self.function(image, **self.params)
        return self.result_image


class Pipeline:
    """
    Modular and reversible image processing pipeline.
    Allows building complex workflows with easy modification and reversal.
    """
    
    def __init__(self, name: str = "Untitled Pipeline"):
        """
        Initialize a pipeline.
        
        Args:
            name: Pipeline name
        """
        self.name = name
        self.operations: List[PipelineOperation] = []
        self.snapshots: Dict[int, Image.Image] = {}
    
    def add_operation(self, name: str, function: Callable, 
                     params: Dict[str, Any]) -> 'Pipeline':
        """
        Add an operation to the pipeline.
        
        Args:
            name: Operation name
            function: Function to execute
            params: Parameters for the function
            
        Returns:
            Self for method chaining
        """
        operation = PipelineOperation(name, function, params)
        self.operations.append(operation)
        return self
    
    def execute(self, image: Image.Image, 
               save_snapshots: bool = True) -> Image.Image:
        """
        Execute the entire pipeline on an image.
        
        Args:
            image: Input PIL Image
            save_snapshots: Whether to save intermediate results
            
        Returns:
            Final processed image
        """
        current_image = image.copy()
        
        if save_snapshots:
            self.snapshots[0] = current_image.copy()
        
        for i, operation in enumerate(self.operations):
            current_image = operation.execute(current_image)
            
            if save_snapshots:
                self.snapshots[i + 1] = current_image.copy()
        
        return current_image
    
    def execute_partial(self, image: Image.Image, 
                       up_to_step: int) -> Image.Image:
        """
        Execute pipeline up to a specific step.
        
        Args:
            image: Input PIL Image
            up_to_step: Step number to execute up to
            
        Returns:
            Partially processed image
        """
        current_image = image.copy()
        
        for i, operation in enumerate(self.operations):
            if i >= up_to_step:
                break
            current_image = operation.execute(current_image)
        
        return current_image
    
    def remove_operation(self, index: int):
        """Remove an operation from the pipeline by index."""
        if 0 <= index < len(self.operations):
            self.operations.pop(index)
    
    def insert_operation(self, index: int, name: str, 
                        function: Callable, params: Dict[str, Any]):
        """Insert an operation at a specific position."""
        operation = PipelineOperation(name, function, params)
        self.operations.insert(index, operation)
    
    def get_snapshot(self, step: int) -> Optional[Image.Image]:
        """Get a saved snapshot from a specific step."""
        return self.snapshots.get(step)
    
    def clear_operations(self):
        """Clear all operations from the pipeline."""
        self.operations.clear()
        self.snapshots.clear()
    
    def get_operation_list(self) -> List[Dict[str, Any]]:
        """Get a list of all operations in the pipeline."""
        return [
            {
                'name': op.name,
                'params': op.params
            }
            for op in self.operations
        ]
    
    def save_pipeline(self) -> Dict[str, Any]:
        """
        Save pipeline configuration for later use.
        
        Returns:
            Dictionary containing pipeline configuration
        """
        return {
            'name': self.name,
            'operations': [
                {
                    'name': op.name,
                    'params': op.params
                }
                for op in self.operations
            ]
        }
    
    def load_pipeline(self, config: Dict[str, Any], 
                     function_registry: Dict[str, Callable]):
        """
        Load pipeline from configuration.
        
        Args:
            config: Pipeline configuration dictionary
            function_registry: Dictionary mapping operation names to functions
        """
        self.name = config.get('name', 'Untitled Pipeline')
        self.operations.clear()
        
        for op_config in config.get('operations', []):
            name = op_config['name']
            params = op_config['params']
            
            if name in function_registry:
                self.add_operation(name, function_registry[name], params)


class PipelinePreset:
    """Predefined pipelines for common workflows."""
    
    @staticmethod
    def portrait_retouch() -> Pipeline:
        """Create a portrait retouching pipeline."""
        from visionflow.modules import ColorCorrector, TextureRefiner
        
        pipeline = Pipeline("Portrait Retouch")
        pipeline.add_operation("Denoise", TextureRefiner.denoise, {'strength': 1.5})
        pipeline.add_operation("Smooth Skin", TextureRefiner.smooth_skin, {'smoothness': 0.4})
        pipeline.add_operation("Enhance Details", TextureRefiner.enhance_details, {'strength': 0.5})
        pipeline.add_operation("Color Correction", ColorCorrector.adjust_saturation, {'saturation': 1.1})
        
        return pipeline
    
    @staticmethod
    def landscape_enhancement() -> Pipeline:
        """Create a landscape enhancement pipeline."""
        from visionflow.modules import ColorCorrector, TextureRefiner, LensSimulator
        
        pipeline = Pipeline("Landscape Enhancement")
        pipeline.add_operation("Clarity", TextureRefiner.apply_clarity, {'amount': 0.7})
        pipeline.add_operation("Saturation", ColorCorrector.adjust_saturation, {'saturation': 1.2})
        pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, {'contrast': 1.15})
        pipeline.add_operation("Vignette", LensSimulator.apply_vignette, {'strength': 0.2})
        
        return pipeline
    
    @staticmethod
    def cinematic_look() -> Pipeline:
        """Create a cinematic look pipeline."""
        from visionflow.modules import ColorCorrector, LensSimulator, TextureRefiner, StyleCreator
        
        pipeline = Pipeline("Cinematic Look")
        pipeline.add_operation("White Balance", ColorCorrector.adjust_white_balance, 
                             {'temperature': 0.1, 'tint': -0.05})
        pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, {'contrast': 1.2})
        pipeline.add_operation("Saturation", ColorCorrector.adjust_saturation, {'saturation': 0.9})
        pipeline.add_operation("Vignette", LensSimulator.apply_vignette, {'strength': 0.3})
        pipeline.add_operation("Grain", TextureRefiner.apply_grain, {'intensity': 0.05})
        
        return pipeline
