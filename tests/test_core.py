"""
Tests for VISIONFLOW core functionality
"""

import unittest
import numpy as np
from PIL import Image
import tempfile
import os

from visionflow.core.image import VisionFlowImage, ImageLayer


class TestVisionFlowImage(unittest.TestCase):
    """Test VisionFlowImage class."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        self.temp_dir = tempfile.mkdtemp()
        self.test_path = os.path.join(self.temp_dir, 'test.jpg')
        self.test_image.save(self.test_path)
    
    def test_load_from_path(self):
        """Test loading image from path."""
        vf_image = VisionFlowImage(image_path=self.test_path)
        self.assertIsNotNone(vf_image.base_image)
        self.assertEqual(vf_image.base_image.size, (100, 100))
    
    def test_load_from_image(self):
        """Test loading from PIL Image."""
        vf_image = VisionFlowImage(image=self.test_image)
        self.assertIsNotNone(vf_image.base_image)
        self.assertEqual(vf_image.base_image.size, (100, 100))
    
    def test_metadata_analysis(self):
        """Test image metadata analysis."""
        vf_image = VisionFlowImage(image=self.test_image)
        metadata = vf_image.get_metadata()
        
        self.assertEqual(metadata['width'], 100)
        self.assertEqual(metadata['height'], 100)
        self.assertEqual(metadata['aspect_ratio'], 1.0)
        self.assertIn('mean_brightness', metadata)
    
    def test_layer_operations(self):
        """Test layer operations."""
        vf_image = VisionFlowImage(image=self.test_image)
        
        # Should start with one layer (background)
        self.assertEqual(len(vf_image.layers), 1)
        
        # Add a new layer
        new_layer_image = Image.new('RGB', (100, 100), color=(255, 0, 0))
        layer = vf_image.add_layer(new_layer_image, "Red Layer")
        
        self.assertEqual(len(vf_image.layers), 2)
        self.assertEqual(layer.name, "Red Layer")
        
        # Get layer
        retrieved_layer = vf_image.get_layer(1)
        self.assertEqual(retrieved_layer.name, "Red Layer")
        
        # Remove layer
        vf_image.remove_layer(1)
        self.assertEqual(len(vf_image.layers), 1)
    
    def test_flatten(self):
        """Test flattening layers."""
        vf_image = VisionFlowImage(image=self.test_image)
        
        # Add a semi-transparent red layer
        red_layer = Image.new('RGB', (100, 100), color=(255, 0, 0))
        vf_image.add_layer(red_layer, "Red", opacity=0.5)
        
        # Flatten
        result = vf_image.flatten()
        self.assertIsNotNone(result)
        self.assertEqual(result.size, (100, 100))
    
    def test_save(self):
        """Test saving image."""
        vf_image = VisionFlowImage(image=self.test_image)
        output_path = os.path.join(self.temp_dir, 'output.jpg')
        
        vf_image.save(output_path)
        self.assertTrue(os.path.exists(output_path))
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


class TestImageLayer(unittest.TestCase):
    """Test ImageLayer class."""
    
    def test_layer_creation(self):
        """Test creating a layer."""
        image = Image.new('RGB', (50, 50), color=(100, 100, 100))
        layer = ImageLayer(image, "Test Layer", opacity=0.8, blend_mode="normal")
        
        self.assertEqual(layer.name, "Test Layer")
        self.assertEqual(layer.opacity, 0.8)
        self.assertEqual(layer.blend_mode, "normal")
        self.assertTrue(layer.visible)
    
    def test_layer_copy(self):
        """Test copying a layer."""
        image = Image.new('RGB', (50, 50), color=(100, 100, 100))
        layer = ImageLayer(image, "Original")
        
        copied = layer.copy()
        self.assertEqual(copied.name, "Original")
        self.assertIsNot(copied.image, layer.image)


if __name__ == '__main__':
    unittest.main()
