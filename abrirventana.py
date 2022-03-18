import tkinter
from asyncio import windows_events
from doctest import master
from tkinter import *
from tkinter import ttk
#CON LIBRERIA DE PIL PODEMOS HACER MANEJO DE IMAGENES
import pickletools
from PIL import Image, ImageTk
# declare the window
window = Tk()
# set window title
window.title("Jackie The Ripper")
# set window width and height
window.configure(width=720, height=480)
# set window background color
window.configure(bg='lightgray')


# Create a photoimage object of the image in the path
imagen1 = Image.open("fire_0003.jpg")
test = ImageTk.PhotoImage(imagen1)

label1 = tkinter.Label(image=test)
label1.image = test

imagen2 = Image.open("fire_0003.jpg")
test2 = ImageTk.PhotoImage(imagen2)

label2 = tkinter.Label(image=test2)
label2.image = test2

imagen3 = Image.open("fire_0003.jpg")
test3 = ImageTk.PhotoImage(imagen3)

label3 = tkinter.Label(image=test3)
label3.image = test3

imagen4 = Image.open("fire_0003.jpg")
test4 = ImageTk.PhotoImage(imagen4)

label4 = tkinter.Label(image=test4)
label4.image = test4

# Position image
label1.place(x=100, y=100)
label2.place(x=300, y=100)
label3.place(x=100, y=300)
label4.place(x=300, y=300)
#Definimos el boton de siguiente
boton = ttk.Button(text="Siguiente")
boton.place(x=600, y=430)
#Label para mostrar el nombre del archivo
texto = Label(master, text="Nombre del archivo")
texto.place(x=30,y=20)
#Mantiene a la ventana abierta
window.mainloop()

# FUNCION QUE MUESTRE LA IMAGEN EN PEQUEÑAS IMAGENES (TIPO CUADRICULA COMO LAS DE LOS CAPTCHAS) 
def jackTheRipper():
    imagen = PhotoImage(file="fire_0002.jpg")
    