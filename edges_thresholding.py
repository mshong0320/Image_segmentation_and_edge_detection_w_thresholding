#!/usr/bin/python

'''
Python code for finding the the thresholded edge intensity values in order to get only the strong edges.
Return value would be matrix called edge_thres_image. 
Next, implementation of the Hough Transform for line detection. Line euqation xsin(theta)-ycos(theta) + rho = 0 will be used.
Find the right resolution of the parameters for the accumulator array. 

created by Minsung Chris Hong.

'''

import sys, os, math, cv2, numpy as np
import copy
import pprint

fname = "2a_complex.pgm"
gray_img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
edge_thres_value = 40

def p6(edge_image, edge_thresh): # return [edge_thresh_image, hough_image_out]
	radian = []
	rho_ = []
	fnameout = raw_input("write the output file name for 2b: ")
	shape = np.shape(edge_image)
	edge_thresh_image = np.empty(shape, dtype=int) #set my return edge_image_out matrix 
	rows = shape[0]
	width = shape[1]
	#print rows, width
	
	max_accum_value = 1

	diag_max = int(round(np.sqrt(np.power(rows, 2)+np.power(width, 2)))) #maximum possible distance from origin
	rho_range = range(-diag_max,diag_max)
	rho_max = diag_max
	theta_range = range(-90,90)
	theta_max = 180
	accum_shape = (2*rho_max, theta_max)

	accumulator_array = np.zeros(accum_shape, dtype=int)
	hough_image_out = np.zeros(accum_shape, dtype=int)

	for i in range(rows-1):
		for j in range(width-1):
			if edge_image[i][j] > edge_thresh:
				edge_thresh_image[i][j] = 255
				for k in range(len(theta_range)): #0-179
					l = theta_range[k] # -90 to 90
					rad = l*np.pi/180; # convert to radians from -90 to 90.
					rho = int(round(float((i*np.cos(rad)-j*np.sin(rad))))) # compute the corresponding rho for that theta value.
					rho_index = rho + diag_max
					accumulator_array[rho_index][k] += 1 #fillout the accumulator array 
					
					if (accumulator_array[rho_index][k]) > max_accum_value:
						max_accum_value = accumulator_array[rho_index][k]
			else:
				edge_thresh_image[i][j] = 0
	print "done!"
	print "max_vote in accumulator array is: ", max_accum_value

	hough_shape = np.shape(accumulator_array)
	hough_row = hough_shape[0]
	hough_wid = hough_shape[1]

	for i in range(hough_row-1):
		for j in range(hough_wid-1):
			scaled_votes = float(accumulator_array[i][j])/float(max_accum_value)*255
			hough_image_out[i][j] = scaled_votes

	cv2.imwrite(fnameout, edge_thresh_image)
	cv2.imwrite("hough_out.pgm", hough_image_out)
	print "hough_image_out returned"

	return [edge_thresh_image, hough_image_out]

p = p6(gray_img, edge_thres_value)
p