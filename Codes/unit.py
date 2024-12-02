
import pygame
import random

# Constantes
GRID_SIZE = 10
CELL_SIZE = 80
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Unit:
    """
    Classe pour représenter une unité et la déplacer.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, team,game):
        """
        Construit un unité avec une position, et une team.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        team : str
            L'équipe de l'unité ('player' ou 'enemy').
        """
        self.__x = x
        self.__y = y
        self.team = team #'player' ou 'enemy'
        self.__is_selected = False
        self.game = game # 引用游戏实例以访问其他游戏元素

    def move(self, dx, dy):
        dx = int(dx)
        dy = int(dy)
        
        new_x = int(self.__x + dx)
        new_y = int(self.__y + dy)
        
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            # mise a jour le type de terrain
            old_terrain = self.game.board.grid[self.__y][self.__x]
            new_terrain = self.game.board.grid[new_y][new_x]

            # 检查地形是否允许移动
            can_move = new_terrain.apply_effect(self)
            print(f"Trying to move to ({new_x}, {new_y}) - Move allowed: {can_move}")

            # Check if the terrain allows movement
            if can_move: # Mise à jour de la position si le mouvement est autorisé
                old_terrain.remove_effect(self)
                self.__x = new_x
                self.__y = new_y
                print("Unit moved to:", new_x, new_y)
            else:
                print("Movement blocked by terrain at:", new_x, new_y)

            
    
    
    
    
    @property
    def x(self):
        return self.__x
    
    @property
    def y(self):
        return self.__y
        
    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_selected doit être un booléen")
        self.__is_selected = value
        
