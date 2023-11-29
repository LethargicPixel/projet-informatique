from random import randint
class Case:
    
    def __init__(self, valeur=None):
        self._valeur=valeur

    def __str__(self):
        match self._valeur:
            case True :
                return "O"
            case False:
                return "X"
            case _:
                return " "


    def valeur(self):
        return self._valeur
    
    def transformeVrai(self):
        self._valeur=True
    
    def transformeFaux(self):
        self._valeur=False
        
a=Case(bool(randint(0,1)))
b=Case(bool(randint(0,1)))

c=[a,b]
print(c)