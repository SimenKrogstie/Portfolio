
# Importing necessary packages for image processing and visualization
import matplotlib.pyplot as plt
from scipy import ndimage
import numpy as np
from skimage import io, measure, draw
from skimage.util import crop
from skimage.filters import threshold_otsu
from skimage.morphology import area_closing, area_opening
from skimage.segmentation import watershed
from skimage.feature import peak_local_max

# Setting path to the image file
filepath = '/Users/simenkrogstie/Documents/Programming/Høst 2024/INF250/Mandatory Exercise 2/DATA.JPG'

# Loading image as grayscale
img = io.imread(filepath, as_gray = True)

# Cropping image to the region of interest
crop_margins = ((300, 300), (600, 600))              
resized_image = crop(img, crop_margins)

# Applying Otsu's thresholding method to determine an optimal binary threshold
threshold_value = threshold_otsu(resized_image)
print(f"Threshold value: {threshold_value}")         

# Manually binarizing the image using a thres, a set threshold value.
thres = 0.54
binary_img = resized_image < thres

# Applying area-based closing to fill small holes in the binary image
img_ac = area_closing(binary_img, area_threshold=10000)

# Applying area-based opening to remove small objects from the binary image
img_ao = area_opening(img_ac, area_threshold=1000)


# Computing a distance map for the binary iomage to measure distances from background to foreground
distance = ndimage.distance_transform_edt(img_ao)

# Detecting local maxima in the distance map to identify potential regions of interest
local_maxi_coords = peak_local_max(
                distance,
                footprint = np.ones((30, 30)),  # Controls sensitivity to nearby maxima
                labels = img_ac,                # Limits detection to labeled regions
                min_distance = 150              # Minimum distance between detected maxima
                )


# Creating a marker array by marking the local maxima in the distance map
local_maxi = np.zeros_like(distance, dtype=bool)
local_maxi[tuple(local_maxi_coords.T)] = True
markers = ndimage.label(local_maxi)[0]

# Applying the watershed algorithm to segment the image based on the distance map and markers
labels = watershed(-distance, markers, mask=img_ao, watershed_line=True)

# Measuring properties of labeled regions in the segmented image
properties = measure.regionprops(labels)

# Reloading the original image in color to visualize the segmentation results
img_ = io.imread(filepath)
cropped_img_ = crop(img_, ((300, 300), (600, 600), (0,0)), copy=True)

# Drawing rectangles around objects larger than a specified size threshold
for i, prop in enumerate(properties):
    value = prop.major_axis_length
    if value > 330:                                            # Filtering regions based on size
        y0, x0, y1, x1 = prop.bbox                             # Bounding box coordinates for the region
        for offset in range(0, 15):                            # Creating a thicker rectangle by iterating over offsets
            rr, cc = draw.rectangle_perimeter(                 
                            (y0 + offset, x0 + offset),        # Start point of rectangle
                            end=(y1 - offset, x1 - offset),    # End point of rectangle
                            shape=cropped_img_.shape)          # Ensures boundaries fit within the image
            cropped_img_[rr, cc] = (0, 0, 255)                 # Setting the rectangle color to blue


# Displaying the final image with rectangles drawn on detected regions. 
plt.imshow(cropped_img_)
plt.show() 





### FRA NOTEBOOK
properties = measure.regionprops(labels)
print("Number of labels:", len(properties))

img_ = io.imread(filepath)
cropped_img_ = crop(img_, ((300, 300), (600, 600), (0,0)), copy=True)

# Markling the M&Ms with a blue boundingbox, based on major-axis-length.
for i, prop in enumerate(properties):
    value = prop.major_axis_length
    if value > 330:
        y0, x0, y1, x1 = prop.bbox
        for offset in range(0, 15):  
            rr, cc = draw.rectangle_perimeter(
                            (y0 + offset, x0 + offset),
                            end=(y1 - offset, x1 - offset),
                            shape=cropped_img_.shape)
            
            cropped_img_[rr, cc] = (0, 0, 255)

plt.imshow(cropped_img_)
plt.axis('off')
plt.show() 