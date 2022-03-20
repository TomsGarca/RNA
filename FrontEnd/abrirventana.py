################LIBRERIAS################
import tkinter
from doctest import master
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import image_slicer
import tempfile
################LIBRERIAS################

################FUNCIONES################
# FUNCION QUE MUESTRE LA IMAGEN EN PEQUEÑAS IMAGENES (TIPO CUADRICULA COMO LAS DE LOS CAPTCHAS) 
def cutPic(tmp, tiles, file):
    #tmp = carpeta donde se guadan las imagenes.
    #tiles = variable que contiene la imagen fragmentada.
    #file = nombre del archivo original, sin extension.

    #Inicializacion de Variables para iraciones.
    c1 = c2 = 1
    x = y = 75
    cmp = cmp2 = comp = ""
    label = []  #Arreglo de objetos label(img).


    for i in range(1, len(tiles)+1):

        #Numero de Iteracion en el fragmento
        if c1 < 10:
            cmp = "_0" + str(c1)
        else:
            cmp = "_" + str(c1)
        
        if c2 < 10:
            cmp2 = "_0" + str(c2)
        else:
            cmp2 = "_" + str(c2)

        comp = cmp + cmp2

        arch = tmp + "/" + file + comp + ".png"

        #Creacion de Label
        img = Image.open(arch)
        pic = ImageTk.PhotoImage(img)
        label.append(tkinter.Label(image=pic))
        label[i-1].image = pic

        #Crecion de matriz para vizualizacion (5x5)
        if c2 < 5:
            c2 += 1
        else:
            c1 += 1
            c2 = 1

        #MAPEO      Ubicacion de cada imagen
        label[i-1].place(x=x, y=y)
        if i%5 == 0:
            x = 75
            y += 55
        else:
            x += 55
################FUNCIONES################

################Declare the Window#####################
window = Tk()
# set window title
window.title("Jackie The Ripper")
# set window width and height
window.configure(width=720, height=600)
# set window background color
window.configure(bg='lightgray')
################Declare the Window#####################

file = "fire_0003"
archv = "FrontEnd/" + file + ".jpg"

#Definimos el boton de siguiente
boton = ttk.Button(text="Siguiente")
boton.place(x=600, y=20)

#Label para mostrar el nombre del archivo
texto = Label(master, text=archv)
texto.place(x=30,y=20)

tiles = image_slicer.slice(archv, 25, save=False)

# Creacion de Carpeta Temporal
with tempfile.TemporaryDirectory(dir="FrontEnd") as tmp:
    # Fragmentos de imagen guardados en la carpeta tmp
    image_slicer.save_tiles(tiles, directory=tmp, prefix=file)
    cutPic(tmp=tmp, tiles=tiles, file=file)
    #Ventana de Vizualizacion.
    window.mainloop()