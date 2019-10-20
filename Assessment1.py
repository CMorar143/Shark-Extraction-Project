
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
I = cv2.imread("Shark_2.PNG")

# Converting the colour space to YUV and extracting the Luminance (Y) From the image:
YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)

# Converting to different colour spaces:
HSV = cv2.cvtColor(I, cv2.COLOR_BGR2HSV)

# Extract the Y, U, and V from the YUV image:
Y, U, V = cv2.split(YUV)

H = HSV[:,:,0]
S = HSV[:,:,1]
HV = HSV[:,:,2]

# Using the Contrast Limited Adaptive Histogram Equalization class to enhance the contrast
# Create the CLAHE object and set the clip limit and tile grid size:
CLAHE = cv2.createCLAHE(clipLimit = 4.5, tileGridSize = (3,3))

# Enchance contrast for the luminance (Y) channel in the image
YE = CLAHE.apply(Y)
HVE = CLAHE.apply(HV)
UE = CLAHE.apply(U) #--------------LOOKS GOOD FOR BOTH IN THRESHOLD(170,BIN_INV)

_, th1U = cv2.threshold(UE, 176, 255, cv2.THRESH_TRUNC)
th2U = cv2.adaptiveThreshold(th1U, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 275, 2)
# th2U = cv2.adaptiveThreshold(th1U, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 275, 5)

# Instead of showing a greyscale image of the luminance alone, merge the enhanced 
# luminance with the original U and V values to form a full YUV image
Enchanced_YUV = cv2.merge((YE,U,V))
Enchanced_HSV = cv2.merge((H,S,HVE))


# Convert the new YUV image back to the BGR colour space
Enchanced_BGR_YUV = cv2.cvtColor(Enchanced_YUV, cv2.COLOR_YUV2BGR)
Enchanced_BGR_HSV = cv2.cvtColor(Enchanced_HSV, cv2.COLOR_HSV2BGR)

# Extract the colour spaces
Enchanced_YUV_B, Enchanced_YUV_G, Enchanced_YUV_R = cv2.split(Enchanced_BGR_YUV)

# Extract the shark using the mask created by the thresholding above
extracted_sharkB = cv2.bitwise_or(th2U, Enchanced_YUV_B)
extracted_sharkG = cv2.bitwise_or(th2U, Enchanced_YUV_G)
extracted_sharkR = cv2.bitwise_or(th2U, Enchanced_YUV_R)

# Merge the channels
f = cv2.merge((extracted_sharkB, extracted_sharkG, extracted_sharkR))
YUV2 = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)
HSV2 = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)

y = YUV2[:,:,0]
u = YUV2[:,:,1]
v = YUV2[:,:,2]

# ue = cv2.equalizeHist(u)
ue = CLAHE.apply(u)

mask_u = cv2.bitwise_not(u)
# extracted_sharkHSV = cv2.bitwise_and(mask, Enchanced_BGR_HSV)

# BG = Enchanced_BGR[:,:,0]

# cv2.imshow("b",I[:,:,0])
# cv2.imshow("Enchanced_YUV_B", Enchanced_YUV_B)
# cv2.imshow("Enchanced_YUV_G", Enchanced_YUV_G)

# cv2.imshow("Enchanced_HSV_B", Enchanced_HSV_B)
# cv2.imshow("Enchanced_HSV_G", Enchanced_HSV_G)

# cv2.imshow("Enchanced ImageH", Enchanced_BGR_HSV)
# cv2.imshow("Enchanced ImageY", Enchanced_BGR_YUV)

# cv2.imshow("th1Y", th1Y)
# cv2.imshow("th2Y", th2Y)
# cv2.imshow("th3Y", th3Y)

# cv2.imshow("th1U", th1U)
cv2.imshow("th2U", th2U)
# cv2.imshow("th3U", th3U)

# cv2.imshow("th1H", th1H)
# cv2.imshow("th2H", th2H)
# cv2.imshow("th3H", th3H)

# cv2.imshow("HV", HV)
# cv2.imshow("Y", Y)
# cv2.imshow("U", U)

# cv2.imshow("extracted_sharkHSV", extracted_sharkHSV)
# cv2.imshow("extracted_sharkYUV", extracted_sharkYUV)

# cv2.imshow("f", f)

# key = cv2.waitKey(0)

minVal = 0
maxVal = 0
minLoc = (0, 0)
maxLoc = (0, 0)
minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(u)
print(minVal)
print(maxVal)
print(minLoc)
print(maxLoc)

range_higher = np.asarray([(maxVal-3)])
masked_range = cv2.inRange(u, 0, range_higher)
# masked_range = cv2.bitwise_not(masked_range)

m = cv2.bitwise_xor(masked_range, th2U)
m = cv2.bitwise_not(m)
# cv2.imshow("m", m)
# cv2.imshow("masked_range", masked_range)

# f2 = cv2.bitwise_and(m, th2U)

# key = cv2.waitKey(0)

# Extract the colour spaces
Enchanced_YUV_B, Enchanced_YUV_G, Enchanced_YUV_R = cv2.split(Enchanced_BGR_YUV)

# Extract the shark using the mask created by the thresholding above
extracted_sharkB = cv2.bitwise_or(m, Enchanced_YUV_B)
extracted_sharkG = cv2.bitwise_or(m, Enchanced_YUV_G)
extracted_sharkR = cv2.bitwise_or(m, Enchanced_YUV_R)

# Merge the channels
f = cv2.merge((extracted_sharkB, extracted_sharkG, extracted_sharkR))

cv2.imshow("f2", f)

# ----------------------------------------------------------------------------------------------------



fig = plt.figure()
gs = fig.add_gridspec(3, 2)

ax1 = fig.add_subplot(gs[0,0])
ax1.imshow(y, cmap='gray')

ax2 = fig.add_subplot(gs[0,1])
ax2.hist(y.ravel(), bins=256, range=[0,256])

ax3 = fig.add_subplot(gs[1,0])
ax3.imshow(u, cmap='gray')

ax4 = fig.add_subplot(gs[1,1])
ax4.hist(u.ravel(), bins=256, range=[0,256])

ax5 = fig.add_subplot(gs[2,0])
ax5.imshow(ue, cmap='gray')

ax6 = fig.add_subplot(gs[2,1])
ax6.hist(ue.ravel(), bins=256, range=[0,256])

# ax7 = fig.add_subplot(gs[3,0])
# ax7.imshow(mask_u, cmap='gray')

# ax8 = fig.add_subplot(gs[3,1])
# ax8.hist(mask_u.ravel(), bins=256, range=[0,256])

# plt.show()
cv2.waitKey(0)
plt.close()