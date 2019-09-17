# CORRECTION

# Situation 1

def occurence_1(L):
    n=len(L)
    i=0
    while ((i<n) and L[i]!=40):
        i=i+1
    if (i<n):
        print(i+1, "est le numero du joueur gagnant")
    else:
        print ("Aucun joueur a fait un score de 40")
    
# Situation 2

def occurence_2(L,x):
    n=len(L)
    i=0
    while ((i<n) and L[i]!=x):
        i=i+1
    if (i<n):
        print(i+1, "est le numero du joueur gagnant")
    else:
        print ("Aucun joueur a fait un score de", x)
