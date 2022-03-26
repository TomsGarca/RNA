################LIBRERIAS################
import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from django.forms import NullBooleanField
import image_slicer
import tempfile

from pprint import pprint
from matplotlib import image
from matplotlib.pyplot import text
import numpy as np
from skimage import io, color, img_as_ubyte
from skimage.color import rgb2gray
from skimage.feature import greycomatrix, greycoprops
from sklearn.metrics.cluster import entropy
################LIBRERIAS################
class Jack():
    def __init__(self) -> None:
        self.directorio = {
            "media": {
                "mediaR": [],
                "mediaG": [],
                "mediaB": [],
            },
            "desv": {
                "desv_R": [],
                "desv_G": [],
                "desv_B": [],
            },
            "med_textura": {
                "energy": [],
                "homogeneity": [],
                "contrast": [],
                "dissimilarity": [],
                "correlation": []
            }
        }

    def jackPrint(self):
        pprint(self.directorio)
    #Funcion que calcula las medias RGB de las imagenes, apendiza los valores en el dicionario
    def mediaRGB(self, directory:str, tiles:list, file:str):
        """directory = Carpeta donde se guadan las imagenes.\n
            tiles = Variable que contiene la imagen fragmentada.\n
            file = Nombre del archivo original, sin extension."""
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

            self.directorio["media"]["mediaR"].append(round(sumR/1800, 4))
            self.directorio["media"]["mediaG"].append(round(sumG/1800, 4))
            self.directorio["media"]["mediaB"].append(round(sumB/1800, 4))
            sumR = sumG = sumB = 0

            if c2 < 5:
                c2 += 1
            else:
                c1 += 1
                c2 = 1
    #Funcion que calcula la desviacion std de las imagenes apendiza los valores dentro del diccionario
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

            self.directorio["desv"]["desv_R"].append(round(np.std(r), 4))
            self.directorio["desv"]["desv_G"].append(round(np.std(g), 4))
            self.directorio["desv"]["desv_B"].append(round(np.std(b), 4))

            if c2 < 5:
                c2 += 1
            else:
                c1 += 1
                c2 = 1

    def descriptores(self, directory:str, tiles:list, file:str):
        c1 = c2 = 1
        cmp = cmp2 = comp = "_01"
        distances = [1]
        angles = [0]
        properties = ['energy', 'homogeneity' ,'contrast', 'dissimilarity', 'correlation']
        bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255])
        imgGray = []
        #arch = directory + "/" + file + comp + ".png"

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

            img = io.imread(arch)
            imgG = img_as_ubyte(rgb2gray(img))

            inds = np.digitize(imgG, bins)

            max_value = inds.max()+1
            glcm = greycomatrix(inds,
                     distances=distances,
                     angles=angles,
                     levels = max_value,
                     symmetric=True,
                     normed=True)

            self.directorio["med_textura"]["energy"].append(greycoprops(glcm, properties[0]))
            self.directorio["med_textura"]["homogeneity"].append(greycoprops(glcm, properties[1]))
            self.directorio["med_textura"]["contrast"].append(greycoprops(glcm, properties[2]))
            self.directorio["med_textura"]["dissimilarity"].append(greycoprops(glcm, properties[3]))
            self.directorio["med_textura"]["correlation"].append(greycoprops(glcm, properties[4]))


            if c2 < 5:
                c2 += 1
            else:
                c1 += 1
                c2 = 1


