# -*- coding: utf-8 -*-
"""
Created on Wed Jul 17 15:58:09 2019

@author: LAU Wai Tong Christian
"""

import random
import time
from tkinter import *
from threading import Thread


# Une case du labyrinthe
class LabCase():
    inited = 0      # est-il inititialisé
    side = list()   # les côtés, entier : 0=fermé, 1=ouvert
    value = 0
    x = 0
    y = 0
    
    def __init__(self):
        self.inited = 0
        side_list = list()
        for i in range(0,4):
            side_list.append(0)
        self.side = side_list
        
        
    def Reset(self, x, y, value):
        self.inited = 0
        for i in range(0,4): self.side[i] = 0
        self.value = value
        self.x = x; self.y = y
        

# Classe représentant le labyrinthe
class Labyrinthe():
    width = 10       # largeur du labyrinthe
    height = 10      # hauteur du labyrinthe
    labcase = list()    # les cases du labyrinthe
    
    draw_case_value = False
    
    
    def __init__(self,w,h):
        # initialisation des cases du labyrinthe
        i = 0
        self.width = w
        self.height = h
        for y in range(0,self.height):
            for x in range(0,self.width):
                case = LabCase()
                case.value = i
                i = i + 1
                case.x = x
                case.y = y
                self.labcase.append(case)

                
    def Case(self,x,y):
        return self.labcase[y*self.width+x]
    
    
    def ResetLabyrinthe(self):
        i = 0
        for y in range(0,self.height):
            for x in range(0,self.width):
                self.Case(x,y).Reset(x,y,i)
                i += 1
    
    
    # Dessin d'un case
    def DrawCase(self, canvas, x, y, background):
        w = self.width
        h = self.height
        dx = int(canvas['width'])/w;
        dy = int(canvas['height'])/h;
        xx = x*dx
        yy = y*dy
        
        case = self.Case(x, y)
        canvas.create_rectangle(xx,yy,xx+dx,yy+dy,fill=background,outline="")
#        if (case.inited == 0):
#            canvas.create_rectangle(xx,yy,xx+dx,yy+dy,fill="white",outline="")
#        else:
#            canvas.create_rectangle(xx,yy,xx+dx,yy+dy,fill="#C0C0C0",outline="")
        if (case.side[0] == 0):
            canvas.create_line(xx,yy,xx+dx,yy,width=3)
        if (case.side[1] == 0):
            canvas.create_line(xx+dx,yy,xx+dx,yy+dy,width=3)
        if (case.side[2] == 0):
            canvas.create_line(xx+dx,yy+dy,xx,yy+dy,width=3)
        if (case.side[3] == 0):
            canvas.create_line(xx,yy+dy,xx,yy,width=3)
        if (self.draw_case_value):
            canvas.create_text(xx+dx/2,yy+dy/2,text=str(case.value))

    
    # Dessin du labyrinthe
    def Draw(self,canvas):
        w = self.width
        h = self.height
        dx = int(canvas['width'])/w;
        dy = int(canvas['height'])/h;
        
        canvas.delete(ALL)
        for x in range(0,w):
            for y in range(0,h):
                back = (self.Case(x,y).inited == 0) and "white" or "#C0C0C0"
                self.DrawCase(canvas,x,y,back)

