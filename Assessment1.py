# import the necessary packages:
import cv2
import easygui as gui

# Function to apply a threshold to an image.
# It is used to remove the background
def ApplyMask(threshold):
	# Extract the shark using the mask created by the thresholding
	extracted_sharkB = cv2.bitwise_or(threshold, Enchanced_YUV_B)
	extracted_sharkG = cv2.bitwise_or(threshold, Enchanced_YUV_G)
	extracted_sharkR = cv2.bitwise_or(threshold, Enchanced_YUV_R)

	# Merge the channels
	merged = cv2.merge((extracted_sharkB, extracted_sharkG, extracted_sharkR))

	return merged

# Messages for the Graphical User Interface
closing_message = "\tHere's The Shark!\n\tWould You Like to Select Another Picture?"
choices = ["Yes", "No"]
opening_message = "This Application Allows You to Extract a Shark From an Image.\n\n\n"
instructions = "Please Choose The Image That You Would Like to Use."

# Repeat until the user exits
while 1:
	# Introduction and instructions
	gui.msgbox(opening_message + instructions, "Hello!")

	# Opening an image using a File Open dialog:
	F = gui.fileopenbox()
	I = cv2.imread(F)

	# Converting the colour space to YUV and extracting the Luminance (Y) From the image:
	YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)

	# Extract the Y, U, and V from the YUV image:
	Y, U, V = cv2.split(YUV)

	# Using the Contrast Limited Adaptive Histogram Equalization class to enhance the contrast
	# Create the CLAHE object and set the clip limit and tile grid size:
	CLAHE = cv2.createCLAHE(clipLimit = 4.5, tileGridSize = (3,3))

	# Enchance contrast for the luminance (Y) channel in the image
	# This is done to improve definition in the image
	YE = CLAHE.apply(Y)

	# Enhance the contrast for the U channel
	# This is used to remove the background
	UE = CLAHE.apply(U)

	# use thresholding to create the mask
	_, th1U = cv2.threshold(UE, 176, 255, cv2.THRESH_TRUNC)
	th2U = cv2.adaptiveThreshold(th1U, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 275, 2)

	# Merge the enhanced luminance with the original U and V values to form a full YUV image
	Enchanced_YUV = cv2.merge((YE,U,V))

	# Convert the new YUV image back to the BGR colour space
	Enchanced_BGR_YUV = cv2.cvtColor(Enchanced_YUV, cv2.COLOR_YUV2BGR)

	# Extract the colour spaces in order to apply the mask to each channel
	Enchanced_YUV_B, Enchanced_YUV_G, Enchanced_YUV_R = cv2.split(Enchanced_BGR_YUV)

	f = ApplyMask(th2U)

	YUV2 = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)

	u = YUV2[:,:,1]

	# Create another mask to remove more noise from the image
	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(u)
	print(minVal)
	print(maxVal)
	print(minLoc)
	print(maxLoc)

	masked_range = cv2.inRange(u, 0, maxVal-3)
	m = cv2.bitwise_xor(masked_range, th2U)
	m = cv2.bitwise_not(m)

	final_image = ApplyMask(m)

	cv2.imwrite("./final_image.png", final_image)

	reply = gui.buttonbox(closing_message, image = "./final_image.png", choices = choices)

	if reply == 'No':

		exit(1)



































































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