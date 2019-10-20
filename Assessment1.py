# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Program to Detect and Extract a Shark From an Image.						  #
# Author: Cian Morar 														  #
# Date: October 2019														  #
# 																			  #
# User selects an image. 													  #
# 																			  #
# Convert image to the YUV color space.										  #
# 																			  #
# Extract and enhance the contrast of the Y and U channels.					  #
# 																			  #
# Threshold the U channel to create a mask (for background subtraction).	  #
# 																			  #
# Using the enhanced Y channel, convert YUV image back to BGR.				  #
# 																			  #
# Apply the mask and convert back to YUV.									  #
# 																			  #
# Extract the U channel from the enhanced YUV image.					 	  #
# 																			  #
# Create another mask.														  #
# 																			  #
# Apply the final mask (to remove some noise from the image).				  #
# 																			  #
# Display the extracted shark.												  #
# 																			  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# import the necessary packages:
import cv2
import easygui as gui

# Messages for the Graphical User Interface:
opening_message = "This Application Allows You to Extract a Shark From an Image.\n\n\n"
instructions = "Please Choose The Image That You Would Like to Use."
closing_message = "\tHere's The Shark!\n\tWould You Like to Select Another Picture?"
choices = ["Yes", "No"]
final_message = "\tHave a great day!"

# Function to apply a threshold to an image
# It is used to remove the background:
def ApplyMask(threshold):
	# Apply the mask to each color channel in the image:
	extracted_sharkB = cv2.bitwise_or(threshold, Enchanced_B)
	extracted_sharkG = cv2.bitwise_or(threshold, Enchanced_G)
	extracted_sharkR = cv2.bitwise_or(threshold, Enchanced_R)

	merged = cv2.merge((extracted_sharkB, extracted_sharkG, extracted_sharkR))

	return merged

# Repeat until the user chooses to exit:
while 1:
	gui.msgbox(opening_message + instructions, "Hello!")

	F = gui.fileopenbox()
	I = cv2.imread(F)

	YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)

	Y, U, V = cv2.split(YUV)

	# Using the Contrast Limited Adaptive Histogram Equalization class to enhance the contrast
	# Create the CLAHE object and set the clip limit and tile grid size:
	CLAHE = cv2.createCLAHE(clipLimit = 4.5, tileGridSize = (3,3))

	# This is done to improve definition in the image:
	Enhanced_Y = CLAHE.apply(Y)

	# This is used to remove the background:
	Enhanced_U = CLAHE.apply(U)

	# Create initial mask to remove the background:
	_, Threshold = cv2.threshold(Enhanced_U, 176, 255, cv2.THRESH_TRUNC)
	Adaptive_Threshold = cv2.adaptiveThreshold(Threshold, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 275, 2)

	Enchanced_YUV = cv2.merge((Enhanced_Y,U,V))
	Enchanced_BGR = cv2.cvtColor(Enchanced_YUV, cv2.COLOR_YUV2BGR)
	Enchanced_B, Enchanced_G, Enchanced_R = cv2.split(Enchanced_BGR)

	Removed_Background = ApplyMask(Adaptive_Threshold)

	# Create the final mask to clean more of the noise:
	Enhanced_YUV2 = cv2.cvtColor(Removed_Background, cv2.COLOR_BGR2YUV)
	u = Enhanced_YUV2[:,:,1]

	_, maxVal, _, _ = cv2.minMaxLoc(u)
	masked_range = cv2.inRange(u, 0, maxVal-3)
	final_mask = cv2.bitwise_xor(masked_range, Adaptive_Threshold)
	final_mask = cv2.bitwise_not(final_mask)

	final_image = ApplyMask(final_mask)

	cv2.imwrite("./final_image.png", final_image)

	reply = gui.buttonbox(closing_message, image = "./final_image.png", choices = choices)

	# Close the application if they click no or if they try to close the window
	if reply == 'No' or reply != 'Yes':
		gui.msgbox(final_message, title = "Thanks!")
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