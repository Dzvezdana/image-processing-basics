#!/usr/bin/env python

__author__ = "Dzvezdana Arsovska"

import numpy as np
from math import pow
from matplotlib import pyplot as plt
from Tkinter import *
import tkFileDialog as filedialog
from PIL import Image
from PIL import ImageTk
from PIL import ImageEnhance
import cv2
from scipy import ndimage

# Variables
content=0
img=0
img_pil=0
panelA=0
sl_var=0
sl1_var=0
img_cv=0
content=0
salt_var2=0
salt_var3=0
kernel=0
imgScale=0
W=0
temp1=0
dilation_var4=0
erosion_var4=0
mean_var=0
sigma_var=0
hpf_var=0
lpf_var=0


# Remove Noise
def remove():
    global img
    image = img
    panelA.configure(image=img)
    panelA.image = img

# Funcions that receive the Scale bar value
def kernel_slider(var1):
    global kernel
    var1=int(var1)
    if var1 % 2!=1: # only odd values for the kernel size
        w1.set(var1+1)
    kernel = w1.get()

def salt_slider(var2):
    global salt_var2
    salt_var2 = var2

def pepper_slider(var3):
    global pepper_var3
    pepper_var3 = var3

def dilation_slider(var4):
    global dilation_var4
    dilation_var4=var4

def erosion_slider(var14):
    global erosion_var4
    erosion_var4=var14

def sigma_slider(var5):
    global sigma_var
    sigma_var=var5
    
def mean_slider(var6):
    global mean_var
    mean_var=var6
    
def lpf_slider(var7):
    global lpf_var
    lpf_var=var7
    
def hpf_slider(var8):
    global hpf_var
    hpf_var=var8


# Browse for an input image
def select_image():

    global img,panelA,img_pil,x1,x2,img_cv,noisy_image_cv,W,imgScale,histo_cv
    
    # Choose the path

    path = filedialog.askopenfilename()

    # If path is selected
    if len(path) > 0:
        
        # Load the image from disk
        img = cv2.imread(path)
        W = 200.
        height, width, depth = img.shape
        imgScale = W/width
        newX,newY = img.shape[1]*imgScale, img.shape[0]*imgScale
        img = cv2.resize(img,(int(newX),int(newY)))
        img_cv = img
        noisy_image_cv = img
        histo_cv = img
        
        # Conversion to RGB for PIL lib
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Convert the images to PIL format
        img_pil = Image.fromarray(img)
        img = Image.fromarray(img)
        x1 = img
        x2 = img

        # Conversion to ImageTk format
        img = ImageTk.PhotoImage(img)

    if panelA is None:
        
        # Storing of browsed image
        panelA = Label(image=img)
        panelA.image = img
        panelA.grid(row=20,column=0,padx=0,pady=0)

        # Update of image panel
    else:
        panelA.configure(image=img)
        panelA.image = img

#Average filter function
def average():
    input_img = noisy_image_cv
    val=int(kernel)
    mask = np.ones((val,val), np.float32) / (val*val)
    afiltered = cv2.filter2D(input_img, -1, mask)

    afiltered = cv2.cvtColor(afiltered, cv2.COLOR_BGR2RGB)
    afiltered= Image.fromarray(afiltered)
    afiltered= ImageTk.PhotoImage(afiltered)
    panelA.configure(image=afiltered)
    panelA.image = afiltered

#Median filter function
def median():
    input_img = noisy_image_cv
    mfiltered = cv2.medianBlur(input_img, int(kernel))
    mfiltered = cv2.cvtColor(mfiltered, cv2.COLOR_BGR2RGB)
    mfiltered = Image.fromarray(mfiltered)
    mfiltered = ImageTk.PhotoImage(mfiltered)
    panelA.configure(image=mfiltered)
    panelA.image = mfiltered

#min filter function
def min():
    input_img = noisy_image_cv
    b, g, r = cv2.split(input_img)
    blue = ndimage.filters.minimum_filter(b,size = int(kernel))
    green = ndimage.filters.minimum_filter(g,size = int(kernel))
    red = ndimage.filters.minimum_filter(r,size = int(kernel))

    min_filtered = cv2.merge((blue, green, red))
    min_filtered = cv2.cvtColor(min_filtered, cv2.COLOR_BGR2RGB)
    min_filtered = Image.fromarray(min_filtered)
    min_filtered = ImageTk.PhotoImage(min_filtered)
    panelA.configure(image=min_filtered)
    panelA.image = min_filtered

