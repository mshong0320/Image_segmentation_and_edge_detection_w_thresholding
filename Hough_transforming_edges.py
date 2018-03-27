#!/usr/bin/python

'''
Python code for finding strong lines in the image using Hough Transforming to look 
for arrays with high votes for parameter value. 
Threshold used here is 50. 

This will then paint the detected strong lines with color on a copy of the original scene image.

created by Minsung Chris Hong.
'''

import sys, os, math, cv2, numpy as np
import copy

fname = "hough_complex_1.pgm"
image_in = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
hough_img_in = cv2.imread("hough_out.pgm", cv2.IMREAD_GRAYSCALE)
hough_thres_value = 60

def p7(image, hough_image, hough_thresh): # returns lines_image
	fnameout = "hough_image_out_2c.pgm"
	lines_image = copy.copy(image)
	shape_image = np.shape(lines_image)
	outputimageshape = np.shape(hough_image)

	print outputimageshape
	rows = shape_image[0]
	width = shape_image[1]
	hough_row = outputimageshape[0]
	hough_wid = outputimageshape[1]

	diag_max = int(round(np.sqrt(np.power(rows, 2)+np.power(width, 2)))) #maximum possible distance from origin
	rho_range = range(-diag_max,diag_max)
	rho_max = diag_max
	theta_range = range(-90,90)
	theta_max = 180
	color = (255,255,255)

	for i in range(hough_row-1):
		for j in range(hough_wid-1):
			if hough_image[i][j] > hough_thresh:
				print i,"i, ", j, "j, ", hough_image[i][j], "output"
				rho_interest = i-diag_max # convert back to the right rho
				theta_interest = (j-90)*np.pi/180 # convert back to the correct theta 
				x = rho_interest * np.cos(theta_interest)
				y = rho_interest * np.sin(theta_interest)
				print rho_interest, theta_interest, x, y

				x_1 = x+diag_max*np.cos(theta_interest)
				y_1 = y+diag_max*np.sin(theta_interest) #(x_1)*np.sin(theta_interest)/np.cos(theta_interest)+rho_interest/np.cos(theta_interest)
				print x_1, y_1

				#cv2.circle(hough_image, (j, i), 8, color, 1)
				cv2.line(lines_image, (int(round(y)), int(round(x))), (int(round(y_1)), int(round(x_1))), color, 1)

	cv2.imshow("img", lines_image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	return lines_image

p = p7(image_in, hough_img_in, hough_thres_value)
p
