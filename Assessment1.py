# import the necessary packages:
import cv2
import easygui as gui

# import the necessary packages:
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as image


# Opening an image using a File Open dialog:
# F = gui.fileopenbox()
# I = cv2.imread(F)
I = cv2.imread("Shark_1.PNG")

h, w, d = I.shape
blue_image = I.copy()
blue_image[:,:] = (255,0,0)


# Converting the colour space to YUV and extracting the Luminance (Y) From the image:
YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)

# Converting to different colour spaces:
HSV = cv2.cvtColor(I, cv2.COLOR_BGR2HSV)

# Extract the Y, U, and V from the YUV image:
Y = YUV[:,:,0]
U = YUV[:,:,1]
V = YUV[:,:,2]

H = HSV[:,:,0]
S = HSV[:,:,1]
HV = HSV[:,:,2]


# Using the Contrast Limited Adaptive Histogram Equalization class to enhance the contrast
# Create the CLAHE object and set the clip limit and tile grid size:
CLAHE = cv2.createCLAHE(clipLimit = 4.5, tileGridSize = (3,3))

# Enchance contrast for the luminance (Y) channel in the image

YE = CLAHE.apply(Y)
HVE = CLAHE.apply(HV)
# HVE = cv2.equalizeHist(HV) 

_, th1 = cv2.threshold(HVE, 170, 255, cv2.THRESH_TRUNC)
th3 = cv2.equalizeHist(th1)


# YY = CLAHE.apply(Y)
# HVV = CLAHE.apply(HV)
# YE = cv2.equalizeHist(Y)
# HVE = cv2.equalizeHist(HV)

# Instead of showing a greyscale image of the luminance alone, merge the enhanced 
# luminance with the original U and V values to form a full YUV image
Enchanced_YUV = cv2.merge((YE,U,V))
Enchanced_HSV = cv2.merge((H,S,HVE))

# range_lower = np.asarray([0,0,150])
# range_higher = np.asarray([255,255,185])

# masked_range = cv2.inRange(HSV, range_lower, range_higher)

# Convert the new YUV image back to the original BGR colour space
Enchanced_BGR_YUV = cv2.cvtColor(Enchanced_YUV, cv2.COLOR_YUV2BGR)
Enchanced_BGR_HSV = cv2.cvtColor(Enchanced_HSV, cv2.COLOR_HSV2BGR)

_, th2 = cv2.threshold(Enchanced_BGR_HSV, 170, 255, cv2.THRESH_TRUNC)

# Enchanced_YUV_B = Enchanced_BGR_YUV[:,:,0]
# Enchanced_YUV_G = Enchanced_BGR_YUV[:,:,1]
# Enchanced_YUV_R = Enchanced_BGR_YUV[:,:,2]

# Enchanced_HSV_B = Enchanced_BGR_HSV[:,:,0]
# Enchanced_HSV_G = Enchanced_BGR_HSV[:,:,1]
# Enchanced_HSV_R = Enchanced_BGR_HSV[:,:,2]

# BG = Enchanced_BGR[:,:,0]

# cv2.imshow("b",I[:,:,0])
# cv2.imshow("Enchanced_YUV_B", Enchanced_YUV_B)
# cv2.imshow("Enchanced_YUV_G", Enchanced_YUV_G)

# cv2.imshow("Enchanced_HSV_B", Enchanced_HSV_B)
# cv2.imshow("Enchanced_HSV_G", Enchanced_HSV_G)
cv2.imshow("Enchanced ImageH", Enchanced_BGR_HSV)
# cv2.imshow("Enchanced ImageY", Enchanced_BGR_YUV)
cv2.imshow("th1", th1)
cv2.imshow("th2", th2)
cv2.imshow("th3", th3)
# cv2.imshow("HV", HV)
# cv2.imshow("Y", Y)
# cv2.imshow("U", U)

key = cv2.waitKey(0)



# ----------------------------------------------------------------------------------------------------



fig = plt.figure()
gs = fig.add_gridspec(2, 2)

ax1 = fig.add_subplot(gs[0,0])
ax1.imshow(th1, cmap='gray')

ax2 = fig.add_subplot(gs[0,1])
ax2.hist(th1.ravel(), bins=256, range=[0,256])

ax3 = fig.add_subplot(gs[1,0])
ax3.imshow(th3, cmap='gray')

ax4 = fig.add_subplot(gs[1,1])
ax4.hist(th3.ravel(), bins=256, range=[0,256])

# ax5 = fig.add_subplot(gs[2,0])
# ax5.imshow(l_channel, cmap='gray')

# ax6 = fig.add_subplot(gs[2,1])
# ax6.hist(l_channel.ravel(), bins=256, range=[0,256])

# ax7 = fig.add_subplot(gs[3,0])
# ax7.imshow(Enchanced_BGR_HSV, cmap='gray')

# ax8 = fig.add_subplot(gs[3,1])
# ax8.hist(Enchanced_BGR_HSV.ravel(), bins=256, range=[0,256])

plt.show()
cv2.waitKey(0)
plt.close()