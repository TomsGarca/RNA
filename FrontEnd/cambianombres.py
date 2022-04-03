import os 

os.chdir('D:\GitHub_Rep\Mineria_de_Datos\FrontEnd\img')

#print(os.getcwd())
cont = 1
comp = "000"

for f in os.listdir():
    #print(f)
    texto, extension = (os.path.splitext(f))
    #print(texto)
    fire, num = texto.split('-')
    #print(num)
    if cont < 10:
        comp = "00" + str(cont)
        cont += 1
    elif cont >= 10 and cont < 100:
        comp = "0" + str(cont)
        cont += 1
    elif cont <= len(os.listdir()):
        comp = str(cont)
        cont += 1

    #num = num.replace('.','')
    #print(num)
    #count = count + 1
    fire = "fire"
    nuevo_archivo = f"{fire}-{comp}.jpg"
    #print(nuevo_archivo)
    print(nuevo_archivo)
    os.rename(f,nuevo_archivo)