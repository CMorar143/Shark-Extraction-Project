               ############## OPENING COMMENT ##############
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Program to Detect and Extract a Shark From an Image.						  #
# Author: Cian Morar 														  #
# Date: October 2019														  #
# 																			  #
# The algorithm for this program is outlined below:							  #
# 																			  #
# User selects an image. 													  #
# 																			  #
# Convert image to the YUV color space.										  #
# 																			  #
# Extract and enhance the contrast of the Y and U channels.					  #
# 																			  #
# Threshold the U channel to create a mask (for background removal).		  #
# 																			  #
# Using the enhanced Y channel, convert YUV image back to BGR.				  #
# 																			  #
# Apply the mask and convert back to YUV.									  #
# 																			  #
# Extract the U channel from the enhanced YUV image.					 	  #
# 																			  #
# Create another mask (to remove some additional noise from the image).		  #
# 																			  #
# Apply the final mask.	   			  										  #
# 																			  #
# Display the extracted shark.												  #
# 																			  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# import the necessary packages:
import cv2
import easygui as gui

# Messages for the Graphical User Interface:
opening_message = "This Application Allows You to Extract a Shark From an Image.\n\n\n"
instructions = 	  "Please Choose The Image That You Would Like to Use."
closing_message = "\tHere's The Shark!\n\tWould You Like to Select Another Picture?"
final_message =   "\tHave a great day!"
choices = 		  ["Yes", "No"]

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
while (1):
	gui.msgbox(opening_message + instructions, "Hello!")

	F = gui.fileopenbox()
	I = cv2.imread(F)

	YUV = cv2.cvtColor(I, cv2.COLOR_BGR2YUV)
	Y, U, V = cv2.split(YUV)

	# Using the Contrast Limited Adaptive Histogram Equalization class to enhance the contrast
	# Create the CLAHE object and set the clip limit and tile grid size:
	CLAHE = cv2.createCLAHE(clipLimit = 4.5, tileGridSize = (3,3))

	# This improves definition in the image:
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
		exit(0)


               ############## CLOSING COMMENT ##############
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Program to Detect and Extract a Shark From an Image.						  #
# Author: Cian Morar 														  #
# Date: October 2019														  #
# 																			  #
# This program does a fairly good job at generalising for both images.		  #
# 																			  #
# I tested all possible color channels and the Y channel provided the 		  #
# most contrast and definition.					  							  #
# 																			  #
# the U channel proved to be the best for cleaning up noise.  				  #
# 																			  #
# However, it was difficult to remove the noise entirely.					  #
# 																			  #
# Regarding The performance of the algorithm:								  #
# I ran the cProfile module with python to see how quickly it 				  #
# was executing the program. The result was that there was 66943 function 	  #
# calls in 0.268 seconds. This is regarded as well within a normal time	 	  #
# for that many function calls												  #
# 																			  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
