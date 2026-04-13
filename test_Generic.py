import unittest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from PIL import Image
import sys
from heicconvert import SingleConvertHeictoJpeg, BatchConvert

class TestHEICConverter(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.converted_dir = os.path.join(self.test_dir, "Converted")
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_image(self, filename):
        """Create a test image file."""
        img = Image.new('RGB', (100, 100), color='red')
        if filename.lower().endswith('.heic'):
            raise unittest.SkipTest("Pillow HEIF plugin required to create test HEIC files")
        filepath = os.path.join(self.test_dir, filename)
        img.save(filepath)
        return filepath
    
    def test_single_convert_heic_to_jpeg(self):
        """Test converting a single HEIC file to JPEG."""
        heic_file = self.create_test_image("test.heic")
        SingleConvertHeictoJpeg(heic_file)
        
        jpg_file = os.path.join(self.test_dir, "test.jpg")
        self.assertTrue(os.path.exists(jpg_file))
        self.assertFalse(os.path.exists(heic_file))
    
    def test_single_convert_case_insensitive(self):
        """Test that conversion works with uppercase HEIC extension."""
        heic_file = self.create_test_image("test.HEIC")
        SingleConvertHeictoJpeg(heic_file)
        
        jpg_file = os.path.join(self.test_dir, "test.jpg")
        self.assertTrue(os.path.exists(jpg_file))
    
    def test_converted_folder_created(self):
        """Test that Converted folder is created if it doesn't exist."""
        heic_file = self.create_test_image("test.heic")
        SingleConvertHeictoJpeg(heic_file)
        
        self.assertTrue(os.path.exists(self.converted_dir))
    
    def test_invalid_file_handling(self):
        """Test handling of non-existent files."""
        invalid_file = os.path.join(self.test_dir, "nonexistent.heic")
        result = SingleConvertHeictoJpeg(invalid_file)
        self.assertIsNone(result)
    
    @patch('heicconvert.tqdm')
    def test_batch_convert(self, mock_tqdm):
        """Test batch conversion of multiple files."""
        files = [
            self.create_test_image("test1.heic"),
            self.create_test_image("test2.heic"),
        ]
        
        mock_tqdm.return_value = files
        BatchConvert(files, len(files))
        
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test1.jpg")))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test2.jpg")))


if __name__ == '__main__':
    unittest.main()