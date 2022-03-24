#CON LIBRERIA DE PIL
import pickletools
from PIL import Image



#Abrimos archivo .jpg
nombreimagen = 'fire_0002.jpg'
im = Image.open(nombreimagen) # Can be many different formats.
pix = im.load()
print (im.size)  # Get the width and hight of the image for iterating over
print (pix[100,100])  # Get the RGBA Value of the a pixel of an image
pix[100,100] = 0,0,255 # Set the RGBA Value of the image (tuple)
pix[101,101] = 0,0,255
pix[102,102] = 0,0,255
pix[100,102] = 0,0,255
pix[100,103] = 0,0,255
pix[100,104] = 0,0,255

#Abrimos archivo .txt
f = open("text.txt", "a") # modo 'a' siempre agrega algo al final al archivo

pixels = list(im.getdata())
print(pixels)
im.save('fire_0003.jpg')  # Save the modified pixels as .png
for i in range(0,len(pixels)):
    print(str(i)+str(pixels[i]))
    f.write(str(pixels[i]))

f.close()

def crop(filename, number):
    im = Image.open(filename)
    w, h = im.size
    unit = w // 25
    for n in range(number):
        im1 = im.crop((unit * n, 0, unit * (n + 1), ))
        im1.save(filename[:-4] + str(n + 1) + ".jpg")
 

crop("fire_0002.jpg", 5)

    #CON SCIPY
#from scipy import misc
#arr = misc.imread('lena.png') # 640x480x3 array
#arr[20, 30] # 3-vector for a pixel
#arr[20, 30, 1] # green value for a pixel