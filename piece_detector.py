#!/usr/bin/python

import cv2
from utils.shape_detector import ShapeDetector
from utils.color_detector import ColorDetector
from utils.boder_detector import BoderDetector
import argparse
import imutils


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())


# load the image:
image = cv2.imread(args["image"])

# Detect border points:
bd = BoderDetector()
border_points = bd.detect(image)

# Detect circles in image:
sd = ShapeDetector()
circles = sd.detect_circles(image)

# translate points in mm:
