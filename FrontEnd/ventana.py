################LIBRERIAS################
 ############## INTERFAZ ##############
import os
import tkinter
from tkinter import *
from tkinter import ttk
 ############## INTERFAZ ##############
 ######### TRATAMIENTO DE IMG #########
from PIL import Image, ImageTk
import image_slicer
import tempfile
from skimage import io, img_as_ubyte
from skimage.color import rgb2gray
from skimage.feature import greycomatrix, greycoprops
 ######### TRATAMIENTO DE IMG #########
 ######## TRATAMIENTO DE DATOS ########
import numpy as np
from pprint import pprint
import pathlib
 ######## TRATAMIENTO DE DATOS ########
################LIBRERIAS################
class Jack():
    def __init__(self) -> None:
        self.dicc = {
            "media": { #coleccion de medias
                "mediaR": [],
                "mediaG": [],
                "mediaB": []
            },
            "desv": { #coleccion de desviaciones
                "desv_R": [],
                "desv_G": [],
                "desv_B": []
            },
            "med_textura": { #medidas de textura
                "energy": [],
                "homogeneity": [],
                "contrast": [],
                "dissimilarity": [],
                "correlation": []
            }
        }
    def get(self, a, b):
        aux = str(self.dicc[a][b])
        aux2 = aux.split("[")[1]
        aux3 = aux2.split("]")[0]
        return aux3

    def jackPrint(self):
        pprint(self.dicc)
    #Funcion que calcula las medias RGB de las imagenes, apendiza los valores en el dicionario
    def mediaRGB(self, posicion, directory):
        arch = "D:/GitHub_Rep/Mineria_de_Datos/" + directory
        cont = 0
        cont2 = 1
        file = "fire-00" + str(cont2)
        c1 = c2 = 1
        cmp = cmp2 = comp = comp2 = ""
        sumR = sumG = sumB = 0
        with os.scandir(arch) as ficheros:
            for fichero in ficheros:
                cont += 1

                if c1 < 10:
                    cmp = "_0" + str(c1)
                else:
                    cmp = "_" + str(c1)

                if c2 < 10:
                    cmp2 = "_0" + str(c2)
                else:
                    cmp2 = "_" + str(c2)

                comp = cmp + cmp2
                comp2 = directory + "/" + file + comp + ".png"

                if posicion == cont:
                    img = Image.open(comp2)
                    pixel = img.load()
                    j1,k1 = img.size

                    for j in range (j1):
                        for k in range(k1):
                            sumR += pixel[j,k][0]
                            sumG += pixel[j,k][1]
                            sumB += pixel[j,k][2]

                    self.dicc["media"]["mediaR"].append(round(sumR/1800, 4))
                    self.dicc["media"]["mediaG"].append(round(sumG/1800, 4))
                    self.dicc["media"]["mediaB"].append(round(sumB/1800, 4))
                    sumR = sumG = sumB = 0


                if cont%25 == 0 and cont > 0:
                    cont2 += 1
                    if cont2 < 10:
                        file = "fire-00" + str(cont2)
                        c1 = c2 = 1
                    elif cont2 < 100:
                        file = "fire-0" + str(cont2)
                        c1 = c2 = 1
                    elif cont2 < len(ficheros):
                        file = "fire-" + str(cont2)
                        c1 = c2 = 1
                else:
                    if c2 < 5:
                        c2 += 1
                    else:
                        c1 += 1
                        c2 = 1

    #Funcion que calcula la desviacion std de las imagenes apendiza los valores dentro del diccionario
    def desviacionRGB(self, posicion, directory):
        arch = "D:/GitHub_Rep/Mineria_de_Datos/" + directory
        cont = 0
        cont2 = 1
        file = "fire-00" + str(cont2)
        c1 = c2 = 1
        cmp = cmp2 = comp = comp2 = ""

        with os.scandir(arch) as ficheros:
            for fichero in ficheros:
                cont += 1

                if c1 < 10:
                    cmp = "_0" + str(c1)
                else:
                    cmp = "_" + str(c1)

                if c2 < 10:
                    cmp2 = "_0" + str(c2)
                else:
                    cmp2 = "_" + str(c2)

                comp = cmp + cmp2
                comp2 = directory + "/" + file + comp + ".png"

                if posicion == cont:
                    img = Image.open(comp2)
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
                    
                    self.dicc["desv"]["desv_R"].append(round(np.std(r), 4))
                    self.dicc["desv"]["desv_G"].append(round(np.std(g), 4))
                    self.dicc["desv"]["desv_B"].append(round(np.std(b), 4))

                if cont%25 == 0 and cont > 0:
                    cont2 += 1
                    if cont2 < 10:
                        file = "fire-00" + str(cont2)
                        c1 = c2 = 1
                    elif cont2 < 100:
                        file = "fire-0" + str(cont2)
                        c1 = c2 = 1
                    elif cont2 < len(ficheros):
                        file = "fire-" + str(cont2)
                        c1 = c2 = 1
                else:
                    if c2 < 5:
                        c2 += 1
                    else:
                        c1 += 1
                        c2 = 1

    def descriptores(self, posicion, directory):
        arch = "D:/GitHub_Rep/Mineria_de_Datos/" + directory
        cont = 0
        cont2 = 1
        file = "fire-00" + str(cont2)
        c1 = c2 = 1
        cmp = cmp2 = comp = comp2 = ""
        distances = [1]
        angles = [0]
        properties = ['energy', 'homogeneity' ,'contrast', 'dissimilarity', 'correlation']
        bins = np.array([0, 16, 32, 48, 64, 80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255])
        imgGray = []
        #arch = directory + "/" + file + comp + ".png"

        with os.scandir(arch) as ficheros:
            for fichero in ficheros:
                cont += 1

                if c1 < 10:
                    cmp = "_0" + str(c1)
                else:
                    cmp = "_" + str(c1)

                if c2 < 10:
                    cmp2 = "_0" + str(c2)
                else:
                    cmp2 = "_" + str(c2)

                comp = cmp + cmp2
                comp2 = directory + "/" + file + comp + ".png"

                if posicion == cont:
                    img = Image.open(comp2)
                    imgG = img_as_ubyte(rgb2gray(img))
                    inds = np.digitize(imgG, bins)

                    max_value = inds.max()+1
                    glcm = greycomatrix(inds,
                        distances=distances,
                        angles=angles,
                        levels = max_value,
                        symmetric=True,
                        normed=True)


                    self.dicc["med_textura"]["energy"].append(round(greycoprops(glcm, properties[0])[0][0], 4))
                    self.dicc["med_textura"]["homogeneity"].append(round(greycoprops(glcm, properties[1])[0][0], 4))
                    self.dicc["med_textura"]["contrast"].append(round(greycoprops(glcm, properties[2])[0][0], 4))
                    self.dicc["med_textura"]["dissimilarity"].append(round(greycoprops(glcm, properties[3])[0][0], 4))
                    self.dicc["med_textura"]["correlation"].append(round(greycoprops(glcm, properties[4])[0][0], 4))

                if cont%25 == 0 and cont > 0:
                    cont2 += 1
                    if cont2 < 10:
                        file = "fire-00" + str(cont2)
                        c1 = c2 = 1
                    elif cont2 < 100:
                        file = "fire-0" + str(cont2)
                        c1 = c2 = 1
                    elif cont2 < len(ficheros):
                        file = "fire-" + str(cont2)
                        c1 = c2 = 1
                else:
                    if c2 < 5:
                        c2 += 1
                    else:
                        c1 += 1
                        c2 = 1

