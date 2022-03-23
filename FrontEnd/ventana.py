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
        mediar = mediag = mediab = []
        media = {
            "R": mediar,
            "G": mediag,
            "B": mediab
        }
        # global colores
        # colores = "none"

        ################Declare the Window#####################
        window = Tk()
        window.geometry('720x360')
        window.title("Jackie The Ripper")
        window.config(bg="lightgray")
        ################Declare the Window#####################

        def colorpick(c):
            "Colores a elegir para seleccion de imagen"
            def click (event):
                global colores
                colores = c
                print (colores)
            return click

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

        #Label para mostrar el nombre del archivo
        ttk.Label(window, text=archv).place(x=30, y=20)
        # ttk.Label(window, text="-------", style="Green").place(x=550, y=70)
        # ttk.Label(window, text="-------").place(x=550, y=100)
        # ttk.Label(window, text="-------").place(x=550, y=130)

        self.tmpfolder(tiles=tiles, file=file, window=window)

        #Ventana Loopeada.
        window.mainloop()
    # Creacion de Carpeta Temporal
    def tmpfolder(self, tiles:list, file:str, window:Tk):
        with tempfile.TemporaryDirectory(dir="FrontEnd") as tmp:
            # Fragmentos de imagen guardados en la carpeta tmp
            #print(tmp)
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

        def clicked(label):
            def click(event):
                label.config(bg=(colores))
            return click
            #print(1)

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
            label.append(tkinter.Label(window, image=pic, borderwidth=4))
            label[i-1].image = pic
            
            label[i-1].bind("<Button-1>", clicked(label=label[i-1]))
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
########### MAIN ############