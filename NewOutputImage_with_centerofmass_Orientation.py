#!/usr/bin/python

'''
For outputing image showing the roundess with orientation and point of center of mass
created by Minsung Chris Hong.

'''

import sys, os, math, cv2, numpy as np
import p1, p2, p3
import copy

# fname = "two_objects.pgm"
# fname1 = "many_objects_1.pgm"

# gray_img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE) 
# gray_img1 = cv2.imread(fname1, cv2.IMREAD_GRAYSCALE) 

# thres_value = 100
# bin_img_out = p1.p1(gray_img, thres_value) #name it a1.pgm
# bin_img_out1 = p1.p1(gray_img1, thres_value) # name it a1_1.pgm

# labeled_img = p2.p2(bin_img_out) # name it a2.pgm

# database_and_outputimg1 = p3.p3(labeled_img)[0] # name it a3_2.pgm
# #database_and_outputimg1 = p3.p3(labeled_img1) # name it a3_2.pgm

def p4(labeled_image, database): # return out_image
	fnameout = "1d.pgm" #output file name
	database1 = p3.p3(labeled_image)[0] #name it a3.pgm
	out_image = copy.copy(labeled_image)
	database_recog = []

	min_moments = []
	roundnesses = []
	min_moments1 = []
	roundnesses1 = []

	for key in database1:
		min_moment = database1[key]['min_moment']
		roundness = database1[key]['Roundness']
		min_moments.append(min_moment)
		roundnesses.append(roundness)

	for key in database:
		min_moment_in = database[key]['min_moment']
		roundness_in = database[key]['Roundness']
		min_moments1.append(min_moment_in)
		roundnesses1.append(roundness_in)

	if getDiff_in_ratio(min_moment, min_moment_in) > 0.9 and getDiff_in_ratio(roundness, roundness_in) > 0.9:
		database_recog.append(database1)

	Data = database_recog[0]

	for key in Data:
		x_pos = Data[key]['mean_x_position']
		y_pos = Data[key]['mean_y_position']

		theta_min = np.radians(Data[key]['orientation'])

		white_color = (255, 0, 0)

		cv2.circle(out_image, (x_pos, y_pos), 5, white_color)
		cv2.line(out_image, (int(x_pos - 50 * np.cos(theta_min)), int(y_pos - 50 * np.sin(theta_min))), (int(x_pos + 50 * np.cos(theta_min)), int(y_pos + 50 * np.sin(theta_min))), white_color)
		cv2.imwrite(fnameout, out_image)

	return out_image

def getDiff_in_ratio(val_1, val_2): # return ratio
	ratio = 1
	if val_1 > val_2:
		ratio = val_2 / val_1
	else:
		ratio = val_1 / val_2
	return ratio


# p = p4(labeled_img, database_and_outputimg1)
# p