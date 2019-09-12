# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 19:18:36 2019

@author: LAU Wai Tong Christian
"""

from labyrinthe_generator import *
import math
import random
from tkinter import *  


class LabSolver(Labyrinthe):

    entree = [0,0]      # case d'entrée
    sortie = [9,9]      # case de sortie
    ecolor = "#99FF99"
    scolor = "#87CEFA"
    banned_color = "#404040"

    pos = [0,0]

    def __init__(self, w, h):
        super().__init__(w, h)
        draw_case_value = False


    def DrawCase(self, canvas, x, y, background):
        v = self.Case(x,y).value
        if (v == -1):
            background = self.banned_color
        elif (v == 1):
            background = self.ecolor
        super().DrawCase(canvas, x, y, background)


    # Dessin du labyrinthe
    def Draw(self,canvas):
        super().Draw(canvas)
        self.DrawCase(canvas, self.entree[0], self.entree[1], self.ecolor)
        self.DrawCase(canvas, self.sortie[0], self.sortie[1], self.scolor)
        dx = int(canvas['width'])/self.width
        dy = int(canvas['height'])/self.height
        canvas.create_text(
            (self.entree[0]+0.5)*dx,
            (self.entree[1]+0.5)*dy,
            text="IN")
        canvas.create_text(
            (self.sortie[0]+0.5)*dx,
            (self.sortie[1]+0.5)*dy,
            text="OUT")
        canvas.create_oval((self.pos[0]+0.2)*dx, (self.pos[1]+0.2)*dy,
            (self.pos[0]+0.8)*dx, (self.pos[1]+0.8)*dy,
            width=3)


    def Reset(self, newval):
        self.pos[0] = self.entree[0]
        self.pos[1] = self.entree[1]
        for x in range(0,self.width):
            for y in range(0,self.height):
                self.Case(x,y).value = newval


    def DistanceSortie(self, x, y):
        dx = x-self.sortie[0]
        dy = y-self.sortie[1]
        return math.sqrt(dx*dx+dy*dy)


    def Solve(self, callback):
        
        print("Début de recherche de solution.")
        
        self.Reset(0)
        mode = 0
        self.Case(self.pos[0],self.pos[1]).value = 1

        while ((self.pos[0] != self.sortie[0]) or (self.pos[1] != self.sortie[1])):
            case = self.Case(self.pos[0],self.pos[1])
            
            if (mode == 0):         # mode "Glouton"
                #--------------------------------------------------------------

                # Construire une liste de côtés ouverts
                s = list()
                for i in range(0,4):
                    if (case.side[i] == 1):
                        c2 = self.GetNextCase(self.pos[0], self.pos[1] ,i)
                        if (c2 != None):
                            if (c2.value == 0):
                                s.append(i)

                if (len(s) > 0):
                    # Déterminer la case d'à côté plus proche de la sortie
                    mindist = math.inf
                    cmin = None
                    for i in s:
                        c2 = self.GetNextCase(self.pos[0], self.pos[1] ,i)
                        d = self.DistanceSortie(c2.x, c2.y)
                        if (d < mindist):
                            mindist = d
                            cmin = c2

                    # Mise à jour de la position
                    self.Case(self.pos[0], self.pos[1]).value = 1
                    self.pos[0] = cmin.x
                    self.pos[1] = cmin.y
                    cmin.value = 1
                else:
                    # Si toutes les cases d'à côté déjà visitées,
                    # alors passer en mode "sortie de cul de sac"
                    mode = 1
                    case.value = -1     # marquer la case comme banni

            elif (mode == 1):       # mode "sortie cul de sac"
                #--------------------------------------------------------------
                
                # Construire une liste de côtés ouverts
                s1 = list()         # liste des cases d'à côté non bannies
                s2 = list()         # liste des cases d'à côté pas encore visitées
                for i in range(0,4):
                    if (case.side[i] == 1):
                        c2 = self.GetNextCase(self.pos[0], self.pos[1] ,i)
                        if (c2 != None):
                            if (c2.value != -1):
                                s1.append(i)
                            if (c2.value == 0):
                                s2.append(i)

                if (len(s2) > 0):
                    # S'il y a des cases d'à côté pas encore visitées,
                    # alors aller dans l'une de ces cases
                    # Et on repasse en mode "glouton"
                    mode = 0
                    self.Case(self.pos[0], self.pos[1]).value = 1
                    i = random.randint(0,len(s2)-1)
                    c2 = self.GetNextCase(self.pos[0], self.pos[1] ,s2[i])
                    self.pos[0] = c2.x; self.pos[1] = c2.y
                elif (len(s1) > 0):
                    # Pas de case d'à côté pas visitées,
                    # aller dans une des cases pas bannies
                    self.Case(self.pos[0], self.pos[1]).value = (len(s1)==1) and -1 or 1
                    i = random.randint(0,len(s1)-1)
                    c2 = self.GetNextCase(self.pos[0], self.pos[1] ,s1[i])                    
                    self.pos[0] = c2.x; self.pos[1] = c2.y

                #--------------------------------------------------------------

            if (callback != None):
                if (callback() == 0): break


# Fonction callback pour mettre à jour l'affichage
# après chaque changement du labyrinthe
def Callback():
    try:
        # Si problème de la fenêtre (fermeture ?),
        # déclencher une exception et sortie du programme
        if (fenetre.state() == "normal"): pass
    except:
        return 0
    lab.Draw(canvas)                # redessiner le labyrinthe
    fenetre.update_idletasks()      # Appel des tâches liées à la fenêtre
    fenetre.update()                # Mise à jour de la fenêtre
    return 1

# Création du labyrinthe
lab = LabSolver(10,10)
lab.sortie = [lab.width-1,lab.height-1]
lab.draw_case_value=True

def Solve():
    print("Recommencer")
    lab.ResetLabyrinthe()
    lab.Generate(Callback)
    lab.Solve(Callback)

def Solve2():
    print("Recommencer sans régénérer")
    lab.Solve(Callback)
    
# Création de la fenêtre
fenetre = Tk()
fenetre.title("Labyrinthe")

# Création d'un menu avec une commande pour recommencer
menubar = Menu(fenetre)
menubar.add_command(label="Recommencer", command=Solve)
menubar.add_command(label="Recommencer sans régénérer", command=Solve2)
fenetre.config(menu=menubar)

# Création du "canvas" de la fenêtre
canvas = Canvas(fenetre,width=600,height=lab.height*600/lab.width,background="white")
canvas.pack()

lab.Generate(Callback)          # Génération du labyrithe
print("Génération du labyrinthe terminée.")
lab.Solve(Callback)             # Résolution du labyrinthe

fenetre.mainloop()
