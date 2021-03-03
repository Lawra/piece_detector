import cv2
import imutils
import numpy as np
import math
from sklearn.cluster import KMeans


class BoderDetector:
    def __init__(self):
        pass

    def detect(self, input_image):
        image = input_image.copy()
        total_heigth, total_width, chanels = image.shape
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        template = cv2.imread('utils/template.jpg', 0)
        w, h = template.shape[::-1]

        # Apply template Matching
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        list_loc = []
        for pt in zip(*loc[::-1]):
            list_loc.append([pt[0]+w/2, pt[1]+h/2])

        # Unify similar points in order to detect only the 6 of them:
        kmeans = KMeans(n_clusters=6).fit(list_loc)
        centroids = kmeans.cluster_centers_.astype(int).tolist()

        # Create dictionari of points
        border_points = {}

        # Get P1
        reference = [0, 0]
        border_points["P1"] = self.get_n_point(reference, centroids)

        # Get P2
        reference = [total_width, 0]
        border_points["P2"] = self.get_n_point(reference, centroids)

        # Get P3
        reference = [total_width, total_heigth]
        border_points["P3"] = self.get_n_point(reference, centroids)

        # Get P4
        reference = [total_width/2, total_heigth]
        border_points["P4"] = self.get_n_point(reference, centroids)

        # Get P5
        reference = [total_width/2, total_heigth]
        border_points["P5"] = self.get_n_point(reference, centroids)

        # Get P6
        border_points["P6"] = centroids[0]

        for key in border_points:
            print(key + ": " + str(border_points[key]))
            cv2.circle(image, (border_points[key][0], border_points[key][1]), radius=10, color=(
                0, 0, 255), thickness=-1)
            cv2.putText(image, key, (border_points[key][0], border_points[key][1]), cv2.FONT_HERSHEY_SIMPLEX,
                        4, (0, 0, 0), 4)

        # self.display_image(image, "result")

        return border_points

    def display_image(self, input_image, title):
        image = input_image.copy()
        image = imutils.resize(image, width=700)

        cv2.imshow(title, image)
        cv2.waitKey(0)

    def get_n_point(self, reference, list_points):
        result = list_points[0]
        min_dist = math.sqrt(
            ((reference[0]-result[0])**2)+((reference[1]-result[1])**2))

        for pt in list_points[1:]:
            distance = math.sqrt(
                ((reference[0]-pt[0])**2)+((reference[1]-pt[1])**2))
            if distance < min_dist:
                min_dist = distance
                result = pt

        # Delete from list
        list_points.remove(result)
        return result