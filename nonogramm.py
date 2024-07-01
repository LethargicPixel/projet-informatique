from itertools import product
from random import randint
import time


class Type:
    colonne: str = "colonne"
    ligne: str = "ligne"


class Case:
    vrai: str = "■"
    faux: str = "X"

    def __init__(self, valeur: bool = None):
        self._valeur: bool = valeur

    def __str__(self) -> str:
        match self._valeur:
            case True:
                return Case.vrai
            case False:
                return Case.faux
            case _:
                return " "

    def __repr__(self) -> str:
        match self._valeur:
            case True:
                return Case.vrai
            case False:
                return Case.faux
            case _:
                return " "

    def __eq__(self, case2) -> bool:
        if isinstance(case2, Case):
            return case2.getValeur() == self.getValeur()
        return False

    def getValeur(self) -> bool | None:
        return self._valeur

    def transformeVrai(self, force: bool = False) -> None:
        if force:
            self._valeur = True
        elif self._valeur is None:
            self._valeur = True

    def transformeFaux(self, force: bool = False) -> None:
        if force:
            self._valeur = False
        elif self._valeur is None:
            self._valeur = False

    def vider(self) -> None:
        self._valeur = None


class Grille:

    def __init__(self) -> None:

        self.lignes: list[list[Case]] = [[]]
        self.colonnes: list[list[Case]] = [[]]
        self.taille_ligne: int = 0
        self.taille_colonne: int = 0
        self._position: dict[str:list[list[int]]] = {
            Type.colonne: {}, Type.ligne: {}}
        self._position_modifiable: dict[str:list[list[int]]] = {
            Type.colonne: {}, Type.ligne: {}}
        self.grille: dict[str:list[list[Case]]] = {}

    def copie(self):
        """
        creer une copiede la grille seulement
        """
        tempo: Grille = Grille()
        tempo.lignes = self.lignes[::]
        tempo.colonnes = self.colonnes[::]
        tempo.grille = dict(self.grille)
        tempo.taille_colonne = self.taille_colonne
        tempo.taille_ligne = self.taille_ligne
        tempo._position = dict(self._position)
        tempo._position_modifiable = dict(self._position)

        return tempo

    def remplace(self, grille_2) -> None:
        self.__dict__.update(grille_2.__dict__)

    def creerGrilleHasard(self, taille_ligne: int, taille_colonne: int = None, effacement: bool = True) -> None:
        """creer une grille au hasard

        Args:
            taille_ligne (int): nombre de ligne de la grille
            taille_colonne (int, optional): nombre de colonne de la ligne. Si non rempli, la grille sera carre avec le premier parametre comme reference
            effacement (bool, optional): efface ou non la grille apres creation, default to True
        """

        if taille_colonne is None:
            self.taille_colonne = taille_ligne
        else:
            self.taille_colonne = taille_colonne

        self.taille_ligne = taille_ligne
        self.lignes = [[]]
        self.colonnes = [[]]

        for i in range(self.taille_ligne):
            self.lignes.append([])
            for j in range(self.taille_colonne):
                self.lignes[i].append(Case(bool(randint(0, 1))))
        self.lignes.pop()

        for i in range(self.taille_colonne):
            self.colonnes.append([])
            for j in range(self.taille_ligne):
                self.colonnes[i].append(self.lignes[j][i])
        self.colonnes.pop()

        self.grille = {Type.colonne: self.colonnes, Type.ligne: self.lignes}
        self._positionsFinal(effacement)

    def creerGrilleParIndex(self, *positions: list[list[int]]) -> None:
        """creer une grille avec les coordonnee donné en parametre

        Args:
            positions (list[list]): prend en parametre une liste de 2 liste, la premiere est les coordonnee des ligne et la seconde est les coordonnee de la colonne
        """
        sequence1: list[list[int]] = positions[0]
        sequence2: list[list[int]] = positions[1]
        somme1: int = 0
        somme2: int = 0
        self.lignes = [[]]
        self.colonnes = [[]]
        self.taille_colonne = len(sequence1)
        self.taille_ligne = len(sequence2)

        for i in sequence1:
            for k in i:
                somme1 += k

        for i in sequence2:
            for k in i:
                somme2 += k

        if somme1 != somme2:
            return False

        self._position[Type.colonne] = []
        for i in range(len(sequence1)):
            self._position[Type.colonne].append(sequence1[i])

        self._position[Type.ligne] = []
        for i in range(len(sequence2)):
            self._position[Type.ligne].append(sequence2[i])

        for i in range(self.taille_ligne):
            self.lignes.append([])
            for j in range(self.taille_colonne):
                self.lignes[i].append(Case())
        self.lignes.pop()

        for i in range(self.taille_colonne):
            self.colonnes.append([])
            for j in range(self.taille_ligne):
                self.colonnes[i].append(self.lignes[j][i])
        self.colonnes.pop()

        self.grille = {Type.colonne: self.colonnes, Type.ligne: self.lignes}
        self._position_modifiable = dict(self._position)

    def creerGrilleParLigne(self, liste_ligne: list[list[Case]], effacement: bool = True) -> None:

        self.lignes = liste_ligne
        self.colonnes = [[]]
        self.taille_colonne = len(liste_ligne)
        self.taille_ligne = len(liste_ligne[0])

        for i in range(self.taille_colonne):
            self.colonnes.append([])
            for j in range(self.taille_ligne):
                self.colonnes[i].append(self.lignes[j][i])
        self.colonnes.pop()

        self._positionsFinal(effacement)
        self.grille = {Type.colonne: self.colonnes, Type.ligne: self.lignes}
        self._position_modifiable = dict(self._position)

    def _positions(self, liste: list[list[Case]]) -> list[list[int]]:
        """calcule les coordonnee pour un cote de la grille

        Args:
            liste (liste[liste[Case]]): un sens de la grille

        Returns:
            liste[liste[int]]: tous les coordonnee pour ce sens de la grille
        """
        tempo: list[list[Case]] = liste[:]
        result: list[list[int]] = []
        for i in range(len(tempo)):
            result.append(self._positionParLigne(tempo[i]))

        return result

    def _positionParLigne(self, liste: list[Case]) -> list[int]:
        """calcule les coordonnee pour une seul ligne

        Args:
            liste (list[Case]): une seul ligne de la grille

        Returns:
            list[int]: les coordonnee correspondant à la grille passe en parametre
        """
        compte: int = 0
        result: list[int] = []
        for y in liste:
            tempo = y.getValeur()
            if tempo is not True:
                tempo = 0

            if compte != compte+tempo:
                compte += 1
            else:
                result.append(compte)
                compte = 0
        result.append(compte)

        while True:
            try:
                result.remove(0)
            except:
                break
        if not result:
            result.append(0)

        return result

    def grilleEgal(self, grille_2) -> bool:
        """verifie si les deux grilles ont les memes valeurs aux memes endroit

        Args:
            grille_2 (Grille): la grille à tester

        Returns:
            Bool: True si les deux grilles sont les même, False sinon
        """
        if self.taille_colonne != grille_2.taille_colonne or self.taille_ligne != grille_2.taille_ligne:
            return False

        for i in range(self.taille_ligne):
            for j in range(self.taille_colonne):
                if self.lignes[i][j] != grille_2.lignes[i][j]:
                    return False

        return True

    def _positionsFinal(self, effacement: bool = True) -> None:
        """
            finalise la creation des coordonnee

        Args:
            effacement (bool, optional): efface ou non la grille de depart. Defaults to True.

        """
        self._position[Type.colonne] = self._positions(self.colonnes)
        self._position[Type.ligne] = self._positions(self.lignes)
        self._position_modifiable = dict(self._position)

        if effacement is True:

            for i in self.lignes:
                for y in i:
                    y.vider()

    def getPosition(self) -> dict[list[list[int]]]:
        """renvoie les coordonnee

        Returns:
            Dict[Type:liste[int]]: les coordonnee
        """
        return self._position

    def remplis(self, type: Type, index: int) -> None:
        def _compteTrou(self, liste: list[Case]) -> list[int]:
            """compte le nombre de case vide

            Arg:
                liste (list[Case]): la ligne/colonne à tester

            Return:
                int: le nombre de Case dont la valeur est égale à None
            """
            result: list[int] = []
            compteur: int = 0
            for i in liste:
                if i.getValeur() is None:
                    compteur += 1
                else:
                    result.append(compteur)
                    compteur = 0
            result.append(compteur)

            while True:
                try:
                    result.remove(0)
                except:
                    break
            if not result:
                result = [len(liste)]
            return result

        def _verifLigneRemplis(self, liste: list[Case]) -> bool:
            """verifis s'il la ligne/colonne a deja été completer

            Args:
                liste (list[Case]): liste contenant la ligne/colonne à tester

            Returns:
                Bool: True si ligne remplis, False sinon
            """
            for i in liste:
                if i.getValeur() is None:
                    return False
            return True

        def _verifLimiteDebut(self, liste: list[Case], coordonnee: list[int], compte: bool = False) -> tuple[bool, int, int]:
            """
            regarde si il y a une partie de la ligne rempli (pour un index en plusieurs parties, si la premiere partie est validé)
            Args:
                liste (_type_): _description_
                coordonnee (_type_): _description_
                compte (bool, optional): _description_. Defaults to False.

            Returns:
                _type_: _description_
            """
            result: bool = False
            coordonnee: list[int] = coordonnee[::]
            i: int
            a_enlever: list[int]
            try:
                i = liste.index(Case())
                tempo = liste[0:i]
                compteur = i
                i = -1
                while tempo[i].getValeur() == True:
                    i -= 1
                    compteur -= 1
                    result = True

                if (not compte) and tempo[i].getValeur() == False:
                    a_enlever = self._positionParLigne(tempo)

                if len(a_enlever) != 0 and tempo[-1].getValeur() is True:
                    a_enlever = a_enlever[:-1]

                if a_enlever[0] == 0 and len(a_enlever) == 1:
                    a_enlever = []

                return result, compteur, len(a_enlever)
            except:
                return result, compteur, 0

        def _verifLimiteFin(self, liste: list[Case], coordonnee: list[int], compte: bool = False) -> tuple[bool, int, int]:
            result: bool = False
            coordonnee: list[int] = coordonnee[::]
            inverser: list[Case] = liste[::-1]
            i: int
            a_enlever: list[int]
            try:
                i = inverser.index(Case())

                tempo = inverser[0:i]
                compteur = i
                i = -1

                while tempo[i].getValeur() == True:
                    i -= 1
                    compteur -= 1
                    result = True

                if not compte and tempo[i].getValeur() == False:
                    coordonnee = coordonnee[::-1]
                    a_enlever = self._positionParLigne(tempo[:i])

                if len(a_enlever) != 0 and tempo[-1].getValeur() is True:
                    a_enlever = a_enlever[:-1]

                if a_enlever[0] == 0 and len(a_enlever) == 1:
                    a_enlever = []

                return result, -(compteur+1), len(a_enlever)
            except:
                return result, -(compteur+1), 0

        def premierNonNul(self, type: str, index: int, debut: int) -> tuple[int, bool]:
            liste: list[Case] = self.grille[type][index]
            i: int = debut
            try:
                while liste[i].getValeur() is None:
                    i += 1
                return debut, liste[i].getValeur()
            except:
                return debut, None

        def dernierNonNul(self, type: str, index: int, fin: int) -> tuple[int, bool]:
            liste: list[Case] = self.grille[type][index]
            i
            int = fin
            try:
                while liste[i].getValeur() is None:
                    i -= 1
                return fin, liste[i].getValeur()
            except:
                return fin, None

        liste: list[Case] = self.grille[type][index]

        if _verifLigneRemplis(liste):
            return

        # donne la liste d'indice correspondant a la ligne/colonne
        coordonnee: list[int] = self._position[type][index]
        trous: list[int] = _compteTrou(liste)
        """    
        if index==1 and type==Type.colonne:
            pass
        """

        limite_debut: tuple[bool, int, int] = _verifLimiteDebut(
            liste, coordonnee)
        limite_fin: tuple[bool, int, int] = _verifLimiteFin(liste, coordonnee)
        coordonnee_modif: list[int] = coordonnee[limite_debut[2]:len(
            coordonnee)-limite_fin[2]]
        nb_a_remplir: int = (len(coordonnee_modif)-1)+sum(coordonnee_modif)
        compteur: int = 0
        premier_trou: int = trous[0]
        premier_non_nul: tuple[int, bool] = premierNonNul(
            type, index, limite_debut[1])
        dernier_trou: int = trous[-1]
        dernier_non_nul: tuple[int, bool] = dernierNonNul(
            type, index, limite_fin[1])
        coordonnee_entre_bornes: list[int] = self._positionParLigne(
            liste[premier_non_nul[0]:len(liste)+dernier_non_nul[0]+1])

        if (not coordonnee_modif) or coordonnee == self._positionParLigne(liste):
            for i in liste:
                i.transformeFaux()

        elif nb_a_remplir == len(liste[limite_debut[1]:len(liste)+limite_fin[1]+1]):
            compteur = limite_debut[1]

            for i in coordonnee_modif:  # [2,2,2]
                for y in range(i):
                    liste[compteur].transformeVrai()
                    compteur += 1

                if compteur < len(liste):
                    liste[compteur].transformeFaux()
                    compteur += 1

        elif dernier_trou < coordonnee_modif[-1] and dernier_non_nul[1] is False:
            # [ , , , , ,F, , ] [1,3]
            compteur = dernier_non_nul[0]  # -1
            while liste[compteur].getValeur() is not False:
                liste[compteur].transformeFaux()
                compteur -= 1

        elif premier_trou < coordonnee_modif[0] and premier_non_nul[1] is False:
            compteur = premier_non_nul[0]
            while liste[compteur].getValeur() is not False:
                liste[compteur].transformeFaux()
                compteur += 1

        elif limite_debut[0]:
            # [F,V,F,V, ] [1,2]
            compteur = limite_debut[1]  # 0

            for i in range(coordonnee_modif[0]):
                liste[compteur].transformeVrai()
                compteur += 1

            liste[compteur].transformeFaux()

        elif limite_fin[0]:
            compteur = limite_fin[1]
            for i in range(coordonnee_modif[-1]):
                liste[compteur].transformeVrai()
                compteur -= 1

            liste[compteur].transformeFaux()

        # peut etre present en bas
        elif premier_trou <= coordonnee_modif[0] and premier_non_nul[1]:
            # [ , ,V, , ]  [2,1]
            compteur = premier_non_nul[0]+premier_trou

            while liste[compteur].getValeur() is True or compteur < len(liste)-1:
                compteur += 1

            if (compteur-coordonnee_modif[0]) >= 0:
                for i in range(compteur-coordonnee_modif[0]+1, compteur):
                    liste[i].transformeVrai()

                for i in range(0, compteur-coordonnee_modif[0]):
                    liste[i].transformeFaux()

        # idem
        elif dernier_trou <= coordonnee_modif[-1] and dernier_non_nul[1] and len(coordonnee_modif) != 1 and premier_trou == nb_a_remplir:

            compteur = dernier_non_nul[0]+dernier_trou

            while liste[compteur].getValeur():
                compteur += 1

            for i in range(compteur+coordonnee_modif[0], compteur):

                liste[i].transformeVrai()

            for i in range(compteur+coordonnee_modif[0], len(liste)):
                liste[i].transformeFaux()

        elif premier_trou == coordonnee_modif[0] and dernier_trou < nb_a_remplir and dernier_non_nul[1] == False:

            compteur = premier_non_nul[0]
            while liste[compteur].getValeur() != False:
                liste[compteur].transformeVrai()
                compteur += 1

        elif dernier_trou == coordonnee_modif[-1] and premier_trou < nb_a_remplir and premier_non_nul[1] == False:
            compteur = dernier_non_nul[0]
            while liste[compteur].getValeur() != False:
                liste[compteur].transformeVrai()
                compteur -= 1

        elif dernier_trou < coordonnee_modif[-1] and not dernier_non_nul[1]:
            compteur = limite_fin[1]

            while (liste[compteur].getValeur() is None) and (-compteur) < len(liste):
                liste[compteur].transformeFaux()
                compteur -= 1

        elif premier_trou < coordonnee_modif[0] and not premier_non_nul[1]:
            compteur = limite_debut[1]

            while (liste[compteur].getValeur() is None) and (compteur) < len(liste):
                liste[compteur].transformeFaux()
                compteur += 1

        elif len(coordonnee) == 1 and len(self._positionParLigne(liste)) > 1:

            while (len(self._positionParLigne(liste)) != 1):
                i = 0

                while liste[i].getValeur() != True:
                    i += 1

                while liste[i].getValeur() == True:
                    i += 1

                while liste[i].getValeur() is None:
                    liste[i].transformeVrai()
                    i += 1

        elif len(coordonnee) == 1:
            tempo = 0
            for i in range(len(liste)):
                tempo = i
                if liste[i].getValeur() == True:
                    break
            for j in range(tempo+coordonnee[0], len(liste)):
                liste[j].transformeFaux()

            for k in range(len(liste)-1, -1, -1):

                tempo = k
                if liste[k].getValeur() == True:
                    break
            for l in range(tempo-coordonnee[0], -1, -1):
                liste[l].transformeFaux()

            while len(self._positionParLigne(liste)) > 1:
                tempo = 0
                while liste[tempo] != True:
                    tempo += 1
                while liste[tempo] == True:
                    tempo += 1
                while liste[tempo] != True:
                    liste.tempo[tempo].transformeVrai()
                    tempo += 1

        elif max(trous) < min(coordonnee_modif):
            i = 0
            try:
                while i+max(trous) < len(liste):
                    trous = self._compteTrou(liste)
                    pasRemplis = liste[i:i+max(trous)+1].index(Case())
                    if liste[i+max(trous)] != None:
                        liste[pasRemplis].transformeFaux()
                    i += 1
            except:
                pass
        elif trous == coordonnee_modif:
            for i in liste:
                i.transformeVrai()

        elif dernier_trou < coordonnee_modif[-1] and dernier_non_nul[1]:
            compteur = dernier_non_nul[0]
            while liste[compteur].getValeur() is None:
                compteur -= 1
            while liste[compteur].getValeur is True:
                compteur -= 1
            if liste[compteur-1].getValeur() is False:
                for i in range(len(liste)+compteur, len(liste)+compteur+coordonnee_modif[-1]):
                    liste[i].transformeVrai()

        elif premier_trou < coordonnee_modif[0] and premier_non_nul[1]:
            compteur = premier_non_nul[0]
            while liste[compteur].getValeur() is None:
                compteur += 1
            while liste[compteur].getValeur is True:
                compteur += 1
            pass

        elif premier_non_nul[0]-dernier_non_nul[0] > nb_a_remplir-1:
            superposition1 = []
            for i in coordonnee_modif:
                for j in range(i):
                    superposition1.append([True, i])
                superposition1.append(False)
            if len(superposition1) > nb_a_remplir:
                superposition1.pop()
            while len(superposition1) != nb_a_remplir:
                superposition1.append[False, None]
            superposition2 = superposition1[::-1]

            position_coordonnee = []

            for i in range(len(superposition1)):
                if superposition1[i] == superposition2[i]:
                    position_coordonnee.append(i+premier_non_nul[0])

            ensemble_position_coordonnee = []
            tempo = []
            for i in range(len(position_coordonnee)-1):
                if position_coordonnee[i] == position_coordonnee[i+1]:
                    tempo.append(i)
                else:
                    tempo.append[i]
                    ensemble_position_coordonnee.append(tempo)
                    tempo = []

        elif max(coordonnee_entre_bornes) == max(coordonnee_modif):
            tempo = 0
            position_tempo = None
            liste_a_borner = []
            for i in range(1, len(liste[premier_non_nul[0]:dernier_non_nul[0]])):
                if liste[i].getValeur() is True:
                    if liste[i-1].getValeur() is None:
                        tempo = 0
                        position_tempo = i-1
                        liste_a_borner.append(position_tempo)
                    tempo += 1
                elif liste[i].getValeur() is None:
                    if tempo == max(coordonnee_entre_bornes) and liste[i-1].getValeur() is True:
                        liste_a_borner.append(i)
                        tempo = 0
                        position_tempo = None
                    else:
                        if position_tempo in liste_a_borner:
                            liste_a_borner.remove(position_tempo)
                        tempo = 0

            for i in liste_a_borner:
                liste[i].transformeFaux()

    def _ligneBrutForce(self, coordonnee: list[int], taille: int) -> list[list[Case]]:
        resultat: list[list[Case]] = []
        if coordonnee[0] == 0:
            return [[Case(False) for i in range(taille)]]
        a_tester = list(product([Case(True), Case(False)], repeat=taille))
        for i in a_tester:
            coordonnee_tempo = self._positionParLigne(i)

            if coordonnee_tempo == coordonnee:
                resultat.append(i)

        return list(map(list, resultat))

    def resoudBrutForce(self) -> None:

        grille_a_tester:Grille = Grille()
        total_ligne: list[list[list[Case]]] = []
        tempo: list[list[list[Case]]] = []

        liste_indice: list[int] = []
        liste_indice_a_tester: list[int] = [
            0 for i in range(self.taille_ligne)]
        liste_indice_a_tester[-1] -= 1
        

        for i in self._position[Type.ligne]:
            total_ligne.append(self._ligneBrutForce(i, self.taille_ligne))

        for i in total_ligne:
            liste_indice.append(len(i)-1)

        fin_de_boucle:bool = False
        while (liste_indice_a_tester != liste_indice) and not fin_de_boucle:

            if liste_indice == liste_indice_a_tester and liste_indice.count(0) == len(liste_indice):
                fin_de_boucle = True
            else:
                liste_indice_a_tester[-1] += 1

            for i in range(-1, -len(liste_indice_a_tester), -1):
                if liste_indice_a_tester[i] > liste_indice[i]:
                    liste_indice_a_tester[i-1] += 1
                    liste_indice_a_tester[i] = 0
                else:
                    break

            tempo:list[list[Case]] = []

            for i in range(len(liste_indice_a_tester)):
                tempo.append(total_ligne[i][liste_indice_a_tester[i]])

            grille_a_tester.creerGrilleParLigne(tempo[::], False)

            if grille_a_tester.getPosition() == self.getPosition():

                self.remplace(grille_a_tester)

                return

    def afficher(self) -> None:
        for i in self.lignes:
            print(i)

    def resoud(self) -> None:
        grille_2:Grille = Grille()
        while not self.grilleEgal(grille_2):
            grille_2 = self.copie()

            for j in range(self.taille_colonne):
                for i in range(self.taille_ligne):
                    self.remplis(Type.ligne, i)
                    self.remplis(Type.colonne, j)

    def resoudBackTracking(self) -> None:
        def estPossibleColonne(self, grille: Grille) -> bool:
            """
            verifie si la grille en cours de resolution est une position pouvant amener à la resolution du jeu

            Returns:
                Bool
            """

            for i in range(self.taille_colonne):

                a_tester: list[int] = grille.getPosition()[Type.colonne][i]
                position_reel: list[int] = self.getPosition()[Type.colonne][i]

                if (max(a_tester) > max(position_reel) or sum(a_tester) > sum(position_reel)) or (sum(a_tester)+len(a_tester)-1) > (sum(position_reel)+len(position_reel)-1):
                    return False

                if len(a_tester) > len(position_reel):
                    return False
                for i in range(len(a_tester)):
                    if a_tester[i] > position_reel[i]:
                        return False
            return True
        index_liste_indice: int = 0
        total_ligne: list[list[list[Case]]] = []
        liste_indice: list[int] = []
        liste_indice_a_tester: list[int] = [None]*self.taille_ligne

        for i in self._position[Type.ligne]:
            total_ligne.append(
                self._ligneBrutForce(i, self.taille_ligne))
        for i in total_ligne:
            liste_indice.append(len(i)-1)

        while True:
            grille_a_tester = Grille()
            tempo: list[list[list[Case]]] = []
            if liste_indice_a_tester[index_liste_indice] is None:
                liste_indice_a_tester[index_liste_indice] = 0
            else:
                liste_indice_a_tester[index_liste_indice] += 1
                for i in range(index_liste_indice, 0, -1):

                    if liste_indice_a_tester[i] > liste_indice[i]:
                        liste_indice_a_tester[i] = None
                        liste_indice_a_tester[i-1] += 1
                        index_liste_indice -= 1
                    else:
                        break

            for i in range(len(liste_indice_a_tester)):
                if liste_indice_a_tester[i] is not None:
                    tempo.append(total_ligne[i][liste_indice_a_tester[i]])
                else:
                    break

            if len(tempo) < self.taille_colonne:
                for i in range(self.taille_colonne-len(tempo)):
                    tempo.append([Case()]*self.taille_ligne)

            tempo = tempo[::]

            grille_a_tester.creerGrilleParLigne(tempo, False)

            if estPossibleColonne(self, grille_a_tester):
                if liste_indice_a_tester[-1] is not None:

                    self.remplace(grille_a_tester)
                    return

                elif grille_a_tester.getPosition() == self.getPosition():

                    self.remplace(grille_a_tester)
                    return
                else:

                    index_liste_indice += 1


