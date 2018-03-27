#!/usr/bin/python

'''
Python code for sequential labeling algorithm using four neighbors. 
Created by Minsung Chris Hong.
'''
import sys, os, math, cv2, copy 
import numpy as np

def p2(binary_in): # returns labels_out
	fnameout = raw_input("Enter your output filename here for p1b: ")
	labels_out = copy.copy(binary_in)
	rows,cols = labels_out.shape

	equiv_table1 = [] # will contain the top-pixels' coordinates for B != C condition
	equiv_table2 = [] # list of all the x-y coordinate info of the left-pixels for when B != C condition
	equiv_table3 = [] # list containing pairings of the elements of the equiv_table1 & 2 lists.
	table1 = [] # list that'll later contain ordered label values in segment 1 that needs to be equated
	table2 = [] # list that'll later contain ordered label values in segment 2 that needs to be equated
	table3 = [] # list that'll later contain label values that failed to be recognized as part of segment 1 or 2, so this will all be just set as segment 1 first.
	label = 100 # label's starting point

	label1 = 110 # label for object 1 recognized
	label2 = 180 # another label for object 2 recognized

	#convert binary values to my label values: so convert 255 --> 100.
	for i in range(rows):
		for j in range(cols):
			if binary_in[i][j] == 0:
				labels_out[i][j] = 0
			else:
				labels_out[i][j] = label

	#get rid of the edge-liers if there are any.
	for i in range(rows):
		if labels_out[i][634] != 0:
			labels_out[i][634] = 0
			labels_out[i][635] = 0
		else:
			pass

	#go through each matrix positions to give new labels according to the matching conditions.
	for i in range(1, rows):
		for j in range(1, cols):
			if labels_out[i][j] != 0:
				if labels_out[i-1][j-1] != 0: #first condition check-point
					labels_out[i][j] = labels_out[i-1][j-1]
				elif labels_out[i-1][j] != 0 and labels_out[i][j-1] == 0 and labels_out[i-1][j-1] == 0: #second condition check-point
					labels_out[i][j] = labels_out[i-1][j]
				elif labels_out[i][j-1] != 0 and labels_out[i-1][j] == 0 and labels_out[i-1][j-1] == 0: #third condition check-point
					labels_out[i][j] = labels_out[i][j-1]
				elif labels_out[i-1][j] == labels_out[i][j-1] and labels_out[i-1][j] != 0 and labels_out[i][j-1] != 0 and labels_out[i-1][j-1] == 0: # fourth condition check-point
					labels_out[i][j] = labels_out[i-1][j] 
				elif labels_out[i-1][j] != labels_out[i][j-1] and labels_out[i-1][j] !=0 and labels_out[i][j-1] != 0 and labels_out[i-1][j-1] == 0: # fifth condition check-point
					labels_out[i][j] = labels_out[i-1][j]
					equiv_table1.append(labels_out[i-1][j])
					equiv_table2.append(labels_out[i][j-1])
				elif labels_out[i-1][j] == labels_out[i][j-1] == labels_out[i-1][j-1] == 0:
					label += 1
					labels_out[i][j] = label
				else:
					print "...", labels_out[i][j]
					pass
			else:
				pass

	#create the equivalence table containing in each row the top pixel's and left pixel's values that should be equivalently labeled.
	for i in range(0, len(equiv_table1)):
		equiv_table3.append([equiv_table1[i],equiv_table2[i]])

	#these conditions will loop through to find correct pairs in equiv_table3 and append those pairs into table 1 and table 2 accordingly
	for i in range(0, len(equiv_table3)-1):
		if i == 0:
			table1.append(equiv_table3[i][0])
			table1.append(equiv_table3[i][1])
			table1.append(equiv_table3[i+1][1])
		elif equiv_table3[i][1] == equiv_table3[i+1][0] and equiv_table3[i][0] in table1 and equiv_table3[i][0] not in table2:
			table1.append(equiv_table3[i][0])
			table1.append(equiv_table3[i][1])
			table1.append(equiv_table3[i+1][1])
		elif equiv_table3[i][1] == equiv_table3[i+1][0] and equiv_table3[i][1] not in table1 and equiv_table3[i][0] != equiv_table3[i-1][1]:
			table2.append(equiv_table3[i][0])
			table2.append(equiv_table3[i][1])
			table2.append(equiv_table3[i+1][1])
		elif equiv_table3[i][1] == equiv_table3[i+2][0] and equiv_table3[i][0] in table1 and equiv_table3[i][0] not in table2:
			table1.append(equiv_table3[i][0])
			table1.append(equiv_table3[i][1])
			table1.append(equiv_table3[i+2][1])
		elif equiv_table3[i][1] == equiv_table3[i+2][0] and equiv_table3[i][0] not in table1 and equiv_table3[i][1] != equiv_table3[i+1][0]:
			table2.append(equiv_table3[i][0])
			table2.append(equiv_table3[i][1])
			table2.append(equiv_table3[i+2][1])
		elif equiv_table3[i][1] == equiv_table3[i+3][0] and equiv_table3[i][0] in table1 and equiv_table3[i][0] not in table2:
			table1.append(equiv_table3[i][0])
			table1.append(equiv_table3[i][1])
			table1.append(equiv_table3[i+3][1])
		elif equiv_table3[i][1] == equiv_table3[i+3][0] and equiv_table3[i][0] not in table1 and equiv_table3[i][1] != equiv_table3[i+1][0]:
			table2.append(equiv_table3[i][0])
			table2.append(equiv_table3[i][1])
			table2.append(equiv_table3[i+3][1])
		elif equiv_table3[i][1] == equiv_table3[i+4][0] and equiv_table3[i][0] in table1 and equiv_table3[i][0] not in table2:
			table1.append(equiv_table3[i][0])
			table1.append(equiv_table3[i][1])
			table1.append(equiv_table3[i+4][1])
		elif equiv_table3[i][1] == equiv_table3[i+4][0] and equiv_table3[i][0] not in table1 and equiv_table3[i][0] != equiv_table3[i-1][1]:
			table2.append(equiv_table3[i][0])
			table2.append(equiv_table3[i][1])
			table2.append(equiv_table3[i+4][1])
		else:
			if equiv_table3[i][0] in table1:
				table1.append(equiv_table3[i][0])
				table1.append(equiv_table3[i][1])
			elif equiv_table3[i][0] in table2:
				table2.append(equiv_table3[i][0])
				table2.append(equiv_table3[i][1])
			else:
				table2.append(equiv_table3[i][0])
				table2.append(equiv_table3[i][1])

	#get rid of the duplicates in the list and rename the sorted tables.
	table1_no_duplic = list(set(table1))
	table2_no_duplic = list(set(table2))
	table1_1 = sorted(table1_no_duplic)
	table2_2 = sorted(table2_no_duplic)

	#reassigning the equivalence by going through each elements in bin_matrix and relabling all of the elements with items in table 1 and table 2.
	for i in range(0,rows-1):
		for j in range(0,cols-1):
			for k in table1_1:
				if labels_out[i][j] == k:
					labels_out[i][j] = label1
				else:
					pass
			for l in table2_2:
				if labels_out[i][j] == l:
					labels_out[i][j] = label2
				else:
					pass

	for i in range(rows):
		for j in range(cols):
			if labels_out[i][j] != 0 and labels_out[i][j] != label1 and labels_out[i][j] != label2:
				labels_out[i][j] = 0

	# outputting the labeled image
	cv2.imwrite(fnameout, labels_out)
	return labels_out #returns the labled matrix
