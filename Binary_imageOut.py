#!/usr/bin/python

'''
Python code for binary image generation. 
created by Minsung Chris Hong.

'''

import sys, os, math, cv2, copy
import numpy as np

def p1(gray_in, thresh_val): # return binary_out
	fnameout = raw_input("Enter your output filename here for p1a: ")
	binary_out = copy.copy(gray_in)
	rows,cols = gray_in.shape
	for i in range(rows):
		for j in range(cols):
			if gray_in[i][j] < thresh_val:
				binary_out[i][j] = 0
			else:
				binary_out[i][j] = 255
	cv2.imwrite(fnameout, binary_out)
	return binary_out

	
