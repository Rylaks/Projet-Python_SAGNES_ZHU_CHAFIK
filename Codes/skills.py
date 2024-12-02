import random   #probabilité de coup critique et de précision
from unit import *
from portee import Portee
    
class Skills:
    
        def __init__(self):
            self.critique = False
            self.miss = False
            
        # on defini ici la portee de chaque competence 
        
            self.portees = {
                 "attack": (1, 1),  # Portée d'une case
                 "heal": (3, 3),   # Portée de 3 cases
                 "fire_ball": (5, 5),  # Portée de 5 cases
                 "bow": (10, 10)   # Portée de 10 cases
             }
        
        def est_dans_portee(self,selected_unit,competence,target):
            """ verifie si la cible est dans la portee 
            Return True si la cible est dans la portee et False sinon""" 
        
            return (abs(selected_unit.x - target.x) <=self.portees[competence][0]  and abs(selected_unit.y - target.y) <= self.portees[competence][1])


        def obtenir_cibles_dans_portee(self,selected_unit, competence):   
            
            """retourne une liste de cible(aliées ou ennemies) dans la portée pour une competence 
          
            """
            
            cibles_dans_portee=[]
            portee=self.portees[competence]
            
            # on verfie si la team de la cible est differente de la team de la source 
           
            # Déterminer si la source est un allié ou un ennemi
            if selected_unit in self.player_units:
                allies = self.player_units
                enemies = self.enemy_units
            elif selected_unit in self.enemy_units:
                allies = self.enemy_units
                enemies = self.player_units
            else:
                raise ValueError("L'unité source ne fait partie d'aucune équipe valide.")
            
            # Identifier les cibles dans la portée en fonction de la compétence
            if competence == "heal":
                # Pour heal, on cible uniquement les alliés
                for cible in allies:
                    if portee.est_dans_portee(selected_unit,"heal", cible):
                        cibles_dans_portee.append(cible)
            elif competence in ["attack", "fireball"]:
                # Pour attack ou fireball, on cible uniquement les ennemis
                for cible in enemies:
                    if portee.est_dans_portee(selected_unit,competence, cible):
                        cibles_dans_portee.append(cible)
          
            return cibles_dans_portee
        
               
     
    
        #Pour tout le monde:
        def attack(self,target):
            """Attaque une unité cible au corps à corps."""
            
            if self.est_dans_portee(self,"attack", target):
                
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
            
            if self.est_dans_portee(self,"heal",target):
                if self.team =="player" :   #ici on veut agir seulement sur les allié 
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
                elif (self.team =="enemy") : 
                    print("ennemi ne peut etre soigné")
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
            
            if self.est_dans_portee(self,"bow",target):
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
                