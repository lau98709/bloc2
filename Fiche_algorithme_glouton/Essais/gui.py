# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:58:09 2019

@author: locutus
"""

from tkinter import *

# Une case du labyrinthe
class LabCase():
    inited = 0      # est-il inititialisé
    side = list()   # les côtés
    value = 0
    
    def __init__(self):
        self.inited = 0
        side_list = list()
        for i in range(0,4):
            side_list.append(0)
        self.side = side_list
        

# Classe représentant le labyrinthe
class Labyrinthe():
    labwidth = 10       # largeur du labyrinthe
    labheight = 10      # hauteur du labyrinthe
    labcase = list()    # les cases du labyrinthe
    entry=(0,0)
    issue=(9,9)
    
    def __init__(self):
        # initialisation des cases du labyrinthe
        i = 0
        for x in range(0,self.labwidth):
            for y in range(0,self.labheight):
                case = LabCase()
                case.value = i
                i = i + 1
                self.labcase.append(case)
    
    # Dessin du labyrinthe
    def Draw(self,canvas):
        w = self.labwidth
        h = self.labheight
        dx = int(canvas['width'])/w;
        dy = int(canvas['height'])/h;
        
        canvas.delete(ALL)
        for x in range(0,w):
            for y in range(0,h):
                case = self.labcase[y*w+x]
                if (case.side[0] == 0):
                    canvas.create_line(x*dx,y*dy,x*dx+dx,y*dy,width=3)
                if (case.side[1] == 0):
                    canvas.create_line(x*dx+dx,y*dy,x*dx+dx,y*dy+dy,width=3)
                if (case.side[2] == 0):
                    canvas.create_line(x*dx+dx,y*dy+dy,x*dx,y*dy+dy,width=3)
                if (case.side[3] == 0):
                    canvas.create_line(x*dx,y*dy+dy,x*dx,y*dy,width=3)
                canvas.create_text(x*dx+dx/2,y*dy+dy/2,text=str(case.value))

    # Ouvrir un passage entre 2 cases adjacente
    def Passage(self,x1,y1,x2,y2):
        w = self.labwidth
        h = self.labheight
        c1 = self.labcase[y1*w+x1]
        c2 = self.labcase[y2*w+x2]
        if (x1 == x2):
            if (y2 == y1+1): 
                c1.side[2]=1; c2.side[0]=1
            if (y2 == y1-1):
                c1.side[0]=1; c2.side[2]=1
        if (y1 == y2):
            if (x2 == x1+1):
                c1.side[1]=1; c2.side[3]=1
            if (x2 == x1-1):
                c1.side[3]=1; c2.side[1]=1


fenetre = Tk()
fenetre.title("Labyrinthe")

canvas = Canvas(fenetre,width=480,height=480,background="#FFFFC0")
canvas.pack()

lab = Labyrinthe()
#lab.Passage(2,2,2,1)

lab.Draw(canvas)


fenetre.mainloop()
