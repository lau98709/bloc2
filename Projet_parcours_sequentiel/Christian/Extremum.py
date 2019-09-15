# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 08:04:04 2019

@author: LAU Wai Tong Christian

"""

from tkinter import *
import math
import time
import random

size = 300
data = None

maximal = 0
i_max = 0
minimal = 0
i_min = 0
index = 0

bias = 0.8
funct = None


def DrawData( canvas, data ):
    global i_max, maximal, i_min, minimal, index
    
    if data == None:
        print("data == None")
        return
    w = int(canvas['width']); h = int(canvas['height'])
    n = len(data)
    size = 1
    for i in range(0,n):
        x = i * w / n;
        y = h/2 + data[i]*h
        canvas.create_oval(x-size,y-size,x+size,y+size,width=2)
        if (i > 0): canvas.create_line(lx, ly, x, y, fill="blue")
        lx = x; ly = y

    if (index >= 0) or (index < n-1):
        x = index*w/n;
        canvas.create_line(x, 0, x, h, width=2, fill="red")

    x = i_max*w/n; y = h/2 + maximal*h; size = 5
    canvas.create_oval(x-size,y-size,x+size,y+size,width=1,fill="#80FF80")
    x = i_min*w/n; y = h/2 + minimal*h; size = 5
    canvas.create_oval(x-size,y-size,x+size,y+size,width=1,fill="#FF8080")


def GenData( n ):
    global funct
    
    data = list()
    for i in range(n):
        data.append(funct(float(i)/n))
    return data


def SinusSinus( x ):
    global bias

    f = 2*math.pi*x;
    return 0.3*math.sin(10*f)*math.cos(2*f)*math.exp(-7*(x-bias)**2)


def ReDraw():
    global canvas, data
    
    canvas.delete(ALL)
    DrawData(canvas, data)
    #fenetre.update_idletasks()      # Appel des tâches liées à la fenêtre
    fenetre.update()                # Mise à jour de la fenêtre


def Search():
    global i_max, maximal, i_min, minimal, data, index
    
    i_max = 0
    maximal = data[0]
    i_min = 0
    minimal = data[0]

    for index in range(len(data)):

        if (data[index] > maximal):
            maximal = data[index]
            i_max = index
        if (data[index] < minimal):
            minimal = data[index]
            i_min = index

        ReDraw()


def ActionMenu():
    global bias, data, size, funct
    bias = 0.3+random.random()*0.6
    data = GenData(size)
    Search()


# Création de la fenêtre
fenetre = Tk()
fenetre.title("Labyrinthe")

# Création d'un menu avec une commande pour recommencer
menubar = Menu(fenetre)
menubar.add_command(label="Recherche extremum", command=ActionMenu)
fenetre.config(menu=menubar)

# Création du "canvas" de la fenêtre
canvas = Canvas(fenetre,width=600,height=480,background="white")
canvas.pack()

funct = SinusSinus
data = GenData(size)

Search()

fenetre.mainloop()
