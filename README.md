# Piece detector

Python script to detect pieces in an image and return their centers position in mm.

## What you need in your system to execute it

- Python 3.7.9
- OpenCV 3.4.2
- imutils
- numpy
- scikit-learn
- scipy
- Pillow

## Usage

Execute in command line in the folder downloaded:

```bash
python .\piece_detector.py --image your_image_file_path
```

Exemple:

```bash
python .\piece_detector.py --image .\test_images\photo01.jpg
```

## raspberry folder

There you can find the code inside the raspberry.
It uses an API to my webside to execute the code for piece detection, it doesn't use the code here.
The robotic arm, executes the main.py inside the raspberry. This code, opens and takes a photo from the raspberry camera, and then send it to the API. Finally send the result to de arm.
