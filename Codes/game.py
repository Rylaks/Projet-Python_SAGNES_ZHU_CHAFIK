
import pygame
import random

from unit import *
from personnages import *
from skills import *
from unit import *
from diff_case import *

class GameBoard:
    def __init__(self, size,occupied_positions):
        self.size = size
        self.grid = [[Terrain() for _ in range(size)] for _ in range(size)]
        
        # Place bushes, rocks, and water avoiding character positions
        self.place_terrain(Bush, random.randint(1, 3),occupied_positions)
        self.place_terrain(Rock, random.randint(1, 5),occupied_positions)
        self.place_terrain(Water, random.randint(1, 3),occupied_positions)
        
        
        
        
    def place_terrain(self, terrain_class, count, occupied_positions):
        for _ in range(count):   # Boucler pour garantir la création du nombre spécifié de terrains.
            placed = False     # Indique que le terrain n'a pas encore été placé avec succès.
            while not placed:   # Boucle pour choisir aléatoirement une position sur la carte jusqu'à ce qu'une position appropriée soit trouvée.
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)  # Génère aléatoirement les coordonnées x et y.
                if (x, y) not in occupied_positions:  # Vérifie si les coordonnées générées (x, y) ne sont pas dans l'ensemble occupied_positions. Cet ensemble contient toutes les positions déjà occupées par les personnages, assurant ainsi que le terrain ne se superpose pas avec les positions des personnages.
                    self.grid[y][x] = terrain_class()   # Si les coordonnées (x, y) ne sont pas dans occupied_positions, cela signifie que cette position peut accueillir un nouveau terrain.
                    placed = True    # Mettre placed à True pour sortir de la boucle while, indiquant que le terrain a été placé avec succès.
    
    
   
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
        #self.board = GameBoard(GRID_SIZE)
        self.player_units = [Mage(0, 0, 'player',self),
                             Voleur(2, 0, 'player',self),
                             Guerrier(0, 2, 'player',self)]

        self.enemy_units = [Mage(GRID_SIZE - 1, GRID_SIZE - 1, 'enemy',self), 
                            Voleur(GRID_SIZE - 1, GRID_SIZE - 3, 'enemy',self),
                            Guerrier(GRID_SIZE - 3, GRID_SIZE - 1, 'enemy',self)]
        
        self.point = Unit(0,0,"player")
        self.point_aff = False
        
    
    def is_occupied(self, x, y):
        for unit in self.player_units + self.enemy_units:
            if unit.x == x and unit.y == y:
                return True
        return False

        
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
            self.player_units[0].is_selected = True
            print("First unit selected:", self.player_units[0].is_selected)
            
            if selected_unit.is_selected:
                
                selected_unit.update_move_range()  # 确保调用此方法以计算移动范围
                print("Updated move range:", selected_unit.green_cases)  # 打印出允许的移动范围
                selected_unit.draw_move_range(self.screen) # 绘制移动范围
                
            
            # 应用当前地形的停留效果
            current_terrain = self.board.grid[selected_unit.y][selected_unit.x]
            current_terrain.stay_effect(selected_unit)
            
            
            
            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()

            # Si l'unité est un mage, il récupère 1 point de mana par tour
            if isinstance(selected_unit,Mage):
                selected_unit.mana += 1

            # Enregistrement de la position initiale de l'unité
            temp1 = selected_unit.x
            temp2 = selected_unit.y

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
                        
                        # Chaque unité à sa vitesse, et donc sa portée de déplacement
                        if not occupied and temp1 - selected_unit.speed <= selected_unit.x + dx <= temp1 + selected_unit.speed and temp2 - selected_unit.speed <= selected_unit.y + dy <= temp2 + selected_unit.speed:
                            selected_unit.move(dx, dy)
                            self.flip_display()

                        if attack: #attaque TOUS les ennemis qui sont à UN de distance.
                            for enemy in self.enemy_units:
                                if abs(enemy.x - selected_unit.x) <= 1 and abs(enemy.y - selected_unit.y) <= 1:
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
                                        elif event.key == pygame.K_ESCAPE:
                                            self.point_aff = False
                                            choose = True
                                            target = 1
                                            special_skill = False
                                            break  # Valide la cible

                                        # Déplace le pointeur dans la portée de 3
                                        if selected_unit.x - 3 <= self.point.x + dx <= selected_unit.x + 3 and selected_unit.y - 3 <= self.point.y + dy <= selected_unit.y + 3:
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
                                    
                            if special_skill and isinstance(selected_unit,Guerrier):
                                selected_unit.bow(target)
                                has_acted = True
                            if special_skill and isinstance(selected_unit,Mage):
                                selected_unit.heal(target) #Peut accumuler des manas à tous les tours pour les utiliser d'un coup sur quelqu'un
                                has_acted = True
                                selected_unit.is_selected = False
                            
                            #Affichage des informations de coups critiques et manqués
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

                        elif special_skill_2 and isinstance(selected_unit,Mage):
                            target = None
                            choose = False
                            self.point.x, self.point.y = selected_unit.x, selected_unit.y
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
                                        elif event.key == pygame.K_ESCAPE:
                                            self.point_aff = False
                                            choose = True
                                            target = 1
                                            special_skill_2 = False
                                            break  # Valide la cible

                                        # Déplace le pointeur dans la portée de 2
                                        if selected_unit.x - 2 <= self.point.x + dx <= selected_unit.x + 2 and selected_unit.y - 2 <= self.point.y + dy <= selected_unit.y + 2:
                                            self.point.move(dx, dy)
                                            self.flip_display()
                                        
                                        if choose and special_skill_2:
                                            self.point_aff = False
                                            selected_unit.fire_ball(self.point.x, self.point.y, self.player_units + self.enemy_units)
                                            has_acted = True

                            #Affichage des informations de coups critiques et manqués
                            if selected_unit.miss:
                                font = pygame.font.Font(None, 40)
                                y_offset = CELL_SIZE * self.point.y
                                x_offset = CELL_SIZE * self.point.x
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
                                y_offset = CELL_SIZE * self.point.y
                                x_offset = CELL_SIZE * self.point.x
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
                        
                        self.flip_display()

    def handle_enemy_turn(self):
        """IA très simple pour les ennemis."""
        for enemy in self.enemy_units:
            
            # 应用当前地形的停留效果
            current_terrain = self.board.grid[enemy.y][enemy.x]
            current_terrain.stay_effect(enemy)
            
            
            is_occupied = False
            # Déplacement aléatoire
            target = random.choice(self.player_units)
            
            dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
            dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
            
            
            # 检查目标位置是否已被其他单位占据
            new_x, new_y = enemy.x + dx, enemy.y + dy
            # 使用is_occupied方法检查该位置是否被占用
            if not self.is_occupied(new_x, new_y):  
                enemy.move(dx, dy)

                # 重新应用移动后的地形效果
                current_terrain = self.board.grid[enemy.y][enemy.x]
                current_terrain.stay_effect(enemy)
            
            
            # Attaque si possible
            if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
                enemy.attack(target)
                if target.health < 0:
                    self.player_units.remove(target)


    def flip_display(self):
        """Affiche le jeu et le HUD."""

        # Affiche la grille
        self.screen.fill(BLACK)

        #Affiche les terrains depuis le gameBoard
        self.board.draw(self.screen)
        
        # 这里调用绘制移动范围，确保每次屏幕更新都能看到
        for unit in self.player_units:
            if unit.is_selected:
                unit.draw_move_range(self.screen)

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
            info2 = "Echap pour annuler"
            info_surface = font.render(info, True, WHITE)
            self.screen.blit(info_surface, (CELL_SIZE * GRID_SIZE + 100, 10))
            info_surface = font.render(info2, True, WHITE)
            self.screen.blit(info_surface, (CELL_SIZE * GRID_SIZE + 200, 40))

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





def main():

    # Initialisation de Pygame
    pygame.init()

    #Initialisation de la musique
    pygame.mixer.init()
    pygame.mixer.music.load("music/The_Shire.mp3")
    pygame.mixer.music.play(-1)  # Joue en boucle infinie

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((1450, 750))
    pygame.display.set_caption("Mon jeu de stratégie")

    # Écran titre
    image = pygame.image.load("images/conte.jpg") #use / instead of \
    # Initialiser une police pour le texte
    font = pygame.font.Font(None, 30)  # Police par défaut, taille 30
    text1 = font.render("Appuyez sur SPACE pour lancer le jeu", True, BLACK)

    font = pygame.font.Font(None, 60)  # Police par défaut, taille 60
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
