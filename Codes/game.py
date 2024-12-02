import random
import pygame 


from unit import GRID_SIZE , CELL_SIZE, WHITE, RED, BLACK, WIDTH, HEIGHT, GREEN 
from unit import *
from personnages import *
from skills import * 
from skills import Skills
from pointeur import *

from diff_case import Bush, Rock,Water,Terrain

class GameBoard:
    def __init__(self, size):
        self.size = size
        self.grid = [[Terrain() for _ in range(size)] for _ in range(size)]
        
        # Terrain herbeux aléatoire
        num_bushes = random.randint(1, 5)  # En supposant qu'il y ait un à cinq buissons
        for _ in range(num_bushes):
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            self.grid[x][y] = Bush()


        # Définir aléatoirement un terrain rocailleux
        num_rocks = random.randint(1, 5)  # En supposant qu'il y ait un à cinq rochers
        for _ in range(num_rocks):
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            self.grid[x][y] = Rock()



        # Terrain d'eau aléatoire
        num_waters = random.randint(1, 5)  # Dans l'hypothèse d'un terrain d'eau de 1 à 5
        for _ in range(num_waters):
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
            self.grid[x][y] = Water()


    def draw(self,screen):
        for y in range(self.size):
            for x in range(self.size):
                self.grid[y][x].draw(screen,x,y) # Dessine chaque case

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
        self.board = GameBoard(GRID_SIZE)
        self.player_units = [Mage(0, 0, 'player'),
                             Voleur(2, 0, 'player'),
                             Guerrier(0, 2, 'player')]

        self.enemy_units = [Mage(GRID_SIZE - 1, GRID_SIZE - 1, 'enemy'), 
                            Voleur(GRID_SIZE - 1, GRID_SIZE - 3, 'enemy'),
                            Guerrier(GRID_SIZE - 3, GRID_SIZE - 1, 'enemy')]
        
        self.point = Pointeur(0,0)
        self.point_aff = False
        
        
    def draw_hud(self):
        """Affiche les informations du HUD."""

        # Couleur et police pour le texte
        font = pygame.font.Font(None, 25)

        # Afficher les informations des unités (joueur)
        y_offset = CELL_SIZE * GRID_SIZE / 2
        x_offset = CELL_SIZE * GRID_SIZE + 100
        unit_info = f"Statistiques (joueur 1):"
        unit_surface = font.render(unit_info, True, WHITE)
        self.screen.blit(unit_surface, (x_offset, y_offset))
        y_offset += 20
        for unit in self.player_units:
            if isinstance(unit, Mage):
                unit_info = f" - {unit.nom}: PV = {unit.health}, Bouclier = {unit.defense_shield}, mana = {unit.mana}"
            else:
                unit_info = f" - {unit.nom}: PV = {unit.health}, Bouclier = {unit.defense_shield}"
            unit_surface = font.render(unit_info, True, WHITE)
            self.screen.blit(unit_surface, (x_offset, y_offset))
            y_offset += 20

        y_offset += 20
        unit_info = f"Statistiques (joueur 2):"
        unit_surface = font.render(unit_info, True, WHITE)
        self.screen.blit(unit_surface, (x_offset, y_offset))
        # Afficher les informations des unités (ennemi)
        y_offset += 20  # Séparateur
        for unit in self.enemy_units:
            unit_info = f" - {unit.nom} : PV = {unit.health}, Bouclier = {unit.defense_shield}"
            unit_surface = font.render(unit_info, True, WHITE)
            self.screen.blit(unit_surface, (x_offset, y_offset))
            y_offset += 20
        

    def handle_player_turn(self):
        """Tour du joueur"""
        for selected_unit in self.player_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            # Si l'unité est un mage, il récupère 1 point de mana par tour
            if isinstance(selected_unit,Mage):
                selected_unit.mana += 1


            while not has_acted:

                # Affichage du joueur
                font = pygame.font.Font(None, 40)
                y_offset = 10
                x_offset = CELL_SIZE * GRID_SIZE + 100
                unit_status = f"C'est à {selected_unit.nom} de jouer !"
                unit_surface = font.render(unit_status, True, WHITE)
                self.screen.blit(unit_surface, (x_offset, y_offset))
                # Mettre à jour l'affichage
                pygame.display.flip()

                if isinstance(selected_unit,Mage):
                    font = pygame.font.Font(None, 40)
                    y_offset = 100
                    x_offset = CELL_SIZE * GRID_SIZE + 50
                    unit_status = ["Déplacement avec les touches du clavier",
                                    "",
                                    " - Ne rien faire: tapez 1",
                                    " - Attaquer au corps à corps: tapez 2",  #afficher le nombre de mana
                                    " - Soigner: tapez 3",
                                    " - Boule de feu: tapez 4"]
                    for unit_status in unit_status:
                        unit_surface = font.render(unit_status, True, WHITE)
                        self.screen.blit(unit_surface, (x_offset, y_offset))
                        y_offset += 30
                
                # Si l'unité est un voleur
                elif isinstance(selected_unit,Voleur):
                    selected_unit.is_invisble = False
                    font = pygame.font.Font(None, 40)
                    y_offset = 100
                    x_offset = CELL_SIZE * GRID_SIZE + 50
                    unit_status = ["Déplacement avec les touches du clavier",
                                    "",
                                    "Compétences:",
                                    " - Ne rien faire: tapez 1",
                                    " - Attaquer au corps à corps: tapez 2",
                                    " - Se rendre invisible: tapez 3"]
                    for unit_status in unit_status:
                        unit_surface = font.render(unit_status, True, WHITE)
                        self.screen.blit(unit_surface, (x_offset, y_offset))
                        y_offset += 30

                elif isinstance(selected_unit,Guerrier):
                    font = pygame.font.Font(None, 40)
                    y_offset = 100
                    x_offset = CELL_SIZE * GRID_SIZE + 50
                    unit_status = ["Déplacement avec les touches du clavier",
                                    "",
                                    "Compétences:",
                                    " - Ne rien faire: tapez 1",
                                    " - Attaquer au corps à corps: tapez 2",
                                    " - Tirer à l'arc: tapez 3"]
                    for unit_status in unit_status:
                        unit_surface = font.render(unit_status, True, WHITE)
                        self.screen.blit(unit_surface, (x_offset, y_offset))
                        y_offset += 30
                
                # Mettre à jour l'affichage
                pygame.display.flip()

                for event in pygame.event.get():

                    attack = False
                    special_skill = False
                    special_skill_2 = False
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
                            no_action = True
                        elif event.key == pygame.K_2:
                            attack = True
                        elif event.key == pygame.K_3:
                            special_skill = True
                        elif event.key == pygame.K_4:
                            special_skill_2 = True

                        #éviter qu'une unité puisse aller sur une case déjà occupée
                        occupied = False
                        for k in self.player_units:
                            if k != selected_unit and selected_unit.x + dx == k.x and selected_unit.y + dy == k.y:
                                occupied = True
                                break
                        for k in self.enemy_units:
                            if k != selected_unit and selected_unit.x + dx == k.x and selected_unit.y + dy == k.y:
                                occupied = True
                                break
                        if not occupied:
                            selected_unit.move(dx, dy)
                            self.flip_display()

                        if attack:
                            
                            #Récupérer les cibles dans la portée
                            cibles_dans_portee = self.skills.obtenir_cibles_dans_portee(selected_unit, "attack")
                            couleur = (255, 0, 0)  # Rouge pour les ennemis
                            #Dessiner la surbrillance autour des cibles
                            self.surbrillance_cibles(self.screen, cibles_dans_portee, couleur)
                            
                            # Mettre à jour l'affichage
                            self.flip_display()

                            for enemy in self.enemy_units:
                            
                                #if enemy in  cibles_dans_portee : # on verfie que l'ennemi visé est dans la portee
                                    if isinstance(enemy,Voleur):
                                        if not enemy.is_invisible:
                                            selected_unit.attack(enemy)
                                            has_acted = True
                                            selected_unit.is_selected = False
                                    else:
                                        selected_unit.attack(enemy)
                                        has_acted = True
                                        selected_unit.is_selected = False

                        if no_action:
                            has_acted = True
                            selected_unit.is_selected = False

                        elif isinstance(selected_unit,Voleur):
                            selected_unit.is_invisible = False
                            if special_skill:
                                selected_unit.invisibility()
                                has_acted = True
                                selected_unit.is_selected = False


                        #Sélection d'une cible
                        elif special_skill:
                            
                            target = None
                            choose = False
                            self.point.x, self.point.y = selected_unit.x, selected_unit.y  # Centrez le pointeur sur l'unité
                            while not choose and target is None:
                                self.point_aff = True
                                self.flip_display() #affichage du pointeur
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
                                        
                                        if choose:
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
                                                error_msg = "Aucune cible valide à cet endroit !"
                                                error_surface = font.render(error_msg, True, RED)
                                                self.screen.blit(error_surface, (CELL_SIZE * GRID_SIZE + 100, 100))
                                                pygame.display.flip()
                                                pygame.time.wait(1000)
                                                choose = False

                                            if isinstance(target,Voleur): # Vérification si la cible n'est pas invisible
                                                if target.is_invisible:
                                                    font = pygame.font.Font(None, 40)
                                                    error_msg = "Cette unité porte l'anneau et est invisible ! Impossible de l'attaquer !"
                                                    error_surface = font.render(error_msg, True, RED)
                                                    self.screen.blit(error_surface, (CELL_SIZE * GRID_SIZE + 100, 100))
                                                    pygame.display.flip()
                                                    pygame.time.wait(1000)
                                                    target = None
                                                    choose = False
                                    
                            if isinstance(selected_unit,Guerrier):
                                selected_unit.bow(target)
                                has_acted = True
                            if isinstance(selected_unit,Mage):
                                selected_unit.heal(target) #Peut accumuler des manas à tous les tours pour les utiiser d'un coup sur quelqu'un
                                has_acted = True
                                selected_unit.is_selected = False
                                    
                            if selected_unit.miss:
                                font = pygame.font.Font(None, 40)
                                y_offset = CELL_SIZE * target.y
                                x_offset = CELL_SIZE * target.x
                                a_status = f"Raté !"
                                a_surface = font.render(a_status, True, RED)
                                self.screen.blit(a_surface, (x_offset, y_offset))
                                # Mettre à jour l'affichage
                                pygame.display.flip()
                                pygame.time.wait(1000)
                                selected_unit.miss = False
                                selected_unit.critique = False

                            if selected_unit.critique and not selected_unit.miss:
                                font = pygame.font.Font(None, 40)
                                y_offset = CELL_SIZE * target.y
                                x_offset = CELL_SIZE * target.x
                                a_status = f"Critique !"
                                a_surface = font.render(a_status, True, RED)
                                self.screen.blit(a_surface, (x_offset, y_offset))
                                # Mettre à jour l'affichage
                                pygame.display.flip()
                                pygame.time.wait(1000)
                                selected_unit.critique = False

                        for enemy in self.enemy_units:
                            if enemy.health <= 0:
                                self.enemy_units.remove(enemy)

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            occupied = False
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

        #Affiche les terrains depuis le gameBoard
        self.board.draw(self.screen)

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

        # Affiche le HUD
        self.draw_hud()

        # Afficher la victoire (à coder, ça ne marche pas)
        if len(self.enemy_units) == 0:
            font = pygame.font.Font(None, 40)
            y_offset = CELL_SIZE * GRID_SIZE + 500
            x_offset = CELL_SIZE * GRID_SIZE + 100
            unit_status = f"Bravo ! La Communauté de l'anneau a vaincu Sauron !"
            unit_surface = font.render(unit_status, True, RED)
            self.screen.blit(unit_surface, (x_offset, y_offset))

        # Rafraîchit l'écran
        pygame.display.flip()
        
        
    
    #methode qui dessine une surbrillance autour des cibles     
        
    def surbrillance_cibles(screen, cibles, couleur):
        """
        Dessine une surbrillance autour des cibles.
    """
        for cible in cibles:
            pygame.draw.rect(
                screen, couleur,
                (cible.x * CELL_SIZE, cible.y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                3  # Épaisseur de la bordure
        )


    





def main():

    # Initialisation de Pygame
    pygame.init()

    #Initialisation de la musique
    pygame.mixer.init()
    pygame.mixer.music.load("music/The_Shire.mp3")
    pygame.mixer.music.play(-1)  # Joue en boucle infinie

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((1400, 900))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Écran titre
    image = pygame.image.load("images/conte.jpg") #use / instead of \
    # Initialiser une police pour le texte
    font = pygame.font.Font(None, 30)  # Police par défaut, taille 50
    text1 = font.render("Appuyez sur SPACE pour lancer le jeu", True, BLACK)

    font = pygame.font.Font(None, 60)  # Police par défaut, taille 50
    text2 = font.render("Bienvenue dans la Comté !", True, BLACK) 

    # Obtenir la position centrale de l'image
    image_rect = image.get_rect(center=(700, 500))

    # Positionner le texte
    text_rect1 = text1.get_rect(center=(950,150))
    # Positionner le texte
    text_rect2 = text2.get_rect(center=(950,100))

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
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)

        # Mettre à jour l'affichage
        pygame.display.flip()

    # Quitter Pygame proprement
    pygame.mixer.music.stop()
    pygame.quit()


    # Initialisation de Pygame
    screen = pygame.display.set_mode((GRID_SIZE * CELL_SIZE * 1.8, GRID_SIZE * CELL_SIZE))
    pygame.display.set_caption("Mon jeu de stratégie")
    pygame.init()

    #Initialisation de la musique
    pygame.mixer.init()
    pygame.mixer.music.load("music/The_Battle_of_the_Pelennor_Fields.mp3")
    pygame.mixer.music.play(-1)  # Joue en boucle infinie

    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_player_turn()
        game.handle_enemy_turn()


if __name__ == "__main__":
    main()