#        for x in range(0,w):
#            xx = x*dx
#            for y in range(0,h):
#                yy = y*dy
#                case = self.labcase[y*w+x]
#                if (case.inited == 0):
#                    canvas.create_rectangle(xx,yy,xx+dx,yy+dy,fill="white",outline="")
#                else:
#                    canvas.create_rectangle(xx,yy,xx+dx,yy+dy,fill="#C0C0C0",outline="")
#                if (case.side[0] == 0):
#                    canvas.create_line(xx,yy,xx+dx,yy,width=3)
#                if (case.side[1] == 0):
#                    canvas.create_line(xx+dx,yy,xx+dx,yy+dy,width=3)
#                if (case.side[2] == 0):
#                    canvas.create_line(xx+dx,yy+dy,xx,yy+dy,width=3)
#                if (case.side[3] == 0):
#                    canvas.create_line(xx,yy+dy,xx,yy,width=3)
#                if (self.draw_case_value):
#                    canvas.create_text(xx+dx/2,yy+dy/2,text=str(case.value))


    # Vérifier si les coordonnées sont à l'intérieur du labyrinthe
    def IsInside(self,x,y):
        if (x < 0) or (x >= self.width) or (y < 0) or (y >= self.height):
            return 0
        return 1


    # Changer la valeur du groupe de case
    def GroupChangeValue(self,x,y,new_value):
        if self.IsInside(x,y) == 0: return
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
        w = self.width
        h = self.height
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
        if ((side == 1) and (x < self.width-1)):
            return self.Case(x+1,y)
        if ((side == 2) and (y < self.height-1)): 
            return self.Case(x,y+1)
        if ((side == 3) and (x > 0)): 
            return self.Case(x-1,y)
        return None


    # Trouver une case non initialisée        
    def FindNotInited(self):
        l = list()
        for y in range(0,self.height):
            for x in range(0,self.width):
                if self.Case(x,y).inited == 0: 
                    l.append(self.Case(x,y))
        if (len(l) != 0):
            return l
        else:
            return None

    
    # Vérifier que tout le labyrinthe est connecté
    # toutes les cases ont le même numéro
    def CheckConnexion(self):
        val = self.Case(0,0).value
        for y in range(0,self.height):
            for x in range(0,self.width):
                if self.Case(x,y).value != val: return 0
        return 1
    
    
    # Extension du labyrinthe à partir d'une case
    def ExtendCase(self,x,y):
        #case = self.labcase[y*self.width+x]
        case = self.Case(x,y)
        case.inited = 1         # Marquer la case 'initialisée'

        # Création d'une liste de côtés fermés
        s = list()
        for i in range(0,4):
            if (case.side[i] == 0):
                if (self.GetNextCase(x,y,i) != None):
                    s.append(i)

        # S'il reste des côtés fermés
        if (len(s) > 0):
            # Choisir une case d'à côté au hasard, de l'autre côté d'une
            # des côtés fermés (liste s)
            case2 = self.GetNextCase(x,y,s[random.randint(0,len(s)-1)])
            if (case2 != None):
                if (case2.value != case.value):
                    # Si la case d'à côté n'est pas du même groupe
                    if (case2.inited == 0):
                        # Si la case n'est pas initialisée,
                        # alors intégrer la case au groupe
                        case2.value = case.value
                        case2.inited = 1
                    else:
                        # Si la case d'à côté fait déjà partie d'un groupe
                        # alors ralier le groupe au groupe de la case courante
                        self.GroupChangeValue(case2.x,case2.y,case.value)
                    # Créer un passage entre les 2 cases
                    self.Passage(x,y,case2.x,case2.y)


    # Génération du labyrinthe
    def Generate(self,callback):
        while self.CheckConnexion() == 0:
            # Si tout les cases du labyrinthe ne sont pas encore connectées
            
            # Création d'une liste de cases pas encore initialisée
            l = self.FindNotInited()
            if (l != None):
                # S'il reste encore des case non initialisée
                # alors initialisation et étendre à un groupe
                case = l[random.randint(0,len(l)-1)]
                self.ExtendCase(case.x,case.y)
            else:
                # S'il ne reste plus de cases non initialisées
                # alors choisir au hasard une case et étendre
                # le groupe à un autre groupe proche
                x = random.randint(0,self.width-1)
                y = random.randint(0,self.height-1)
                self.ExtendCase(x,y)
            # Appel du callback
            # Si le callback retourne 0 alors, sortie de la boucle
            if (callback != None):
                if callback() == 0: break
                   

def Test():
#    # Exemple de création d'un thread
#    class Tache(Thread):
#        win = None
#        running = 1
#        
#        def __init__(self,fenetre):
#            Thread.__init__(self)
#            self.win = fenetre
#            self.start()
#            
#        def run(self):
#            while self.running:
#                #print(str(time.time()))
#                time.sleep(0.3)
#                
#        def stop(self):
#            self.running = 0

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

    # Création de la fenêtre
    fenetre = Tk()
    fenetre.title("Labyrinthe")

    # Création du labyrinthe
    lab = Labyrinthe(10,10)
    #thread = Tache(fenetre)
    lab.draw_case_value = True
    
    # Création du "canvas" de la fenêtre
    canvas = Canvas(fenetre,width=600,height=lab.height*600/lab.width,background="white")
    canvas.pack()    
    
    # Génération du labyrithe
    lab.Generate(Callback)
        #time.sleep(0.05)
    
    print("stop")
    
    #thread.stop()
    
    #thread_1.join()
    fenetre.mainloop()
