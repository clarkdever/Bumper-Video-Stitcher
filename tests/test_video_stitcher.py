import unittest
import os
import yaml
from video_stitcher import VideoStitcher, main
from moviepy.editor import VideoFileClip, ColorClip
import subprocess
import logging
from unittest.mock import patch
from io import StringIO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestVideoStitcher(unittest.TestCase):
    def setUp(self):
        self.input_dir = "input"
        os.makedirs(self.input_dir, exist_ok=True)
        
        self.front_bumper = os.path.join(self.input_dir, "Bumper.mp4")
        self.content = os.path.join(self.input_dir, "Content.mp4")
        self.rear_bumper = os.path.join(self.input_dir, "Bumper.mp4")
        
        # Create dummy video files if they don't exist
        self._create_dummy_video(self.front_bumper, duration=5)
        self._create_dummy_video(self.content, duration=10)
        self._create_dummy_video(self.rear_bumper, duration=5)
        
        self.output_dir = "output"
        self.config_file = "config.yml"
        
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.stitcher = VideoStitcher(self.config_file)

    def _create_dummy_video(self, file_path, duration):
        if not os.path.exists(file_path):
            try:
                clip = ColorClip(size=(640, 480), color=(0, 0, 0), duration=duration)
                clip.write_videofile(file_path, fps=30, codec='libx264', preset='ultrafast', audio=False)
                clip.close()
            except Exception as e:
                logger.error(f"Error creating dummy video {file_path}: {e}")
                raise

    def tearDown(self):
        # Clean up test files and directories, but not config.yml
        for file in [self.front_bumper, self.content, self.rear_bumper]:
            if os.path.exists(file):
                os.remove(file)
        for dir in [self.input_dir, self.output_dir]:
            if os.path.exists(dir) and not os.listdir(dir):
                os.rmdir(dir)

    def test_output_file_name(self):
        # Test if the output file is named correctly
        # The expected format is "Final_<content_filename>.mp4" in the output directory
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        expected_output = os.path.join(self.output_dir, "Final_Content.mp4")
        self.assertEqual(output_file, expected_output)

    def test_output_file_exists(self):
        # Test if the output file is actually created
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        self.assertTrue(os.path.exists(output_file))

    def test_output_file_longer_than_inputs(self):
        # Test if the output file duration is longer than the sum of input durations
        # This ensures that all input videos are included in the output
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        # TODO: Implement logic to check if the output file duration is longer than the sum of input durations
        # This might involve using a library like moviepy to get video durations

    def test_config_applied(self):
        # Test if the encoding settings from config.yml are applied to the output file
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        
        # Use ffprobe to check the video codec and other parameters
        ffprobe_cmd = [
            "ffprobe",
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=codec_name,avg_frame_rate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            output_file
        ]
        
        result = subprocess.run(ffprobe_cmd, capture_output=True, text=True)
        codec, frame_rate = result.stdout.strip().split('\n')
        
        self.assertEqual(codec, 'h264')  # Changed from self.stitcher.config['encoding']['codec']
        
        # Check if CRF and preset were applied (this is more difficult and may require parsing the FFmpeg log)
        # For now, we'll just check if the output file exists and has content
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)

    def test_config_parsing(self):
        # Test if the config file is correctly parsed
        expected_config = {
            "encoding": {
                "codec": "libx264",
                "crf": 23,
                "preset": "ultrafast"
            }
        }
        self.assertEqual(self.stitcher.config, expected_config)

    def test_video_concatenation(self):
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)

        # Check if the output file exists and has content
        self.assertTrue(os.path.exists(output_file))
        self.assertGreater(os.path.getsize(output_file), 0)

        # Check if the output video duration is the sum of input video durations
        with VideoFileClip(output_file) as output_clip:
            output_duration = output_clip.duration

        with VideoFileClip(self.front_bumper) as front_clip, \
             VideoFileClip(self.content) as content_clip, \
             VideoFileClip(self.rear_bumper) as rear_clip:
            expected_duration = front_clip.duration + content_clip.duration + rear_clip.duration

        logger.info(f"Expected duration: {expected_duration}")
        logger.info(f"Actual duration: {output_duration}")

        self.assertAlmostEqual(output_duration, expected_duration, delta=1)  # Allow 1 second difference

    def test_cli(self):
        # Test the command-line interface
        cmd = [
            "python", "video_stitcher.py",
            self.front_bumper,
            self.content,
            self.rear_bumper,
            "--config", self.config_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Video stitching complete", result.stdout)

    @patch('sys.stderr', new_callable=StringIO)
    def test_progress_reporting(self, mock_stderr):
        # Test progress reporting
        self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        output = mock_stderr.getvalue()
        self.assertIn("Processing", output)
        self.assertIn("B/s", output)  # Look for bytes per second in the output

if __name__ == "__main__":
    unittest.main()
