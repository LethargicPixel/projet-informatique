from os import system
from time import sleep
from time import perf_counter
from nonogramm import Grille, Type

aResoudre=Grille()
resolu=Grille()


for a in range(10,11):
    system('cls')
    print(a)
    aResoudre.creerGrilleHasard(a,a)
    resolu.lignes=aResoudre.copie()
    aResoudre.positionsFinal()

    temps=perf_counter()
    print(aResoudre.getPosition())
    for i in range(len(aResoudre.lignes)):
    
        aResoudre.remplis(Type.ligne,i)
        aResoudre.remplis(Type.colonne,i)
    





        


    """
    for i in range(aResoudre.tailleLigne):
        for j in range(aResoudre.tailleColonne):
            if aResoudre.lignes[j][i]!=resolu.lignes[j][i]:
                print(aResoudre.lignes[j][i],resolu.lignes[j][i])
                print(j,i)
    if not aResoudre.grilleEgal(resolu) :break   
    """
    aResoudre.afficher()
    print(round(perf_counter()-temps,2))  
    print(aResoudre.grilleEgal(resolu))
    