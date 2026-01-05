# -*- coding: utf-8 -*-

"""
Skeleton for first part of the blob-detection coursework as part of INF250
at NMBU (Autumn 2017).
"""

__author__ = "Yngve Mardal Moe"
__email__ = "yngve.m.moe@gmail.com"

import numpy as np
import matplotlib.pyplot as plt
from skimage import io


# Reading in the image
path = '/Users/simenkrogstie/Documents/Programming/Høst 2024/INF250/Mandatory Exercise 1/gingerbreads.jpg'
img = io.imread(path)


def threshold(image, th=None):
    """Returns a binarised version of given image, thresholded at given value.

    Binarises the image using a global threshold `th`. Uses Otsu's method
    to find optimal thrshold value if the threshold variable is None. The
    returned image will be in the form of an 8-bit unsigned integer array
    with 255 as white and 0 as black.

    Parameters:
    -----------
    image : np.ndarray
        Image to binarise. If this image is a colour image then the last
        dimension will be the colour value (as RGB values).
    th : numeric
        Threshold value. Uses Otsu's method if this variable is None.

    Returns:
    --------
    binarised : np.ndarray(dtype=np.uint8)
        Image where all pixel values are either 0 or 255.
    """
    # Setup
    shape = np.shape(image)
    binarised = np.zeros([shape[0], shape[1]], dtype=np.uint8)

    if len(shape) == 3:
        image = image.mean(axis=2)
    elif len(shape) > 3:
        raise ValueError('Must be at 2D image')

    if th is None:
        th = otsu(image)

    # Start thresholding

    binarised = np.where(image < th, 0, 255).astype(np.uint8)

    plt.imshow(binarised, cmap='gray')
    plt.title('gingerbreads binarized')
    plt.axis('on')
    plt.show()

    return binarised


def histogram(image):
    """Returns the image histogram with 256 bins.
    """
    # Setup
    shape = np.shape(image)                      
    histogram = np.zeros(256)                   

    if len(shape) == 3:                         
        image = image.mean(axis=2)               
    elif len(shape) > 3:                         
        raise ValueError('Must be at 2D image')

    for i in range(shape[0]):                    
        for j in range(shape[1]):               
            pixval = int(image[i, j])           
            histogram[pixval] += 1              

    plt.plot(histogram)                         
    plt.title('Gingerbreads histogram')         
    plt.xlabel('Pixel intensity')               
    plt.ylabel('Pixel frequency')                     
    plt.show()

    return histogram


def otsu(image):
    """Finds the optimal threshold value of a given image using Otsu's method.
    """
    hist = histogram(image)  
    th = 0
    max_variance = 0

    pixel_sum= np.sum(hist)  
    hist_norm = hist / pixel_sum  
   
    pixel_values = np.arange(len(hist))  
    total_mean = np.sum(pixel_values * hist_norm)  
    
    background_weight = 0  
    background_mean = 0   
    
    for t in range(len(hist)):
        
        background_weight += hist_norm[t] 
        if background_weight == 0:
            continue  
        
        foreground_weight = 1 - background_weight  
        if foreground_weight == 0:
            break  
        
        background_mean += t * hist_norm[t]  
        
        foreground_mean = (total_mean - background_mean) / foreground_weight
        inter_class_variance = background_weight * foreground_weight * ((background_mean / background_weight - foreground_mean) ** 2)
        
        if inter_class_variance > max_variance:
            max_variance = inter_class_variance
            th = t
    
    return th

# histogram(img)
# otsu(img)
threshold(img)