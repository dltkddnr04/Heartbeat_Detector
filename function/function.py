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