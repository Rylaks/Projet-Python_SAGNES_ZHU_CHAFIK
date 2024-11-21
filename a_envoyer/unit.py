import pygame
import random

# Constantes
GRID_SIZE = 8
CELL_SIZE = 60
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

from skills import *

class Unit(Skills):
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

    def __init__(self, x, y, team):
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

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.__x + dx < GRID_SIZE and 0 <= self.__y + dy < GRID_SIZE:
            self.__x += dx
            self.__y += dy

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        color = BLUE if self.team == 'player' else RED
        if self.__is_selected:
            pygame.draw.rect(screen, GREEN, (self.__x * CELL_SIZE,
                             self.__y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, color, (self.__x * CELL_SIZE + CELL_SIZE //
                           2, self.__y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        
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
            raise ValueError("is_selected must be a boolean")
        self.__is_selected = value
        