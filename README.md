# Image Loop
Script for creating time lapse videos on a RaspberryPi.

## Usage
`./time_lapse.py [config file]`

### Config File
JSON File with the following keys:
* `width` - width of the video in pixels with default 800.
* `height` - height of the video in pixels with default 600.
* `quality` - jpeg quality of the images comprising the video with default 25.
* `image_dir` - output directory for images take by the camera with default `images/`.
* `video_file` - file into which the video is rendered with default `time_lapse.mp4`.
* `frames_per_second` - frames per second of the final video with default 16.


## Requirements
* `picamera`
* `libav-tools`
