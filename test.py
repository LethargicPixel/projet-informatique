class MaClasse:
    def __init__(self, attribut1, attribut2):
        self.attribut1 = attribut1
        self.attribut2 = attribut2

    def __bool__(self):
        return True

# Création d'une instance de la classe
objet = MaClasse(attribut1="Valeur1", attribut2="Valeur2")

# Affichage en imprimant l'objet (la classe)
print(objet)