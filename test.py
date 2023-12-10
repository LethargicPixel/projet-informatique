from nonogramm import Grille

aResoudre=Grille()
resolu=Grille()

aResoudre.creerGrilleHasard(5,5)
aResoudre.afficher()
resolu.lignes=aResoudre.copie()
aResoudre.positionsFinal()

print("________________________________________________________________________________________________________________________________________")
resolu.afficher()
aResoudre.afficher()
"""
for i in aResoudre.lignes:
    print(i)

aResoudre.remplis(Grille.ligne,0)
print()
for i in aResoudre.lignes:
    print(i)



    

aResoudre.afficher()"""
aResoudre.position()