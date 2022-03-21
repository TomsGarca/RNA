################LIBRERIAS################
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import image_slicer
import tempfile
################LIBRERIAS################
file = "fire_0004"
archv = "FrontEnd/" + file + ".jpg"
tiles = image_slicer.slice(archv, 25, save=False)

class App():
    def __init__(self):

        ################Declare the Window#####################
        window = Tk()
        window.geometry('720x500')
        window.title("Jackie The Ripper")
        window.config(bg="lightgray")
        ################Declare the Window#####################

        #Definimos el boton de siguiente
        ttk.Button(window, text='Siguiente').place(x=600, y=20)

        #Label para mostrar el nombre del archivo
        ttk.Label(window, text="archivo").place(x=30,y=20)

        self.tmpfolder(tiles=tiles, file=file, window=window)

        #Ventana Loopeada.
        window.mainloop()

    # Creacion de Carpeta Temporal
    def tmpfolder(self, tiles:list, file:str, window:Tk):
        with tempfile.TemporaryDirectory(dir="FrontEnd") as tmp:
            # Fragmentos de imagen guardados en la carpeta tmp
            image_slicer.save_tiles(tiles, directory=tmp, prefix=file)
            self.jackTheRipper(tmp=tmp, tiles=tiles, file=file, window=window)

    # FUNCION QUE MUESTRE LA IMAGEN EN PEQUEÑAS IMAGENES (TIPO CUADRICULA COMO LAS DE LOS CAPTCHAS) 
    def jackTheRipper(self, tmp: str, tiles: list, file: str, window: Tk):
        """tmp = Carpeta donde se guadan las imagenes.\n
            tiles = Variable que contiene la imagen fragmentada.\n
            file = Nombre del archivo original, sin extension.\n
            window = Interfaz que pertenece"""

        #Inicializacion de Variables para iraciones.
        c1 = c2 = 1
        x = y = 75
        cmp = cmp2 = comp = ""
        label = []  # Arreglo de objetos label(img).

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
            #label.append(tkinter.Label(window, image=pic))
            label.append(tkinter.Label(window, image=pic, borderwidth=4, relief="groove"))
            label[i-1].image = pic
            
            #label[i-1].bind("<Button-1>", clicked)
            #label[i-1].config(bg="green") #Cambia Color el borde

            #Crecion de matriz para vizualizacion (5x5)
            if c2 < 5:
                c2 += 1
            else:
                c1 += 1
                c2 = 1

            #MAPEO      Ubicacion de cada imagen
            label[i-1].place(x=x, y=y)
            if i % 5 == 0:
                x = 75
                y += 50
            else:
                x += 65

########### MAIN ############
if __name__ == '__main__':
    App()