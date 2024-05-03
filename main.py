import pygame
import sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # Initialisation générale
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Fondu')
        self.clock = pygame.time.Clock()
        
        self.level = None  # Initialisation du niveau à None
        
        self.running = False  # Variable pour suivre si le jeu est en cours ou non

    def run(self):
        self.show_start_screen()  # Afficher l'écran de démarrage

        while self.running:
            self.level = Level()  # Création d'un nouveau niveau
            self.game_loop()

    def game_loop(self):
        game_over = False  # Variable pour suivre si le jeu est terminé
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()
                    if game_over and self.level.player.dead:  # Si le jeu est terminé et que le joueur est mort et qu'une touche est pressée
                        self.restart_game()  # Redémarre le jeu

            # Exécution de la logique du jeu
            self.screen.fill(WATER_COLOR)
            self.level.run()

            # Vérifie si le joueur est mort et affiche l'écran de fin de partie
            if self.level.game_over_screen:
                game_over = True  # Définit le drapeau du jeu terminé sur True

            pygame.display.update()
            self.clock.tick(FPS)

    def show_start_screen(self):
        self.screen.fill((0, 0, 0))  # Remplit l'écran avec une couleur noire

        # Texte "Jouer" au centre de l'écran
        font = pygame.font.Font(None, 64)
        text = font.render("Start", True, (255, 255, 255))  # Couleur blanche
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)

        # Rafraîchir l'écran pour afficher le texte
        pygame.display.update()

        # Contrôle du temps d'attente
        clock = pygame.time.Clock()
        waiting = True
        while waiting:
            clock.tick(120)  # Limite la boucle à 120 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
                    
                    # Effacer l'écran
                    self.screen.fill((0, 0, 0))
                    
                    # Afficher le message de lancement
                    launch_font = pygame.font.Font(None, 32)
                    launch_text = launch_font.render("Lancement du Jeu...", True, (255, 255, 255))  # Couleur blanche
                    launch_text_rect = launch_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    self.screen.blit(launch_text, launch_text_rect)
                    pygame.display.update()
                    
                    # Attendre un court instant pour que l'utilisateur voie le message
                    pygame.time.wait(1000)  # Attendre 1 seconde (1000 millisecondes)
                    
                    # Démarrer le jeu
                    self.running = True

    def restart_game(self):
        self.level.player.dead = False
        self.level = Level()  # Crée un nouveau niveau
        self.level.game_over_screen = False

if __name__ == '__main__':
    game = Game()
    game.run()