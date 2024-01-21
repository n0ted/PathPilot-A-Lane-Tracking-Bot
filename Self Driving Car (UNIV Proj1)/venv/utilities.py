import cv2
import numpy as np

def white_thresholding(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_white = np.array([80, 0, 0])
    upper_white = np.array([255, 160, 255])
    white_mask = cv2.inRange(hsv_image, lower_white, upper_white)
    return white_mask

def perspective_transform(image, points, width, height, inverse=False):
    pts1 = np.float32(points)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    if inverse:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
    warped_image = cv2.warpPerspective(image, matrix, (width, height))
    return warped_image

def initialize_trackbars(initial_trackbar_values, width, height):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", initial_trackbar_values[0], width // 2, lambda a: None)
    cv2.createTrackbar("Height Top", "Trackbars", initial_trackbar_values[1], height, lambda a: None)
    cv2.createTrackbar("Width Bottom", "Trackbars", initial_trackbar_values[2], width // 2, lambda a: None)
    cv2.createTrackbar("Height Bottom", "Trackbars", initial_trackbar_values[3], height, lambda a: None)

def get_trackbar_values(width, height):
    width_top = cv2.getTrackbarPos("Width Top", "Trackbars")
    height_top = cv2.getTrackbarPos("Height Top", "Trackbars")
    width_bottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    height_bottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(width_top, height_top), (width - width_top, height_top),
                         (width_bottom, height_bottom), (width - width_bottom, height_bottom)])
    return points

def draw_points(image, points):
    for point in points:
        cv2.circle(image, (int(point[0]), int(point[1])), 15, (0, 0, 255), cv2.FILLED)
    return image

def get_histogram(image, min_percentage=0.1, display=False, region=1):

    if region == 1:
        hist_values = np.sum(image, axis=0)
    else:
        hist_values = np.sum(image[image.shape[0] // region:, :], axis=0)

    max_value = np.max(hist_values)
    min_value = min_percentage * max_value

    index_array = np.where(hist_values >= min_value)
    base_point = int(np.average(index_array))

    if display:
        hist_image = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
        for x, intensity in enumerate(hist_values):
            cv2.line(hist_image, (x, image.shape[0]), (x, image.shape[0] - intensity // 255 // region), (255, 0, 255), 1)
            cv2.circle(hist_image, (base_point, image.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return base_point, hist_image

    return base_point

def stack_images(scale, image_array):
    rows = len(image_array)
    cols = len(image_array[0])
    rows_available = isinstance(image_array[0], list)
    width = image_array[0][0].shape[1]
    height = image_array[0][0].shape[0]

    if rows_available:
        for row in range(rows):
            for col in range(cols):
                if image_array[row][col].shape[:2] == image_array[0][0].shape[:2]:
                    image_array[row][col] = cv2.resize(image_array[row][col], (0, 0), None, scale, scale)
                else:
                    image_array[row][col] = cv2.resize(image_array[row][col], (image_array[0][0].shape[1], image_array[0][0].shape[0]), None, scale, scale)
                if len(image_array[row][col].shape) == 2:
                    image_array[row][col] = cv2.cvtColor(image_array[row][col], cv2.COLOR_GRAY2BGR)
        blank_image = np.zeros((height, width, 3), np.uint8)
        horizontal_images = [blank_image] * rows
        horizontal_concatenated_images = [blank_image] * rows
        for row in range(rows):
            horizontal_images[row] = np.hstack(image_array[row])
        vertical_image = np.vstack(horizontal_images)
    else:
        for row in range(rows):
            if image_array[row].shape[:2] == image_array[0].shape[:2]:
                image_array[row] = cv2.resize(image_array[row], (0, 0), None, scale, scale)
            else:
                image_array[row] = cv2.resize(image_array[row], (image_array[0].shape[1], image_array[0].shape[0]), None, scale, scale)
            if len(image_array[row].shape) == 2:
                image_array[row] = cv2
