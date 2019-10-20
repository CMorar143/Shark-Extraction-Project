
# import the necessary packages:
import cv2
import easygui as gui

# import the necessary packages:
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as image


def ApplyMask(threshold):
	# Extract the shark using the mask created by the thresholding
	extracted_sharkB = cv2.bitwise_or(threshold, Enchanced_YUV_B)
	extracted_sharkG = cv2.bitwise_or(threshold, Enchanced_YUV_G)
	extracted_sharkR = cv2.bitwise_or(threshold, Enchanced_YUV_R)

	# Merge the channels
	merged = cv2.merge((extracted_sharkB, extracted_sharkG, extracted_sharkR))

	return merged

# Opening an image using a File Open dialog:
F = gui.fileopenbox()
I = cv2.imread(F)
# I = cv2.imread("Shark_2.PNG")

# Converting the colour space to YUV and extracting the Luminance (Y) From the image:
YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)

# Extract the Y, U, and V from the YUV image:
Y, U, V = cv2.split(YUV)

# Using the Contrast Limited Adaptive Histogram Equalization class to enhance the contrast
# Create the CLAHE object and set the clip limit and tile grid size:
CLAHE = cv2.createCLAHE(clipLimit = 4.5, tileGridSize = (3,3))

# Enchance contrast for the luminance (Y) channel in the image
YE = CLAHE.apply(Y)
# HVE = CLAHE.apply(HV)
UE = CLAHE.apply(U) #--------------LOOKS GOOD FOR BOTH IN THRESHOLD(170,BIN_INV)

_, th1U = cv2.threshold(UE, 176, 255, cv2.THRESH_TRUNC)
th2U = cv2.adaptiveThreshold(th1U, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 275, 2)

# Instead of showing a greyscale image of the luminance alone, merge the enhanced 
# luminance with the original U and V values to form a full YUV image
Enchanced_YUV = cv2.merge((YE,U,V))


# Convert the new YUV image back to the BGR colour space
Enchanced_BGR_YUV = cv2.cvtColor(Enchanced_YUV, cv2.COLOR_YUV2BGR)

# Extract the colour spaces
Enchanced_YUV_B, Enchanced_YUV_G, Enchanced_YUV_R = cv2.split(Enchanced_BGR_YUV)

# # Extract the shark using the mask created by the thresholding above
# extracted_sharkB = cv2.bitwise_or(th2U, Enchanced_YUV_B)
# extracted_sharkG = cv2.bitwise_or(th2U, Enchanced_YUV_G)
# extracted_sharkR = cv2.bitwise_or(th2U, Enchanced_YUV_R)

# # Merge the channels
# f = cv2.merge((extracted_sharkB, extracted_sharkG, extracted_sharkR))
f = ApplyMask(th2U)

YUV2 = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)

u = YUV2[:,:,1]

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

m = cv2.bitwise_xor(masked_range, th2U)
m = cv2.bitwise_not(m)

# key = cv2.waitKey(0)


# # Extract the colour spaces
# Enchanced_YUV_B, Enchanced_YUV_G, Enchanced_YUV_R = cv2.split(Enchanced_BGR_YUV)

# # Extract the shark using the mask created by the thresholding above
# extracted_sharkB = cv2.bitwise_or(m, Enchanced_YUV_B)
# extracted_sharkG = cv2.bitwise_or(m, Enchanced_YUV_G)
# extracted_sharkR = cv2.bitwise_or(m, Enchanced_YUV_R)

# # Merge the channels
# f = cv2.merge((extracted_sharkB, extracted_sharkG, extracted_sharkR))

# cv2.imshow("f2", f)

img = ApplyMask(m)

cv2.imshow("img", img)



































































# ----------------------------------------------------------------------------------------------------



# fig = plt.figure()
# gs = fig.add_gridspec(3, 2)

# ax1 = fig.add_subplot(gs[0,0])
# ax1.imshow(y, cmap='gray')

# ax2 = fig.add_subplot(gs[0,1])
# ax2.hist(y.ravel(), bins=256, range=[0,256])

# ax3 = fig.add_subplot(gs[1,0])
# ax3.imshow(u, cmap='gray')

# ax4 = fig.add_subplot(gs[1,1])
# ax4.hist(u.ravel(), bins=256, range=[0,256])

# ax5 = fig.add_subplot(gs[2,0])
# ax5.imshow(ue, cmap='gray')

# ax6 = fig.add_subplot(gs[2,1])
# ax6.hist(ue.ravel(), bins=256, range=[0,256])

# ax7 = fig.add_subplot(gs[3,0])
# ax7.imshow(mask_u, cmap='gray')

# ax8 = fig.add_subplot(gs[3,1])
# ax8.hist(mask_u.ravel(), bins=256, range=[0,256])

# plt.show()
cv2.waitKey(0)
# plt.close()