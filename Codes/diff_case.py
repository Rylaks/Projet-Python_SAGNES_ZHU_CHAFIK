"""

- Grass terrain ce terrain est visible, on peut savoir quelle grille est de l'herbe, ce que je veux implémenter c'est deux effets pour la grille d'herbe : 1. quand un personnage passe à travers cette grille : le personnage devient invisible et double sa vitesse ; 2. quand un personnage reste finalement dans cette grille, il ne devient pas invisible, le personnage est montré mais s'il reste plus de 2 rounds ou plus, sa valeur de vie sera +. 10.人物经过这个格子的时候：人物会变得不可见，并且速度会增加一倍；2. 人物最后停留在这个格子的时候，并不会隐身，会显示这个人物，但如果他停留超过2回合以上，生命值会+10

- 1.un terrain rocailleux génère des rochers sur une case, alors tous les personnages sauf Guerrier ne peuvent pas traverser cette case, donc si le personnage avance de 4 cases, mais que la case 2 est rocailleuse, le personnage ne peut faire qu'un pas et s'arrêter sur la case avant la case rocailleuse. 2. pour Guerrier, il peut soit ignorer les rochers, soit les écraser, donc si le personnage est maintenant Guerrier, et qu'il veut avancer de 4 cases, il ne peut faire qu'un pas et s'arrêter sur la case avant la case rocailleuse. 3. pour Guerrier, il peut ignorer les rochers, soit les écraser. Si le personnage est un Guerrier et qu'il veut avancer de 4 cases, mais que la deuxième case est rocheuse, il peut détruire le rocher sur cette case, de sorte que cette case ne soit plus rocheuse, et il peut alors avancer de 4 cases comme d'habitude.. 对于Guerrier，他可以无视岩石，或者说他可以撞碎岩石，假如说人物现在是Guerrier，要前进四格，但第2格是岩石，他就可以毁掉这个格子的岩石，就这个格子不再是岩石了，然后他照样可以前进4格

- Eau : le personnage sera ralenti de trente pour cent lors de son passage ; s'il reste sur cette grille pendant plus de deux tours, il perdra 10 points de sang.
"""

class Terrain:
    def __init__(self):
        self.visible = True  # 是否影响单位可见性

    def apply_effect(self, unit):
        """Appliquer l'effet du terrain à l'unité, implémenté dans les sous-classes"""
        pass

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
        self.image = pygame.image.load("images/bush.png")  # Charge l'image du buisson
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))# assurer qu l'image est le bon size

    def apply_effect(self, unit):
        """Méthode appelée lorsque l'unité traverse un buisson"""
        unit.invisible = True  # Rend l'unité invisible
        unit.speed *= 2  # Double la vitesse de l'unité
        unit.turns_in_bush = 0  # Initialise le nombre de tours dans le buisson

    def stay_effect(self, unit):
        """Effet appliqué lorsque l'unité reste dans le buisson"""
        unit.turns_in_bush += 1  # Incrémente le nombre de tours dans le buisson
        unit.invisible = False  # Devient visible en restant
        if unit.turns_in_bush > 2:
            unit.health += 10  # Si plus de deux tours, augmente la santé

    def remove_effect(self, unit):
        """Méthode appelée lorsque l'unité quitte le buisson"""
        unit.invisible = False  # Rend l'unité visible
        unit.speed /= 2  # Restaure la vitesse originale
        unit.turns_in_bush = 0  # Réinitialise le nombre de tours dans le buisson

class Rock(Terrain):
    def __init__(self):
        super().__init__()
        self.passable = False  # Par défaut, le rocher est infranchissable
        self.image = pygame.image.load("images/rock.png")  # Charge l'image du rocher
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
        self.image = pygame.image.load("images/water.png")  # Charge l'image de l'eau
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))# assurer qu l'image est le bon size

    def apply_effect(self, unit):
        """Méthode appelée lorsque l'unité traverse de l'eau"""
        unit.speed *= 0.7  # Réduit la vitesse de 30%
        unit.turns_in_water = 0  # Initialise le nombre de tours dans l'eau

    def stay_effect(self, unit):
        """Effet appliqué lorsque l'unité reste dans l'eau"""
        unit.turns_in_water += 1  # Incrémente le nombre de tours dans l'eau
        if unit.turns_in_water > 2:
            unit.health -= 10  # Si plus de deux tours, réduit la santé de 10

    def remove_effect(self, unit):
        """Méthode appelée lorsque l'unité quitte l'eau"""
        unit.speed /= 0.7  # Restaure la vitesse originale
        unit.turns_in_water = 0  # Réinitialise le nombre de tours dans l'eau
