from nonogramm import Grille

aResoudre=Grille()
resolu=Grille()


a=5
aResoudre.creerGrilleHasard(a,a)
resolu.lignes=aResoudre.copie()
aResoudre.positionsFinal()


for i in range(len(aResoudre.lignes)):
    aResoudre.remplis(Grille.ligne,i)
    aResoudre.remplis(Grille.colonne,i)






    



for i in range(aResoudre.tailleLigne):
    for j in range(aResoudre.tailleColonne):
        if aResoudre.lignes[j][i]!=resolu.lignes[j][i]:
            print(aResoudre.lignes[j][i],resolu.lignes[j][i])
            print(j,i)
            
print(aResoudre.grilleEgal(resolu))