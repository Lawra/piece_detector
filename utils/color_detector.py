
import cv2
import numpy as np
import imutils


class ColorDetector:
    def __init__(self):
        pass

    def detect(self, image, contour):
        # initialize the shape name and approximate the contour
        color = "unidentified"

        mask = np.zeros(image.shape, np.uint8)
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), cv2.FILLED)

        result = cv2.bitwise_and(image, mask)
        resized = imutils.resize(result, width=600)
        cv2.imshow("mask", resized)
        cv2.waitKey(0)

        return color