if __name__ == "__main__":

    grille = Grille()

    """  grille.creerGrilleParIndex(
        [[1,5],[1,1,1,1,1],[2,2,1,1],[5,4],[2,2],[1],[2],[1,1,1],[1,1,2],[2,1,3]],
        [[2,1],[3,1,1],[1,2,4],[4],[1,2,1,1],[2,2],[1,2,1],[2,1,1],[1,2,1],[4,1,1]]
        ) """

    grille.creerGrilleHasard(5)

    grille.creerGrilleParIndex([[2], [1, 1], [4], [1], [1, 1]],
                               [[1], [1], [3, 1], [1, 1], [3]])

    print(grille.getPosition())

    avant = time.time()

    grille.resoudBackTracking()
    grille.afficher()
    print(f"{round(time.time()-avant, 5)} s")

    """ 
    #grille.resoud()
    print()
    #print(grille.getPosition())
    print()
    #grille.afficher()
    print()

     """
    for i in grille.grille.keys():
        for j in range(len(grille.grille[i])):

            a = grille._positionParLigne(grille.grille[i][j])
            b = grille.getPosition()[i][j]
            if a == b:
                continue
            print("________________________")
            print(f"indice actuel : {a}")
            print(f"indice voulu  : {b}")
            # print(a==b)
            print(i, j)
            print("________________________")
