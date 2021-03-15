import cv2
import imutils
import numpy as np
import math
from sklearn.cluster import KMeans


class BoderDetector:
    POINTS_MM = {
        "P1": [0, 0],
        "P2": [220, 0],
        "P3": [220, 155]
    }

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

        return border_points

    def perspective_transform(self, input_image, border_points):
        im_src = input_image.copy()
        height, width, dim = im_src.shape

        line1 = [border_points["P1"], border_points["P6"]]
        line2 = [border_points["P4"], border_points["P3"]]
        p4 = self.line_intersection(line1, line2)
        pts_src = np.array(
            [border_points["P1"], border_points["P2"], border_points["P3"], p4], np.float32)
        pts_dst = np.array(
            [(0., 0.), (width-1, 0.), (width-1, height-1), (0., height-1)], np.float32)

        M = cv2.getPerspectiveTransform(pts_src, pts_dst)

        im_out = cv2.warpPerspective(
            im_src, M, (width, height), flags=cv2.INTER_LINEAR)

        return im_out

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

    def convert_px_to_mm(self, border_px_points, point):
        p1_mm = self.POINTS_MM["P1"]
        p1_px = border_px_points["P1"]

        p2_mm = self.POINTS_MM["P2"]
        p2_px = border_px_points["P2"]

        p3_mm = self.POINTS_MM["P3"]
        p3_px = border_px_points["P3"]

        # Pixels per mmm on x
        dist_px_x = p2_px[0] - p1_px[0]
        dist_mm_x = p2_mm[0]
        px_mm_x = dist_mm_x/dist_px_x

        # Pixels per mmm on y
        dist_px_y = p3_px[1] - p2_px[1]
        dist_mm_y = p3_mm[1]
        px_mm_y = dist_mm_y/dist_px_y

        point_mm_x = round(point[0]*px_mm_x, 2)
        point_mm_y = round(point[1]*px_mm_y, 2)

        return [point_mm_x, point_mm_y]

    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return [x, y]
