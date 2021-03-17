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
img_height, img_width, chanels = image.shape

result_img = image.copy()

# Detect border points:
bd = BoderDetector()
border_points = bd.detect(image)
for key in border_points:
    cv2.circle(result_img, (border_points[key][0], border_points[key][1]), radius=10, color=(
        0, 0, 255), thickness=-1)
    cv2.putText(result_img, key, (border_points[key][0], border_points[key][1]), cv2.FONT_HERSHEY_SIMPLEX,
                4, (0, 0, 0), 4)

# Compute perspective correction transform
image_trans = bd.perspective_transform(image, border_points)

# Detect circles in image:
sd = ShapeDetector()
# sd.display_image(image_trans, "image_trans")
circles = sd.detect_circles(image_trans)

for i in circles:
    # draw the outer circle
    cv2.circle(image_trans, (i[0], i[1]), i[2], (0, 255, 0), 6)
    # draw the center of the circle
    cv2.circle(image_trans, (i[0], i[1]), 2, (0, 0, 255), 10)

# sd.display_image(image_trans, "circles")

# translate points in mm:
for point in circles:
    result = bd.convert_px_to_mm(point[:2], img_width, img_height)
    cv2.putText(image_trans, str(
        result), (point[0], point[1]),  cv2.FONT_HERSHEY_SIMPLEX,  3.5, (255, 255, 255), 7)

# sd.display_image(image_trans, "result_img")
