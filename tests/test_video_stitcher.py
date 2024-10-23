import os
import unittest
from unittest.mock import patch, MagicMock
from video_stitcher import VideoStitcher

class TestVideoStitcher(unittest.TestCase):
    @patch('subprocess.run')
    @patch('subprocess.Popen')
    def setUp(self, mock_popen, mock_run):
        self.input_dir = "input"
        os.makedirs(self.input_dir, exist_ok=True)
        
        self.front_bumper = os.path.join(self.input_dir, "Bumper.mp4")
        self.content = os.path.join(self.input_dir, "Content.mp4")
        self.rear_bumper = os.path.join(self.input_dir, "Bumper.mp4")
        
        # Create empty files instead of dummy videos
        for file in [self.front_bumper, self.content, self.rear_bumper]:
            open(file, 'w').close()
        
        self.output_dir = "output"
        self.config_file = "config.yml"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Mock FFmpeg version check
        mock_run.return_value = MagicMock(returncode=0, stdout="ffmpeg version 4.2.2")
        
        self.stitcher = VideoStitcher(self.config_file)

    def tearDown(self):
        # Clean up test files and directories
        
        # IMPORTANT: DO NOT DELETE OR MODIFY THE FOLLOWING LINES
        # These lines ensure we don't delete the original input files
        input_files = [self.front_bumper, self.content, self.rear_bumper]
        # END OF IMPORTANT SECTION

        # Remove the output directory if it's empty
        if os.path.exists(self.output_dir) and not os.listdir(self.output_dir):
            os.rmdir(self.output_dir)
        
        # Remove any temporary files created during the test
        if os.path.exists('concat.txt'):
            os.remove('concat.txt')

        # Add any other cleanup code here, but be careful not to delete input files

    @patch('yaml.safe_load')
    def test_config_parsing(self, mock_yaml_load):
        mock_config = {
            'encoding': {
                'codec': 'libx264',
                'crf': 23,
                'preset': 'medium',
                'audio_codec': 'aac',
                'audio_bitrate': '128k'
            },
            'output': {
                'format': 'mp4'
            }
        }
        mock_yaml_load.return_value = mock_config
        
        config = self.stitcher._parse_config()
        self.assertEqual(config, mock_config)

    def test_create_concat_file(self):
        self.stitcher._create_concat_file([self.front_bumper, self.content, self.rear_bumper])
        self.assertTrue(os.path.exists('concat.txt'))
        with open('concat.txt', 'r') as f:
            content = f.read()
        self.assertIn(self.front_bumper, content)
        self.assertIn(self.content, content)
        self.assertIn(self.rear_bumper, content)
        os.remove('concat.txt')

    @patch('subprocess.run')
    def test_get_video_duration(self, mock_run):
        mock_run.return_value = MagicMock(stdout=b"5.0")
        duration = self.stitcher._get_video_duration(self.front_bumper)
        self.assertEqual(duration, 5.0)

    @patch.object(VideoStitcher, '_get_video_duration')
    @patch('subprocess.Popen')
    @patch('os.remove')
    def test_stitch(self, mock_remove, mock_popen, mock_get_duration):
        mock_get_duration.return_value = 5.0  # Mock the duration method
        
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stderr = iter([
            "frame=   10 fps=0.0 q=-1.0 size=       0kB time=00:00:01.00 bitrate=   0.0kbits/s speed=   0x    \n",
            "frame=   20 fps=0.0 q=-1.0 size=     128kB time=00:00:02.00 bitrate= 524.8kbits/s speed=1.99x    \n",
            "frame=   30 fps=0.0 q=-1.0 size=     256kB time=00:00:03.00 bitrate= 698.4kbits/s speed=1.99x    \n",
        ])
        mock_process.wait.return_value = 0
        mock_popen.return_value = mock_process

        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        
        self.assertTrue(output_file.startswith(self.output_dir))
        self.assertTrue(output_file.endswith('.mp4'))
        mock_popen.assert_called_once()
        mock_remove.assert_called_once_with('concat.txt')

if __name__ == '__main__':
    unittest.main()
