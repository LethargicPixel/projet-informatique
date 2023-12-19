from os import system
from time import perf_counter
from nonogramm import Grille, Type

aResoudre=Grille()
resolu=Grille()


a=10
system('cls')
print(a)
aResoudre.creerGrilleHasard(a,a)
resolu.lignes=aResoudre.copie()
for i in aResoudre.lignes[0]:
    print(i)
    i.transformeVrai(force=True)
print()
aResoudre.lignes[0][0].transformeFaux(force=True)

aResoudre.lignes[0][1].transformeFaux(force=True)
aResoudre.afficher()
aResoudre.positionsFinal()
print("-")

aResoudre.lignes[0][0].transformeFaux(force=True)
aResoudre.remplis(Type.ligne,0)
temps=perf_counter()

aResoudre.afficher()

"""
for j in range(5):
    print(j)
    
    aResoudre.afficher()
    for i in range(len(aResoudre.lignes)):

        aResoudre.remplis(Type.ligne,i)
        aResoudre.remplis(Type.colonne,i)     


   
    for i in range(aResoudre.tailleLigne):
        for j in range(aResoudre.tailleColonne):
            if aResoudre.lignes[j][i]!=resolu.lignes[j][i]:
                print(aResoudre.lignes[j][i],resolu.lignes[j][i])
                print(j,i)
    if not aResoudre.grilleEgal(resolu) :break   
    
    print(round(perf_counter()-temps,2))  
    print(aResoudre.grilleEgal(resolu))
"""