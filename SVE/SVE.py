#!/usr/bin/env python

__author__ = "Dzvezdana Arsovska"

import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread('old.jpg')
image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

#Compute SVD of the image, s contains the sorted singular values
u,s,v=np.linalg.svd(image.astype(np.double)/255.0,1,1)
u.shape, v.shape, s.shape

#Creates random normal distribution with mean = 0.5, variance = 1 (synthetic intesity matrix)
pseudo=np.random.normal(0.5,1,image.shape)

#Compute the SVD of the synthetic intesity matrix
#full_matrices=1, compute_uv=0, s2 is the singular value matrix of the equalized image
s_p=np.linalg.svd(pseudo,1,0)

#First(largest) singular value of s2 diveded by the largest singular value of s
ksi=s_p[0]/s[0]
print(ksi)

#ksi > 1 if the image has low contrast with low intensity
#ksi < 1 if the image has low contrast with high intensity

#Create the new diagonal matrix and recontruct the image

#u is mxm,v is nxn matrix, S is mxn matrix filled with zeros
S = np.zeros((u.shape[0], v.shape[0]))

#Multiply the matrix s with ksi
S[:s.shape[0], :s.shape[0]] = np.diag(ksi*s)

new=np.dot(u, np.dot(S, v))*255.0

np.clip(new,0,255,new)
sve_image=new.astype(np.uint8)

numpy_horizontal_concat = np.concatenate((image, sve_image), axis=1)

h,w = numpy_horizontal_concat.shape

font = cv2.FONT_HERSHEY_SIMPLEX
#color (200,255,155)
cv2.putText(numpy_horizontal_concat,'OLD                  NEW',(w/16,h/16), font, 1, (0,0,40), 2, cv2.LINE_AA)

cv2.namedWindow('My Image With Text', cv2.WINDOW_NORMAL)

cv2.imshow('numpy_horizontal_concat', numpy_horizontal_concat)
cv2.waitKey(7000)
cv2.destroyAllWindows()

#plot histogram
his = np.array(sve_image)
plt.hist(his.ravel(),256,[0,256]); plt.show()

his1 = np.array(image)
plt.hist(his1.ravel(),256,[0,256]); plt.show()
