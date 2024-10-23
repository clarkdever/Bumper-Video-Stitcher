import os
import yaml
import logging
import argparse
import time
import warnings
from tqdm import tqdm
from moviepy.editor import VideoFileClip, concatenate_videoclips

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

    def stitch(self, front_bumper, content, rear_bumper):
        for file in [front_bumper, content, rear_bumper]:
            if not os.path.exists(file):
                logger.error(f"Input file not found: {file}")
                raise FileNotFoundError(f"Input file not found: {file}")

        try:
            logger.info(f"Loading front bumper: {front_bumper}")
            front_clip = self._safe_load_video(front_bumper)
            logger.info(f"Loading content: {content}")
            content_clip = self._safe_load_video(content)
            logger.info(f"Loading rear bumper: {rear_bumper}")
            rear_clip = self._safe_load_video(rear_bumper)

            logger.info(f"Front bumper duration: {front_clip.duration}")
            logger.info(f"Content duration: {content_clip.duration}")
            logger.info(f"Rear bumper duration: {rear_clip.duration}")

            # Concatenate clips
            clips = [front_clip, content_clip, rear_clip]
            final_clip = concatenate_videoclips(clips, method="compose")

            logger.info(f"Final clip duration: {final_clip.duration}")

            # Generate output file name
            content_name = os.path.splitext(os.path.basename(content))[0]
            output_file = os.path.join(self.output_dir, f"Final_{content_name}.mp4")

            logger.info(f"Writing output file: {output_file}")
            self._write_video_with_progress(final_clip, output_file)

            for clip in clips + [final_clip]:
                clip.close()

            return output_file
        except Exception as e:
            logger.error(f"Error processing video files: {e}")
            raise IOError(f"Error processing video files: {e}")

    def _safe_load_video(self, file_path):
        try:
            clip = VideoFileClip(file_path)
            return clip
        except Exception as e:
            logger.error(f"Error loading video file {file_path}: {e}")
            raise IOError(f"Error loading video file {file_path}: {e}")

    def _write_video_with_progress(self, clip, output_file):
        # Start writing the video file
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            clip.write_videofile(output_file, 
                                 codec=self.config['encoding']['codec'],
                                 preset=self.config['encoding']['preset'],
                                 ffmpeg_params=["-crf", str(self.config['encoding']['crf'])],
                                 audio_codec=self.config['encoding']['audio_codec'],
                                 audio_bitrate=self.config['encoding']['audio_bitrate'],
                                 fps=self.config['output']['framerate'],
                                 logger=None)
            for warning in w:
                logger.warning(f"Warning during video writing: {warning.message}")

        # Get the final file size
        file_size = os.path.getsize(output_file)

        # Show a progress bar based on file size
        with tqdm(total=file_size, unit='B', unit_scale=True, desc="Processing") as pbar:
            last_size = 0
            while last_size < file_size:
                current_size = os.path.getsize(output_file)
                pbar.update(current_size - last_size)
                last_size = current_size
                time.sleep(0.1)  # Add a small delay to reduce CPU usage

def main():
    parser = argparse.ArgumentParser(description="Video Stitcher")
    parser.add_argument("front_bumper", help="Path to the front bumper video")
    parser.add_argument("content", help="Path to the main content video")
    parser.add_argument("rear_bumper", help="Path to the rear bumper video")
    parser.add_argument("--config", default="config.yml", help="Path to the configuration file")
    args = parser.parse_args()

    stitcher = VideoStitcher(args.config)
    output_file = stitcher.stitch(args.front_bumper, args.content, args.rear_bumper)
    print(f"Video stitching complete. Output file: {output_file}")

if __name__ == "__main__":
    main()
