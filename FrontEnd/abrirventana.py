from cmath import pi
import tkinter
from asyncio import windows_events
from doctest import master
from tkinter import *
from tkinter import ttk
#CON LIBRERIA DE PIL PODEMOS HACER MANEJO DE IMAGENES
import pickletools
from xml.sax import xmlreader
from PIL import Image, ImageTk
import image_slicer
import tempfile

################FUNCIONES################
# FUNCION QUE MUESTRE LA IMAGEN EN PEQUEÑAS IMAGENES (TIPO CUADRICULA COMO LAS DE LOS CAPTCHAS) 
# def jackTheRipper():
#     imagen = PhotoImage(file="FrontEnd/fire_0002.jpg")
################FUNCIONES################


################Declare the Window#####################
window = Tk()
# set window title
window.title("Jackie The Ripper")
# set window width and height
window.configure(width=720, height=600)
# set window background color
window.configure(bg='lightgray')
#######################################################

file = "fire_0003"
archv = "FrontEnd/" + file + ".jpg"
# Create a photoimage object of the image in the path
# imagen1 = Image.open(archv)
# test = ImageTk.PhotoImage(imagen1)
# label1 = tkinter.Label(image=test)

# imagen2 = Image.open(archv)
# test2 = ImageTk.PhotoImage(imagen2)
# label2 = tkinter.Label(image=test2)

# imagen3 = Image.open(archv)
# test3 = ImageTk.PhotoImage(imagen3)
# label3 = tkinter.Label(image=test3)

# imagen4 = Image.open(archv)
# test4 = ImageTk.PhotoImage(imagen4)
# label4 = tkinter.Label(image=test4)
#label4.image = test4

# Position image
# label1.place(x=100, y=75)
# label2.place(x=400, y=75)
# label3.place(x=100, y=275)
# label4.place(x=400, y=275)

#Definimos el boton de siguiente
boton = ttk.Button(text="Siguiente")
boton.place(x=600, y=20)
#Label para mostrar el nombre del archivo
texto = Label(master, text=archv)
texto.place(x=30,y=20)


tiles = image_slicer.slice(archv, 25, save=False)
# image_slicer.save_tiles(tiles, directory="FrontEnd/tmp", prefix=file)
with tempfile.TemporaryDirectory(dir="FrontEnd") as tmp:
    image_slicer.save_tiles(tiles, directory=tmp, prefix=file)
    c1 = 1
    c2 = 1
    x = 75
    y = 75
    label = []
    for i in range(1, len(tiles)+1):
        arch = tmp + "/" + file + "_0" + str(c1) + "_0" + str(c2) + ".png"
        img = Image.open(arch)
        pic = ImageTk.PhotoImage(img)
        label.append(tkinter.Label(image=pic))
        label[i-1].image = pic
        
        if c2 < 5:
            c2 += 1
        else:
            c1 += 1
            c2 = 1
        
        label[i-1].place(x=x, y=y)
        if i%5 == 0:
            x = 75
            y += 55
        else:
            x += 55
    window.mainloop()
#Mantiene a la ventana abierta
# window.mainloop()


# tiles = image_slicer.slice(archv, 4, save=False)
# # image_slicer.save_tiles(tiles, directory="FrontEnd/tmp", prefix=file)