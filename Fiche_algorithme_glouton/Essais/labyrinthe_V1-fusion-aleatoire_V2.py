# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:58:09 2019

@author: locutus
"""

import random
import time
from tkinter import *
from threading import Thread


# Une case du labyrinthe
class LabCase():
    inited = 0      # est-il inititialisé
    side = list()   # les côtés
    value = 0
    x = 0
    y = 0
    
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
        for y in range(0,self.labheight):
            for x in range(0,self.labwidth):
                case = LabCase()
                case.value = i
                i = i + 1
                case.x = x
                case.y = y
                self.labcase.append(case)
                
    def Case(self,x,y):
        return self.labcase[y*self.labwidth+x]
    
    # Dessin du labyrinthe
    def Draw(self,canvas):
        w = self.labwidth
        h = self.labheight
        dx = int(canvas['width'])/w;
        dy = int(canvas['height'])/h;
        
        canvas.delete(ALL)
        for x in range(0,w):
            xx = x*dx
            for y in range(0,h):
                yy = y*dy
                case = self.labcase[y*w+x]
                if (case.inited == 0):
                    canvas.create_rectangle(xx,yy,xx+dx,yy+dy,fill="white",outline="")
                else:
                    canvas.create_rectangle(xx,yy,xx+dx,yy+dy,fill="#C0C0C0",outline="")
                if (case.side[0] == 0):
                    canvas.create_line(xx,yy,xx+dx,yy,width=3)
                if (case.side[1] == 0):
                    canvas.create_line(xx+dx,yy,xx+dx,yy+dy,width=3)
                if (case.side[2] == 0):
                    canvas.create_line(xx+dx,yy+dy,xx,yy+dy,width=3)
                if (case.side[3] == 0):
                    canvas.create_line(xx,yy+dy,xx,yy,width=3)
                canvas.create_text(xx+dx/2,yy+dy/2,text=str(case.value))

    # Changer la valeur du groupe de case
    def GroupChangeValue(self,x,y,new_value):
        if (x < 0) or (x >= self.labwidth) or (y < 0) or (y >= self.labheight): return
        case = self.Case(x,y)
        if (case.value == new_value): return
        case.value = new_value
        if (case.side[0] == 1):
            self.GroupChangeValue(x,y-1,new_value)
        if (case.side[1] == 1):
            self.GroupChangeValue(x+1,y,new_value)
        if (case.side[2] == 1):
            self.GroupChangeValue(x,y+1,new_value)
        if (case.side[3] == 1):
            self.GroupChangeValue(x-1,y,new_value)

    # Ouvrir un passage entre 2 cases adjacente
    def Passage(self,x1,y1,x2,y2):
        w = self.labwidth
        h = self.labheight
        c1 = self.Case(x1,y1)
        c2 = self.Case(x2,y2)
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
                
    # Chercher la case voisine
    def GetNextCase(self,x,y,side):
        if ((side == 0) and (y > 0)):
            return self.Case(x,y-1)
        if ((side == 1) and (x < self.labwidth-1)):
            return self.Case(x+1,y)
        if ((side == 2) and (y < self.labheight-1)): 
            return self.Case(x,y+1)
        if ((side == 3) and (x > 0)): 
            return self.Case(x-1,y)
        return None
    
    # Extension du labyrinthe à partir d'une case
    def ExtendCase(self,x,y):
        s = list()
        case = self.labcase[y*self.labwidth+x]
        for i in range(0,4):
            if (case.side[i] == 0): s.append(i)
        #for i in range(0,len(s)): print(s[i])
        if (len(s) == 0): return None
        i = random.randint(0,len(s)-1)
        return self.GetNextCase(x,y,s[i])

    # Trouver une case non initialisée        
    def FindNotInited(self):
        for y in range(0,self.labheight):
            for x in range(0,self.labwidth):
                if self.Case(x,y).inited == 0: return (x,y)
        return None
    
    # Vérifier que tout le labyrinthe est connecté
    # toutes les cases ont le même numéro
    def CheckConnexion(self):
        val = Case(0,0).value
        for y in range(0,self.labheight):
            for x in range(0,self.labwidth):
                if self.Case(x,y).value != val: return 0
        return 1


fenetre = Tk()
fenetre.title("Labyrinthe")


class Tache(Thread):
    win = None
    
    def __init__(self,fenetre):
        Thread.__init__(self)
        self.win = fenetre
        self.start()
        
    def run(self):
        while 1:
            #print(str(time.time()))
            time.sleep(0.3)


canvas = Canvas(fenetre,width=480,height=480,background="white")
canvas.pack()

lab = Labyrinthe()

thread = Tache(fenetre)

while 1:
    if lab.FindNotInited() == None: break
    while 1:
        x = random.randint(0,lab.labwidth-1)
        y = random.randint(0,lab.labheight-1)
        case = lab.ExtendCase(x,y)
        if case != None:
            if case.inited == 0: break
    if case != None:
        print(case.x,case.y)
        lab.Passage(x,y,case.x,case.y)
        case.value = lab.Case(x,y).value
        lab.Case(x,y).inited = 1
        case.inited = 1
        
    lab.Draw(canvas)
    fenetre.update_idletasks()
    fenetre.update()    
    time.sleep(0.1)


#thread_1.join()
fenetre.mainloop()
