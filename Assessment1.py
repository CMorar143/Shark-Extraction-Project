# import the necessary packages:
import cv2
import easygui as gui

# import the necessary packages:
# import numpy as np
# from matplotlib import pyplot as plt
# from matplotlib import image as image


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
# cv2.imshow("Original", I)
# cv2.imshow("Y", Y)
# key = cv2.waitKey(0)

# Using the Contrast Limited Adaptive Histogram Equalization class to enhance the contrast
# Create the CLAHE object and set the clip limit and tile grid size:
CLAHE = cv2.createCLAHE(clipLimit = 4.5, tileGridSize = (6,6))

# Enchance contrast for the luminance (Y) channel in the image
E = CLAHE.apply(Y)
cv2.imshow("enhanced Y channel", E)

# Instead of showing a greyscale image of the luminance alone, merge the enhanced 
# luminance with the original U and V values to form a full YUV image
Enchanced_YUV = cv2.merge((E,U,V))

# Convert the new YUV image back to the original BGR colour space
Enchanced_BGR = cv2.cvtColor(Enchanced_YUV, cv2.COLOR_YUV2BGR)
BG = Enchanced_BGR[:,:,0]
cv2.imshow("Enchanced BG", BG)
cv2.imshow("BG", I[:,:,0])
# cv2.imshow("Enchanced Image", Enchanced_BGR)
key = cv2.waitKey(0)


# ----------------------------------------------------------------------------------------------------


# fig = plt.figure()
# gs = fig.add_gridspec(2, 2)

# ax1 = fig.add_subplot(gs[0,0])
# ax1.imshow(I[:,:,0], cmap='gray')

# ax2 = fig.add_subplot(gs[0,1])
# ax2.hist(I[:,:,0].ravel(), bins=256, range=[0,256])

# ax3 = fig.add_subplot(gs[1,0])
# ax3.imshow(BG, cmap='gray')

# ax4 = fig.add_subplot(gs[1,1])
# ax4.hist(BG.ravel(), bins=256, range=[0,256])

# plt.show()
# cv2.waitKey(0)
# plt.close()