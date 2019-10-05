# import the necessary packages:
import cv2
import easygui as gui

# Opening an image using a File Open dialog:
F = gui.fileopenbox()
I = cv2.imread(F)

# Converting the colour space to YUV and extracting the Luminance (Y) From the image:
YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)

# Extract the Y, U, and V from the YUV image:
Y = YUV[:,:,0]
U = YUV[:,:,1]
V = YUV[:,:,2]


# Showing each image on the screen in a different window (OpenCV):
cv2.imshow("Original", I)
cv2.imshow("Y", Y)

key = cv2.waitKey(0)
