# Enhanced video capture mode (enhancer.py)
## Configuration:
Edit the file [config.json](config.json) to set up the video capture process.
#### fourcc
4-CC code for the video, e.g. "mp4v",
#### date_time_fmt
Format of the date/time when the script is started, to be used in the video output filename. 
Example value: "%Y%m%d_%H%M%S",
#### mp4_filename_fmt
Format of the video output filename that will be set with the date/time when the script is started where "%s" in the
format string.
Example value: "C:\\Users\\Public\\Videos\\output_%s.mp4",
#### vidcap_camera_index
Video source number on the PC to use.
Example value: 0
This can be set to a URL string as well, for IP cameras, as OpenCV supports capture from such devices.
Example value: "http://192.168.1.101/video"

## Usage:
To execute the process, run [enhancer.py](enhancer.py) with your locally installed python3 interpreter
as per normal python procedures.

To switch between different enhancement settings:
Press "L" to change the image "levels" setting.
Levels Modes: None, "harsh" (100% auto-adjusted levels), "friendly" (50% adjusted)
Default mode: "friendly"
Press "S" to change the image sharpening setting.
Sharpening Modes: None, "harsh" (100% auto-adjusted levels), "friendly" (50% adjusted)
Default mode: "friendly"

To record video, press "V" to start/stop video capture.
To take a snapshot, press "P".

# Dependencies:
This project requires the module [pyopencv](https://pypi.org/project/pyopencv/).
You can install it using [pip](https://pypi.org/project/pip/):
run `pip install pyopencv` as per normal [python](https://www.python.org/) procedures.
pyopencv requires a local [OpenCV](https://opencv.org/) installation; please see its documentation for help with that.

