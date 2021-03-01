import cv2
import numpy as np
import imutils
from PIL import Image
from scipy.spatial import KDTree
from webcolors import hex_to_rgb
from collections import defaultdict
import operator


class ColorDetector:
    available_colors_list = [
        ((0, 0, 0), "black"),
        ((255, 255, 255), "white"),
        ((255, 0, 0), "red"),
        ((0, 128, 0), "green"),
        ((255, 255, 0), "yellow"),
        ((0, 255, 0), "lime"),
        ((0, 255, 255), "cian"),
        ((255, 0, 255), "magenta"),
        ((192, 192, 192), "silver"),
        ((128, 128, 128), "grey"),
        ((128, 0, 0), "maroon"),
        ((128, 128, 0), "olive"),
        ((128, 0, 128), "purple"),
        ((0, 128, 128), "teal"),
        ((0, 0, 128), "navy")
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
        resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(resized, 'RGB')
        # img.show()
        w, h = img.size
        pixels = img.getcolors(w * h)

        most_frequent_color = defaultdict(int)

        for count, colour in pixels:
            if colour != black:  # avoid mask
                color_name = ColorDetector.convert_rgb_to_names(colour)
                most_frequent_color[color_name] += count

        print(most_frequent_color)
        color = max(most_frequent_color.items(), key=operator.itemgetter(1))[0]
        return color

    def convert_rgb_to_names(rgb_tuple):
        names = []
        rgb_values = []
        for color_rgb, color_name in ColorDetector.available_colors_list:
            names.append(color_name)
            rgb_values.append(color_rgb)

        kdt_db = KDTree(rgb_values)
        distance, index = kdt_db.query(rgb_tuple)
        return names[index]
