# Unfreeze the Frozen World - An Eyetracking Keyboard for ALS
# HackPrinceton 2020
# Bowei Liu, Ruohui Cui, Yechen Hu


# Description
This is a Python program intended to facilitate the communication of ALS patients. The program tracks eye movements and uses a special keyboard to output wor\
ds.


# Installation

## Install these dependencies (scikit-learn, pandas, numpy, opencv_python, dlib):
pip install -r requirements.txt

## Run the program:
python main_demo.py


# How to use the program

## the keyboard
The program currently supports a keyboard consisting of 26 letters, 10 roman numerals, the space character, and 8 frequently used sentence shortcuts.

## how to type
The screen displayed is divided into six parts, indicating the six directions one can fix his gaze on: top-left, top-center, top-right, left, center, right.
Each tile shows the part of keyboard it represents. To choose one of the tile, hold you gaze on the center until it becomes green, then look in the direction\
 indicated by the tile until it turns green. Note that the tile on which your gaze is fixed will appear yellow.

## how to delete/undo
close your eyes for several seconds and then open.

## calibration
The program begins in the calibration phase. Look in the direction indicated on the screen. Try to hold your gaze steadily.


# Acknowledgement
Part of this project is based on the GazeTracking project by Antoine Lamé (https://github.com/antoinelame/GazeTracking.git).
