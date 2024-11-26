import pygame
import random

from unit import *
from personnages import *
from skills import *
from pointeur import *

from diff_case import Bush, Rock,Water,Terrain

class GameBoard:
    def __init__(self, size):
        self.size = size
        self.grid = [[Terrain() for _ in range(size)] for _ in range(size)]
        
        # 随机设置草丛地形
        num_bushes = random.randint(1, 5)  # 假设有1到5个草丛
        for _ in range(num_bushes):
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            self.grid[x][y] = Bush()


        # 随机设置岩石地形
        num_rocks = random.randint(1, 5)  # 假设有1到5个岩石
        for _ in range(num_rocks):
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            self.grid[x][y] = Rock()



        # 随机设置水地形
        num_waters = random.randint(1, 5)  # 假设有1到5个水地形
        for _ in range(num_waters):
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            self.grid[x][y] = Water()

class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    player_units : list[Unit]
        La liste des unités du joueur.
    enemy_units : list[Unit]
        La liste des unités de l'adversaire.
    """

    def __init__(self, screen,board_size):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.board = GameBoard(board_size)
        self.player_units = [Mage(0, 0, 'player'),
                             Voleur(1, 0, 'player'),
                             Guerrier(0, 1, 'player')]

        self.enemy_units = [Mage(7, 7, 'enemy'), 
                            Voleur(7, 6, 'enemy'),
                            Guerrier(6, 7, 'enemy')]
        
        self.point = Pointer(0,0)
        self.point_aff = False
        
        
    def draw_hud(self):
        """Affiche les informations du HUD."""

        # Couleur et police pour le texte
        font = pygame.font.Font(None, 25)
        white = (255, 255, 255)

        # Afficher les informations des unités (joueur)
        y_offset = 300
        x_offset = CELL_SIZE * GRID_SIZE + 100
        unit_info = f"Statistiques:"
        unit_surface = font.render(unit_info, True, white)
        self.screen.blit(unit_surface, (x_offset, y_offset))
        y_offset += 20
        for unit in self.player_units:
            unit_info = f" - {unit.nom}: PV = {unit.health}, Bouclier = {unit.defense_shield}"
            unit_surface = font.render(unit_info, True, white)
            self.screen.blit(unit_surface, (x_offset, y_offset))
            y_offset += 20

        # Afficher les informations des unités (ennemi)
        y_offset += 20  # Séparateur
        for unit in self.enemy_units:
            unit_info = f" - {unit.nom} (Ennemi): PV = {unit.health}, Bouclier = {unit.defense_shield}"
            unit_surface = font.render(unit_info, True, white)
            self.screen.blit(unit_surface, (x_offset, y_offset))
            y_offset += 20
        

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:

                # Affichage du joueur
                # Police et position pour le texte
                font = pygame.font.Font(None, 40)
                white = (255, 255, 255)
                y_offset = 10
                x_offset = CELL_SIZE * GRID_SIZE + 100
                unit_status = f"C'est à {selected_unit.nom} de jouer !"
                unit_surface = font.render(unit_status, True, white)
                self.screen.blit(unit_surface, (x_offset, y_offset))
                # Mettre à jour l'affichage
                pygame.display.flip()

                # Si l'unité est un mage, il récupère 1 point de mana par tour
                if isinstance(selected_unit,Mage):
                    selected_unit.mana += 1

                    font = pygame.font.Font(None, 40)
                    white = (255, 255, 255)
                    y_offset = 100
                    x_offset = CELL_SIZE * GRID_SIZE + 50
                    unit_status = ["Déplacement avec les touches du clavier",
                                    "",
                                    " - Attaquer au corps à corps: tapez 1",
                                    " - Soigner: tapez 2", #afficher le nombre de mana
                                    " - Ne rien faire: tapez 3"]
                    for unit_status in unit_status:
                        unit_surface = font.render(unit_status, True, white)
                        self.screen.blit(unit_surface, (x_offset, y_offset))
                        y_offset += 30
                
                # Si l'unité est un voleur
                elif isinstance(selected_unit,Voleur):
                    selected_unit.is_invisble = False
                    font = pygame.font.Font(None, 40)
                    white = (255, 255, 255)
                    y_offset = 100
                    x_offset = CELL_SIZE * GRID_SIZE + 50
                    unit_status = ["Déplacement avec les touches du clavier",
                                    "",
                                    "Compétences:",
                                    " - Attaquer au corps à corps: tapez 1",
                                    " - Se rendre invisible: tapez 2",
                                    " - Ne rien faire: tapez 3"]
                    for unit_status in unit_status:
                        unit_surface = font.render(unit_status, True, white)
                        self.screen.blit(unit_surface, (x_offset, y_offset))
                        y_offset += 30

                elif isinstance(selected_unit,Guerrier):
                    font = pygame.font.Font(None, 40)
                    white = (255, 255, 255)
                    y_offset = 100
                    x_offset = CELL_SIZE * GRID_SIZE + 50
                    unit_status = ["Déplacement avec les touches du clavier",
                                    "",
                                    "Compétences:",
                                    " - Attaquer au corps à corps: tapez 1",
                                    " - Tirez à l'arc: tapez 2",
                                    " - Ne rien faire: tapez 3"]
                    for unit_status in unit_status:
                        unit_surface = font.render(unit_status, True, white)
                        self.screen.blit(unit_surface, (x_offset, y_offset))
                        y_offset += 30
                
                # Mettre à jour l'affichage
                pygame.display.flip()

                for event in pygame.event.get():
                    attack = False
                    special_skill = False
                    no_action = False

                    # Gestion de la fermeture de la fenêtre
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    # Gestion des touches du clavier
                    if event.type == pygame.KEYDOWN:

                        # Déplacement (touches fléchées)
                        dx, dy = 0, 0
                        if event.key == pygame.K_LEFT:
                            dx = -1
                        elif event.key == pygame.K_RIGHT:
                            dx = 1
                        elif event.key == pygame.K_UP:
                            dy = -1
                        elif event.key == pygame.K_DOWN:
                            dy = 1
                        elif event.key == pygame.K_1:
                            attack = True
                        elif event.key == pygame.K_2:
                            special_skill = True
                        elif event.key == pygame.K_3:
                            no_action = True

                        selected_unit.move(dx, dy)
                        self.flip_display()

                    #Sélection d'une cible
                    if special_skill and not isinstance(selected_unit,Voleur):
                        self.point_aff = True
                        choose = False
                        self.point.x, self.point.y = selected_unit.x, selected_unit.y  # Centrez le pointeur sur l'unité
                        self.flip_display() #affichage du pointeur
                        target = None
                        while not choose and target is None:
                            for event in pygame.event.get():

                                if event.type == pygame.KEYDOWN:
                                    dx, dy = 0, 0
                                    if event.key == pygame.K_LEFT:
                                        dx = -1
                                    elif event.key == pygame.K_RIGHT:
                                        dx = 1
                                    elif event.key == pygame.K_UP:
                                        dy = -1
                                    elif event.key == pygame.K_DOWN:
                                        dy = 1
                                    elif event.key == pygame.K_SPACE:
                                        choose = True  # Valide la cible

                                    # Déplace le pointeur
                                    self.point.move(dx, dy)
                                    self.flip_display()

                        self.point_aff = False

                        for enemy in self.enemy_units:
                            for unit in self.player_units:
                                if (enemy.x == self.point.x and enemy.y == self.point.y):
                                    target = enemy
                                    break  # Trouvé la cible
                                if (unit.x == self.point.x and unit.y == self.point.y):
                                    target = unit
                                    break  # Trouvé la cible

                        if target is None:
                            # Affiche un message d'erreur si aucune cible n'est trouvée
                            font = pygame.font.Font(None, 40)
                            red = (255, 0, 0)
                            error_msg = "Aucune cible valide à cet endroit !"
                            error_surface = font.render(error_msg, True, red)
                            self.screen.blit(error_surface, (CELL_SIZE * GRID_SIZE + 100, 100))
                            pygame.display.flip()
                            pygame.time.wait(1000)  # Pause pour que le joueur voie le message

                            if isinstance(target,Voleur): # Vérification si la cible n'est pas invisible
                                if target.set_invisible:
                                    font = pygame.font.Font(None, 40)
                                    red = (255, 0, 0)
                                    error_msg = "Cette unité porte l'anneau et est invisible ! Impossible !"
                                    error_surface = font.render(error_msg, True, red)
                                    self.screen.blit(error_surface, (CELL_SIZE * GRID_SIZE + 100, 100))
                                    pygame.display.flip()
                                    pygame.time.wait(1000)  # Pause pour que le joueur voie le message

                                    target = None
                        
                    if attack:
                        for enemy in self.enemy_units:
                            selected_unit.attack(enemy)
                        has_acted = True
                        selected_unit.is_selected = False
                        
                    if special_skill:
                        if isinstance(selected_unit,Voleur):
                            selected_unit.invisibility()
                        if isinstance(selected_unit,Guerrier):
                            selected_unit.bow(target)
                        if isinstance(selected_unit,Mage):
                            selected_unit.heal(target,5) #à coder: pouvoir choisir la valeur
                        has_acted = True
                        selected_unit.is_selected = False

                    if no_action:
                        has_acted = True
                        selected_unit.is_selected = False

                    for enemy in self.enemy_units:
                        if enemy.health <= 0:
                            self.enemy_units.remove(enemy)

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:

            # Déplacement aléatoire
            target = random.choice(self.player_units)
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            enemy.move(dx, dy)

            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health <= 0:
                    self.player_units.remove(target)


    def flip_display(self):
        """Affiche le jeu et le HUD."""

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.player_units + self.enemy_units:
            unit.draw(self.screen)

        # Affiche le pointeur
        if self.point_aff:
            pygame.draw.rect(self.screen, GREEN, (self.point.x * CELL_SIZE,
                            self.point.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),width=5)
            font = pygame.font.Font(None, 30)
            red = (255, 0, 0)
            info = "Choisir une cible avec les touches directionnelles"
            info_surface = font.render(info, True, WHITE)
            self.screen.blit(info_surface, (CELL_SIZE * GRID_SIZE + 100, 10))
            pygame.display.flip()

        # Affiche le HUD
        self.draw_hud()

        # Afficher la victoire (à coder, ça ne marche pas)
        if len(self.enemy_units) == 0:
            font = pygame.font.Font(None, 40)
            white = (255, 255, 255)
            y_offset = CELL_SIZE * GRID_SIZE + 100
            x_offset = CELL_SIZE * GRID_SIZE + 100
            unit_status = f"Bravo ! La Communauté de l'anneau a vaincu Sauron !"
            unit_surface = font.render(unit_status, True, white)
            self.screen.blit(unit_surface, (x_offset, y_offset))

        # Rafraîchit l'écran
        pygame.display.flip()

    




def main():

    # Initialisation de Pygame
    pygame.init()

    #Initialisation de la musique
    pygame.mixer.init()
    pygame.mixer.music.load("music\The_Bridge_of_Khazad_Dum.mp3")
    pygame.mixer.music.play(-1)  # Joue en boucle infinie

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((1300, 800))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Écran titre
    image = pygame.image.load("images\conte.jpg")
    # Initialiser une police pour le texte
    font = pygame.font.Font(None, 50)  # Police par défaut, taille 50
    text = font.render("Appuyez sur SPACE pour lancer le jeu", True, BLACK)  # Texte blanc

    # Obtenir la position centrale de l'image
    image_rect = image.get_rect(center=(700, 500))  # Centré à (400, 300)

    # Positionner le texte (centré sur l'image)
    text_rect = text.get_rect(center=(950,100))

    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = False

        # Remplir l'écran avec une couleur unie (optionnel)
        screen.fill((0, 0, 0))  # Fond noir

        # Dessiner l'image sur l'écran
        screen.blit(image, image_rect)

        # Dessiner le texte sur l'écran
        screen.blit(text, text_rect)

        # Mettre à jour l'affichage
        pygame.display.flip()

    # Quitter Pygame proprement
    pygame.mixer.music.stop()
    pygame.quit()

    # Initialisation de Pygame
    screen = pygame.display.set_mode((1300, 700))
    pygame.display.set_caption("Mon jeu de stratégie")
    pygame.init()
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
