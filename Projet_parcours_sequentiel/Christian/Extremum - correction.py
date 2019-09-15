# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 08:04:04 2019

@author: LAU Wai Tong Christian

"""

from tkinter import *
import math
import time
import random

#------ Les variables globale ---------

size = 300
data = None

maximal = 0
i_max = 0
minimal = 0
i_min = 0
index = 0

bias = 0.8
funct = None

#---------------------------- ---------


#  Affichage des données
def DrawData( canvas, data ):
    global i_max, maximal, i_min, minimal, index
    
    if data == None:
        print("data == None")
        return

    w = int(canvas['width']); h = int(canvas['height'])
    
    # Dessin des points et les lignes les reliant
    n = len(data)
    size = 1
    for i in range(0,n):
        x = i * w / n;
        y = h/2 + data[i]*h
        canvas.create_oval(x-size,y-size,x+size,y+size,width=2)
        if (i > 0): canvas.create_line(lx, ly, x, y, fill="blue")
        lx = x; ly = y

    # Dessin de la ligne de balayage
    if (index >= 0) or (index < n-1):
        x = index*w/n;
        canvas.create_line(x, 0, x, h, width=2, fill="red")

    # Dessin des points du maximum et du minimum    
    x = i_max*w/n; y = h/2 + maximal*h; size = 5
    canvas.create_oval(x-size,y-size,x+size,y+size,width=1,fill="#80FF80")
    x = i_min*w/n; y = h/2 + minimal*h; size = 5
    canvas.create_oval(x-size,y-size,x+size,y+size,width=1,fill="#FF8080")


# Création des données
def GenData( n ):
    # n = nombre d'échantillons
    # Retourne la liste des données créée
    # Cette fonction fait appel à la fonction pointée par la variable "funct"
    global funct
    
    data = list()
    for i in range(n):
        data.append(funct(float(i)/n))
    return data


# Fonction génératrice des données
def SinusSinus( x ):
    # x = valeur entrée de la fonction, compris entre 0 et 1
    # Retourne la valeur correspondante à x
    global bias

    f = 2*math.pi*x;
    return 0.3*math.sin(10*f)*math.cos(2*f)*math.exp(-7*(x-bias)**2)


# Redessiner le graphique
def ReDraw():
    global canvas, data
    
    canvas.delete(ALL)
    DrawData(canvas, data)
    #fenetre.update_idletasks()      # Appel des tâches liées à la fenêtre
    fenetre.update()                # Mise à jour de la fenêtre


# Fonction de recherche des extremum
def Search():
    # Cette fonction met à jour les valeurs des extremums
    # représentés par les variables "maximal", "minimal".
    # Met aussi à jour les variables "i_max" et "i_min"
    # correspondant à l'index des extremums dans la liste des données
    global i_max, maximal, i_min, minimal, data, index
    
    # Initialisation des extremums à la 1ère valeur
    i_max = 0
    maximal = data[0]
    i_min = 0
    minimal = data[0]

    # Boucle de balayage de la liste
    for index in range(len(data)):

        if (data[index] > maximal):
            maximal = data[index]
            i_max = index
        if (data[index] < minimal):
            minimal = data[index]
            i_min = index

        ReDraw()    # Mise à jour graphique


# Action déclencher par le menu "Recherche extremum"
def ActionMenu():
    # Remise à zéro de la recherche
    global bias, data, size, funct
    bias = 0.3+random.random()*0.6
    data = GenData(size)
    Search()


# Création de la fenêtre
fenetre = Tk()
fenetre.title("Recherche d'extremums")

# Création d'un menu avec une commande pour remise à zéro
menubar = Menu(fenetre)
menubar.add_command(label="Recherche extremum", command=ActionMenu)
fenetre.config(menu=menubar)

# Création du "canvas" de la fenêtre
canvas = Canvas(fenetre,width=600,height=480,background="white")
canvas.pack()

# Génération des données
funct = SinusSinus
data = GenData(size)

# Recherche des extremums
Search()

fenetre.mainloop()
