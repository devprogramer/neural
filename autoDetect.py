# USAGE
# python /var/www/brain/neural/autoDetect.py --image full.jpg

# import the necessary packages
import numpy as np
import argparse
import cv2
import logging
import json
import os

import copy
import math

from wand.image import Image

from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer


# convert   -crop 10x10+0+0  1.jpeg   tile.jpg

# convert -size 600x400 xc:white canvas.jpg ///neednt

# convert -size 600x400 tile:tile.jpg  canvas2.jpg


sourcePhotoDir = os.path.dirname(os.path.abspath(__file__))+"/../public/auto/audi/"
#resultPhotoDir=os.path.dirname(os.path.abspath(__file__))+"/../public/photos/"

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "path to the image file")
#ap.add_argument("-r", "--result", required = True, help = "path to the result file without extension")
args = vars(ap.parse_args())

imgBasePath, imgBaseExt = os.path.splitext(args["image"])
imgBaseName = os.path.basename(imgBasePath)

# load the image and convert it to grayscale



# filePath =  sourcePhotoDir+args["image"];

with Image(filename=sourcePhotoDir+args["image"]) as img:
    for  k,v in  img.metadata.items():
        if k.startswith('exif:Orientation') :
            if int(v) != 1 :
                if int(v) == 3 :
                    img.rotate(180) 
                elif int(v) == 8 :
                    img.rotate(270)
                elif int(v) == 6 :
                    img.rotate(90)
                img.strip();
    img.resize( 160, 120 )
    img.save(filename=sourcePhotoDir +""+ imgBaseName + "-tmp.jpg")




image = cv2.imread(sourcePhotoDir+imgBaseName + "-tmp.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

imgHeight, imgWidth, channels = image.shape


# cv2.imwrite(sourcePhotoDir +"det/"+ imgBaseName + "opencv-gray.jpg", gray)


######################################  1 var ############################
gray = cv2.GaussianBlur(gray,(5,5),0)

ret,thresh = cv2.threshold(gray, 200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


imArr = [];
for y in thresh.tolist() :
    for x in y :
        p = 0;
        if x > 100 :
            p = 1
        imArr.append(p)


with open(sourcePhotoDir +"det/"+ imgBaseName + ".json", 'w') as outfile:
    json.dump(imArr, outfile)


cv2.imwrite(sourcePhotoDir +"det/"+ imgBaseName + "opencv-thrash.jpg", thresh)
exit(0)

