#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: sayf
"""
""" Implementation de la porteee des competences: diff´erentes comp´etences peuvent avoir
des port´ees diff´erentes. La cible de la comp´etence doit se trouver `a port´ee de l’unit´e qui
utilise la comp´etence.


# on fixe une portee pour chaque competence 

on fais la liste des competences  



Competence 1: attack : Attaque une unité cible au corps à corps.

Competence 2: heal : Soigne les points de vie d'une unité alliée à portée, ( soigne toute une zone precise)

competence 3 : fireball : Attaque à distance qui explose sur une zone d'effet importante

competence 4: bow : attaque de longue portée avec arc 

 """



from unit import *


class Portee: 
    
    
    def __init__(self,x_range,y_range):
        """ on initialise la portee en fonction des distance autorisée """ 
        self.x_range=x_range
        self.y_range=y_range 
        
   
          
# on veut utiliser la competence sur un endroit et toutes les cibles alentours seront atteinte 