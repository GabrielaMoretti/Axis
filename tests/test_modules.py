"""
Tests for VISIONFLOW modules
"""

import unittest
import numpy as np
from PIL import Image
import tempfile
import os

from visionflow.modules import (
    ImageImporter, ColorCorrector, FocusDepthController,
    LensSimulator, TextureRefiner, StyleCreator
)


class TestImageImporter(unittest.TestCase):
    """Test ImageImporter module."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        self.temp_dir = tempfile.mkdtemp()
        self.test_path = os.path.join(self.temp_dir, 'test.jpg')
        self.test_image.save(self.test_path)
    
    def test_import_image(self):
        """Test importing an image."""
        image = ImageImporter.import_image(self.test_path)
        self.assertIsNotNone(image)
        self.assertEqual(image.size, (100, 100))
    
    def test_analyze_properties(self):
        """Test technical analysis."""
        analysis = ImageImporter.analyze_technical_properties(self.test_image)
        
        self.assertIn('dimensions', analysis)
        self.assertIn('brightness', analysis)
        self.assertIn('channels', analysis)
        self.assertIn('sharpness', analysis)
        
        self.assertEqual(analysis['dimensions']['width'], 100)
        self.assertEqual(analysis['dimensions']['height'], 100)
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)


class TestColorCorrector(unittest.TestCase):
    """Test ColorCorrector module."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new('RGB', (50, 50), color=(128, 128, 128))
    
    def test_white_balance(self):
        """Test white balance adjustment."""
        result = ColorCorrector.adjust_white_balance(self.test_image, 
                                                     temperature=0.2, tint=-0.1)
        self.assertEqual(result.size, self.test_image.size)
        self.assertEqual(result.mode, 'RGB')
    
    def test_exposure(self):
        """Test exposure adjustment."""
        result = ColorCorrector.adjust_exposure(self.test_image, exposure=0.5)
        self.assertEqual(result.size, self.test_image.size)
        
        # Brighter image
        original_brightness = np.mean(np.array(self.test_image))
        result_brightness = np.mean(np.array(result))
        self.assertGreater(result_brightness, original_brightness)
    
    def test_contrast(self):
        """Test contrast adjustment."""
        result = ColorCorrector.adjust_contrast(self.test_image, contrast=1.5)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_saturation(self):
        """Test saturation adjustment."""
        result = ColorCorrector.adjust_saturation(self.test_image, saturation=1.5)
        self.assertEqual(result.size, self.test_image.size)


class TestFocusDepthController(unittest.TestCase):
    """Test FocusDepthController module."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
    
    def test_gaussian_blur(self):
        """Test Gaussian blur."""
        result = FocusDepthController.apply_gaussian_blur(self.test_image, radius=3.0)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_sharpen(self):
        """Test sharpening."""
        result = FocusDepthController.sharpen(self.test_image, strength=1.5)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_tilt_shift(self):
        """Test tilt-shift effect."""
        result = FocusDepthController.apply_tilt_shift(self.test_image, 
                                                       focus_line_y=0.5, 
                                                       focus_width=0.2)
        self.assertEqual(result.size, self.test_image.size)


class TestLensSimulator(unittest.TestCase):
    """Test LensSimulator module."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new('RGB', (100, 100), color=(200, 200, 200))
    
    def test_vignette(self):
        """Test vignette effect."""
        result = LensSimulator.apply_vignette(self.test_image, strength=0.5)
        self.assertEqual(result.size, self.test_image.size)
        
        # Check that edges are darker
        img_array = np.array(result)
        center_brightness = np.mean(img_array[40:60, 40:60])
        edge_brightness = np.mean(img_array[0:10, 0:10])
        self.assertLess(edge_brightness, center_brightness)
    
    def test_chromatic_aberration(self):
        """Test chromatic aberration."""
        result = LensSimulator.apply_chromatic_aberration(self.test_image, strength=2.0)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_bokeh(self):
        """Test bokeh effect."""
        result = LensSimulator.apply_bokeh(self.test_image, blur_amount=5.0)
        self.assertEqual(result.size, self.test_image.size)


class TestTextureRefiner(unittest.TestCase):
    """Test TextureRefiner module."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
    
    def test_denoise(self):
        """Test denoising."""
        result = TextureRefiner.denoise(self.test_image, strength=1.0)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_enhance_details(self):
        """Test detail enhancement."""
        result = TextureRefiner.enhance_details(self.test_image, strength=1.0)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_apply_grain(self):
        """Test grain application."""
        result = TextureRefiner.apply_grain(self.test_image, intensity=0.1, size=1.0)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_apply_clarity(self):
        """Test clarity enhancement."""
        result = TextureRefiner.apply_clarity(self.test_image, amount=0.5)
        self.assertEqual(result.size, self.test_image.size)


class TestStyleCreator(unittest.TestCase):
    """Test StyleCreator module."""
    
    def setUp(self):
        """Create a test image."""
        self.test_image = Image.new('RGB', (100, 100), color=(128, 128, 128))
        self.style_creator = StyleCreator()
    
    def test_get_available_styles(self):
        """Test getting available styles."""
        styles = self.style_creator.get_available_styles()
        self.assertGreater(len(styles), 0)
        self.assertIn('cinematic', styles)
        self.assertIn('vintage', styles)
    
    def test_apply_style(self):
        """Test applying a style."""
        result = self.style_creator.apply_style(self.test_image, 'cinematic', intensity=0.8)
        self.assertEqual(result.size, self.test_image.size)
    
    def test_create_custom_style(self):
        """Test creating custom style."""
        custom_params = {
            'contrast': 1.3,
            'saturation': 1.1,
            'vignette': 0.3
        }
        self.style_creator.create_custom_style('my_style', custom_params)
        
        styles = self.style_creator.get_available_styles()
        self.assertIn('my_style', styles)
    
    def test_color_grade(self):
        """Test color grading."""
        result = StyleCreator.create_color_grade(
            self.test_image,
            shadows=(10, 0, -10),
            midtones=(5, 5, 0),
            highlights=(0, 5, 10)
        )
        self.assertEqual(result.size, self.test_image.size)


if __name__ == '__main__':
    unittest.main()
