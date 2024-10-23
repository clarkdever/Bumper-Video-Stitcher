Certainly! I'll rewrite the README.md to reflect our current project state and discussion. Here's the updated version:

```markdown:README.md
# Video Stitcher

Video Stitcher is a Python tool designed to concatenate three video files (front bumper, content, and rear bumper) into a single output video file. The tool uses encoding and compression settings specified in a configuration file.

## Project Status

This project is currently in development. The basic structure and unit tests have been set up, but the core functionality is not yet implemented.

## Requirements

- Python 3.7+
- Anaconda or Miniconda

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/clarkdever/Bumper-Video-Stitcher.git
   cd video-stitcher
   ```

2. Create and activate the Anaconda environment:
   ```
   conda env create -f environment.yml
   conda activate video-stitcher
   ```

## Project Structure

- `video_stitcher.py`: Main script containing the `VideoStitcher` class (currently a skeleton).
- `tests/test_video_stitcher.py`: Unit tests for the `VideoStitcher` class.
- `config.yml`: Configuration file for encoding and compression settings (to be implemented).
- `environment.yml`: Conda environment specification.
- `LICENSE.md`: MIT License file.

## Development Status

- Basic project structure is set up.
- Unit tests are defined but not all are passing due to incomplete implementation.
- The `VideoStitcher` class is defined with a skeleton `stitch` method.
- Actual video stitching functionality is not yet implemented.

## Next Steps

1. Implement the video stitching logic in the `stitch` method.
2. Complete the command-line interface in `video_stitcher.py`.
3. Finalize and refine unit tests.
4. Implement config file parsing and application of encoding settings.

## Running Tests

To run the unit tests, use the following command:

```
python -m unittest discover tests
```

Note: Currently, most tests will fail due to incomplete implementation.

## Usage

Once implemented, the tool will be used as follows:

```
python video_stitcher.py <front_bumper> <content> <rear_bumper>
```

Replace `<front_bumper>`, `<content>`, and `<rear_bumper>` with the paths to your input video files.

The stitched video will be saved in the `output/` directory with the name `Final_<content_file_name>.mp4`.

## Configuration

Encoding and compression settings will be modifiable in the `config.yml` file. The planned default settings are:

```yaml
encoding:
  codec: libx264
  crf: 23
  preset: medium
```

## Contributing

This project is in its early stages. Contributions, ideas, and feedback are welcome. Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
```