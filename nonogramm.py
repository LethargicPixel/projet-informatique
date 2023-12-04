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
        
    def vider(self):
        self._valeur=None
        
        
        
        
        
class Grille:
    
    colonne="colonne"
    ligne="ligne"
    
    def __init__(self) -> None:
        
        
        self.tailleLigne=0
        self.tailleColonne=0
        self._position={}
        self.lignes=[[]]
        self.colonnes=[[]]
        self.grille={}

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
        
        self.grille={Grille.colonne:self.colonnes,Grille.ligne:self.lignes}
        
        
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
        self._position= {Grille.colonne:self._positions(self.colonnes),Grille.ligne:self._positions(self.lignes)}
        tempo=self.lignes
        for i in self.lignes:
            for y in i:
                y.vider()            
        return self._position,tempo

    def position(self):
        return self._position

    def compteTotalCase(self,type,index):
        indexs=self._position[type][index]
        tempo=0
        for i in indexs:
            tempo+=i
        tempo+=len(indexs)-1
        return tempo
    
    def comptePlaceLibre(self,type:str,index:int):
        liste=self.grille[type]
        liste=liste[index]
        tempo=0
        for i in liste:
            if i.valeur() == None or i.valeur()==True :
                tempo+=1
        return tempo
                
    def remplis(self,type,index):
        
        liste=self.grille[type][index]
        indexs=self._position[type][index]
        
        nbLibres=self.comptePlaceLibre(type,index)
        nbARemplir=self.compteTotalCase(type,index)
        
        if indexs==[nbARemplir]:
            for i in liste:
                if i.valeur()==None:
                    i.transformeVrai()
                    print(i)
            
        

                

grille=Grille()
grille.creerGrilleHasard(5,5)
for i in range(5):
    grille.lignes[0][i].transformeVrai()
    
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