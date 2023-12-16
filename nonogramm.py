from random import randint
class Type:
    colonne="colonne"
    ligne="ligne"
    
    
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
    
    def __eq__(self,case2):
        if isinstance(case2,Case):
            return case2.getValeur()==self.getValeur()
        return False
            
    def getValeur(self):
        return self._valeur
    
    def transformeVrai(self):
        self._valeur=True
    
    def transformeFaux(self):
        self._valeur=False
        
    def vider(self):
        self._valeur=None
        
        
        
        
        
class Grille:
        
    def __init__(self) -> None:
        
        self.lignes=[[]]
        self.colonnes=[[]]
        self.tailleLigne=0
        self.tailleColonne=0
        self._position={}
        self.grille={}

    def copie(self):
        tempo=[[]]
        for i in range(len(self.lignes)):
            for j in self.lignes[i]:
                tempo[i].append(Case(j.getValeur()))
            tempo.append([])
        return tempo[:-1]
    
    def creerGrilleHasard(self,tailleLigne,tailleColonne):
        self.tailleLigne=tailleLigne
        self.tailleColonne=tailleColonne
        self.lignes=[[]]
        self.colonnes=[[]]
        
        for i in range(tailleLigne):
            self.lignes.append([])
            for j in range(tailleColonne):
                self.lignes[i].append(Case(bool(randint(0,1))))
 
        
        for i in range(tailleColonne):
            self.colonnes.append([])
            for j in range(tailleLigne):
                self.colonnes[i].append(self.lignes[j][i])
            
        
        self.grille={Type.colonne:self.colonnes,Type.ligne:self.lignes}
        
        
        
        
        
    def _positions(self,liste):
        tempo=liste[:]
        result={}
        for i in range(len(tempo)):
            result[i]=self._positionParLigne(tempo[i])

        return result
    
    
    def _positionParLigne(self,liste):
        compte=0
        result=[]
        for y in liste:
            tempo=y.getValeur()
            if tempo==None:tempo=0
            
            if compte!=compte+tempo:
                compte+=1
            else:
                result.append(compte)
                compte=0
        result.append(compte)
        
        for i in result:
            while True:
                try:
                    result[i].remove(0)
                except:
                    break
        
        return result
    
    def grilleEgal(self,grille2):
        for i in range(self.tailleLigne):
            for j in range(self.tailleColonne):
                try:
                    if self.lignes[i][j]!=grille2.lignes[i][j]:
                        
                        return False
                except:
                    return False

                return True
    
    def positionsFinal(self):
        self._position= {Type.colonne:self._positions(self.colonnes),Type.ligne:self._positions(self.lignes)}
        tempo=[[]]
        for i in range(self.tailleLigne):
          
            for j in self.lignes[i]:
            
                tempo[i].append(j.getValeur())
            tempo.append([])
        tempo=tempo[:-1]
        

        for i in self.lignes:
            for y in i:
                y.vider()            
        return tempo

    def getPosition(self):
        return self._position

    def _compteTotalCase(self,type,index):
        indexs=self._position[type][index]
        tempo=0
        for i in indexs:
            tempo+=i
        tempo+=len(indexs)-1
        return tempo
    
    def _comptePlaceLibre(self,type:str,index:int):

        liste=self.grille[type]
        liste=liste[index]
        tempo=len(liste)
        i=0
        
        while liste[i]==False:
            print(i)
            tempo-=1
            i+=1
        i=1
        while liste[-i]==False:
            tempo-=1
            i+=1
        return tempo
                
    def remplis(self,type,indexs):
        
        nbLibres=self._comptePlaceLibre(type,indexs)
        nbARemplir=self._compteTotalCase(type,indexs)
        liste=self.grille[type][indexs]
        indexs=self._position[type][indexs]
    
        compteur=0
        
        
        
        if indexs==[nbLibres]:
            for i in liste:
                if i.getValeur()==None:
                    i.transformeVrai()
                    
        elif nbLibres==nbARemplir and len(indexs)>1:
            for i in indexs:
                for j in range(i):
                    liste[compteur].transformeVrai()
                    compteur+=1

                if compteur<len(liste):
                    liste[compteur].transformeFaux()
                    compteur+=1
                    
        elif indexs>[nbLibres/2] and len(indexs)==1:
            
            compteur=nbLibres-indexs[0]

            while liste[compteur].getValeur()==False:
                compteur+=1
            
            if indexs[0]%2==nbLibres%2:
                
                for i in range(compteur,compteur+(indexs[0]-(nbLibres-1)//2)):
                   
                    liste[i].transformeVrai()
            else:  
                for i in range(compteur,1+compteur+(indexs[0]-(nbLibres-1)//2)):
                   
                    liste[i].transformeVrai()
                    
        elif not indexs:
            for i in liste:
                i.transformeFaux()
                
        elif indexs==self._positionParLigne(liste):
            for i in liste:
                if i.getValeur() == None:
                    i.transformeFaux() 
        """
        elif len(indexs)==1 and len(self._positionParLigne(liste))>1:
            
            print("oui")
            print(type)
            print(indexs)
            print(self._positionParLigne(liste))
            
            
            while (len(self._positionParLigne(liste))!=1):
                i=0 
                
                while liste[i].getValeur()!=True:
                    i+=1
                    print(i)
                while liste[i].getValeur()==True:
                    i+=1
                    print(i)
                while liste[i].getValeur()==None:
                    liste[i].transformeVrai()
                    i+=1
                    print(i)
            """

            
    def afficher(self):
        for i in self.lignes:
            print(i)  
            
    def resoud(self):
        for i in range(len(self.lignes)):
            self.remplis(Type.ligne,i)
            self.remplis(Type.colonne,i)  

