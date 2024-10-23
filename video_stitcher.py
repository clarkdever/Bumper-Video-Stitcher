import os
import yaml
from moviepy.editor import VideoFileClip, concatenate_videoclips
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VideoStitcher:
    def __init__(self, config_file):
        self.config_file = config_file
        self.output_dir = "output"
        self.config = self._parse_config()

    def _parse_config(self):
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing config file: {e}")

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
            final_clip.write_videofile(output_file, codec=self.config['encoding']['codec'],
                                       preset=self.config['encoding']['preset'],
                                       ffmpeg_params=["-crf", str(self.config['encoding']['crf'])])

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

if __name__ == "__main__":
    # Implement command-line interface here
    pass
