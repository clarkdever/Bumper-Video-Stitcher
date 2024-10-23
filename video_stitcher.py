import os
import yaml
import logging
import argparse
import subprocess
import re
from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoStitcher:
    def __init__(self, config_file='config.yml'):
        self.config_file = config_file
        self.output_dir = "output"
        self.config = self._parse_config()

    def _parse_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except (yaml.YAMLError, FileNotFoundError) as e:
            logger.error(f"Error parsing config file: {e}. Please ensure config.yml exists and is properly formatted.")
            raise

    def _get_video_duration(self, filename):
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", filename],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        return float(result.stdout)

    def _create_concat_file(self, video_files):
        with open('concat.txt', 'w') as f:
            for video in video_files:
                f.write(f"file '{video}'\n")

    def stitch(self, front_bumper, content, rear_bumper):
        for file in [front_bumper, content, rear_bumper]:
            if not os.path.exists(file):
                logger.error(f"Input file not found: {file}")
                raise FileNotFoundError(f"Input file not found: {file}")

        try:
            print("Preparing to stitch videos...")
            self._create_concat_file([front_bumper, content, rear_bumper])

            total_duration = sum(self._get_video_duration(video) for video in [front_bumper, content, rear_bumper])

            content_name = os.path.splitext(os.path.basename(content))[0]
            output_file = os.path.join(self.output_dir, f"Final_{content_name}.mp4")

            ffmpeg_cmd = [
                "ffmpeg",
                "-f", "concat",
                "-safe", "0",
                "-i", "concat.txt",
                "-c:v", self.config['encoding']['codec'],
                "-preset", self.config['encoding']['preset'],
                "-crf", str(self.config['encoding']['crf']),
                "-c:a", self.config['encoding']['audio_codec'],
                "-b:a", self.config['encoding']['audio_bitrate'],
                "-y",
                output_file
            ]

            print(f"Starting video stitching. This may take a while...")
            print(f"Output file will be: {output_file}")

            process = subprocess.Popen(ffmpeg_cmd, stderr=subprocess.PIPE, universal_newlines=True)

            with tqdm(total=100, desc="Stitching Progress", unit="%") as pbar:
                for line in process.stderr:
                    matches = re.search(r"time=(\d{2}):(\d{2}):(\d{2}\.\d{2})", line)
                    if matches:
                        hours, minutes, seconds = map(float, matches.groups())
                        current_time = hours * 3600 + minutes * 60 + seconds
                        progress = min(100, int(current_time / total_duration * 100))
                        pbar.update(progress - pbar.n)

            return_code = process.wait()
            if return_code != 0:
                raise subprocess.CalledProcessError(return_code, ffmpeg_cmd)

            os.remove('concat.txt')
            print(f"Video stitching complete. Output file: {output_file}")
            return output_file

        except Exception as e:
            logger.error(f"Error processing video files: {e}")
            raise IOError(f"Error processing video files: {e}")

def main():
    parser = argparse.ArgumentParser(description="Video Stitcher")
    parser.add_argument("front_bumper", help="Path to the front bumper video")
    parser.add_argument("content", help="Path to the main content video")
    parser.add_argument("rear_bumper", help="Path to the rear bumper video")
    parser.add_argument("--config", default="config.yml", help="Path to the configuration file")
    args = parser.parse_args()

    stitcher = VideoStitcher(args.config)
    stitcher.stitch(args.front_bumper, args.content, args.rear_bumper)

if __name__ == "__main__":
    main()