#max filter function
def max():
    input_img = noisy_image_cv
    b, g, r = cv2.split(input_img)
    blue = ndimage.filters.maximum_filter(b, size = int(kernel))
    green = ndimage.filters.maximum_filter(g, size = int(kernel))
    red = ndimage.filters.maximum_filter(r, size = int(kernel))

    max_filtered = cv2.merge((blue, green, red))
    max_filtered = cv2.cvtColor(max_filtered , cv2.COLOR_BGR2RGB)
    max_filtered = Image.fromarray(max_filtered )
    max_filtered = ImageTk.PhotoImage(max_filtered )
    panelA.configure(image=max_filtered )
    panelA.image = max_filtered

#function that adds s&p noise
def salt_and_pepper():
    global noisy_image_cv

    input_img=img_pil
    r, c = input_img.size
    img_np = np.array(input_img)
    rand_arr = np.random.random((r, c))
    rand_arr = rand_arr.transpose()

    s=(float(salt_var2)+90)/100
    p=float(pepper_var3)/100

    salt_val = np.ones(rand_arr.shape) * s
    pepper_val = np.ones(rand_arr.shape) * p

    salt = np.uint8(np.greater(rand_arr, salt_val) * 255)
    salt3 = np.dstack((salt, salt, salt))

    pepper = np.uint8(np.greater(rand_arr, pepper_val) * 1)
    pepper3 = np.dstack((pepper, pepper, pepper))

    m = int(dilation_var4)
    mask = np.ones((m, m), np.uint8)
    dilated = cv2.dilate(salt3, mask, iterations=1)

    mm = int(erosion_var4)
    mask = np.ones((mm, mm), np.uint8)
    eroded = cv2.erode(pepper3, mask, iterations=1)

    temp = cv2.add(dilated, img_np)
    temp = cv2.multiply(temp, eroded)

    n1=np.uint8(temp)
    noisy_image_cv = np.asarray(n1).copy()
    noisy_image_cv=cv2.cvtColor(noisy_image_cv, cv2.COLOR_RGB2BGR)

    noisy_img = Image.fromarray(np.uint8(temp))
    noisy_img = ImageTk.PhotoImage(noisy_img)
    panelA.configure(image=noisy_img)
    panelA.image = noisy_img


#Salt noise function
def salt_only():
    global noisy_img_cv

    input_img = img_pil
    r, c = input_img.size
    img_np = np.array(input_img)
    rand_arr = np.random.random((r, c))
    rand_arr = rand_arr.transpose()

    s = (float(salt_var2) + 90) / 100
    salt_val = np.ones(rand_arr.shape) * s
    salt = np.uint8(np.greater(rand_arr, salt_val) * 255)
    salt3 = np.dstack((salt, salt, salt))

    m = int(dilation_var4)
    mask = np.ones((m, m), np.uint8)
    dilated = cv2.dilate(salt3, mask, iterations=1)
    temp = cv2.add(dilated, img_np)

    n1 = np.uint8(temp)
    noisy_image_cv = np.asarray(n1).copy()
    noisy_image_cv = cv2.cvtColor(noisy_image_cv, cv2.COLOR_RGB2BGR)

    noisy_img = Image.fromarray(np.uint8(temp))
    noisy_img = ImageTk.PhotoImage(noisy_img)
    panelA.configure(image=noisy_img)
    panelA.image = noisy_img

#Pepper noise function
def pepper_only():
    global noisy_image_cv

    input_img = img_pil
    r, c = input_img.size
    img_np = np.array(input_img)
    rand_arr = np.random.random((r, c))
    rand_arr = rand_arr.transpose()

    p = float(pepper_var3) / 100
    pepper_val = np.ones(rand_arr.shape) * p
    pepper = np.uint8(np.greater(rand_arr, pepper_val) * 1)
    pepper3 = np.dstack((pepper, pepper, pepper))

    m = int(erosion_var4)
    mask = np.ones((m, m), np.uint8)
    eroded = cv2.erode(pepper3, mask, iterations=1)
    
    temp = cv2.multiply(img_np, eroded)
    n1 = np.uint8(temp)
    noisy_image_cv = np.asarray(n1).copy()
    noisy_image_cv = cv2.cvtColor(noisy_image_cv, cv2.COLOR_RGB2BGR)

    noisy_img = Image.fromarray(np.uint8(temp))
    noisy_img = ImageTk.PhotoImage(noisy_img)
    panelA.configure(image=noisy_img)
    panelA.image = noisy_img
    
