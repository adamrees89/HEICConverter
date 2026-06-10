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

    def test_single_convert_saves_jpeg_and_moves_source(self):
        """Test that conversion writes a JPEG and moves the original to Converted/."""
        source = Path(self.test_dir) / "sample.heic"
        source.write_bytes(b"fake-heic-data")

        fake_image = MagicMock()

        with patch('heicconvert.Image.open', return_value=fake_image), \
             patch('heicconvert.os.rename') as mock_rename:
            SingleConvertHeictoJpeg(str(source))

        fake_image.save.assert_called_once_with(
            str(source.with_suffix('.jpg')),
            'JPEG',
            quality=90,
            optimize=False,
            progressive=False,
        )
        mock_rename.assert_called_once_with(
            str(source),
            str(Path(self.test_dir) / 'Converted' / 'sample.heic'),
        )

    def test_single_convert_handles_open_error(self):
        """Test that image open failures are handled without crashing."""
        source = Path(self.test_dir) / "broken.heic"
        source.write_bytes(b"not-a-real-heic")

        with patch('heicconvert.Image.open', side_effect=OSError('bad image')), \
             patch('heicconvert.tqdm.write') as mock_write:
            result = SingleConvertHeictoJpeg(str(source))

        self.assertIsNone(result)
        mock_write.assert_called_once()

    def test_batch_convert_uses_executor_and_progress_bar(self):
        """Test batch conversion delegates work through the process pool and progress bar."""
        files = [os.path.join(self.test_dir, 'a.heic'), os.path.join(self.test_dir, 'b.heic')]

        class DummyExecutor:
            def __init__(self):
                self.map_calls = []

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def map(self, func, iterable, chunksize=1):
                self.map_calls.append((func, list(iterable), chunksize))
                return [func(path) for path in iterable]

        dummy_executor = DummyExecutor()

        with patch('heicconvert.concurrent.futures.ProcessPoolExecutor', return_value=dummy_executor) as mock_executor, \
             patch('heicconvert.tqdm', side_effect=lambda iterable, total=None: list(iterable)) as mock_tqdm:
            BatchConvert(files, len(files))

        mock_executor.assert_called_once()
        self.assertEqual(len(dummy_executor.map_calls), 1)
        self.assertEqual(dummy_executor.map_calls[0][1], files)
        mock_tqdm.assert_called_once()

#Just a test comment for PR purposes.

if __name__ == '__main__':
    unittest.main()
