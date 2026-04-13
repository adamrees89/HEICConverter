import unittest
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
from PIL import Image
import sys
import re
import heicconvert

class TestHEICConverter(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.converted_dir = os.path.join(self.test_dir, "Converted")
    
    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def create_test_image(self, filename):
        """Create a test image file."""
        img = Image.new('RGB', (100, 100), color='red')
        filepath = os.path.join(self.test_dir, filename)
        # Save as PNG first, then rename to .heic if needed
        if filename.lower().endswith('.heic'):
            png_path = filepath.replace('.heic', '.png').replace('.HEIC', '.png')
            img.save(png_path)
            os.rename(png_path, filepath)
        else:
            img.save(filepath)
        return filepath
    
    def test_single_convert_heic_to_jpeg(self):
        """Test converting a single HEIC file to JPEG."""
        heic_file = self.create_test_image("test.heic")
        with patch('heicconvert.Image.open') as mock_open, \
             patch('heicconvert.Image.new') as mock_new:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            heicconvert.SingleConvertHeictoJpeg(heic_file)
            mock_img.save.assert_called()
    
    def test_single_convert_case_insensitive(self):
        """Test that conversion works with uppercase HEIC extension."""
        heic_file = self.create_test_image("test.HEIC")
        with patch('heicconvert.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            heicconvert.SingleConvertHeictoJpeg(heic_file)
            mock_img.save.assert_called()
    
    def test_single_convert_mixed_case(self):
        """Test that conversion works with mixed case HEIC extension."""
        heic_file = self.create_test_image("test.Heic")
        with patch('heicconvert.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            heicconvert.SingleConvertHeictoJpeg(heic_file)
            mock_img.save.assert_called()
    
    def test_converted_folder_created(self):
        """Test that Converted folder is created if it doesn't exist."""
        heic_file = self.create_test_image("test.heic")
        with patch('heicconvert.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            heicconvert.SingleConvertHeictoJpeg(heic_file)
        self.assertTrue(os.path.exists(self.converted_dir))
    
    def test_invalid_file_handling(self):
        """Test handling of non-existent files."""
        invalid_file = os.path.join(self.test_dir, "nonexistent.heic")
        with patch('heicconvert.tqdm.write'):
            result = heicconvert.SingleConvertHeictoJpeg(invalid_file)
        self.assertIsNone(result)
    
    def test_heic_moved_to_converted(self):
        """Test that HEIC file is moved to Converted folder after conversion."""
        heic_file = self.create_test_image("test.heic")
        with patch('heicconvert.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            heicconvert.SingleConvertHeictoJpeg(heic_file)
        # After conversion, original HEIC should be moved to Converted folder
        self.assertFalse(os.path.exists(heic_file))
        converted_heic = os.path.join(self.converted_dir, "test.heic")
        self.assertTrue(os.path.exists(converted_heic))
    
    def test_jpg_saved_in_source_dir(self):
        """Test that JPG is saved in the same directory as source HEIC."""
        heic_file = self.create_test_image("test.heic")
        with patch('heicconvert.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            heicconvert.SingleConvertHeictoJpeg(heic_file)
            # Verify save was called with jpg path in source directory
            saved_path = mock_img.save.call_args[0][0]
            self.assertTrue(saved_path.endswith('.jpg'))
            self.assertTrue(saved_path.startswith(self.test_dir))
    
    def test_regex_extension_replacement(self):
        """Test that extension replacement works correctly."""
        heic_file = self.create_test_image("photo.HEIC")
        expected_jpg = heic_file.replace('.HEIC', '.jpg')
        with patch('heicconvert.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            heicconvert.SingleConvertHeictoJpeg(heic_file)
            # Verify the path passed to save has .jpg extension
            saved_path = mock_img.save.call_args[0][0]
            self.assertTrue(saved_path.endswith('.jpg'))
    
    @patch('heicconvert.register_heif_opener')
    @patch('heicconvert.tqdm')
    @patch('heicconvert.concurrent.futures.ThreadPoolExecutor')
    def test_batch_convert_calls_register_heif(self, mock_executor_class, mock_tqdm, mock_register):
        """Test that BatchConvert calls register_heif_opener."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor
        mock_executor.map.return_value = []
        mock_tqdm.return_value = []
        
        heicconvert.BatchConvert([], 0)
        mock_register.assert_called_once()
    
    @patch('heicconvert.register_heif_opener')
    @patch('heicconvert.tqdm')
    @patch('heicconvert.concurrent.futures.ThreadPoolExecutor')
    def test_batch_convert_uses_thread_pool(self, mock_executor_class, mock_tqdm, mock_register):
        """Test that BatchConvert uses ThreadPoolExecutor."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor
        mock_executor.map.return_value = []
        mock_tqdm.return_value = []
        
        files = ["file1.heic", "file2.heic"]
        heicconvert.BatchConvert(files, len(files))
        
        mock_executor.map.assert_called_once()
    
    @patch('heicconvert.register_heif_opener')
    @patch('heicconvert.tqdm')
    @patch('heicconvert.concurrent.futures.ThreadPoolExecutor')
    def test_batch_convert_passes_correct_params(self, mock_executor_class, mock_tqdm, mock_register):
        """Test that BatchConvert passes correct parameters to ThreadPoolExecutor.map."""
        mock_executor = MagicMock()
        mock_executor_class.return_value.__enter__.return_value = mock_executor
        mock_executor.map.return_value = []
        mock_tqdm.return_value = []
        
        files = ["file1.heic", "file2.heic"]
        heicconvert.BatchConvert(files, 2)
        
        # Verify map was called with correct chunksize
        call_kwargs = mock_executor.map.call_args[1]
        self.assertEqual(call_kwargs['chunksize'], 3)
    
    def test_exception_message_format(self):
        """Test that exception messages are formatted correctly."""
        invalid_file = os.path.join(self.test_dir, "nonexistent.heic")
        with patch('heicconvert.tqdm.write') as mock_write:
            heicconvert.SingleConvertHeictoJpeg(invalid_file)
            mock_write.assert_called_once()
            message = mock_write.call_args[0][0]
            self.assertIn("Open/save failed", message)
            self.assertIn(invalid_file, message)
    
    def test_nested_directory_structure(self):
        """Test conversion with nested directory structure."""
        nested_dir = os.path.join(self.test_dir, "subdir")
        os.makedirs(nested_dir)
        heic_file = os.path.join(nested_dir, "test.heic")
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(heic_file + '.png')
        os.rename(heic_file + '.png', heic_file)
        
        with patch('heicconvert.Image.open') as mock_open:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            heicconvert.SingleConvertHeictoJpeg(heic_file)
        
        converted_heic = os.path.join(nested_dir, "Converted", "test.heic")
        self.assertTrue(os.path.exists(converted_heic))
    
    def test_multiple_files_conversion(self):
        """Test converting multiple files in sequence."""
        files = ["file1.heic", "file2.heic", "file3.heic"]
        for filename in files:
            heic_file = self.create_test_image(filename)
            with patch('heicconvert.Image.open') as mock_open:
                mock_img = MagicMock()
                mock_open.return_value = mock_img
                heicconvert.SingleConvertHeictoJpeg(heic_file)
        
        # Verify all original files were moved
        for filename in files:
            original_file = os.path.join(self.test_dir, filename)
            self.assertFalse(os.path.exists(original_file))
    
    def test_path_object_handling(self):
        """Test that Path objects are handled correctly."""
        heic_file = self.create_test_image("test.heic")
        with patch('heicconvert.Image.open') as mock_open, \
             patch('heicconvert.Path') as mock_path_class:
            mock_img = MagicMock()
            mock_open.return_value = mock_img
            mock_path_obj = MagicMock()
            mock_path_obj.parent = Path(self.test_dir)
            mock_path_class.return_value = mock_path_obj
            
            heicconvert.SingleConvertHeictoJpeg(heic_file)
            mock_path_class.assert_called_once_with(heic_file)


if __name__ == '__main__':
    unittest.main()