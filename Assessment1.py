# import the necessary packages:
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as image
import easygui

######### Reading Images #########

# Opening an image using a File Open dialog:
f = easygui.fileopenbox()
I = cv2.imread(f)

######### Colourspaces #########

# Converting to different colour spaces:
RGB = cv2.cvtColor(I, cv2.COLOR_BGR2RGB)
HSV = cv2.cvtColor(I, cv2.COLOR_BGR2HSV)
YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)
G = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)

# Showing each image on the screen in a different window (OpenCV):
cv2.imshow("Original", I)
cv2.imshow("HSV", HSV)
cv2.imshow("YUV", YUV)
cv2.imshow("Grayscale", G)
cv2.imshow("Y", Y)
key = cv2.waitKey(0)
