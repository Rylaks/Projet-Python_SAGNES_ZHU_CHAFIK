from skills import *
from unit import *

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
    def __init__(self,x ,y, team):
        Unit.__init__(self,x,y,team)
        self.health = 10
        self.mana = 3
        self.attack_power = 8
        self.defense_shield = 3
        self.speed = 3
        if team == "player":
            self.nom = "Gandalf le Gris"
        elif team == "enemy":
            self.nom = "Saroumane le Blanc"
        else:
            raise TypeError ("La team doit être - player - ou - enemy - !")
        
    image1 = pygame.image.load("images/gandalf.png")
    image1 = pygame.transform.scale(image1, (CELL_SIZE, CELL_SIZE))
    image2 = pygame.image.load("images/saroumane.png")
    image2 = pygame.transform.scale(image2, (CELL_SIZE, CELL_SIZE))
        
    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                            self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    

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
        self.set_invisible = False
        self.defense_shield = 7
        self.speed = 5
        if team == "player":
            self.nom = "Bilbon"
        elif team == "enemy":
            self.nom = "Gollum"
        else:
            raise TypeError ("La team doit être - player - ou - enemy - !")
        
    image1 = pygame.image.load("images/Bilbon.png")
    image1 = pygame.transform.scale(image1, (CELL_SIZE, CELL_SIZE))
    image2 = pygame.image.load("images/gollum.png")
    image2 = pygame.transform.scale(image2, (CELL_SIZE, CELL_SIZE))
        
    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                            self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                           2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
    
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
        
    image1 = pygame.image.load("images/aragorn.png")
    image1 = pygame.transform.scale(image1, (CELL_SIZE, CELL_SIZE))
    image2 = pygame.image.load("images/Angmar.png")
    image2 = pygame.transform.scale(image2, (CELL_SIZE, CELL_SIZE))
        
    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.is_selected:
            pygame.draw.rect(screen, GREEN, (self.x * CELL_SIZE,
                            self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.x * CELL_SIZE + CELL_SIZE //
                            2, self.y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)