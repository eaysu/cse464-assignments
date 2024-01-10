import cv2
import numpy as np

def showImage(filter, name):
    cv2.imshow(f"{name}", filter)

test_image = "img1.jpg"    

##### Read the image #####
image = cv2.imread(f"test_images/{test_image}")
##########################

##### Blur the image #####
median = cv2.medianBlur(image, 5)
##########################

##### Applying k-means clustering #####
pixels = median.reshape((-1, 3)) # Reshape the image into a 2D array of pixels
pixels = np.float32(pixels) # Convert the data type to floating point
k = 7 # Define the number of clusters (K)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.5) # Apply K-means clustering
_, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

centers = np.uint8(centers) # Convert the centers to integers
segmented_image = centers[labels.flatten()] # Map the labels to their respective centers
segmented_image = segmented_image.reshape(image.shape) # Reshape the segmented image back to the original shape
#######################################

##### Applying gray-scale #####
gray = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2GRAY )
###############################

##### Applying gray-scale #####
equalized = cv2.equalizeHist(gray)
###############################

##### Applying threshold #####
ret, thresh = cv2.threshold(equalized, 220, 255, cv2.THRESH_BINARY)
##############################

##### Applying closing filter #####
kernel_size = 5
kernel = np.ones((kernel_size, kernel_size), np.uint8)

# Perform closing operation
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
###################################


##### Apply connected components analysis #####
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(closed)

mask = np.zeros_like(closed) # creating mask
min_area = 100 # for ignore white areas that below 100 pixels

# Iterate through each connected component
for i in range(1, num_labels):
    # Extract the region of interest (ROI)
    x, y, w, h, area = stats[i]
    bounding_area = w * h # finding bounding box for every segmentation
    if w > mask.shape[1] * 0.95 or h > mask.shape[0] * 0.95 or (area > min_area and area < bounding_area * 0.25):
        # first and second condition: for avoid losing map-sized and straight roads
        # third condition: for get rid of structures outside the road and white noise smaller than 100 pixels
        # (if the white area < bounding box area * 0.25, program counts the white area as a road))
        mask[labels == i] = 255
################################################

# Convert the single-channel image to a 3-channel image
red_parts = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

# Set the color to red (BGR format) where the thresholded image is white
red_parts[mask > 0] = [0, 0, 255]

# Create a mask where with red parts
red_mask = red_parts[:, :, 2] == 255  # Check if the red channel is fully red

# Replace the corresponding pixels in the original RGB image with the red parts
overlayed = np.copy(image)
overlayed[red_mask] = red_parts[red_mask]

# Display every step results
showImage(image, "original")
showImage(median, "blurred") 
showImage(segmented_image, "k-means")
showImage(gray, "gray")
showImage(equalized, "equalized")
showImage(thresh, "thresholded")
showImage(closed, "closed")  
showImage(mask, "segmented")
showImage(overlayed, "overlayed")

cv2.imwrite(f"output_images/{test_image}", mask)
cv2.imwrite(f"output_images/overlay_{test_image}", overlayed)

cv2.waitKey(0)
cv2.destroyAllWindows()