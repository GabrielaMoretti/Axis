"""
Tests for VISIONFLOW pipeline
"""

import unittest
from PIL import Image

from visionflow.pipeline import Pipeline, PipelinePreset, PipelineOperation
from visionflow.modules import ColorCorrector


class TestPipeline(unittest.TestCase):
    """Test Pipeline class."""
    
    def setUp(self):
        """Create a test image and pipeline."""
        self.test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        self.pipeline = Pipeline("Test Pipeline")
    
    def test_add_operation(self):
        """Test adding operations to pipeline."""
        self.pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, 
                                   {'contrast': 1.2})
        
        self.assertEqual(len(self.pipeline.operations), 1)
        self.assertEqual(self.pipeline.operations[0].name, "Contrast")
    
    def test_execute_pipeline(self):
        """Test executing pipeline."""
        self.pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, 
                                   {'contrast': 1.2})
        self.pipeline.add_operation("Saturation", ColorCorrector.adjust_saturation, 
                                   {'saturation': 1.1})
        
        result = self.pipeline.execute(self.test_image, save_snapshots=True)
        
        self.assertIsNotNone(result)
        self.assertEqual(result.size, self.test_image.size)
        
        # Check snapshots
        self.assertEqual(len(self.pipeline.snapshots), 3)  # Initial + 2 operations
    
    def test_remove_operation(self):
        """Test removing operation."""
        self.pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, 
                                   {'contrast': 1.2})
        self.pipeline.add_operation("Saturation", ColorCorrector.adjust_saturation, 
                                   {'saturation': 1.1})
        
        self.pipeline.remove_operation(0)
        self.assertEqual(len(self.pipeline.operations), 1)
    
    def test_insert_operation(self):
        """Test inserting operation."""
        self.pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, 
                                   {'contrast': 1.2})
        self.pipeline.insert_operation(0, "Saturation", ColorCorrector.adjust_saturation, 
                                      {'saturation': 1.1})
        
        self.assertEqual(len(self.pipeline.operations), 2)
        self.assertEqual(self.pipeline.operations[0].name, "Saturation")
    
    def test_get_snapshot(self):
        """Test getting snapshots."""
        self.pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, 
                                   {'contrast': 1.2})
        
        result = self.pipeline.execute(self.test_image, save_snapshots=True)
        
        snapshot_0 = self.pipeline.get_snapshot(0)  # Initial
        snapshot_1 = self.pipeline.get_snapshot(1)  # After contrast
        
        self.assertIsNotNone(snapshot_0)
        self.assertIsNotNone(snapshot_1)
    
    def test_save_load_pipeline(self):
        """Test saving and loading pipeline configuration."""
        self.pipeline.add_operation("Contrast", ColorCorrector.adjust_contrast, 
                                   {'contrast': 1.2})
        
        # Save
        config = self.pipeline.save_pipeline()
        self.assertIn('name', config)
        self.assertIn('operations', config)
        self.assertEqual(len(config['operations']), 1)
        
        # Load
        new_pipeline = Pipeline()
        function_registry = {'Contrast': ColorCorrector.adjust_contrast}
        new_pipeline.load_pipeline(config, function_registry)
        
        self.assertEqual(new_pipeline.name, self.pipeline.name)
        self.assertEqual(len(new_pipeline.operations), 1)


class TestPipelinePresets(unittest.TestCase):
    """Test pipeline presets."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
    
    def test_portrait_retouch_preset(self):
        """Test portrait retouch preset."""
        pipeline = PipelinePreset.portrait_retouch()
        self.assertIsNotNone(pipeline)
        self.assertGreater(len(pipeline.operations), 0)
        
        result = pipeline.execute(self.test_image)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_landscape_enhancement_preset(self):
        """Test landscape enhancement preset."""
        pipeline = PipelinePreset.landscape_enhancement()
        self.assertIsNotNone(pipeline)
        self.assertGreater(len(pipeline.operations), 0)
        
        result = pipeline.execute(self.test_image)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_cinematic_look_preset(self):
        """Test cinematic look preset."""
        pipeline = PipelinePreset.cinematic_look()
        self.assertIsNotNone(pipeline)
        self.assertGreater(len(pipeline.operations), 0)
        
        result = pipeline.execute(self.test_image)
        self.assertEqual(result.size, self.test_image.size)


if __name__ == '__main__':
    unittest.main()
