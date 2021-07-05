#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 11:02:04 2021

@author: adrian
"""
import os
import os.path
#from PyQt5 import QMessageBox

escribir=None
ruta=os.getcwd()

def crearDocumento(id_caso):
    global escribir
    global ruta
    archivo="Informe_Pericial_"
    archivo+=id_caso
    ruta+='/Informes/'
    ruta+= archivo
    if os.path.isfile(ruta):   
        escribir=False
        return -1        
    else:
        escribir=True
        file = open(ruta, "w")
        return file

    
def escribirDocumento(file, id_caso, titulo, texto):
    global escribir
    global ruta
    if escribir == True:
        file = open(ruta, "a")
        if texto=="":
            file.write("{}:\n  ****No especificado****\n\n".format(titulo))
        else:
            file.write("{}:\n  {}\n\n".format(titulo, texto))
        
        file.close()
    else:
        return Exception



