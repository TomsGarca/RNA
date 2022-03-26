from lib2to3.pytree import convert
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import image_slicer
import tempfile
from skimage.feature import greycomatrix, greycoprops

from pprint import pprint
from matplotlib import image
import numpy as np
from skimage import io, color, img_as_ubyte
from skimage.color import rgb2gray
from skimage.feature import greycomatrix, greycoprops
from sklearn.metrics.cluster import entropy
import cv2
####           FrontEnd\tmp2bx8ovlz
distances = [1]
angles = [0]
properties = ['energy', 'homogeneity' ,'contrast', 'dissimilarity', 'correlation'] # 
#img = Image.open("FrontEnd/tmp/fire_0004_01_01.png")
img = io.imread("FrontEnd/tmp/fire_0004_01_01.png")
#print("img:")
#print(img)
imgG = img_as_ubyte(rgb2gray(img))     
#print("imgG:")
#print(imgG)

bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255])
inds = np.digitize(imgG, bins)

max_value = inds.max()+1

glcm = greycomatrix(inds,
                     distances=distances, 
                     angles=angles,
                     levels = max_value,
                     symmetric=True,
                     normed=True)
#print("glcm:")
#print(*glcm)
print("enegia: ")
a = greycoprops(glcm, properties[0])
print(a)

print("homogeneity: ")
a = greycoprops(glcm, properties[1])
print(a)

print("contrast: ")
a = greycoprops(glcm, properties[2])
print(a)

print("dissimilarity: ")
a = greycoprops(glcm, properties[3])
print(a)

print("correlation: ")
a = greycoprops(glcm, properties[4])
print(a)

#print("rgb2grayimg:")
#print(rgb2gray(img))
#print(a)

###2da forma
# img = io.imread("FrontEnd/tmp/fire_0004_01_01.png")
# gray = color.rgb2gray(img)
# image = img_as_ubyte(gray)
# print("image")
# print(image)
# #io.imshow(image)

# bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255]) #16-bit
# inds = np.digitize(image, bins)

# max_value = inds.max()+1
# matrix_coocurrence = greycomatrix(inds, [1, 2, 3, 4], [0, np.pi/4, np.pi/2, 3*np.pi/4], levels=max_value, normed=False, symmetric=False)
# print(*matrix_coocurrence)
# #print(greycoprops(matrix_coocurrence, 'energy'))