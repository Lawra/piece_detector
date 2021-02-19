#!/usr/bin/python

import cv2
from pyimagesearch.shape_detector import ShapeDetector
from pyimagesearch.color_detector import ColorDetector
import argparse
import imutils


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
args = vars(ap.parse_args())


# load the image and resize it to a smaller factor so that
# the shapes can be approximated better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])
# convert the resized image to grayscale, blur it slightly,
# and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresh = cv2.threshold(blurred, 120, 255, cv2.THRESH_BINARY_INV)[1]

# cv2.imshow('thresh', thresh)
# cv2.waitKey(0)

# find contours in the thresholded image and initialize the
# shape detector
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
sd = ShapeDetector()
cd = ColorDetector()

# loop over the contours
for c in cnts:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(c)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape = sd.detect(c)
    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    c = c.astype("float")
    c *= ratio
    c = c.astype("int")

    color = cd.detect(image, c)
    cv2.drawContours(image, [c], -1, (0, 0, 255), 2)

    cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
                4, (255, 255, 255), 4)
    cv2.putText(image, '('+str(cX) + ', ' + str(cY)+')', (cX, cY+100), cv2.FONT_HERSHEY_SIMPLEX,
                2.5, (255, 255, 255), 4)
    image = cv2.circle(image, (cX, cY), radius=8,
                       color=(0, 0, 255), thickness=-1)
    # show the output image
    # cv2.imshow("Image", image)
    # cv2.waitKey(0)
    print('Shape: ' + shape)
    print('Center: ' + str(cX) + ', ' + str(cY))
    print('Image size: ' + str(image.shape[0]) + ', ' + str(image.shape[1]))


resized = imutils.resize(image, width=600)
cv2.imshow("Image resized", resized)
cv2.waitKey(0)
