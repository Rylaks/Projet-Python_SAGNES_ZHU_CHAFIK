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
        self.x = x
        self.y = y
        self.team = team #'player' ou 'enemy'
        self.__is_selected = False
        self.game = game # 引用游戏实例以访问其他游戏元素
        self.green_cases = []
        
    
  
    def move(self, dx, dy):
        dx = int(dx)
        dy = int(dy)
        
        new_x = int(self.x + dx)
        new_y = int(self.y + dy)
        
         # 检查是否在允许的移动范围内
        if (new_x, new_y) not in self.green_cases:
            print(f"Movement to ({new_x}, {new_y}) is out of allowed range.")
            return  # 如果不在允许的范围内，不进行移动
        
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            
            # mise a jour le type de terrain
            old_terrain = self.game.board.grid[self.y][self.x]
            new_terrain = self.game.board.grid[new_y][new_x]

            # 检查地形是否允许移动
            can_move = new_terrain.apply_effect(self)
            print(f"Trying to move to ({new_x}, {new_y}) - Move allowed: {can_move}")

            # Check if the terrain allows movement
            if can_move: # Mise à jour de la position si le mouvement est autorisé
                old_terrain.remove_effect(self)
                self.x = new_x
                self.y = new_y
                print("Unit moved to:", new_x, new_y)
            else:
                print("Movement blocked by terrain at:", new_x, new_y)

    def update_move_range(self):
        self.green_cases = [] # 清空旧的移动范围
        
        start_x, start_y = self.x, self.y  # 获取当前单位的位置
        speed = int(self.speed)
        print(f"Speed: {speed}, Position: ({self.x}, {self.y})")  # 打印速度和位置
        
        # 包括单位当前所在格子
        self.green_cases.append((start_x, start_y))
        
        # 遍历以单位为中心的正方形区域
        for dy in range(-speed, speed + 1):
            for dx in range(-speed, speed + 1):
                green_x = start_x + dx
                green_y = start_y + dy
                
                # 确保格子在边界内
                if 0 <= green_x < GRID_SIZE and 0 <= green_y < GRID_SIZE:
                    # 检查格子是否被占用
                    if not self.game.is_occupied(green_x, green_y):
                        
                        terrain = self.game.board.grid[green_y][green_x]
                        
                        if terrain.apply_effect(self):
                            self.green_cases.append((green_x, green_y))
        
        print(f"{self.nom}'s move range updated: {self.green_cases}")
     
     
    def draw_move_range(self, screen):
        for green_x, green_y in self.green_cases:
            # 用绿色高亮显示可以移动到的格子
            pygame.draw.rect(screen, GREEN, (green_x * CELL_SIZE, green_y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)    
         
                                    
    
            
    @property
    def is_selected(self):
        return self.__is_selected

    @is_selected.setter
    def is_selected(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_selected doit être un booléen")
        self.__is_selected = value
        