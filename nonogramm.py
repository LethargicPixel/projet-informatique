from audioop import reverse
from random import randint
from os import system
from re import search
from time import perf_counter

#from pip import image

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
    
    def transformeVrai(self,force=False):
        if force:
            self._valeur=True
        elif self._valeur==None:
            self._valeur=True
    
    def transformeFaux(self,force=False):
        if force:
            self._valeur=False
        elif self._valeur==None:
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
        self._positionModifiable={}
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
        self.lignes.pop()
        
        for i in range(tailleColonne):
            self.colonnes.append([])
            for j in range(tailleLigne):
                self.colonnes[i].append(self.lignes[j][i])
        self.colonnes.pop()
        
        self.grille={Type.colonne:self.colonnes,Type.ligne:self.lignes}
    
    
    def creerGrilleParImage(self,img):
        return
        
        
        
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
        
        
        while True:
            try:
                result.remove(0)
            except:
                break
        if not result:
            result.append(0)
            
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
            
    def compteTrou(self,liste):
        result=[]
        compteur=0
        for i in liste:
            if i.getValeur()==None:
                compteur+=1
            else:
                result.append(compteur)
                compteur=0
        result.append(compteur)
        
        while True:
            try:
                result.remove(0)
            except:
                break
        if not result:
            result=[len(liste)]
        return result
        
    def positionsFinal(self):
        
        self._position= {Type.colonne:self._positions(self.colonnes),Type.ligne:self._positions(self.lignes)}
        self._positionModifiable=dict(self._position) 
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
       
        liste=self.grille[type][index]
        indexs=self._positionModifiable[type][index]
        place=[]
        
        debut=self._verifLimiteDebut(liste,indexs,compte=True)
        fin=self._verifLimiteFin(liste,indexs,compte=True)
        
        tempo=len(liste)-debut[1]+(fin[1]+1)
        i=debut[1]
        
        while liste[i].getValeur()!=None and i<(len(liste)-1):
            i+=1
            tempo-=1
        while liste[i-1].getValeur()==True and i>0 and i<(len(liste)-1):
            i-=1
        place.append(i)
        i=-fin[1]
        while liste[-i].getValeur()!=None and i<(len(liste)-2):
            i+=1
            tempo-=1
            
        while liste[-i-1].getValeur()==True and i>1 and i<(len(liste)-2):
            i+=1
        place.append(-i)
        if tempo<0:
            tempo=0
        return tempo,place
    
    def _verifLigneRemplis(self,liste):
        for i in liste:
            if i.getValeur()==None:
                return False
        return True
    
    def _verifLimiteDebut(self,liste,indexs,compte=False):
        result=False
        
        try:
            i=liste.index(Case())
            tempo=liste[0:i]
            compteur=i
            i=-1
            while tempo[i].getValeur==True:
                i-=1
                compteur-=1
                result=True
            if not compte:
                aEnlever=self._positionParLigne(tempo[:i])
                for i in aEnlever:
                    indexs.remove(i)
            return result,compteur
        except:
            return result,0
    
    
    def _verifLimiteFin(self,liste,indexs,compte=False):
        result=False
        inverser=reversed(liste)
        try:
            inverser=inverser.index(Case())
            tempo=inverser[0:i]
            compteur=i
            i=-1
            while tempo[i].getValeur==True:
                i-=1
                compteur-=1
                result=True
            if not compte:
                indexs=reverse(indexs)
                aEnlever=self._positionParLigne(tempo[:i])
                for i in aEnlever:
                    indexs.remove(i)
                indexs=reverse(indexs)
            return result,-compteur-1
        except:
            return result,0
    
          
          
          
          
          
           
    def remplis(self,type,indexs):
        
        coordonnee=indexs
        nbLibres=self._comptePlaceLibre(type,coordonnee)
        nbARemplir=self._compteTotalCase(type,coordonnee)
        liste=self.grille[type][coordonnee]
        indexs=self._position[type][coordonnee]
        indexsModif=self._positionModifiable[type][coordonnee]
        trous=self.compteTrou(liste)
        
        print(indexsModif)
        limiteDebut=self._verifLimiteDebut(liste,indexsModif)
        limiteFin=self._verifLimiteFin(liste,indexsModif)
        
        compteur=0
        
        
        
        if (indexsModif==[nbLibres[0]] or indexsModif==len(liste)):
            for i in liste:
                i.transformeVrai()
                
        elif max(trous)<min(indexsModif) and not self._verifLigneRemplis(liste):
            i=0
            try:
                while i+max(trous)<len(liste):
                    trous=self.compteTrou(liste)
                    pasRemplis=liste[i:i+max(trous)+1].index(Case())
                    if liste[i+max(trous)]!=None:
                        liste[pasRemplis].transformeFaux()
                    i+=1
            except:
                pass
        
        elif limiteDebut[0]:
            compteur=limiteDebut[1]
            for i in range(indexsModif[0]):
                
                liste[compteur].transformeVrai()
                compteur+=1
            if compteur<len(liste):
                liste[compteur].transformeFaux()
        
        elif limiteFin[0]:
            compteur=-limiteFin[1]+1
            for i in range(indexsModif[-1]):
                
                liste[compteur].transformeVrai()
                compteur+=1
            if -compteur<len(liste):
                liste[-(compteur+1)].transformeFaux()
                         
        elif nbLibres[0]==nbARemplir and len(indexs)>1  and not self._verifLigneRemplis(liste):
            for i in indexsModif:
                for j in range(i):
                    liste[compteur].transformeVrai()
                    compteur+=1

                if compteur<len(liste):
                    liste[compteur].transformeFaux()
                    compteur+=1
                    
        elif indexsModif>[nbLibres[0]/2] and len(indexsModif)==1 and not self._verifLigneRemplis(liste):
            
            compteurDebut=nbLibres[1][0]+nbLibres[0]-indexsModif[0]
            compteurFin=nbLibres[1][1]-nbLibres[0]+indexsModif[0]              
            
                
            for i in range(compteurDebut,len(liste)+compteurFin+1):
                   
                liste[i].transformeVrai()
           
                    
        elif not indexsModif and not self._verifLigneRemplis(liste):
            for i in liste:
                if i.getValeur()==None:
                    i.transformeFaux()
                
        elif indexs==self._positionParLigne(liste) and not self._verifLigneRemplis(liste):
            for i in liste:
                if i.getValeur() == None:
                    i.transformeFaux() 
       
        elif len(indexs)==1 and len(self._positionParLigne(liste))>1 and not self._verifLigneRemplis(liste):
           
        
            while (len(self._positionParLigne(liste))!=1):
                i=0 
                
                while liste[i].getValeur()!=True:
                    i+=1
                   
                while liste[i].getValeur()==True:
                    i+=1
                    
                while liste[i].getValeur()==None:
                    liste[i].transformeVrai()
                    i+=1
        elif len(indexs)==1 and not self._verifLigneRemplis(liste):
            tempo=0
            for i in range(len(liste)):
                tempo=i
                if liste[i].getValeur()==True:
                    break
            for j in range(tempo+indexs[0],len(liste)):
                liste[j].transformeFaux()
            
            
            for k in range(len(liste)-1,-1,-1):
                
                tempo=k
                if liste[k].getValeur()==True:
                    break
            for l in range(tempo-indexs[0],-1,-1):
                liste[l].transformeFaux()
            
            while len(self._positionParLigne(liste))>1:
                tempo=0
                while liste[tempo]!=True:
                    tempo+=1
                while liste[tempo]==True:
                    tempo+=1
                while liste[tempo]!=True:
                    liste.tempo[tempo].transformeVrai()
                    tempo+=1
        
               
                    
                    
                        

            
    def afficher(self):
        for i in self.lignes:
            print(i)  
            
    def resoud(self):
        for i in range(len(self.lignes)):
            self.remplis(Type.ligne,i)
            self.remplis(Type.colonne,i)  

if __name__=="__main__":
    
    aResoudre=Grille()
    resolu=Grille()


    a=10
    system('cls')
    print(a)
    aResoudre.creerGrilleHasard(a,a)
    resolu.lignes=aResoudre.copie()
    for i in aResoudre.lignes[0]:
        i.transformeVrai(force=True)
    print()
    aResoudre.lignes[0][0].transformeVrai(force=True)
    aResoudre.lignes[0][1].transformeVrai(force=True)
    aResoudre.lignes[0][2].transformeFaux(force=True)
    aResoudre.lignes[0][3].transformeFaux(force=True)
    aResoudre.afficher()
    aResoudre.positionsFinal()
    print("-")
    print()
    aResoudre.lignes[0][0].transformeVrai(force=True)
    aResoudre.remplis(Type.ligne,0)

    temps=perf_counter()

    aResoudre.afficher()
    aResoudre.remplis(Type.ligne,0)
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