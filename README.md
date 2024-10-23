# Video Stitcher

Video Stitcher is a Python tool designed to concatenate three video files (front bumper, content, and rear bumper) into a single output video file. The tool uses encoding and compression settings specified in a configuration file.

## Project Status

This project is currently in development. The basic structure and unit tests have been set up, but the core functionality is not yet implemented.

## Requirements

- Python 3.7+
- Anaconda or Miniconda

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

- `video_stitcher.py`: Main script containing the `VideoStitcher` class (currently in development).
- `tests/`: Directory containing unit tests for the project.
- `environment.yml`: Conda environment file specifying dependencies.

## Usage

Once the project is fully implemented, you will be able to run:

```bash
python video_stitcher.py --config config.yaml
```

Where `config.yaml` contains the settings for video concatenation.

### Running Tests

To run the tests, use:
```bash
pytest tests/
```

## Contributing

Feel free to fork this repository and create pull requests for improvements or feature additions. Ensure that new code is covered by unit tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE.md) file for details.

## Contact

For questions, you can contact the project maintainer, Clark Dever.
