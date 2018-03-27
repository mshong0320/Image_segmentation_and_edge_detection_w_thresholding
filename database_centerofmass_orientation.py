#!/usr/bin/python

'''
Python code for obtaining the center of mass and orientation of segmented objects. 
created by Minsung Chris Hong.
'''

import sys, os, math, cv2, numpy as np
import pprint
import copy


def p3(labeled_image): #returns a list [database_out, output_image]
	fnameout = raw_input("Enter your output filename here for p1c: ")
	labeled = copy.copy(labeled_image)
	rows,cols = labeled.shape
	label1 = 110 # label for object 1 recognized
	label2 = 180 # another label for object 2 recognized
	database_out = {} # output database list initialized
	output_image = copy.copy(labeled_image) #copy the contents in labeled_image
	dict_of_attributes = {} #attributes' order is as follows: [ x_pos, y_pos, area, a, b, c, theta_min, theta_max, E_min, E_max ]
	count = 0
	count1 = 0 #area of the gray-scale labeled pixels of object 1 assuming each pixel area is 1.
	count2 = 0 # area of the gray-scale labeled pixels of object 2 assuming each pixel area is 1. 
    
    # Compute area, x_pos, y_pos for the two labeled objects!
	x_position1 = 0
	y_position1 = 0
	x_position2 = 0
	y_position2 = 0
	Spring_Green = (0,255,127) #color code for the line

	for i in range(rows):
		for j in range(cols):
			Label = labeled[i][j]
			if Label == label1:
				x_position1 += j #updates the x-position values 
				y_position1 += i #updating the y-position values
				count1 += 1 
				dict_of_attributes[Label] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #initialize
				dict_of_attributes[Label][0] = x_position1
				dict_of_attributes[Label][1] = y_position1
				dict_of_attributes[Label][2] = count1 #updating the area by incrementing w/ pixel area
			elif Label == label2:
				x_position2 += j #updates the x-position values 
				y_position2 += i #updating the y-position values
				count2 += 1
				dict_of_attributes[Label] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #initialize
				dict_of_attributes[Label][0] = x_position2
				dict_of_attributes[Label][1] = y_position2
				dict_of_attributes[Label][2] = count2 #updating the area by incrementing w/ pixel area
			elif Label == 0:
				dict_of_attributes[Label] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
				count += 1
				dict_of_attributes[Label][2] = count

    # Divide x_pos and y_pos by area to get the mean positions of each object
	for key in dict_of_attributes:
		if key > 0:
			dict_of_attributes[key][0] = dict_of_attributes[key][0] / dict_of_attributes[key][2] # the mean x_position value in this pixel image
			dict_of_attributes[key][1] = dict_of_attributes[key][1] / dict_of_attributes[key][2] # the mean y_position value in this pixel image
	#print dict_of_attributes
	
    # Compute values of a, b, c 
	for i in range(rows):
		for j in range(cols):
			Label = labeled_image[i][j]
			if Label == label1: # Not background
            	#change coordinates 
				x_prime = j - dict_of_attributes[Label][0] # (x - x_position(mean))
				y_prime = i - dict_of_attributes[Label][1] # (y - y_position(mean))

				#updates a,b,c
				a = (x_prime * x_prime)
				b = (2 * x_prime * y_prime)
				c = (y_prime * y_prime)

				dict_of_attributes[Label][3] += a 
				dict_of_attributes[Label][4] += b 
				dict_of_attributes[Label][5] += c
			elif Label == label2:
				x_prime = j - dict_of_attributes[Label][0] # (x - x_position(mean))
				y_prime = i - dict_of_attributes[Label][1] # (y - y_position(mean))

				#updates a,b,c
				a = (x_prime * x_prime)
				b = (2 * x_prime * y_prime)
				c = (y_prime * y_prime)

				dict_of_attributes[Label][3] += a 
				dict_of_attributes[Label][4] += b 
				dict_of_attributes[Label][5] += c
			else:
				pass

    # Compute angles for each labels
	for key in dict_of_attributes:
		a = dict_of_attributes[key][3]
		b = dict_of_attributes[key][4]
		c = dict_of_attributes[key][5]
		if b != 0 and a != c and key != 0:
			theta_1 = (np.arctan2(b, a - c)) / 2 
			theta_2 = theta_1 + (np.pi / 2)
			if theta_1 > 0: 
				dict_of_attributes[key][6] = theta_1
				dict_of_attributes[key][7] = theta_2
				E_1 = computing_E(theta_1, a, b, c)
				E_2 = computing_E(theta_2, a, b, c)
				dict_of_attributes[key][8] = E_1
				dict_of_attributes[key][9] = E_2
			elif theta_1 < 0:
				dict_of_attributes[key][6] = theta_2
				dict_of_attributes[key][7] = theta_1
				E_1 = computing_E(theta_1, a, b, c)
				E_2 = computing_E(theta_2, a, b, c)
				dict_of_attributes[key][8] = E_1
				dict_of_attributes[key][9] = E_2

    # time to collect out database_out
	datab_index = 0
	
    #go through the keys in dict_of_attributes and they will become values to the keys in database_out
	for key in dict_of_attributes:
		if key != 0:
			x_pos = dict_of_attributes[key][0]
			y_pos = dict_of_attributes[key][1]
			area = dict_of_attributes[key][2]
			theta_min = dict_of_attributes[key][6]
			theta_max = dict_of_attributes[key][7]
			min_moment = dict_of_attributes[key][8]
			Roundedness = dict_of_attributes[key][8]/dict_of_attributes[key][9]
			database_out[key] = dict([('mean_x_position', x_pos), ('mean_y_position', y_pos), ('Object_area', area), ('min_moment', min_moment), ('orientation', theta_min), ('Roundness', Roundedness)])
			print "database_out", database_out[key]
			datab_index += 1
			cv2.circle(output_image, (int(x_pos), int(y_pos)), 5, Spring_Green)
			cv2.line(output_image, (int(x_pos - 150 * np.cos(theta_min)), int(y_pos - 150 * np.sin(theta_min))), (int(x_pos + 150 * np.cos(theta_min)), int(y_pos + 150 * np.sin(theta_min))), Spring_Green)
	cv2.imwrite(fnameout, output_image)
	print "output_image", output_image
	return [database_out, output_image]

#Other function used:
def computing_E(theta, a, b, c): #computes E with inputs angles, a, b, c.
	E = (a * np.power(np.sin(theta), 2)) - (b * np.sin(theta) * np.cos(theta)) + (c * np.power(np.cos(theta), 2))
	return E




