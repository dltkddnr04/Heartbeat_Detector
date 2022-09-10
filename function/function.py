import pyvirtualcam
import numpy as np
import cv2

def get_webcam_number():
    index = 0
    list = []
    while True:
        camera = cv2.VideoCapture(index)
        if not camera.read()[0]:
            break
        else:
            list.append(index)
        camera.release()
        index += 1
    list.sort()
    return list[0], list[-1]

def get_webcam_resolution(webcam_id):
    camera = cv2.VideoCapture(webcam_id)
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    camera.release()
    return width, height

def get_webcam_fps(webcam_id):
    camera = cv2.VideoCapture(webcam_id)
    fps = int(camera.get(cv2.CAP_PROP_FPS))
    camera.release()
    return fps

def get_camera(id):
    return cv2.VideoCapture(id)

def get_camera_frame(camera):
    ret, frame = camera.read()
    if not ret:
        return None
    return frame

def process_monitor_frame(frame):
    # crop image to square and resize to 256x256
    height, width, _ = frame.shape
    if height > width:
        crop = int((height - width) / 2)
        frame = frame[crop:height - crop, 0:width]
    else:
        crop = int((width - height) / 2)
        frame = frame[0:height, crop:width - crop]
    frame = cv2.resize(frame, (256, 256))
    return frame