class App():
    def __init__(self):

        self.muestra = []
        self.interador = 4
        self.file = "fire_000" + str(self.interador)
        self.archv = "FrontEnd/" + self.file + ".jpg"
        self.dir = ""
        self.tiles = image_slicer.slice(self.archv, 25, save=False)
        self.colores = "lightgray"
        self.labelmatrix = ""

        ################Declare the Window#####################
        self.window = Tk()
        self.window.geometry('720x360')
        self.window.title("Jack The Ripper")
        self.window.config(bg="lightgray")
        ################Declare the Window#####################

        # print(self.archv)
        ttk.Label(self.window, text="Archivo: ", background="lightgray").place(x=30, y=20)
        self.labelA = ttk.Label(self.window, text=self.archv).place(x=80, y=20)
        ttk.Label(self.window, text="Color: ", background="lightgray"). place(x=420, y=100)
        self.color = ttk.Label(self.window, text="            ", background=self.colores).place(x=460, y=100)
        
            #Definimos el boton de siguiente
        siguiente_btn = ttk.Button(self.window, text='Siguiente', command=self.siguiente())
        siguiente_btn.place(x=600, y=20)

            #Boton Incendio
        incendio_btn = ttk.Button(self.window, text='Inciendo', command=self.colorpick("orange"))
        incendio_btn.place(x=600, y=70)

            #Boton No Incendio
        noincendio_btn = ttk.Button(self.window, text='No Incendio', command=self.colorpick("green"))
        noincendio_btn.place(x=600, y=100)

            #Boton Humo
        humo_btn = ttk.Button(self.window, text='Humo', command=self.colorpick("blue"))
        humo_btn.place(x=600, y=130)

            #boton nulo
        nulo_btn = ttk.Button(self.window, text='Null', command=self.colorpick("lightgray"))
        nulo_btn.place(x=600, y=160)


        with tempfile.TemporaryDirectory(dir="FrontEnd") as tmp:
            #Label para mostrar el nombre del archivo
            # Fragmentos de imagen guardados en la carpeta tmp
            
            self.labelmatrix = self.jackTheRipper(tmp=tmp, tiles=self.tiles, file=self.file, window=self.window)
            self.dir = tmp
            minifoto = Jack()
            minifoto.mediaRGB(directory=tmp, tiles=self.tiles, file=self.file)
            minifoto.desviacionRGB(directory=tmp, tiles=self.tiles, file=self.file)
            minifoto.descriptores(directory=tmp, tiles=self.tiles, file=self.file)
            #pprint(minifoto.directorio)
            #minifoto.jackPrint()
            self.muestra.append(minifoto)
            # LOOP PARA MANTENER ACCESO A LA CARPETA GENERADA TODO EL TIEMPO
            self.arrayPrint()
            self.window.mainloop()

    ############################## FUNCIONES DE BOTONES ##############################
    def arrayPrint(self):
        for i in range(0, len(self.muestra)):
            self.muestra[i].jackPrint()
    
    def siguiente(self):
        "Iterar Imagenes"
        def click ():
            self.interador += 1
            self.file = "fire_000" + str(self.interador)
            self.archv = "FrontEnd/" + self.file + ".jpg"
            self.tiles = image_slicer.slice(self.archv, 25, save=False)
            self.labelA =  ttk.Label(self.window, text=self.archv).place(x=80, y=20)
            self.labelmatrix = self.jackTheRipper(tmp=self.dir, tiles=self.tiles, file=self.file, window=self.window)

            minifoto = Jack()
            minifoto.mediaRGB(directory=self.dir, tiles=self.tiles, file=self.file)
            minifoto.desviacionRGB(directory=self.dir, tiles=self.tiles, file=self.file)
            minifoto.descriptores(directory=self.dir, tiles=self.tiles, file=self.file)
            #pprint(minifoto.directorio)
            #minifoto.jackPrint()
            self.muestra.append(minifoto)
            self.arrayPrint()

            # print(self.archv)
            # print(self.tiles)
        return click
    def colorpick(self, c):
        "Colores a elegir para seleccion de imagen"
        def click ():
            self.colores = c
            self.color = ttk.Label(self.window, text="            ", background=self.colores).place(x=460, y=100)
            #print (self.colores)
        return click

    def clicked(self, label):
        def click(e):
            #amigo aqui colores no esta definido
            label.config(bg=(self.colores))
        return click
    ############################## FUNCIONES DE BOTONES ##############################

    def jackTheRipper(self, tmp:str, tiles:list, file:str, window):
        """tmp = Carpeta donde se guadan las imagenes.\n
            tiles = Variable que contiene la imagen fragmentada.\n
            file = Nombre del archivo original, sin extension.\n
            window = Interfaz que pertenece"""
        image_slicer.save_tiles(tiles, directory=tmp, prefix=file)

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
            label.append(tkinter.Label(window, image=pic, borderwidth=4))
            label[i-1].image = pic
            label[i-1].config(bg=(self.colores))

            label[i-1].bind("<Button-1>", self.clicked(label=label[i-1]))

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
    #pprint(app.Jack)
########### MAIN ############