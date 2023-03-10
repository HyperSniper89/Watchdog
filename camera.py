#Modified by smartbuilds.io
#Date: 27.09.20

#Modified by Jákup and Heidi 2022

import cv2 as cv
from imutils.video.pivideostream import PiVideoStream
import time
import numpy as np

class VideoCamera(object):
    def __init__(self, flip = False, file_type  = ".jpg", photo_string= "stream_photo"):
        self.vs = PiVideoStream().start()
        self.flip = flip # Flip frame vertically
        self.file_type = file_type # image type i.e. .jpg
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv.imencode(self.file_type, frame)
        self.previous_frame = jpeg
        return jpeg.tobytes()