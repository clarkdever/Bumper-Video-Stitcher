import unittest
import os
import yaml
from video_stitcher import VideoStitcher

class TestVideoStitcher(unittest.TestCase):
    def setUp(self):
        self.front_bumper = "test_files/front_bumper.mp4"
        self.content = "test_files/content.mp4"
        self.rear_bumper = "test_files/rear_bumper.mp4"
        self.output_dir = "output"
        self.config_file = "config.yml"
        
        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Create a sample config.yml for testing
        config = {
            "encoding": {
                "codec": "libx264",
                "crf": 23,
                "preset": "medium"
            }
        }
        with open(self.config_file, "w") as f:
            yaml.dump(config, f)
        
        self.stitcher = VideoStitcher(self.config_file)

    def test_output_file_name(self):
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        expected_output = os.path.join(self.output_dir, f"Final_content.mp4")
        self.assertEqual(output_file, expected_output)

    def test_output_file_exists(self):
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        self.assertTrue(os.path.exists(output_file))

    def test_output_file_longer_than_inputs(self):
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        # Implement logic to check if the output file duration is longer than the sum of input durations

    def test_config_applied(self):
        output_file = self.stitcher.stitch(self.front_bumper, self.content, self.rear_bumper)
        # Implement logic to check if the output file uses the encoding settings from config.yml

    def tearDown(self):
        # Clean up test files and directories
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))
        os.rmdir(self.output_dir)

if __name__ == "__main__":
    unittest.main()

