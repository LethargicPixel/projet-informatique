from nonogramm import Grille

aResoudre=Grille()
resolu=Grille()

aResoudre.creerGrilleHasard(10,10)
aResoudre.afficher()
resolu.lignes=aResoudre.copie()
aResoudre.positionsFinal()
print(aResoudre.getPosition())
print("________________________________________________________________________________________________________________________________________")


for i in range(len(aResoudre.lignes)):
    aResoudre.remplis(Grille.ligne,i)
    aResoudre.remplis(Grille.colonne,i)
    aResoudre.afficher()
    print(i)





    

aResoudre.afficher()
aResoudre.getPosition()