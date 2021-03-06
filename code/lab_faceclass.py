# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 13:16:47 2017

@ Author: Carter
@ Purpose: Classify a tile image using pre-trained model
"""

from skimage import io, color
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import LinearSVC
import numpy as np
from matplotlib import pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib
import image_slicer

mlMod = joblib.load('multiTest.pkl')

ScStd = np.asarray([ 20.05160679,  26.71302974,  28.34072409])
ScMean = np.asarray([ 51.11707912,   9.64668695,  27.22938423])

filename="../trainingimg/cropped_faces/lightingD (5).jpg"
rgb = io.imread(filename)
lab = color.rgb2lab(rgb)

def interpret(filename):
    image_slicer.slice(filename,9)

    clrCounts = [0,0,0,0,0,0]
    clrs = ['B','R','G','O','W','Y']

    extens = ".jpg"
    prefix = filename.replace(extens,"")
    
    face = [['0','0','0'],
            ['0','0','0'],
            ['0','0','0']]
    face = np.asarray(face)
    
    for row in range(1,4):
        for col in range(1,4):
            curr_file = prefix + "_0" + str(row) + "_0" + str(col) + ".png"
            
            print([row,col])
            img = io.imread(curr_file)
            rows,cols,rgb = img.shape
            img_crop = img[round(rows/4):round(rows*3/4), round(cols/4):round(cols*3/4)]
#            plt.imshow(img_crop)
            img_lab = color.rgb2lab(img_crop)
            
            max_rows, max_cols, hsv = img_lab.shape
    
            for pix_row in range(max_rows):
                for pix_col in range(max_cols):
                    
                    currPix = img_lab[pix_row, pix_col, :]
                    currPix = np.asarray([currPix])
                    currPix = currPix - ScMean
                    currPix = currPix / ScStd
                    
                    choice = mlMod.predict(currPix)
                    #print(choice)
                    clrCounts[choice-1] = clrCounts[choice-1] + 1

#            print(clrCounts)
            ind = np.argmax(clrCounts)
            face[row-1,col-1] = clrs[ind]
            clrCounts = [0,0,0,0,0,0]
               
#    print(clrCounts)      
    return face     

print(interpret(filename))
   