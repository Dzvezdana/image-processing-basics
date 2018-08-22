#!/usr/bin/env python

__author__ = "Dzvezdana Arsovska"

import numpy as np
import cv2
import argparse
import os, sys, inspect
import image_utils as utils
from imutils import *
from imutils.perspective import four_point_transform
import glob

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--img_dir", required=True, help="Path to the input images")
args = vars(ap.parse_args())

directory = args["image"]
for filename in glob.glob(directory):
	print(filename)
	#load the image
	im=cv2.imread(filename)
	#fit in screen when displayed
	#im = resize(im, height = 300)

	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	thresh = cv2.adaptiveThreshold(imgray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV,13, 2)
	#blur, then extract edges
	gray = cv2.medianBlur(thresh, 7)
	edged = cv2.Canny(gray, 30, 150, apertureSize=5) #30,150

	# cv2.imshow("Outline", edged)
	# cv2.waitKey(1000)

	im2, contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	cnt = max(contours, key=cv2.contourArea)
	
	# cnts = sorted(contours, key = cv2.contourArea, reverse = True)
	# cv2.drawContours(im, cnts[:-1], 0, (0,255,0), 3)
	# cv2.imshow("Largest contour", im)
	# cv2.waitKey(1000)

	hull = cv2.convexHull(cnt)
	# cv2.drawContours(im,[hull],0, (255,0,0),2)
	# cv2.imshow("Outline1", im)
	# cv2.waitKey(1000)

	rect = cv2.minAreaRect(hull)
	box = np.int0(cv2.boxPoints(rect))
	# cv2.drawContours(im,[box],0, (0,0,255),2)
	# cv2.imshow("Box", im)
	# cv2.waitKey(1000)

	approx = cv2.approxPolyDP(hull, 0.02 * cv2.arcLength(hull, True), True)
	if len(approx) == 4:
		box = approx.reshape(4,2)

	# cv2.drawContours(im, [box], -1, (0, 255, 0), 3)
	# cv2.imshow("Final", im)
	# cv2.waitKey(1000)

	# apply 4 points transformation 
	output = four_point_transform(im, box)
	# create a directory for saving output images
	dir, sep, tail = directory.partition('*')
	path = dir + "output_imagess"
	if not os.path.exists(path):
		os.makedirs(path)

	# save images
	filename_w_ext = os.path.basename(filename)
	file_name, file_extension = os.path.splitext(filename_w_ext)
	save_dir = path + "/" + file_name + "_updated" + file_extension
	print("SAVING IMAGE IN DIR " + save_dir)

	cv2.imwrite(save_dir, output)
	print("DONE")
	cv2.destroyAllWindows()

