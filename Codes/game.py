import pygame
import random

from unit import *
from personnages import *
from skills import *

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

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.player_units = [Mage(0, 0, 'player'),
                             Voleur(1, 0, 'player'),
                             Guerrier(0, 1, 'player')]

        self.enemy_units = [Mage(7, 7, 'enemy'), 
                            Voleur(7, 6, 'enemy'),
                            Guerrier(6, 7, 'enemy')]
        
        
    def draw_hud(self):
        """Affiche les informations du HUD."""

        # Couleur et police pour le texte
        font = pygame.font.Font(None, 25)
        white = (255, 255, 255)

        # Afficher les informations des unités (joueur)
        y_offset = 300
        x_offset = 490
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
                x_offset = 600
                unit_status = f"C'est à {selected_unit.nom} de jouer !"
                unit_surface = font.render(unit_status, True, white)
                self.screen.blit(unit_surface, (x_offset, y_offset))
                # Mettre à jour l'affichage
                pygame.display.flip()

                # Si l'unité est un mage, il récupère 1 point de mana par tour et peut jouer une compétence
                if isinstance(selected_unit,Mage):
                    selected_unit.mana += 1

                    font = pygame.font.Font(None, 40)
                    white = (255, 255, 255)
                    y_offset = 100
                    x_offset = 500
                    unit_status = ["Déplacement avec les touches du clavier",
                                    "",
                                    " - Attaquer au corps à corps: tapez 1",
                                    " - Soigner: tapez 2",
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
                    x_offset = 500
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
                    x_offset = 500
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

                    
                    if attack:
                    #Sélection d'une cible (à coder)

                        # Important: cette boucle permet de gérer les événements Pygame
                        if isinstance(target,Voleur): #Vérification si la cible n'est pas invisible
                            while target.is_invisible:
                                font = pygame.font.Font(None, 40)
                                white = (255, 255, 255)
                                y_offset = 10
                                x_offset = 600
                                unit_status = f"Impossible ! Cette unité est invisible !"
                                unit_surface = font.render(unit_status, True, white)
                                self.screen.blit(unit_surface, (x_offset, y_offset))
                                # Mettre à jour l'affichage
                                pygame.display.flip()

                        has_acted = True
                        selected_unit.is_selected = False
                        
                    if special_skill:
                        has_acted = True
                        selected_unit.is_selected = False

                    if no_action:
                        has_acted = True
                        selected_unit.is_selected = False

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

        # Affiche le HUD
        self.draw_hud()

        # Rafraîchit l'écran
        pygame.display.flip()



def main():

    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((1100, 480))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
