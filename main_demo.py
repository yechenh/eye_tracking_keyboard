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
# x = []
# y = []
#
# data_size = 150
#
# horizontal = pd.read_csv('trained_models/dict_horizontal.csv', sep=',', header=None).values
# vertical = pd.read_csv('trained_models/dict_vertical.csv', sep=',', header=None).values
# for i in range(6):
#     x = horizontal[i][1:]
#     y = vertical[i][1:]
#     xy = np.concatenate((np.array(x).reshape(data_size, 1), np.array(y).reshape(data_size, 1)), axis = 1)
#     if i>0:
#         data = np.concatenate((data, xy), axis = 0)
#     else: data = xy
#
# horizontal = pd.read_csv('trained_models/dict_horizontal.csv', sep=',', header=None).values
# vertical = pd.read_csv('trained_models/dict_vertical.csv', sep=',', header=None).values
# for i in range(6):
#     x = horizontal[i][1:]
#     y = vertical[i][1:]
#     xy = np.concatenate((np.array(x).reshape(data_size, 1), np.array(y).reshape(data_size, 1)), axis = 1)
#     if i>0:
#         data_test = np.concatenate((data_test, xy), axis=0)
#     else: data_test = xy
# data = np.concatenate((data, data_test), axis = 0)
# y = np.zeros((6*data_size,1))
# for i in range(6):
#     y[i*data_size:(i+1)*data_size] = i
# y2 = np.zeros((6*data_size,1))
# for i in range(6):
#     y2[i*data_size:(i+1)*data_size] = i
# y = np.concatenate((y, y2))
# y = np.ravel(y)
#
# clf = SVC(decision_function_shape='ovo')
# clf.fit(data, y)
#
# gaze.set_clf(clf)

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