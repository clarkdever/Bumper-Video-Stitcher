import unittest
import os
import yaml
from video_stitcher import VideoStitcher

class TestVideoStitcher(unittest.TestCase):
    def setUp(self):
        # Define paths for test input files and output directory
        self.front_bumper = "test_files/front_bumper.mp4"
        self.content = "test_files/content.mp4"
        self.rear_bumper = "test_files/rear_bumper.mp4"
        self.output_dir = "output"
        self.config_file = "config.yml"
        
        # Ensure the output directory exists
        # This is necessary for the VideoStitcher to save its output
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create a sample config.yml file for testing purposes
        # This mimics the configuration file that would be used in production
        config = {
            "encoding": {
                "codec": "libx264",  # Use H.264 codec for video compression
                "crf": 23,           # Constant Rate Factor for quality-to-filesize balance
                "preset": "medium"   # Encoding speed preset (affects compression efficiency)
            }
        }
        # Write the configuration to a file
        with open(self.config_file, "w") as f:
            yaml.dump(config, f)
        
        # Initialize the VideoStitcher with the test configuration
        self.stitcher = VideoStitcher(self.config_file)

    def test_output_file_name(self):
        # Test if the output file is named correctly
        # The expected format is "Final_<content_filename>.mp4" in the output directory
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        expected_output = os.path.join(self.output_dir, f"Final_content.mp4")
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
        # TODO: Implement logic to check if the output file uses the encoding settings from config.yml
        # This might involve using ffprobe or a similar tool to inspect the video metadata

    def tearDown(self):
        # Clean up test files and directories after each test
        # This ensures a clean state for subsequent tests and avoids leftover files
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))
        os.rmdir(self.output_dir)

if __name__ == "__main__":
    unittest.main()
