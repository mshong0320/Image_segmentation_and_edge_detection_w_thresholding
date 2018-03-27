#!/usr/bin/python

'''
Edge point location finding script. 
This script will find the locations of the edge points in the image using Sobel 5x5 mask. 
created by Minsung Chris Hong.
'''

import sys, os, math, cv2, numpy as np
import copy
import pprint

fname = "hough_complex_1.pgm"
gray_img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
thres_value = 100

def p5(image): #return edge_image_out 
	fnameout = raw_input("Enter the desired output file name for 2a: ")
	#edge_image_out = copy.copy(image)
	shape = np.shape(image)
	rows = shape[0]
	width = shape[1]
	edge_image_out = np.empty(shape, dtype=int) #set my return edge_image_out matrix 
	max_intensity = 0

	for i in range(rows):
		for j in range(width):
			current_pix_gradient = sobel_masking(image, j, i, rows, width) #convolving sobel mask onto the image pixels.
    
			edge_image_out[i][j] = current_pix_gradient
            
            #finding the max_intensity for normalizing later on
			if (current_pix_gradient > max_intensity):
				max_intensity = current_pix_gradient
    
    # Compute scaled intensities and update it to the elements in the edge_image_out array by iterating through.
	for x in np.nditer(edge_image_out, op_flags=['readwrite']):
		scaled_intensity = (float(x) / float(max_intensity)) * 255.0
		x[Ellipsis] = int(round(scaled_intensity))
		#print x, "new"
    
	cv2.imwrite(fnameout, edge_image_out)
	return edge_image_out


def sobel_masking(image, pix_x, pix_y, rows, width):
	x_gradient = 0.0
	y_gradient = 0.0

    # 5x5 Sobel filter matrix:
	sobel_x_5 = [[-1, -50, 0, 50, 1], [-2, -100, 0, 100, 2], [-3, -150, 0, 150, 3], [-2, -100, 0, 100, 2], [-1, -50, 0, 50, 1]]
	sobel_y_5 = [[1, 2,  3, 2, 1], [50, 100, 150, 100, 10], [0, 0, 0, 0, 0], [-50, -100, -150, -100, -10], [-1, -2, -3, -2, -1]]
	
	for i in range(5):
		for j in range(5):
			intensity = find_intensity(image, pix_x - 3 + j, pix_y - 3 + i, rows, width) #find the intensities covering all 25 pixels centered at the 13th pixel.
            
			if intensity < 0: # if the gray scale intensity of searched pixel location is less than 0, than return 0.
				return 0
            
			x_gradient += (sobel_x_5[i][j] * intensity) # find gradient in x-direction for each pixel of the total 25 pixels centered around the current image pixel.
			y_gradient += (sobel_y_5[i][j] * intensity) # find gradient in y-direction for each pixel of the total 25 pixels centered around the current image pixel.
    
	gradient = np.sqrt(np.power(x_gradient, 2) + np.power(y_gradient, 2)) # gradient magnitude equation to combine x-y-gradients
	return int(round(gradient))

#returns gray_scale intensity values of each pixels
def find_intensity(image, pix_x, pix_y, rows, width):
	if pix_x < 0 or pix_y < 0 or pix_x > (width - 1) or pix_y > (rows - 1):
		return 0
	else:
		return image[pix_y][pix_x]

p = p5(gray_img)
p
