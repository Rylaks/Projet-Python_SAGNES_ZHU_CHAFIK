from unit import *
from skills import *

class Mage(Unit,Skills):    #Mage: vitesse myenne, attaque elevée, boucliers et vie faibles
    """
    Type d'unité mage

    Paramètres
    ----------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    defense_shield : int
        Le bouclier de l'unité.
    speed : int
        Vitesse de l'unité.
    """
    def __init__(self,x ,y, team):
        Unit.__init__(self,x,y,team)
        self.health = 10
        self.attack_power = 8
        self.defense_shield = 3
        self.speed = 5
        if team == "player":
            self.nom = "Gandalf le Gris"
        elif team == "enemy":
            self.nom = "Saroumane le Blanc"
        else:
            raise TypeError ("La team doit être - player - ou - enemy - !")
    

class Voleur(Unit,Skills):    #Voleur: vitesse grande, attaque faible, boucliers et vie moyennes
    """
    Type d'unité voleur

    Paramètres
    ----------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    defense_shield : int
        Le bouclier de l'unité.
    speed : int
        Vitesse de l'unité.
    """
    def __init__(self,x ,y, team):
        Unit.__init__(self,x,y,team)
        self.health = 10
        self.attack_power = 5
        self.defense_shield = 7
        self.speed = 5
        if team == "player":
            self.nom = "Bilbon"
        elif team == "enemy":
            self.nom = "Gollum"
        else:
            raise TypeError ("La team doit être - player - ou - enemy - !")
    
class Guerrier(Unit,Skills):    #Guerrier: vitesse faible, attaque grandes, boucliers et vie importants
    """
    Type d'unité guerrier

    Paramètres
    ----------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    defense_shield : int
        Le bouclier de l'unité.
    speed : int
        Vitesse de l'unité.
    """
    def __init__(self,x ,y, team):
        Unit.__init__(self,x,y,team)
        self.health = 30
        self.attack_power = 10
        self.defense_shield = 10
        self.speed = 2
        if team == "player":
            self.nom = "Aragorn"
        elif team == "enemy":
            self.nom = "Le Roi-Sorcier d'Angmar"
        else:
            raise TypeError ("La team doit être - player - ou - enemy - !")