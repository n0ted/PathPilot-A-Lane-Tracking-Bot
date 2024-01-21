import cv2

video_capture = cv2.VideoCapture(0)

def capture_image(display=False, size=[480, 240]):
    _, image = video_capture.read()
    image = cv2.resize(image, (size[0], size[1]))
    if display:
        cv2.imshow('Captured Image', image)
    return image

if __name__ == '__main__':
    while True:
        captured_image = capture_image(display=True)