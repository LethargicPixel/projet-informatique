from random import randint

class Grille():
    def __init__(self) -> None:
        
        self.tailleLigne=0
        self.tailleColonne=0
        self.numColonne={}
        self.numLigne={}
        self.lignes=[[]]


    def creerGrilleHasard(self,tailleLigne,tailleColonne):
        self.tailleLigne=tailleLigne
        self.tailleColonne=tailleColonne
        
        for i in range(tailleLigne):
            for j in range(tailleColonne):
                self.lignes[i].append(bool(randint(0,1)))
            self.lignes.append([])
        self.lignes=self.lignes[:-1]

    def indexer(self):
        tempo=self.lignes[:]
        for i in range(len(tempo)):
            compte=0
            self.numLigne[i]=[]
            for y in tempo[i]:
                if compte!=compte+y:
                    compte+=1
                else:
                    self.numLigne[i].append(compte)
                    compte=0
            self.numLigne[i].append(compte)
        
        for i in self.numLigne:
            while True:
                try:
                    self.numLigne[i].remove(0)
                except:
                    break



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
grille.creerGrilleHasard(2,2)
grille.indexer()
print(grille.lignes)
print("\n\n\n")
print(grille.numLigne)