#Add random gaussian noise
def Gauss():
    global noisy_image_cv
    input_img=img_cv
    print(mean_var)
    print(sigma_var)
    print(input_img.shape)

#Draws random samples from a normal (Gaussian) distribution. It's input
#arguments are the mean, the standard deviation and the size of the input image.
# The values of mean and sigma are changed using sliders.
	
    noise=np.random.normal(float(mean_var), float(sigma_var), input_img.shape)
    noise=noise.astype(np.uint8)
    noisy_image_cv = cv2.add(input_img,noise)

    noisy_img = cv2.cvtColor(noisy_image_cv, cv2.COLOR_BGR2RGB)
    noisy_img = Image.fromarray(np.uint8(noisy_img))
    noisy_img = ImageTk.PhotoImage(noisy_img)
    panelA.configure(image=noisy_img)
    panelA.image = noisy_img

#ideal low pass filter   
def LPF():
    
    input_img= cv2.cvtColor(noisy_image_cv, cv2.COLOR_BGR2GRAY)
    dft = cv2.dft(np.float32(input_img),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = input_img.shape
    crow,ccol = int(rows/2) , int(cols/2)
    
# create a mask, the center square is 1
    mask1 = np.zeros((rows,cols,2),np.uint8)
    mask1[crow-int(lpf_var):crow+int(lpf_var), ccol-int(lpf_var):ccol+int(lpf_var)] = 1

    mask = np.zeros((rows,cols),np.uint8)
    mask[crow-int(lpf_var):crow+int(lpf_var), ccol-int(lpf_var):ccol+int(lpf_var)] = 1

# apply mask and inverse DFT
    fshift = dft_shift*mask1
    f_ishift = np.fft.ifftshift(fshift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

    plt.subplot(131),plt.imshow(img_back, cmap = 'gray')
    plt.title('Image after LPF'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(mask, cmap = 'gray')
    plt.title('Mask'),plt.xticks([]), plt.yticks([])
    plt.show()

#ideal high pass filter   
def HPF():
    
    input_img= cv2.cvtColor(noisy_image_cv, cv2.COLOR_BGR2GRAY)
    dft = cv2.dft(np.float32(input_img),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    rows, cols = input_img.shape
    crow,ccol = int(rows/2) , int(cols/2)

    # creates a mask, the center square is 0
    dft_shift[crow-int(hpf_var):crow+int(hpf_var), ccol-int(hpf_var):ccol+int(hpf_var)] = 0

    mask = np.ones((rows,cols),np.uint8)
    mask[crow-int(hpf_var):crow+int(hpf_var), ccol-int(hpf_var):ccol+int(hpf_var)] = 0

    # apply mask and inverse DFT
    f_ishift = np.fft.ifftshift(dft_shift)
    img_back = cv2.idft(f_ishift)
    img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

    plt.subplot(131),plt.imshow(img_back, cmap = 'gray')
    plt.title('Image after HPF'), plt.xticks([]), plt.yticks([])
    plt.subplot(132),plt.imshow(img_back)
    plt.title('Result in JET'), plt.xticks([]), plt.yticks([])
    plt.show()

root = Tk()
root.title("Image Processing GUI")
panelA = None

var1 = IntVar()
var2 = IntVar()
var3 = IntVar()
var4 = IntVar()
var14 = IntVar()
var5 = IntVar()
var6 = IntVar()
var7 = IntVar()
var8 = IntVar()


#Button for browsing an image
btn1 = Button(root, text="Browse Button", bg="green", command=select_image)
btn1.grid(row=0,column=0)

# Average Filter
btn2 = Button(root, text="Average filter", bg="yellow", command=average)
btn2.grid(row=0,column=8,padx=5,pady=5)

# Median Filter
btn3 = Button(root, text="Median filter", bg="yellow", command=median)
btn3.grid(row=0,column=7,pady=5)

# Min Filter
btn4 = Button(root, text="Min filter", bg="yellow", command=min)
btn4.grid(row=1,column=8)

# Max Filter
btn5 = Button(root, text="Max filter", bg="yellow", command=max)
btn5.grid(row=1,column=7)

# S&P noise button
btn6 = Button(root, text="Salt&Pepper noise", bg="blue", command=salt_and_pepper)
btn6.grid(row=3,column=0)

# Salt noise button
btn7 = Button(root, text="Salt noise", bg="blue", command=salt_only)
btn7.grid(row=4,column=0)

# Pepper noise button
btn8 = Button(root, text="Pepper noise", bg="blue", command=pepper_only)
btn8.grid(row=5,column=0)

# S&P Remove
btn9 = Button(root, text="Remove Noise", bg="blue", command=remove)
btn9.grid(row=6,column=0)

#Slider for kernel
Label(root, text="Kernel size").grid(row=2,column=4)
w1 = Scale(root, from_=1, to=15,tickinterva=2, resolution = 1, orient=HORIZONTAL, length = 200, command=kernel_slider,variable=var1)
w1.set(3)
w1.grid(row=3,column=4)

#Slider for salt value
Label(root, text="Salt value").grid(row=4,column=4)
w2 = Scale(root, from_=9, to=1,tickinterva=1, resolution = 1, orient=HORIZONTAL, length = 200, command=salt_slider,variable=var2)
w2.set(9)
w2.grid(row=5,column=4)

#Slider for pepper value
Label(root, text="Pepper value").grid(row=2,column=5)
w3 = Scale(root, from_=1, to=9,tickinterva=1, resolution = 1, orient=HORIZONTAL, length = 200, command=pepper_slider,variable=var3)
w3.set(1)
w3.grid(row=3,column=5)

#Slider for dilation kernel
Label(root, text="Dilation kernel").grid(row=4,column=5)
w4 = Scale(root, from_=1, to=9,tickinterva=1, resolution = 1, orient=HORIZONTAL, length = 200, command=dilation_slider,variable=var4)
w4.set(1)
w4.grid(row=5,column=5)

#Slider for erosion kernel
Label(root, text="Erosion Kernel").grid(row=6,column=4)
w5 = Scale(root, from_=1, to=9,tickinterva=1, resolution = 1, orient=HORIZONTAL, length = 200, command=erosion_slider,variable=var14)
w5.set(1)
w5.grid(row=7,column=4)

#Sigma slider
Label(root, text="Sigma").grid(row=2,column=6)
w6 = Scale(root, from_=0.1, to=5,tickinterva=1, resolution = 0.1, orient=HORIZONTAL, length = 200,command=sigma_slider,variable=var5)
w6.set(0.5)
w6.grid(row=3,column=6)

#Mean slider
Label(root, text="Mean").grid(row=4,column=6)
w7 = Scale(root, from_=0.1, to=5,tickinterva=1, resolution = 0.1, orient=HORIZONTAL, length = 200,command=mean_slider, variable=var6)
w7.set(0.5)
w7.grid(row=5,column=6)

#LPF slider
Label(root, text="LPF").grid(row=6,column=5)
w8 = Scale(root, from_=10, to=50,tickinterva=10, resolution = 5, orient=HORIZONTAL, length = 200,command=lpf_slider, variable=var7)
w8.set(10)
w8.grid(row=7,column=5)

#HPF slider
Label(root, text="HPF").grid(row=6,column=6)
w9 = Scale(root, from_=10, to=50,tickinterva=10, resolution = 5, orient=HORIZONTAL, length = 200,command=hpf_slider, variable=var8)
w9.set(10)
w9.grid(row=7,column=6)

# Gauss noise button
btn10 = Button(root, text="Gauss noise", bg="blue",command=Gauss)
btn10.grid(row=7,column=0)

# HPF button
btn11 = Button(root, text="HPF", bg="blue",command=HPF)
btn11.grid(row=0,column=9)

# LPF button
btn12 = Button(root, text="LPF", bg="blue",command=LPF)
btn12.grid(row=1,column=9)

# Histogram plotting (for the original image and it plots different histogram if some changes are made (like grayscale or gamma change))
def histo_plot(event):
    
    his=x1.convert('RGB')
    his = np.array(his)
    his = his[:, :, ::-1].copy()
    plt.hist(his.ravel(),256,[0,256]); plt.show()

#Button for histogram
btn15 = Button(root, text="Histogram", bg="gray")
btn15.grid(row=4,column=8)
btn15.bind('<Button-1>',histo_plot)

root.mainloop()

