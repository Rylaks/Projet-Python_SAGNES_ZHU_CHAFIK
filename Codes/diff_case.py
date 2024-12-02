

import os
import pygame
from unit import CELL_SIZE
from personnages import Guerrier


class Terrain:
    def __init__(self):
        self.visible = True  # visibilité
        
         # Définit une image par défaut pour Terrain
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))  # Crée une surface de base
        self.image.fill((100, 100, 100))  # Colore la surface en gris par défaut

    def stay_effect(self, unit):
        """Appliquer l'effet du terrain à l'unité, implémenté dans les sous-classes"""
        pass
    
    def apply_effect(self, unit):
        """Appliquer l'effet du terrain à l'unité, implémenté dans les sous-classes"""
        return True

    def remove_effect(self, unit):
        """Retirer l'effet du terrain sur l'unité, s'il y a un effet persistant"""
        pass

    def draw(self, screen, x, y):
        """Dessine le terrain sur la grille."""
        screen.blit(self.image, (x * CELL_SIZE, y * CELL_SIZE))

class Bush(Terrain):
    def __init__(self):
        super().__init__()
        self.visible = True  # Le buisson est visible
        
        project_root = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(project_root, "images", "bush.png")
        
        self.image = pygame.image.load(image_path)  # Charge l'image du buisson
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))# assurer qu l'image est le bon size

    def apply_effect(self, unit):
        """Méthode appelée lorsque l'unité traverse un buisson"""
        unit.invisible = True  # Rend l'unité invisible
        unit.speed = int(unit.speed *2)  # Double la vitesse de l'unité
        unit.turns_in_bush = 0  # Initialise le nombre de tours dans le buisson
        return True
    
    def stay_effect(self, unit):
        """Effet appliqué lorsque l'unité reste dans le buisson"""
        unit.turns_in_bush += 1  # Incrémente le nombre de tours dans le buisson
        unit.invisible = False  # Devient visible en restant
        if unit.turns_in_bush > 2:
            unit.health += 1  # Si plus de deux tours, augmente la santé

    def remove_effect(self, unit):
        """Méthode appelée lorsque l'unité quitte le buisson"""
        unit.invisible = False  # Rend l'unité visible
        unit.speed /= 2  # Restaure la vitesse originale
        unit.turns_in_bush = 0  # Réinitialise le nombre de tours dans le buisson

class Rock(Terrain):
    def __init__(self):
        super().__init__()
        self.passable = False  # Par défaut, le rocher est infranchissable
        
        # 动态构造图片路径
        project_root = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(project_root, "images", "rock.png")
        
        self.image = pygame.image.load(image_path)  # Charge l'image du rocher
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))# assurer qu l'image est le bon size


    def apply_effect(self, unit):
        """Gère la logique lorsque l'unité tente d'entrer dans une case rocheuse"""
        if isinstance(unit, Guerrier):
            self.passable = True  # Le Guerrier peut détruire le rocher pour le rendre franchissable
            return True  # Permet au Guerrier de continuer son mouvement
        return False  # Les autres unités ne peuvent pas traverser le rocher

    def remove_effect(self, unit):
        """Logique lorsqu'une unité quitte une case rocheuse"""
        # Ajouter une logique supplémentaire ici si nécessaire
        pass

class Water(Terrain):
    def __init__(self):
        super().__init__()
        self.visible = True  # L'eau est visible
        
        # 动态构造图片路径
        project_root = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(project_root, "images", "water.png")
        
        self.image = pygame.image.load(image_path)  # Charge l'image de l'eau
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))# assurer qu l'image est le bon size

    def apply_effect(self, unit):
        """Méthode appelée lorsque l'unité traverse de l'eau"""
        unit.speed *= max(1, int(unit.speed * 0.7))  # 最小速度为 1，避免速度归零, Réduit la vitesse de 30%
        unit.turns_in_water = 0  # Initialise le nombre de tours dans l'eau
        return True
    
    def stay_effect(self, unit):
        """Effet appliqué lorsque l'unité reste dans l'eau"""
        unit.turns_in_water += 1  # Incrémente le nombre de tours dans l'eau
        if unit.turns_in_water > 2:
            unit.health -= 1  # Si plus de deux tours, réduit la santé de 10

    def remove_effect(self, unit):
        """Méthode appelée lorsque l'unité quitte l'eau"""
        unit.speed /= 0.7  # Restaure la vitesse originale
        unit.turns_in_water = 0  # Réinitialise le nombre de tours dans l'eau
