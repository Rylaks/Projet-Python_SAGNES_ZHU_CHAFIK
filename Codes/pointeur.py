from skills import *
from unit import *

class Pointeur(Skills):
    """Classe pour représenter le pointeur."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        #chaque compétence à une portée différente:
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy