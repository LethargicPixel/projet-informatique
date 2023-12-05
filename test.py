from nonogramm import Grille

aResoudre=Grille()
aResoudre.creerGrilleHasard(5,5)
aResoudre.afficher()
resolu=aResoudre
aResoudre.positionsFinal()

print("________________________________________________________________________________________________________________________________________")
resolu.afficher()

"""
for i in aResoudre.lignes:
    print(i)

aResoudre.remplis(Grille.ligne,0)
print()
for i in aResoudre.lignes:
    print(i)



    

aResoudre.afficher()"""
aResoudre.position()