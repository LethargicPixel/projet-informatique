from nonogramm import Grille

grille=Grille()
grille.creerGrilleHasard(5,5)
for i in range(5):
    grille.lignes[0][i].transformeVrai()
grille.lignes[0][-1].transformeFaux()

grille.lignes[0][-2].transformeFaux()

for i in grille.lignes:
    print(i)


print()
print(grille.positionsFinal()[0],"\n")
for i in grille.lignes:
    print(i)

grille.remplis(Grille.ligne,0)
print()
for i in grille.lignes:
    print(i)