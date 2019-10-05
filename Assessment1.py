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
# cv2.imshow("Original", I)
# cv2.imshow("Y", Y)
# key = cv2.waitKey(0)

# Using the Contrast Limited Adaptive Histogram Equalization class to enhance the contrast
# Create the CLAHE object and the set the clip limit and tile grid size:
CLAHE = cv2.createCLAHE()
CLAHE.setClipLimit(4.5)
CLAHE.setTilesGridSize((10, 10))

# Enchance contrast for the luminance (Y) channel in the image
E = CLAHE.apply(Y)

# Instead of showing a greyscale image of the luminance alone, merge the enhanced 
# luminance with the original U and V values to form a full YUV image
Enchanced_YUV = cv2.merge((E,U,V))

# Convert the new YUV image back to the original BGR colour space
Enchanced_BGR = cv2.cvtColor(Enchanced_YUV, cv2.COLOR_YUV2BGR)

cv2.imshow("Enchanced Image", Enchanced_BGR)
key = cv2.waitKey(0)