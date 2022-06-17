"""
all the vision functions are in this file  
"""
import cv2 as cv
import numpy as np
import config as CONFIG

class camera_2d(object):
    """docstring for camera"""
    def __init__(self, camera_index=0):
        super(camera_2d, self).__init__()
        self.camera_index = camera_index
        self.capture_init()

    def capture_init(self):
        self.cap = cv.VideoCapture(self.camera_index)

    def frame(self):
        ret, frame = self.cap.read()
        return ret, frame
    
    def release(self):
        self.cap.release()

        
def color_detector(frame, hsv_low, hsv_high):
    # select by color
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    thr = cv.inRange(hsv, hsv_low, hsv_high)

    # opening
    thr = cv.morphologyEx(thr, cv.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)

    # find largest contour
    contours, hierarchy = cv.findContours(thr, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    if len(contours) == 0:
        result = 0    
    else:
        cnt =  max(contours, key = cv.contourArea)
        result = rect_detector(cnt, CONFIG.rect_ratio, CONFIG.error_thr)
    return thr, result


def rect_detector(cnt, rect_ratio, error_thr):
    # width and height
    center, dim, theta = cv.minAreaRect(cnt)    

    # ratio
    if abs(rect_ratio - min(dim)/max(dim)) < error_thr:
        return 1
    return 0


def main():
    # create the camera 
    camera = camera_2d(CONFIG.camera_index)

    while True:
        # get a frame 
        ret, frame = camera.frame()
        if frame is None:
            break
        if ret:
            # detect pass
            thr, result = color_detector(frame, CONFIG.pass_hsv["low"], CONFIG.pass_hsv["high"])

            # show the result
            cv.imshow(CONFIG.window_name, thr)
            key = cv.waitKey(30)
            if key == ord('q') or key == 27:
                break

if __name__ == '__main__':
    main()