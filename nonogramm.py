from random import randint
class Case:
    vrai="|"
    faux="O"
    def __init__(self, valeur=None):
        self._valeur=valeur

    def __str__(self):
        match self._valeur:
            case True :
                return Case.vrai
            case False:
                return Case.faux
            case _:
                return " "

    def __repr__(self) -> str:
        match self._valeur:
            case True :
                return Case.vrai
            case False:
                return Case.faux
            case _:
                return " "
            
    def valeur(self):
        return self._valeur
    
    def transformeVrai(self):
        self._valeur=True
    
    def transformeFaux(self):
        self._valeur=False
        
        
        
class Grille:
    def __init__(self) -> None:
        
        self.tailleLigne=0
        self.tailleColonne=0
        self._position={}
        self.lignes=[[]]
        self.colonnes=[[]]


    def creerGrilleHasard(self,tailleLigne,tailleColonne):
        self.tailleLigne=tailleLigne
        self.tailleColonne=tailleColonne
        
        for i in range(tailleLigne):
            for j in range(tailleColonne):
                self.lignes[i].append(Case(bool(randint(0,1))))
            self.lignes.append([])
        self.lignes=self.lignes[:-1]
        
        for i in range(tailleColonne):
            for j in range(tailleLigne):
                self.colonnes[i].append(self.lignes[j][i])
            self.colonnes.append([])
        self.colonnes=self.colonnes[:-1]
        
        
    def _positions(self,liste):
        tempo=liste[:]
        result={}
        for i in range(len(tempo)):
            compte=0
            result[i]=[]
            for y in tempo[i]:
                if compte!=compte+y.valeur():
                    compte+=1
                else:
                    result[i].append(compte)
                    compte=0
            result[i].append(compte)
        
        for i in result:
            while True:
                try:
                    result[i].remove(0)
                except:
                    break
        return result
    
    def positionsFinal(self):
        self._position= {"colonne":self._positions(self.colonnes),"ligne":self._positions(self.lignes)}

    def position(self):
        return self._position

    def compteTotalCase(self,numeroLigne):
        tempo=0
        for i in self.numLigne[numeroLigne]:
            tempo+=i
        tempo+=len(self.numLigne[numeroLigne])-1
        return tempo
    
    def resoudLigne(self,numeroLigne):
        self.lignes[numeroLigne]=[]
        if self.compteTotalCase(numeroLigne)==self.tailleLigne:
            for i in self.numLigne[numeroLigne]:
                self.lignes[numeroLigne]+=i*[True]+[False]
            self.lignes[numeroLigne]=self.lignes[numeroLigne][:-1]

                

grille=Grille()
grille.creerGrilleHasard(5,5)
grille.positionsFinal()

for i in grille.lignes:
    print(i)
print()

for i in grille.colonnes:
    print(i)
print("e")

grille.colonnes[0][0].transformeFaux()

for i in grille.lignes:
    print(i)
print()

for i in grille.colonnes:
    print(i)
print()