import random   #probabilité de coup critique et de précision
from unit import *
from portee import Portee
    
class Skills:
    
    def __init__(self):
        self.critique = False
        self.miss = False
            
        # on defini ici la portee de chaque competence 
        
        self.portees = {
            "attack": Portee(1, 1),  # Portée d'une case
            "heal": Portee(3, 3),   # Portée de 3 cases
            "fire_ball": Portee(5, 5),  # Portée de 5 cases
            "bow": Portee(10, 10)   # Portée de 10 cases
             }
         
    #Pour tout le monde:
    def attack(self,target):
        """Attaque une unité cible au corps à corps."""
        
        if self.portees["attack"].est_dans_portee(self, target):
            
            if target.defense_shield >= self.attack_power:
                target.defense_shield -= self.attack_power
            else:
                target.health -= self.attack_power - target.defense_shield
                target.defense_shield = 0
        else :
            print("cible hors de portee ")
            
            
    #pour les mages:
    def heal(self,target):
        """Soigne les points de vie d'une unité alliée à portée, et utilise du mana"""
        
        if self.portees["heal"].est_dans_portee(self,target):
            p1 = random.random()
            p2 = random.random()
            if p1 < 0.2: #20% de chances de coup critique
                self.critique = True
            if p2 < 0.1: #10% de chances de rater
                self.miss = True
            if self.miss:
                print("Manqué !")
            elif not self.critique:
                if target.team == "player":
                    target.health += self.mana
                    self.mana = 0
                else:
                    raise TypeError ("Cette compétence ne peut être utiliser que sur des unités alliées")
            elif self.critique:
                if target.team == "player":
                    target.health += self.mana*2
                    self.mana = 0
                else:
                    raise TypeError ("Cette compétence ne peut être utiliser que sur des unités alliées")
                (print("Critique !"))
        else: 
            print("cible hors de portee")
            
            
            
            
    def fire_ball(self,target):
        """Attaque à distance qui explose sur une zone d'effet importante"""
        pass
    
    

    #pour les voleurs:
    def invisibility(self):
        """Porte l'anneau et se rend invisible (et donc intouchable) des unités ennemies pour un tour.
            Ne peut pas non plus se faire soigner par le mage !"""
        #coûte des points de bouclier (ça fatigue!), puis des points de vie quand le bouclier est à 0.
        self.is_invisible = True
        if self.defense_shield > 0:
            self.defense_shield -= 1
        else:
            self.health -= 1
            
            
    #pour les guerriers:       
    def bow(self,target):
        """Attaque (divisée par 2) à longue portée avec un arc"""
        
        if self.portees["bow"].est_dans_portee(self,target):
            p1 = random.random()
            p2 = random.random()
            if p1 < 0.2: #20% de chances de coup critique
                self.critique = True
            if p2 < 0.1: #10% de chances de rater
                self.miss = True
            if abs(self.x - target.x) <= 10 and abs(self.y - target.y) <= 10: #portée de 10 cases
                if self.miss:
                    print("Coup raté !")
                elif not self.critique :
                    if target.defense_shield >= round(self.attack_power*0.5):
                        target.defense_shield -= round(self.attack_power*0.5)
                    else:
                        target.health -= round((self.attack_power - target.defense_shield)*0.5)
                        target.defense_shield = 0
                elif self.critique:
                    if target.defense_shield >= self.attack_power:
                        target.defense_shield -= self.attack_power
                    else:
                        target.health -= (self.attack_power - target.defense_shield)
                        target.defense_shield = 0
                    print('Coup critique !')
        else:
            print("Cible hors de portee")
                