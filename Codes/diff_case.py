import os
import pygame
from unit import *
from personnages import*


class Terrain():
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
     
        if not hasattr(unit, 'original_speed'):
            unit.original_speed = unit.speed  # 存储原始速度
        
        unit.invisible = True  # 隐身
        
        unit.speed = unit.original_speed * 2  # 双倍速度
       
        return True
    
    def stay_effect(self,unit):
        
        unit.health +=1
        
    
    def remove_effect(self, unit):
        print(f"Before remove: {unit.speed}")
        """Méthode appelée lorsque l'unité quitte le buisson"""
        if hasattr(unit, 'original_speed'):
            unit.speed = unit.original_speed  # 恢复原始速度
        unit.invisible = False
        unit.turns_in_bush = 0
        print(f"After remove: {unit.speed}")
        
        
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
            self.passable = True  # Le Guerrier peut passer le rock
            return True  # Permet au Guerrier de continuer son mouvement
        return False  # Les autres unités ne peuvent pas traverser le rocher

    def remove_effect(self, unit):
        """Logique lorsqu'une unité quitte une case rocheuse"""
        
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
        if not hasattr(unit, 'original_speed'):
            unit.original_speed = unit.speed  # 存储原始速度
        unit.speed = max(1, int(unit.original_speed * 0.5))  # 减速到原来的 50%
        
        if isinstance(unit, Mage):
            self.passable = True  # Le Mage peut passer le water 
            return True  # Permet au Guerrier de continuer son mouvement
        return False  # Les autres unités ne peuvent pas traverser le rocher
      
    
    
    def remove_effect(self, unit):
        """Méthode appelée lorsque l'unité quitte l'eau"""
        if hasattr(unit, 'original_speed'):
            unit.speed = unit.original_speed  # 恢复原始速度
      
      
class HealthPack(Terrain):
    def __init__(self):
        super().__init__()
        self.visible = True  # 血包是可见的
        
        # 动态构造图片路径
        project_root = os.path.dirname(os.path.dirname(__file__))
        image_path = os.path.join(project_root, "images", "health_pack.png")
        
        # 加载图片
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))  # 确保大小正确

    def apply_effect(self, unit):
        """
        当单位踩上去时，恢复单位的生命值，并将格子变成普通地形。
        """
        if hasattr(unit, 'health') and hasattr(unit, 'max_health'):
            if unit.health < unit.max_health:  # 只有在生命值未满时才加血
                unit.health = min(unit.health + 1, unit.max_health) 
                print(f"{unit} has healed 1 HP!")
        
        # 告诉单位切换当前格子
        unit.replace_current_terrain(Terrain())

        return True  # 允许单位继续移动
