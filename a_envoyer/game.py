import pygame
import random

from unit import *
from personnages import *

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
        y_offset = 50
        x_offset = 490
        for unit in self.player_units:
            unit_info = f"{unit.nom}: PV={unit.health}, Bouclier={unit.defense_shield}"
            unit_surface = font.render(unit_info, True, white)
            self.screen.blit(unit_surface, (x_offset, y_offset))
            y_offset += 30

        # Afficher les informations des unités (ennemi)
        y_offset += 20  # Séparateur
        for unit in self.enemy_units:
            unit_info = f"{unit.nom} (Ennemi): PV={unit.health}"
            unit_surface = font.render(unit_info, True, white)
            self.screen.blit(unit_surface, (x_offset, y_offset))
            y_offset += 30

        # Instructions
        instructions = [
            "Déplacer: flèches",
            "Attaquer: espace",
            "Quitter: croix rouge",
        ]
        y_offset += 20
        for instruction in instructions:
            instruction_surface = font.render(instruction, True, white)
            self.screen.blit(instruction_surface, (x_offset, y_offset))
            y_offset += 30
        

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour

            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
            while not has_acted:

                # Important: cette boucle permet de gérer les événements Pygame
                for event in pygame.event.get():

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

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        # Attaque (touche espace) met fin au tour
                        if event.key == pygame.K_SPACE:
                            for enemy in self.enemy_units:
                                selected_unit.attack(enemy)

                            has_acted = True
                            selected_unit.is_selected = False

                        #Affiche l'HUD
                        

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
    screen = pygame.display.set_mode((900, 480))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()
