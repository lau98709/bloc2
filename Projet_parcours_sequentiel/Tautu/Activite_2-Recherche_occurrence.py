# CORRECTION 1 : avec boucle bornée "for"

# Situation 1

# L est la liste des scores de chaque joueur
def occurence_1(L):
    n=len(L)
    for i in range(n):
        if (L[i]==40):
            return (i+1, 'le numéro du joueur gagnant')
    print ("Aucun joueur a fait un score de 40")
    
# Situation 2

# x est le score choisi par le gérant
def occurence_2(L,x):
    n=len(L)
    for i in range(n):
        if (L[i]==x):
            return (i+1, 'le numéro du joueur gagnant')
    print ("Aucun joueur a fait un score de",x)
    
# CORRECTION 2 : avec boucle non bornée "while"

# Situation 1

def occurence_1bis(L):
    n=len(L)
    i=0
    while ((i<n) and L[i]!=40):
        i=i+1
    if (i<n):
        print(i+1,'est le numéro du joueur gagnant')
    else:
        print ("Aucun joueur a fait un score de 40")
    
# Situation 2

def occurence_2bis(L,x):
    n=len(L)
    i=0
    while ((i<n) and L[i]!=x):
        i=i+1
    if (i<n):
        print(i+1,'est le numéro du joueur gagnant')
    else:
        print ("Aucun joueur a fait un score de",x)
