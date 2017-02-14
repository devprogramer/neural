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

import datetime
import mysql.connector

from urllib2 import urlopen

import hashlib
import time



def prepareImage(path, marka_id):
    sourcePhotoDir = '../auto/'
    imgBaseName =  hashlib.md5( path+str(time.time()) ).hexdigest();

    if not os.path.exists(sourcePhotoDir +str(marka_id)+"/"):
        os.makedirs(sourcePhotoDir +str(marka_id)+"/")
    sourcePhotoDir = '../auto/'+str(marka_id)+"/"

    if not os.path.exists(sourcePhotoDir +"tmp/"):
        os.makedirs(sourcePhotoDir +"tmp/")


    response = urlopen("https://cdn.riastatic.com/photos/"+ path.replace(".jpg", "mx.jpg"))


    with Image(file=response) as img:
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
        img.resize( 40, 30 )
        img.save(filename=sourcePhotoDir +"tmp/"+ imgBaseName + "-tmp.jpg")




    image = cv2.imread(sourcePhotoDir+"tmp/"+imgBaseName + "-tmp.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    imgHeight, imgWidth, channels = image.shape


	# cv2.imwrite(sourcePhotoDir +"det/"+ imgBaseName + "opencv-gray.jpg", gray)


	######################################  1 var ############################
	# gray = cv2.GaussianBlur(gray,(5,5),0)
    medianbluered = cv2.medianBlur(gray,3)

	# ret,thresh = cv2.threshold(medianbluered, 200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    thresh = cv2.adaptiveThreshold(medianbluered,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
	            cv2.THRESH_BINARY,11,3)

	# cv2.imwrite(sourcePhotoDir +"det/"+ imgBaseName + "opencv-thrash.jpg", thresh);

    imArr = [];
    for y in thresh.tolist() :
        for x in y :
            p = 0;
            if x > 100 :
                p = 1
            imArr.append(p)


    if not os.path.exists(sourcePhotoDir +"json/"):
        os.makedirs(sourcePhotoDir +"json/")
    with open(sourcePhotoDir +"json/"+ imgBaseName + ".json", 'w') as outfile :
        json.dump(imArr, outfile)

    # print sourcePhotoDir+ "tmp/"+ imgBaseName + "-tmp.jpg"
    os.unlink(sourcePhotoDir+ "tmp/"+ imgBaseName + "-tmp.jpg")

	# cv2.imwrite(sourcePhotoDir +"det/"+ imgBaseName + "opencv-thrash.jpg", thresh)


markaPhoto = {}

cnx = mysql.connector.connect(host='10.1.18.111',user="master", password="gtnhjdbx", database='auto4_cars')
cursor = cnx.cursor()

query = ('''SELECT mn.marka_id, mn.model_id, mp.path 
	FROM auto3.models_photos mp inner join auto3.model_new mn on mn.model_id = mp.model_id and mn.lang_id = 2 
	where mn.marka_id in (84, 9, 24, 29, 52, 79, 48, 23, 6, 55) ''')

cursor.execute(query)
for marka_id, model_id, path  in cursor:

	if markaPhoto.get(marka_id) is None :
		markaPhoto[marka_id] = [];
	markaPhoto[marka_id].append(path);
	


cursor.close()
cnx.close()


# exit();


# convert   -crop 10x10+0+0  1.jpeg   tile.jpg

# convert -size 600x400 xc:white canvas.jpg ///neednt

# convert -size 600x400 tile:tile.jpg  canvas2.jpg


# sourcePhotoDir = os.path.dirname(os.path.abspath(__file__))+"/../auto/mitsubishi/"
#resultPhotoDir=os.path.dirname(os.path.abspath(__file__))+"/../public/photos/"

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required = True, help = "path to the image file")
# #ap.add_argument("-r", "--result", required = True, help = "path to the result file without extension")
# args = vars(ap.parse_args())

# imgBasePath, imgBaseExt = os.path.splitext(args["image"])
# imgBaseName = os.path.basename(imgBasePath)

# load the image and convert it to grayscale



# filePath =  sourcePhotoDir+args["image"];

for marka in markaPhoto :
	_p = markaPhoto[marka]
	print marka
	for path in _p :
		prepareImage(path, marka)



exit();

if not os.path.exists(sourcePhotoDir +"tmp/"):
	os.makedirs(sourcePhotoDir +"tmp/")



# response = urlopen('http://62.149.26.88/photos_orig'+ path+"."+ext)


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
    img.resize( 40, 30 )
    img.save(filename=sourcePhotoDir +"tmp/"+ imgBaseName + "-tmp.jpg")




image = cv2.imread(sourcePhotoDir+"tmp/"+imgBaseName + "-tmp.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

imgHeight, imgWidth, channels = image.shape


# cv2.imwrite(sourcePhotoDir +"det/"+ imgBaseName + "opencv-gray.jpg", gray)


######################################  1 var ############################
# gray = cv2.GaussianBlur(gray,(5,5),0)
medianbluered = cv2.medianBlur(gray,3)

# ret,thresh = cv2.threshold(medianbluered, 200,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

thresh = cv2.adaptiveThreshold(medianbluered,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3)

cv2.imwrite(sourcePhotoDir +"det/"+ imgBaseName + "opencv-thrash.jpg", thresh);

imArr = [];
for y in thresh.tolist() :
    for x in y :
        p = 0;
        if x > 100 :
            p = 1
        imArr.append(p)



if not os.path.exists(sourcePhotoDir +"json/"):
	os.makedirs(sourcePhotoDir +"json/")
with open(sourcePhotoDir +"json/"+ imgBaseName + ".json", 'w') as outfile:
    json.dump(imArr, outfile)


cv2.imwrite(sourcePhotoDir +"det/"+ imgBaseName + "opencv-thrash.jpg", thresh)
exit(0)


