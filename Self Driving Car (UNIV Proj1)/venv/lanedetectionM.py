import cv2
import numpy as np
import utility_functions as utils

curve_list = []
average_value = 10

def get_lane_curve(image, display_mode=2):

    image_copy = image.copy()
    result_image = image.copy()

    # STEP 1: Thresholding
    thresholded_image = utils.thresholding(image)

    # STEP 2: Perspective Transformation
    height, width, channels = image.shape
    control_points = utils.get_initial_trackbar_values()
    warped_image = utils.warp_image(thresholded_image, control_points, width, height)
    image_with_points = utils.draw_points(image_copy, control_points)

    # STEP 3: Histogram Analysis
    middle_point, histogram_image = utils.get_histogram(warped_image, display=True, min_percentage=0.5, region=4)
    average_curve_point, histogram_image = utils.get_histogram(warped_image, display=True, min_percentage=0.9)
    raw_curve = average_curve_point - middle_point

    # STEP 4: Smoothing Curve
    curve_list.append(raw_curve)
    if len(curve_list) > average_value:
        curve_list.pop(0)
    smoothed_curve = int(sum(curve_list) / len(curve_list))

    # STEP 5: Visualization
    if display_mode != 0:
        inverse_warped_image = utils.warp_image(warped_image, control_points, width, height, inverse=True)
        inverse_warped_image = cv2.cvtColor(inverse_warped_image, cv2.COLOR_GRAY2BGR)
        inverse_warped_image[0:height // 3, 0:width] = 0, 0, 0
        lane_color_image = np.zeros_like(image)
        lane_color_image[:] = 0, 255, 0
        lane_color_image = cv2.bitwise_and(inverse_warped_image, lane_color_image)
        result_image = cv2.addWeighted(result_image, 1, lane_color_image, 1, 0)
        mid_y = 450
        cv2.putText(result_image, str(smoothed_curve), (width // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(result_image, (width // 2, mid_y), (width // 2 + (smoothed_curve * 3), mid_y), (255, 0, 255), 5)
        cv2.line(result_image, ((width // 2 + (smoothed_curve * 3)), mid_y - 25), (width // 2 + (smoothed_curve * 3), mid_y + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = width // 20
            cv2.line(result_image, (w * x + int(smoothed_curve // 50), mid_y - 10),
                     (w * x + int(smoothed_curve // 50), mid_y + 10), (0, 0, 255), 2)

    if display_mode == 2:
        stacked_images = utils.stack_images(0.7, ([image, image_with_points, warped_image],
                                                  [histogram_image, lane_color_image, result_image]))
        cv2.imshow('ImageStack', stacked_images)
    elif display_mode == 1:
        cv2.imshow('Result', result_image)

    # Normalization
    smoothed_curve = smoothed_curve / 100
    if smoothed_curve > 1:
        smoothed_curve = 1
    if smoothed_curve < -1:
        smoothed_curve = -1

    return smoothed_curve


if __name__ == '__main__':
    video_capture = cv2.VideoCapture('vid1.mp4')
    initial_trackbar_values = [102, 80, 20, 214]
    utils.initialize_trackbars(initial_trackbar_values)
    frame_counter = 0

    while True:
        frame_counter += 1
        if video_capture.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0

        success, current_frame = video_capture.read()
        current_frame = cv2.resize(current_frame, (480, 240))
        lane_curve = get_lane_curve(current_frame, display_mode=2)
        print(lane_curve)
        cv2.waitKey(1)
