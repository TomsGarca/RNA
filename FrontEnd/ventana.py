################LIBRERIAS################
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import image_slicer
import tempfile

from pprint import pprint

import numpy as np
from skimage.feature import greycomatrix, greycoprops
from skimage import io, color, img_as_ubyte
################LIBRERIAS################

file = "fire_0004"
archv = "FrontEnd/" + file + ".jpg"
tiles = image_slicer.slice(archv, 25, save=False)

class App():
    def __init__(self):
        self.Jack = {
            "mediaR": [], "mediaG": [], "mediaB": [],
            "desv_R": [], "desv_G": [], "desv_B": []
        }
        # global colores

        ################Declare the Window#####################
        window = Tk()
        window.geometry('720x360')
        window.title("Jack The Ripper")
        window.config(bg="lightgray")
        ################Declare the Window#####################

        def colorpick(c):
            "Colores a elegir para seleccion de imagen"
            def click (event):
                global colores
                colores = c
                ttk.Label(window, text="            ", background=colores).place(x=460, y=100)
                #print (colores)
            return click

        #Label para mostrar el nombre del archivo
        ttk.Label(window, text="Archivo: ", background="lightgray").place(x=30, y=20)
        ttk.Label(window, text=archv).place(x=80, y=20)
        ttk.Label(window, text="Color: ", background="lightgray"). place(x=420, y=100)
        ttk.Label(window, text="            ").place(x=460, y=100)


        #Definimos el boton de siguiente
        siguiente_btn = ttk.Button(window, text='Siguiente')
        siguiente_btn.place(x=600, y=20)
        incendio_btn = ttk.Button(window, text='Inciendo')
        incendio_btn.place(x=600, y=70)
        incendio_btn.bind("<Button-1>", colorpick("orange"))
        noincendio_btn = ttk.Button(window, text='No Incendio')
        noincendio_btn.place(x=600, y=100)
        noincendio_btn.bind("<Button-1>", colorpick("green"))
        humo_btn = ttk.Button(window, text='Humo')
        humo_btn.place(x=600, y=130)
        humo_btn.bind("<Button-1>", colorpick("blue"))

        self.tmpfolder(tiles=tiles, file=file, window=window)

        #Ventana Loopeada.
        #pprint(self.Jack)
        #window.mainloop()

    # Creacion de Carpeta Temporal
    def tmpfolder(self, tiles:list, file:str, window:Tk):
        with tempfile.TemporaryDirectory(dir="FrontEnd") as tmp:
            # Fragmentos de imagen guardados en la carpeta tmp
            #print(tmp)
            image_slicer.save_tiles(tiles, directory=tmp, prefix=file)
            self.jackTheRipper(tmp=tmp, tiles=tiles, file=file, window=window)
            #self.mediaRGB(directory=tmp, tiles=tiles, file=file)
            #self.desviacionRGB(directory=tmp,tiles=tiles, file=file)
            self.toEscalaGrises(directory=tmp, tiles=tiles, file=file)
            
            print(f"\nDiccionario Jack:")
            pprint(self.Jack)

    # FUNCION QUE MUESTRE LA IMAGEN EN PEQUEÑAS IMAGENES (TIPO CUADRICULA COMO LAS DE LOS CAPTCHAS) 
    def jackTheRipper(self, tmp:str, tiles:list, file:str, window:Tk):
        """tmp = Carpeta donde se guadan las imagenes.\n
            tiles = Variable que contiene la imagen fragmentada.\n
            file = Nombre del archivo original, sin extension.\n
            window = Interfaz que pertenece"""

        #Inicializacion de Variables para iraciones.
        c1 = c2 = 1
        x = y = 75
        cmp = cmp2 = comp = ""
        label = []  # Arreglo de objetos label(img).

        def clicked(label):
            def click(event):
                label.config(bg=(colores))
            return click

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
            label.append(tkinter.Label(window, image=pic, borderwidth=4))
            label[i-1].image = pic
            
            label[i-1].bind("<Button-1>", clicked(label=label[i-1]))

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

    def mediaRGB(self, directory:str, tiles:list, file:str):
        """directory = Carpeta donde se guadan las imagenes"""
        c1 = c2 = 1
        cmp = cmp2 = comp = ""
        sumR = sumG = sumB = 0

        for i in range(1, len(tiles)+1):
            if c1 < 10:
                cmp = "_0" + str(c1)
            else:
                cmp = "_" + str(c1)

            if c2 < 10:
                cmp2 = "_0" + str(c2)
            else:
                cmp2 = "_" + str(c2)

            comp = cmp + cmp2

            arch = directory + "/" + file + comp + ".png"

            img = Image.open(arch)
            pixel = img.load()
            j1,k1 = img.size

            for j in range (j1):
                for k in range(k1):
                    sumR += pixel[j,k][0]
                    sumG += pixel[j,k][1]
                    sumB += pixel[j,k][2]

            self.Jack["mediaR"].append(round(sumR/1800, 4))
            self.Jack["mediaG"].append(round(sumG/1800, 4))
            self.Jack["mediaB"].append(round(sumB/1800, 4))
            sumR = sumG = sumB = 0

            if c2 < 5:
                c2 += 1
            else:
                c1 += 1
                c2 = 1

    def desviacionRGB(self, directory:str, tiles:list, file:str):
        c1 = c2 = 1
        cmp = cmp2 = comp = ""

        for i in range(1, len(tiles)+1):
            if c1 < 10:
                cmp = "_0" + str(c1)
            else:
                cmp = "_" + str(c1)

            if c2 < 10:
                cmp2 = "_0" + str(c2)
            else:
                cmp2 = "_" + str(c2)

            comp = cmp + cmp2

            arch = directory + "/" + file + comp + ".png"

            img = Image.open(arch)
            pixel = img.load()
            j1,k1 = img.size

            desvR = []
            desvG = []
            desvB = []

            for j in range (j1):
                for k in range(k1):
                    desvR.append(pixel[j,k][0])
                    desvG.append(pixel[j,k][1])
                    desvB.append(pixel[j,k][2])

            r = []
            g = []
            b = []
            r = np.array(desvR)
            g = np.array(desvG)
            b = np.array(desvB)

            self.Jack["desv_R"].append(round(np.std(r), 4))
            self.Jack["desv_G"].append(round(np.std(g), 4))
            self.Jack["desv_B"].append(round(np.std(b), 4))

            if c2 < 5:
                c2 += 1
            else:
                c1 += 1
                c2 = 1

    def toEscalaGrises(self, directory:str, tiles:list, file:str):
        c1 = c2 = 1
        cmp = cmp2 = comp = ""
        imgGray = []
        imgAlpha = []

        for i in range(1, len(tiles)+1):
            if c1 < 10:
                cmp = "_0" + str(c1)
            else:
                cmp = "_" + str(c1)

            if c2 < 10:
                cmp2 = "_0" + str(c2)
            else:
                cmp2 = "_" + str(c2)

            comp = cmp + cmp2

            arch = directory + "/" + file + comp + ".png"

            img = Image.open(arch)
            imgGray.append(img.convert('L'))
            imgAlpha.append(img.convert("LA"))
        
        print(f"Escala Grises:")
        pprint(imgGray)
        print(f"Escala Alpha:")
        pprint(imgAlpha)


    def contrast_feature(matrix_coocurrence):
        contrast = greycoprops(matrix_coocurrence, 'contrast')
        return "Contrast = ", contrast

    def dissimilarity_feature(matrix_coocurrence):
        dissimilarity = greycoprops(matrix_coocurrence, 'dissimilarity')
        return "Dissimilarity = ", dissimilarity

    def homogeneity_feature(matrix_coocurrence):
        homogeneity = greycoprops(matrix_coocurrence, 'homogeneity')
        return "Homogeneity = ", homogeneity

    def energy_feature(matrix_coocurrence):
        energy = greycoprops(matrix_coocurrence, 'energy')
        return "Energy = ", energy

    def correlation_feature(matrix_coocurrence):
        correlation = greycoprops(matrix_coocurrence, 'correlation')
        return "Correlation = ", correlation


########### MAIN ############
if __name__ == '__main__':
    App()
########### MAIN ############