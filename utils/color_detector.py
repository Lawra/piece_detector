import cv2
import numpy as np
import imutils
from PIL import Image
from scipy.spatial import KDTree
from webcolors import hex_to_rgb


class ColorDetector:
    available_colors_list = [
        ("#FF0000", "red"),
        ("#008000", "green"),
        ("#FFFF00", "yellow"),
        ("#808080", "grey")
    ]

    def __init__(self):
        pass

    def detect(self, image, contour):
        black = (0, 0, 0)

        # mask the object detected to get de color of this only.
        mask = np.zeros(image.shape, np.uint8)
        cv2.drawContours(mask, [contour], -1, (255, 255, 255), cv2.FILLED)

        result = cv2.bitwise_and(image, mask)
        resized = imutils.resize(result, width=600)

        cv2.imshow("mask", resized)
        cv2.waitKey(0)

        # get most frequent color, except black
        img = Image.fromarray(resized, 'RGB')
        w, h = img.size
        pixels = img.getcolors(w * h)

        most_frequent_pixel = pixels[0]
        if (most_frequent_pixel[1] == black):
            most_frequent_pixel = pixels[1]

        for count, colour in pixels:
            if colour != black and count > most_frequent_pixel[0]:
                most_frequent_pixel = (count, colour)

        return ColorDetector.convert_rgb_to_names(most_frequent_pixel[1])

    def convert_rgb_to_names(rgb_tuple):
        names = []
        rgb_values = []
        for color_hex, color_name in ColorDetector.available_colors_list:
            names.append(color_name)
            rgb_values.append(hex_to_rgb(color_hex))

        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return names[index]
