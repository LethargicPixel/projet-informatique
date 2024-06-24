import copy
from itertools import product
from random import randint



class Type:
    colonne="colonne"
    ligne="ligne"
    
    
class Case:
    vrai="■"
    faux="X"
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
        elif self._valeur is None:
            self._valeur=True
    
    def transformeFaux(self,force=False):
        if force:
            self._valeur=False
        elif self._valeur is None:
            self._valeur=False
        
    def vider(self):
        self._valeur=None
             
        
class Grille:
        
    def __init__(self) -> None:
        
        self.lignes:list[list[Case]]=[[]]
        self.colonnes:list[list[Case]]=[[]]
        self.tailleLigne:int=0
        self.tailleColonne:int=0
        self._position:dict[str:list[int]] = {Type.colonne: {}, Type.ligne: {}}
        self._positionModifiable:dict[str:list[int]] = {Type.colonne: {}, Type.ligne: {}}
        self.grille={}

    def copie(self):
        """creer une copie non egale de la grille seulement

        Returns:
            Grille: copie de la grille 
        """    
        return copy.deepcopy(self)
    
    def creerGrilleHasard(self,tailleLigne,tailleColonne=None):
        """creer une grille au hasard

        Args:
            tailleLigne (int): nombre de ligne de la grille
            tailleColonne (int, optional): nombre de colonne de la ligne. Si non rempli, la grille sera carre avec le premier parametre comme reference
        """
        
        if tailleColonne is None:
            self.tailleColonne=tailleLigne
        else:
            self.tailleColonne=tailleColonne
            
        self.tailleLigne=tailleLigne
        self.lignes=[[]]
        self.colonnes=[[]]
        
        for i in range(self.tailleLigne):
            self.lignes.append([])
            for j in range(self.tailleColonne):
                self.lignes[i].append(Case(bool(randint(0,1))))
        self.lignes.pop()
        
        for i in range(self.tailleColonne):
            self.colonnes.append([])
            for j in range(self.tailleLigne):
                self.colonnes[i].append(self.lignes[j][i])
        self.colonnes.pop()
        
        self.grille={Type.colonne:self.colonnes,Type.ligne:self.lignes}
        self._positionsFinal()
    
    def creerGrilleParIndex(self,*positions):
        """creer une grille avec les coordonnee donné en parametre

        Args:
            positions (List[List]): prend en parametre une liste de 2 liste, la premiere est les coordonnee des ligne et la seconde est les coordonnee de la colonne
        """
        sequence1=positions[0]
        sequence2=positions[1]
        somme1=0
        somme2=0
        self.lignes=[[]]
        self.colonnes=[[]]
        self.tailleColonne=len(sequence1)
        self.tailleLigne=len(sequence2)
        
        for i in sequence1:
            for k in i:
                somme1+=k
               
        for i in sequence2:
            for k in i:
                somme2+=k
                      
        if somme1!=somme2:
            return False
        
        self._position[Type.colonne]=[]
        for i in range(len(sequence1)):
            self._position[Type.colonne].append(sequence1[i])    
                
        self._position[Type.ligne]=[]
        for i in range(len(sequence2)):
            self._position[Type.ligne].append(sequence2[i])
        


        
        for i in range(self.tailleLigne):
            self.lignes.append([])
            for j in range(self.tailleColonne):
                self.lignes[i].append(Case())
        self.lignes.pop()
        
        for i in range(self.tailleColonne):
            self.colonnes.append([])
            for j in range(self.tailleLigne):
                self.colonnes[i].append(self.lignes[j][i])
        self.colonnes.pop()
        
        self.grille={Type.colonne:self.colonnes,Type.ligne:self.lignes}
        self._positionModifiable=copy.deepcopy(self._position)
    
    def creerGrilleParLigne(self,liste_ligne:list[list[Case]]):
        
        self.lignes=liste_ligne
        self.colonnes=[[]]
        self.tailleColonne=len(liste_ligne)
        self.tailleLigne=len(liste_ligne[0])
        
        for i in range(self.tailleColonne):
            self.colonnes.append([])
            for j in range(self.tailleLigne):
                self.colonnes[i].append(self.lignes[j][i])
        self.colonnes.pop()
        self.grille={Type.colonne:self.colonnes,Type.ligne:self.lignes}
        self._positionModifiable=copy.deepcopy(self._position)
         
        
    def _positions(self,liste):
        """calcule les coordonnee pour un cote de la grille

        Args:
            liste (Liste[Liste[Case]]): un sens de la grille

        Returns:
            Liste[Liste[int]]: tous les coordonnee pour ce sens de la grille
        """
        tempo=liste[:]
        result=[]
        for i in range(len(tempo)):
            result.append(self._positionParLigne(tempo[i]))

        return result
    
    def _positionParLigne(self,liste):
        """calcule les coordonnee pour une seul ligne

        Args:
            liste (List[Case]): une seul ligne de la grille

        Returns:
            List[int]: les coordonnee correspondant à la grille passe en parametre
        """
        compte=0
        result=[]
        for y in liste:
            tempo=y.getValeur()
            if tempo is not True:
                tempo=0
            
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
        """verifie si les deux grilles ont les memes valeurs aux memes endroit

        Args:
            grille2 (Grille): la grille à tester

        Returns:
            Bool: True si les deux grilles sont les même, False sinon
        """
        if self.tailleColonne!=grille2.tailleColonne or self.tailleLigne!=grille2.tailleLigne:
            return False
        
        for i in range(self.tailleLigne):
            for j in range(self.tailleColonne):
                if self.lignes[i][j]!=grille2.lignes[i][j]:                   
                    return False
          
        return True
    
            
    def _compteTrou(self,liste):
        """compte le nombre de case vide

        Arg:
            liste (List[Case]): la ligne/colonne à tester

        Return:
            int: le nombre de Case dont la valeur est égale à None
        """
        result=[]
        compteur=0
        for i in liste:
            if i.getValeur() is None:
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
        
        
        
        
    def _positionsFinal(self):
        """
            finalise la creation des coordonnee et vide la grille qui a servie à creer les coordonnee
        Returns:
            List[List[Case]]: une copie de la Grille de depart
        """
        self._position[Type.colonne] = self._positions(self.colonnes)
        self._position[Type.ligne] = self._positions(self.lignes)
        self._positionModifiable=copy.deepcopy(self._position) 
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
        """renvoie les coordonnee

        Returns:
            Dict[Type:Liste[int]]: les coordonnee
        """
        return self._position


    
    def _comptePlaceLibre(self,type:str,index:int):
        """compte le nombre de case remplissable entre les deux bornes

        Args:
            type (str): ligne ou colonne
            index (int): numero de lign/colonne

        Returns:
            List[int,list[int]]: en [0], le nombre de cases libres au milieu de la lign/colonne, en [1] la liste des bornes
        """
        liste=self.grille[type][index]
        coordonnee=self._positionModifiable[type][index]
        place=[]
        
        debut=self._verifLimiteDebut(liste,coordonnee,compte=True)
        fin=self._verifLimiteFin(liste,coordonnee,compte=True)
        
        tempo=len(liste)-debut[1]+(fin[1]+1)
        i=debut[1]
        
        while liste[i].getValeur()!=None and i<(len(liste)-1):
            
            i+=1
            tempo-=1
        while liste[i-1].getValeur()==True and i>0 and i<(len(liste)-1):
            i-=1
            tempo+=1
        place.append(i)
        i=fin[1]
        while liste[i].getValeur()!=None and i<(len(liste)-2):
            i-=1
            tempo-=1
            
        while liste[-i-1].getValeur()==True and i>1 and i<(len(liste)-2):
            i+=1
        place.append(i)
        if tempo<0:
            tempo=0
        return tempo,place
    
    def _verifLigneRemplis(self,liste):
        """verifis s'il la ligne/colonne a deja été completer

        Args:
            liste (Case): liste contenant la ligne/colonne à tester

        Returns:
            Bool: True si ligne remplis, False sinon
        """
        for i in liste:
            if i.getValeur() is None:
                return False
        return True
    
    def _verifLimiteDebut(self,liste,coordonnee,compte=False):
        """
        regarde si il y a une partie de la ligne rempli (pour un index en plusieurs parties, si la premiere partie est validé)
        Args:
            liste (_type_): _description_
            coordonnee (_type_): _description_
            compte (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        result=False
        coordonnee=copy.deepcopy(coordonnee)
        try:
            i=liste.index(Case())
            tempo=liste[0:i]
            compteur=i
            i=-1
            while tempo[i].getValeur()==True:
                i-=1
                compteur-=1
                result=True
            
                

            if (not compte) and tempo[i].getValeur()==False:
                aEnlever=self._positionParLigne(tempo)
                
            if len(aEnlever)!=0 and tempo[-1].getValeur() is True:
                aEnlever=aEnlever[:-1]
                
            if aEnlever[0]==0 and len(aEnlever)==1:
                aEnlever=[]
                 
            return result,compteur,len(aEnlever)
        except:
            return result,compteur,0
    
    def _verifLimiteFin(self,liste,coordonnee,compte=False):
        result=False
        coordonnee=copy.deepcopy(coordonnee)
        inverser=liste[::-1]
        try:
            i=inverser.index(Case())
            
            
            tempo=inverser[0:i]
            compteur=i
            i=-1
            
            while tempo[i].getValeur()==True:
                i-=1
                compteur-=1
                result=True
                
            if not compte and tempo[i].getValeur()==False:
                coordonnee=coordonnee[::-1]
                aEnlever=self._positionParLigne(tempo[:i])
            
            if len(aEnlever)!=0 and tempo[-1].getValeur() is True:
                aEnlever=aEnlever[:-1]

            if aEnlever[0]==0 and len(aEnlever)==1:
                aEnlever=[]
                
            return result,-(compteur+1),len(aEnlever)
        except:
            return result,-(compteur+1),0

    
    def premierNonNul(self,type,index,debut):
        liste:list[Case]=self.grille[type][index]
        i=debut
        try:
            while liste[i].getValeur() is None:
                i+=1
            return debut,liste[i].getValeur()
        except:
            return debut,None
        
    def dernierNonNul(self,type,index,fin):
        liste:list[Case]=self.grille[type][index]
        i=fin
        try:
            while liste[i].getValeur() is None:
                i-=1
            return fin,liste[i].getValeur()
        except:
            return fin,None
     
      
      
      
     
    def remplis(self,type,index):
        
        
        liste:list[Case]=self.grille[type][index]

        if self._verifLigneRemplis(liste):
            return
        
        nbLibres=self._comptePlaceLibre(type,index)
        coordonnee=self._position[type][index]#donne la liste d'indice correspondant a la ligne/colonne
        trous=self._compteTrou(liste)
        """    
        if index==1 and type==Type.colonne:
            pass
        """
        
        limiteDebut=self._verifLimiteDebut(liste,coordonnee)
        limiteFin=self._verifLimiteFin(liste,coordonnee)
        coordonneeModif=coordonnee[limiteDebut[2]:len(coordonnee)-limiteFin[2]]
        nbARemplir:int=(len(coordonneeModif)-1)+sum(coordonneeModif)
        compteur:int=0
        premier_trou=trous[0]
        premier_non_nul=self.premierNonNul(type,index,limiteDebut[1])
        dernier_trou=trous[-1]
        dernier_non_nul=self.dernierNonNul(type,index,limiteFin[1])
        coordonnee_entre_bornes=self._positionParLigne(liste[premier_non_nul[0]:len(liste)+dernier_non_nul[0]+1])

        
        if (not coordonneeModif) or coordonnee==self._positionParLigne(liste):
            for i in liste:
                i.transformeFaux()
        
        elif nbARemplir==len(liste[limiteDebut[1]:len(liste)+limiteFin[1]+1]):
            compteur=limiteDebut[1]
            
            for i in coordonneeModif:#[2,2,2]
                for y in range(i): 
                    liste[compteur].transformeVrai()
                    compteur+=1    
                
                if compteur<len(liste) :
                    liste[compteur].transformeFaux()
                    compteur+=1
        
        elif dernier_trou<coordonneeModif[-1] and dernier_non_nul[1] is False:
            #[ , , , , ,F, , ] [1,3]
            compteur=dernier_non_nul[0]#-1
            while liste[compteur].getValeur() is not False:
                liste[compteur].transformeFaux()
                compteur-=1
            
                
        elif premier_trou<coordonneeModif[0] and premier_non_nul[1] is False:
            compteur=premier_non_nul[0]
            while liste[compteur].getValeur() is not False:
                liste[compteur].transformeFaux()
                compteur+=1
        
        elif limiteDebut[0]:
            #[F,V,F,V, ] [1,2]
            compteur=limiteDebut[1]#0
            
            for i in range(coordonneeModif[0]):
                liste[compteur].transformeVrai()
                compteur+=1
                
            liste[compteur].transformeFaux()
        
        elif limiteFin[0]:
            compteur=limiteFin[1]
            for i in range(coordonneeModif[-1]):
                liste[compteur].transformeVrai()
                compteur-=1
           
            liste[compteur].transformeFaux()                    
        
        #peut etre present en bas
        elif premier_trou<=coordonneeModif[0] and premier_non_nul[1]:
            #[ , ,V, , ]  [2,1]
            compteur=premier_non_nul[0]+premier_trou
            
            while liste[compteur].getValeur() is True or compteur<len(liste)-1:
                compteur+=1

            if (compteur-coordonneeModif[0])>=0:
                for i in range(compteur-coordonneeModif[0]+1,compteur):
                    liste[i].transformeVrai()
                    
                for i in range(0,compteur-coordonneeModif[0]):
                    liste[i].transformeFaux()
        
        #idem
        elif dernier_trou<=coordonneeModif[-1] and dernier_non_nul[1] and len(coordonneeModif)!=1 and premier_trou==nbARemplir:
            
            compteur=dernier_non_nul[0]+dernier_trou
            
            

            while liste[compteur].getValeur():
                compteur+=1
            
            
            for i in range(compteur+coordonneeModif[0],compteur):

                liste[i].transformeVrai()
                
            for i in range(compteur+coordonneeModif[0],len(liste)):
                liste[i].transformeFaux()
                
        elif premier_trou==coordonneeModif[0] and dernier_trou<nbARemplir and dernier_non_nul[1]==False:
            #[1,2,3] []
            compteur=premier_non_nul[0]
            while liste[compteur].getValeur()!=False:
                liste[compteur].transformeVrai()
                compteur+=1
                    
        elif dernier_trou==coordonneeModif[-1] and premier_trou<nbARemplir and premier_non_nul[1]==False :
            compteur=dernier_non_nul[0]
            while liste[compteur].getValeur()!=False:
                liste[compteur].transformeVrai() 
                compteur-=1
           
        elif dernier_trou<coordonneeModif[-1] and not dernier_non_nul[1]:
            compteur=limiteFin[1]

            while (liste[compteur].getValeur() is None) and (-compteur)<len(liste):
                liste[compteur].transformeFaux()
                compteur-=1
        
        elif premier_trou<coordonneeModif[0] and not premier_non_nul[1]:
            compteur=limiteDebut[1]

            while (liste[compteur].getValeur() is None) and (compteur)<len(liste):
                liste[compteur].transformeFaux()
                compteur+=1
                
        elif len(coordonnee)==1 and len(self._positionParLigne(liste))>1 and not self._verifLigneRemplis(liste):
           
        
            while (len(self._positionParLigne(liste))!=1):
                i=0 
                
                while liste[i].getValeur()!=True:
                    i+=1
                   
                while liste[i].getValeur()==True:
                    i+=1
                    
                while liste[i].getValeur() is None:
                    liste[i].transformeVrai()
                    i+=1
                    
        elif len(coordonnee)==1 and not self._verifLigneRemplis(liste):
            tempo=0
            for i in range(len(liste)):
                tempo=i
                if liste[i].getValeur()==True:
                    break
            for j in range(tempo+coordonnee[0],len(liste)):
                liste[j].transformeFaux()
            
            
            for k in range(len(liste)-1,-1,-1):
                
                tempo=k
                if liste[k].getValeur()==True:
                    break
            for l in range(tempo-coordonnee[0],-1,-1):
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
        
        elif max(trous)<min(coordonneeModif) and not self._verifLigneRemplis(liste):
            i=0
            try:
                while i+max(trous)<len(liste):
                    trous=self._compteTrou(liste)
                    pasRemplis=liste[i:i+max(trous)+1].index(Case())
                    if liste[i+max(trous)]!=None:
                        liste[pasRemplis].transformeFaux()
                    i+=1
            except:
                pass
        elif trous==coordonneeModif:
            for i in liste:
                i.transformeVrai()
        
        elif dernier_trou<coordonneeModif[-1] and dernier_non_nul[1]:
            compteur=dernier_non_nul[0]
            while liste[compteur].getValeur() is None:
                compteur-=1
            while liste[compteur].getValeur is True:
                compteur-=1
            if liste[compteur-1].getValeur() is False:
                for i in range(len(liste)+compteur,len(liste)+compteur+coordonneeModif[-1]):
                    liste[i].transformeVrai()
                    
        elif premier_trou<coordonneeModif[0] and premier_non_nul[1]:
            compteur=premier_non_nul[0]
            while liste[compteur].getValeur() is None:
                compteur+=1
            while liste[compteur].getValeur is True:
                compteur+=1 
            pass
        
        elif premier_non_nul[0]-dernier_non_nul[0]>nbARemplir-1:
            superposition1=[]
            for i in coordonneeModif:
                for j in range(i):
                    superposition1.append([True,i])
                superposition1.append(False)
            if len(superposition1)>nbARemplir:
                superposition1.pop()
            while len(superposition1)!=nbARemplir:
                superposition1.append[False,None]
            superposition2=superposition1[::-1]
            
            position_coordonnee=[]
            
            for i in range(len(superposition1)):
                if superposition1[i]==superposition2[i]:
                    position_coordonnee.append(i+premier_non_nul[0])
            
            ensemble_position_coordonnee=[]
            tempo=[]
            for i in range(len(position_coordonnee)-1):
                if position_coordonnee[i]==position_coordonnee[i+1]:
                    tempo.append(i)
                else:
                    tempo.append[i]
                    ensemble_position_coordonnee.append(tempo)
                    tempo=[]
                    
                    
        
        elif max(coordonnee_entre_bornes)==max(coordonneeModif):
            tempo=0
            position_tempo=None
            liste_a_borner=[]
            for i in range(1,len(liste[premier_non_nul[0]:dernier_non_nul[0]])):
                if liste[i].getValeur() is True:
                    if liste[i-1].getValeur() is None:
                        tempo=0
                        position_tempo=i-1
                        liste_a_borner.append(position_tempo)
                    tempo+=1
                elif liste[i].getValeur() is None:
                    if tempo==max(coordonnee_entre_bornes) and liste[i-1].getValeur() is True:
                        liste_a_borner.append(i)
                        tempo=0
                        position_tempo=None
                    else:
                        if position_tempo in liste_a_borner:
                            liste_a_borner.remove(position_tempo)
                        tempo=0
                        
            for i in liste_a_borner:
                liste[i].transformeFaux()           
    
    def _ligneBrutForce(self,coordonnee:list[int],taille:int):
        resultat:list[list[int]]=[]
        if coordonnee[0]==0:
            return [Case(False) for i in range(taille)]
        a_tester=list(product([Case(True),Case(False)],repeat=taille))
        for i in a_tester:
            coordonnee_tempo=self._positionParLigne(i)
            
            if coordonnee_tempo==coordonnee:
                resultat.append(i)
                
        return resultat
    
    def resoudBrutForce(self):
        grille_a_tester=Grille()
        total_ligne=[]
        for i in self._position[Type.ligne]:
            total_ligne.append(self._ligneBrutForce(i,self.tailleLigne))
        
        
            
        

                  
                
                    

                             
    def afficher(self):
        for i in self.lignes:
            print(i)  
            
    def resoud(self):
        grille2=Grille()
        while not self.grilleEgal(grille2):
            grille2=self.copie()
            
            for j in range(self.tailleColonne):
                for i in range(self.tailleLigne):
                    self.remplis(Type.ligne,i)
                    self.remplis(Type.colonne,j)
    
    

  
        
                    
                  
    
   
                    
                 
if __name__=="__main__":
    
  
    grille=Grille()
    
    """  grille.creerGrilleParIndex(
        [[1,5],[1,1,1,1,1],[2,2,1,1],[5,4],[2,2],[1],[2],[1,1,1],[1,1,2],[2,1,3]],
        [[2,1],[3,1,1],[1,2,4],[4],[1,2,1,1],[2,2],[1,2,1],[2,1,1],[1,2,1],[4,1,1]]
        ) """
    
    grille.creerGrilleHasard(2)
    print(grille.getPosition())
    grille.resoudBrutForce()

    """ 
    #grille.resoud()
    print()
    print(grille.getPosition())
    print()
    grille.afficher()
    print()

    
    for i in grille.grille.keys():
        for j in range(len(grille.grille[i])):
            
            
            a=grille._positionParLigne(grille.grille[i][j])
            b=grille.getPosition()[i][j]
            if a==b:
                continue
            print("________________________")
            print(f"indice actuel : {a}")
            print(f"indice voulu  : {b}")
            #print(a==b)
            print(i,j)
            print("________________________")
            
     """
     
     
    
 