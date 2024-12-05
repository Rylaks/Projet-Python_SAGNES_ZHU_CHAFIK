from skills import *
from unit import *

from abc import ABC, abstractmethod

class Personnage(ABC):

    @abstractmethod
    def draw(self,screen):
        pass

class Mage(Unit,Skills):    #Mage: vitesse moyenne, attaque elevée, boucliers et vie faibles
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
    def __init__(self,x ,y, team,game):
        Unit.__init__(self,x,y,team,game)
        Skills.__init__(self)
        self.health = 10
        self.mana = 9 #commencera la partie avec 10 car en obtient 1 à chaque tour.
        self.attack_power = 8
        self.defense_shield = 3
        self.speed = 3
        self.original_speed = self.speed
        self.turns_in_water = 0  # 初始化在水中的回合数
        self.turns_in_bush = 0   # 初始化在灌木中的回合数
        if team == "player":
            self.nom = "Gandalf le Gris"
        elif team == "enemy":
            self.nom = "Saroumane le Blanc"
        else:
            raise TypeError ("La team doit être - player - ou - enemy - !")
        
    #Charger les images
    def draw(self,screen):
        if self.team == "player":
            image_path = "images/gandalf.png"
        elif self.team == "enemy":
            image_path = "images/Saroumane.png"

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        # Dessiner l'image correspondant à l'unité
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))
    

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
    def __init__(self,x ,y, team,game):
        Unit.__init__(self,x,y,team,game)
        Skills.__init__(self)
        self.health = 10
        self.attack_power = 5
        self.is_invisible = False
        self.defense_shield = 7
        self.speed = 5
        self.original_speed = self.speed
        self.turns_in_water = 0  # 初始化在水中的回合数
        self.turns_in_bush = 0   # 初始化在灌木中的回合数
        if team == "player":
            self.nom = "Bilbon"
        elif team == "enemy":
            self.nom = "Gollum"
        else:
            raise TypeError ("La team doit être - player - ou - enemy - !")
        
    #Charger les images
    def draw(self,screen):
        if self.team == "player":
            image_path = "images/Bilbon.png"
        elif self.team == "enemy":
            image_path = "images/gollum.png"

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        # Dessiner l'image correspondant à l'unité
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))

    
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
    def __init__(self,x ,y, team,game):
        Unit.__init__(self,x,y,team,game)
        Skills.__init__(self)
        self.health = 30
        self.attack_power = 10
        self.defense_shield = 10
        self.speed = 2
        self.original_speed = self.speed
        self.turns_in_water = 0  # 初始化在水中的回合数
        self.turns_in_bush = 0   # 初始化在灌木中的回合数
        if team == "player":
            self.nom = "Aragorn"
        elif team == "enemy":
            self.nom = "Le Roi-Sorcier d'Angmar"
        else:
            raise TypeError ("La team doit être - player - ou - enemy - !")
        
    # Charger les images
    def draw(self,screen):
        if self.team == "player":
            image_path = "images/aragorn.jpg"
        elif self.team == "enemy":
            image_path = "images/Angmar.png"

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        # Dessiner l'image correspondant à l'unité
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))