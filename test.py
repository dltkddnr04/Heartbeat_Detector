from function import (function)
import cv2
import time

# 웹캠 0번에서 영상을 받아와서 실시간으로 출력
camera = function.get_camera(0)
while True:
    frame = function.get_camera_frame(camera)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()