class App():
    def __init__(self):

        self.dicc = {
            "muestra": { #GUARDA JACKS
                "incendio": [],
                "no_incendio": [],
                "humo": []
            },
            "imagenes": { #GUARDA NUM DE MINIFOTO
                "incendio": [],
                "no_incendio": [],
                "humo": []
            }
        }

        self.iterador = 1
        self.file = "fire-00" + str(self.iterador)
        #self.file = "fire-300"
        self.archv = "FrontEnd/img/" + self.file + ".jpg"
        self.dir = ""
        self.tiles = image_slicer.slice(self.archv, 25, save=False)
        self.coloresD = "lightgray"
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

        analizar_btn = ttk.Button(self.window, text='Analizar', command=self.procesar())
        analizar_btn.place(x=600, y=235)

        exportar_btn = ttk.Button(self.window, text='Exportar TXT', command=self.expTxt())
        exportar_btn.place(x=600, y=283)

        with tempfile.TemporaryDirectory(dir="FrontEnd") as tmp:
            #Label para mostrar el nombre del archivo
            # Fragmentos de imagen guardados en la carpeta tmp
            
            self.dir = tmp
            self.labelmatrix = self.jackTheRipper(tiles=self.tiles, file=self.file, window=self.window)
            #pprint(self.dicc)
            self.window.mainloop()

    ############################## FUNCIONES DE BOTONES ##############################
    def arrayPrint(self):
        for i in self.dicc["muestra"]:
            print(f"{str(i).upper()}\n")
            for j in range(len(self.dicc["muestra"][i])):
                self.dicc["muestra"][i][j].jackPrint()
                print("\n")

    def lenDir(self):
        contador = 0
        for path in pathlib.Path("FrontEnd/img").iterdir():
            if path.is_file():
                contador += 1
        return contador

    def siguiente(self):
        "Iterar Imagenes"
        def click ():
            self.iterador += 1
            if self.iterador < 10:
                self.file = "fire-00" + str(self.iterador)
            elif self.iterador >= 10 and self.iterador < 100:
                self.file = "fire-0" + str(self.iterador)
            elif self.iterador > 100 and self.iterador < self.lenDir():
                self.file = "fire-" + str(self.iterador)
            elif self.iterador >= self.lenDir():
                self.file = "fire-" + str(self.lenDir())
                # analizar_btn = ttk.Button(self.window, text='Analizar', command=self.procesar())
                # analizar_btn.place(x=600, y=235)
                # exportar_btn = ttk.Button(self.window, text='Exportar TXT', command=self.expTxt())
                # exportar_btn.place(x=600, y=283)
            
            self.archv = "FrontEnd/img/" + self.file + ".jpg"
            self.tiles = image_slicer.slice(self.archv, 25, save=False)
            self.labelA =  ttk.Label(self.window, text=self.archv).place(x=80, y=20)
            self.labelmatrix = self.jackTheRipper(tiles=self.tiles, file=self.file, window=self.window)
            #pprint(self.dicc)
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

    def guardar(self, label_list:list):
        def click ():
            for i in range (0, len(label_list)):
                if label_list[i]["background"] == "orange":

                    label = label_list[i]
                    img = str(label.image)
                    num = int(img.split("pyimage")[1])
                    self.dicc["imagenes"]["incendio"].append(num)

                elif label_list[i]["background"] == "green":
                    
                    label = label_list[i]
                    img = str(label.image)
                    num = int(img.split("pyimage")[1])
                    self.dicc["imagenes"]["no_incendio"].append(num)

                elif label_list[i]["background"] == "blue":
                    
                    label = label_list[i]
                    img = str(label.image)
                    num = int(img.split("pyimage")[1])
                    self.dicc["imagenes"]["humo"].append(num)
            #ttk.Label(self.window, text="Guardado", background="lightgray"). place(x=420, y=200)
        return click
    
    def procesar(self):
        def click():
            #print("ANALIZANDO")
            #print(f"tiles: {str(len(self.tiles))}")
            for i in self.dicc["imagenes"]:
                if i == "incendio":
                    for j in range(len(self.dicc["imagenes"]["incendio"])):

                        m = Jack()
                        m.mediaRGB(posicion=self.dicc["imagenes"]["incendio"][j], directory=self.dir)
                        m.desviacionRGB(posicion=self.dicc["imagenes"]["incendio"][j], directory=self.dir)
                        m.descriptores(posicion=self.dicc["imagenes"]["incendio"][j], directory=self.dir)
                        self.dicc["muestra"]["incendio"].append(m)

                elif i == "no_incendio":
                    for j in range(len(self.dicc["imagenes"]["no_incendio"])):

                        m = Jack()
                        m.mediaRGB(posicion=self.dicc["imagenes"]["no_incendio"][j], directory=self.dir)
                        m.desviacionRGB(posicion=self.dicc["imagenes"]["no_incendio"][j], directory=self.dir)
                        m.descriptores(posicion=self.dicc["imagenes"]["no_incendio"][j], directory=self.dir)
                        self.dicc["muestra"]["no_incendio"].append(m)

                elif i == "humo":
                    for j in range(len(self.dicc["imagenes"]["humo"])):

                        m = Jack()
                        m.mediaRGB(posicion=self.dicc["imagenes"]["humo"][j], directory=self.dir)
                        m.desviacionRGB(posicion=self.dicc["imagenes"]["humo"][j], directory=self.dir)
                        m.descriptores(posicion=self.dicc["imagenes"]["humo"][j], directory=self.dir)
                        self.dicc["muestra"]["humo"].append(m)
            #self.arrayPrint()
        return click

    def expTxt(self):
        def click():
            clase = ""
            for i in self.dicc['muestra']:
                if i == "incendio":
                    clase = "fire"
                    for j in range(len(self.dicc['muestra'][i])):
                        linea = ""
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaR")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaG")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaB")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_R")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_G")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_B")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "energy")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "homogeneity")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "contrast")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "dissimilarity")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "correlation")) + ","
                        linea += clase + "\n"
                        f = open("muestra.txt", "a") # modo 'a' siempre agrega algo al final al archivo
                        f.write(linea)
                        f.close()

                elif i == "no_incendio":
                    clase = "no_fire"
                    for j in range(len(self.dicc['muestra'][i])):
                        linea = ""
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaR")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaG")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaB")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_R")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_G")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_B")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "energy")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "homogeneity")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "contrast")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "dissimilarity")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "correlation")) + ","
                        linea += clase + "\n"
                        f = open("muestra.txt", "a") # modo 'a' siempre agrega algo al final al archivo
                        f.write(linea)
                        f.close()

                elif i == "humo":
                    clase = "smoke"
                    for j in range(len(self.dicc['muestra'][i])):
                        linea = ""
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaR")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaG")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("media", "mediaB")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_R")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_G")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("desv", "desv_B")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "energy")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "homogeneity")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "contrast")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "dissimilarity")) + ","
                        linea += str(self.dicc['muestra'][i][j].get("med_textura", "correlation")) + ","
                        linea += clase + "\n"
                        f = open("muestra.txt", "a") # modo 'a' siempre agrega algo al final al archivo
                        f.write(linea)
                        f.close()
        return click
    ############################## FUNCIONES DE BOTONES ##############################

    def jackTheRipper(self, tiles:list, file:str, window):
        """ tiles = Variable que contiene la imagen fragmentada.\n
            file = Nombre del archivo original, sin extension.\n
            window = Interfaz que pertenece"""
        image_slicer.save_tiles(tiles, directory=self.dir, prefix=file)

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

            arch = self.dir + "/" + file + comp + ".png"

            #Creacion de Label
            img = Image.open(arch)
            pic = ImageTk.PhotoImage(img)
            label.append(tkinter.Label(window, image=pic, borderwidth=4))
            label[i-1].image = pic
            label[i-1].config(bg=(self.coloresD))

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

        guardar_btn = ttk.Button(self.window, text='Guardar', command=self.guardar(label))
        guardar_btn.place(x=600, y=200)

########### MAIN ############
if __name__ == '__main__':
    App()
    #pprint(app.Jack)
########### MAIN ############