# Video Stitcher

Video Stitcher is a Python application that combines a front bumper video, main content video, and rear bumper video into a single output video.

## Features

- Combines three video files (front bumper, main content, rear bumper) into one
- Configurable encoding settings via YAML configuration file
- Progress bar to show stitching progress
- Error handling and logging

## Requirements

- Python 3.8
- FFmpeg

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/clarkdever/Bumper-Video-Stitcher.git
   cd Bumper-Video-Stitcher
   ```

2. Create and activate the Anaconda environment:
   ```bash
   conda env create -f environment.yml
   conda activate video-stitcher
   ```

## Project Structure

- `video_stitcher.py`: Main script containing the `VideoStitcher` class.
- `tests/`: Directory containing unit tests for the project.
- `environment.yml`: Conda environment file specifying dependencies.

## Usage

1. Ensure you have a `config.yml` file in the project root directory. Example:
   ```yaml
   encoding:
     codec: libx264
     crf: 23
     preset: medium
     audio_codec: aac
     audio_bitrate: 128k
   output:
     format: mp4
   ```

2. Run the script with the following command:
   ```bash
   python video_stitcher.py path/to/front_bumper.mp4 path/to/content.mp4 path/to/rear_bumper.mp4
   ```

   You can also specify a custom config file:
   ```bash
   python video_stitcher.py path/to/front_bumper.mp4 path/to/content.mp4 path/to/rear_bumper.mp4 --config path/to/custom_config.yml
   ```

3. The stitched video will be saved in the `output` directory.

## Running Tests

To run the unit tests, use the following command:
```bash
pytest tests/test_video_stitcher.py -v
```

## Contributing

Feel free to fork this repository and create pull requests for improvements or feature additions. Ensure that new code is covered by unit tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

## Contact

For questions, you can contact the project maintainer, Clark Dever.
