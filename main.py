import cv2 as cv
import numpy as np

# Load the image in grayscale
img = cv.imread('Formula_IT_2023_Images/s_1_1101_a.tif', cv.IMREAD_GRAYSCALE)

# Normalize the grayscale image
img_normalized = cv.normalize(img, dst=None, alpha=0, beta=65535, norm_type=cv.NORM_MINMAX)

# Apply thresholding to the normalized image to create a binary image
_, thresh = cv.threshold(img_normalized, 150, 65535, cv.THRESH_BINARY)

contours, hierarchies = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contour(s) found')

# Initialize an empty list to store contour areas
contour_areas = []

# Initialize a counter for the number of pieces
piece_count = 0
cluster_count = 0


# Iterate through the detected contours
for contour in contours:
    # Calculate the area of each contour
    area = cv.contourArea(contour)
    contour_areas.append(area)

mean_area = np.mean(contour_areas)
std_deviation = np.std(contour_areas)

# Define a threshold for distinguishing between pieces and clusters
piece_threshold = mean_area - 0.5 * std_deviation
cluster_threshold = mean_area + 0.5 * std_deviation



for contour_area in contour_areas:
    # Compare mean_area with every area in image      
    if contour_area > cluster_threshold:
                cluster_count += 1
    elif contour_area > piece_threshold:
                piece_count += 1

print(f"Number of pieces: {piece_count}")
print(f"Number of clasters: {cluster_count}")

# Display the original image, the normalized image, and the thresholded image
cv.imshow("Original Image", img)
cv.imshow("Normalized Image", img_normalized)
cv.imshow("Thresholded Image", thresh)



cv.waitKey(0)
cv.destroyAllWindows()
