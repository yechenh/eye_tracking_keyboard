import cv2
from gaze_tracking import GazeTracking
from page import Page
from sklearn.svm import SVC
import pandas as pd
import numpy as np
#
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)
outn="init.avi"

fps = webcam.get(cv2.CAP_PROP_FPS)
print(fps)
_, frame = webcam.read()
(hgt, wid, dep) = frame.shape
frc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter(outn, frc, 25.0, (wid*2, hgt), 1)


page_initialization = Page(-1, gaze, webcam, out)
gaze.set_clf(page_initialization.initialization())

pages = [Page(0, gaze, webcam), Page(1, gaze, webcam), Page(2, gaze, webcam), Page(3, gaze, webcam),
         Page(4, gaze, webcam), Page(5, gaze, webcam), Page(6, gaze, webcam), Page(7, gaze, webcam),
         Page(8, gaze, webcam), Page(9, gaze, webcam), Page(10, gaze, webcam)]
index = 0
str_input = ""
while True:
    index, str_input, whe_break = pages[index].run(str_input, out)

    if(whe_break):
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
print(str_input)
webcam.release()
out.release()
print(hgt, wid)
