#!/usr/bin/env python

__author__ = "Dzvezdana Arsovska"

from Tkinter import *
import cv2
import os
from PIL import Image, ImageTk
import numpy as np
import tkFileDialog as filedialog

#__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.load_img()

    def create_widgets(self):
        self.btn_apply = Button(self, text="Apply", command=self.apply_changes).grid(column=3, row=1, rowspan=2)
        self.btn_reset = Button(self, text="Reset", command=self.reset_changes).grid(column=4, row=1, rowspan=2)
        self.dropVarLable=Label(self,text="Select Image:").grid(row=1,column=1)
        optionList = ['1','2','3','4','5']
        self.dropVar=StringVar()
        self.dropVar.set('1') 
        self.dropMenu1 = OptionMenu(self, self.dropVar, *optionList, command=self.func)
        self.dropMenu1.grid(row=1,column=2)
        self.canvas = Canvas(self, height=400, width=600)
        self.canvas.grid(columnspan=6, rowspan=6, row=4, column=0)
    
    def prep_canvas(self,img_dsip):
        img_dsip = cv2.resize(img_dsip, (600, 300))
        img_dsip = Image.fromarray(img_dsip)
        self.canvas.image = ImageTk.PhotoImage(image=img_dsip)
        self.canvas.create_image(0, 0, anchor="nw", image=self.canvas.image)
    
    def concat_images(self, imga, imgb):
        ha,wa = imga.shape[:2]
        hb,wb = imgb.shape[:2]
        max_height = np.max([ha, hb])
        total_width = wa+wb
        new_img = np.zeros((max_height, total_width), dtype=np.uint8)
        new_img[0:ha,0:wa]=imga
        new_img[0:hb,wa:wa+wb]=imgb
        self.prep_canvas(new_img)
    
    def disp_img(self):
        x = self.dropVar.get()
        if x == '1':
            self.concat_images(self.img1,self.img11)
        elif x == '2':
            self.concat_images(self.img2,self.img22)
        elif x == '3':
            self.concat_images(self.img3,self.img33)
        elif x == '4':
            self.concat_images(self.img4,self.img44)
        elif x == '5':
            self.concat_images(self.img5,self.img55)
    
    def func(self,value):
        self.disp_img()

    def read_img(self, name):
        #image = cv2.imread(os.path.join(__location__, name))
        image = cv2.imread(name)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret,thresh1 = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
        return thresh1
        
    def load_img(self):
        self.img1 = self.read_img('squares.png')
        self.img2 = self.read_img('fingerprint.png')
        self.img3 = self.read_img('head.png')
        self.img4 = self.read_img('circles.png')
        self.img5 = self.read_img('data.png')
        self.img11 = self.img1
        self.img22 = self.img2
        self.img33 = self.img3
        self.img44 = self.img4
        self.img55 = self.img5
        self.disp_img()

    def reset_changes(self):
        x = self.dropVar.get()
        if x == '1':
            self.img11 = self.img1 
        elif x == '2':
            self.img22 = self.img2
        elif x == '3':
            self.img33 = self.img3
        elif x == '4':
            self.img44 = self.img4
        elif x == '5':
            self.img55 = self.img5
        self.disp_img()
        
    def apply_changes(self):
        x = self.dropVar.get()
        
        if x == '1':

            mask11 = np.ones((5,5),np.uint8)
            self.img11 = cv2.erode(self.img1,mask11,iterations = 4)
            self.img11 = cv2.dilate(self.img11,mask11,iterations = 4)
            
        elif x == '2':
            
            mask22 = np.ones((8,8),np.uint8)
            self.img22 = cv2.morphologyEx(self.img2, cv2.MORPH_OPEN, mask22)
            
        elif x == '3':
            
            mask33 = np.ones((5,5),np.uint8)
            self.img33 = cv2.morphologyEx(self.img3, cv2.MORPH_GRADIENT, mask33)
            
        elif x == '4':
            
            im_floodfill=self.img4
            
            h,w=im_floodfill.shape[:2]
            filled_image=np.zeros((h+2,w+2),np.uint8)
            filled_image[1:h+1,1:w+1]=im_floodfill
            mask=np.zeros((h+4,w+4),np.uint8)
            cv2.floodFill(filled_image,mask,(0,0),255)
            filled_image_reshaped=filled_image[1:h+1,1:w+1]
            im_floodfill_inv=cv2.bitwise_not(filled_image_reshaped)
            self.img44=im_floodfill | im_floodfill_inv
            
        elif x == '5':
            
            ks=9
            A=self.img5
            AC=cv2.bitwise_not(A)
            kernel=np.ones((ks,ks),np.uint8)*255

            kernel5=np.ones((ks+2,ks+2),np.uint8)*255
            kernel5[1:ks+1,1:ks+1]=np.zeros((ks,ks),np.uint8)

            a1=cv2.erode(np.array(A),kernel)
            a2=cv2.erode(np.array(AC),kernel5)

            self.img55=cv2.bitwise_and(a1,a2)
            print('Number of squares is:')
            print(np.sum(self.img55)/255)
            

        
        self.disp_img()
    


root = Tk()
root.title("Morphology app");
app = Application(master=root)
app.mainloop()
