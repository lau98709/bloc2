# -*- coding: utf-8 -*-
"""
Created on Thu Sep 12 00:01:58 2019

@author: LAU Wai Tong Christian
"""

from labyrinthe_solver import *


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
lab.draw_case_value=False

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

# Génération du labyrithe
lab.Generate(Callback)
    #time.sleep(0.05)

print("stop")

#thread.stop()

#thread_1.join()
fenetre.mainloop()
