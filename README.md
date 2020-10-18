# Cascade Classifier Training Helper

This scripts is designed to help capture images from an oCam usb camera and save the image and other required annotation information to train the OpenCV Cascade Classifier. See [here](https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html) for details on training the OpenCV Cascade Classifier.

## Included files:
- `captureImage.py` - the main executable
- `liboCams.py` - python file to initialize an oCam usb camera. This file was downloaded from [this product page](http://withrobot.com/en/camera/ocam-1cgn-u-t/) and modified so that it was usable. See comments at the top of the file for details on what was modified.

## How to use:
- Make sure the `captureImage.py` file is made executable. `chmod +x captureImage.py`
- run using `./captureImage.py` or `python captureImage.py` with additional options if desired.

```
Options:
  -h, --help            show this help message and exit
  -d DIR, --directory=DIR
                        directory to store the images
  -t INFO_FILE, --textfile=INFO_FILE
                        info file to train opencv cascade classifier
  -a ANNOTATE, --annotation=ANNOTATE
                        Set to 0 if you only want to save an image and skip
                        the annotation
  -f FORMAT, --format=FORMAT
                        Set the format of the camera
```

- If the -f option is not set, the user will be prompted to enter in the desired format number from a list printed to the terminal.

- After the camera has been initialized, the live camera feed will be displayed on the screen.
  - Press `s` to save the current image
  - Press 'q' or 'ESC' to exit the program


- After pressing `s`, the image will be saved in the provided or default directory, the live feed will close, and a new window with the saved image will be opened.
  - Click and drag to define a bounding rectangle around the section of the image containing the object you want to identify.
  - Press `ESC` to cancel the annotation and delete the most recent image.

- After clicking and dragging, the rectangle will be displayed on the image
  - Press `y` to confirm the rectangle and save the parameters
  - Press `n` to redraw the rectangle and try again

- The annotation information will be appended to the default/provided info file.


This package tested using python 2 on Ubuntu 18 LTS. There was a conflict the `fnctl` package when trying to run with python 3.
