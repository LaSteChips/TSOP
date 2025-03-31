import pygame
import sys
import asyncio
import os

# Récupérer le chemin absolu du dossier contenant ce script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Ajouter le dossier du projet au sys.path
sys.path.append(BASE_DIR)

from settings import *
from level import Level

class Game:
    def __init__(self):
        # Initialisation générale
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('The Slime Of Pain')
        self.clock = pygame.time.Clock()
        
        self.level = None  # Initialisation du niveau à None
        
        self.running = True  # Démarrer le jeu immédiatement

    async def run(self):
        self.show_loading_screen()  # Afficher l'écran de chargement
        self.level = Level()  # Création d'un nouveau niveau
        await self.game_loop()

    def show_loading_screen(self):
        self.screen.fill((0, 0, 0))  # Remplit l'écran avec une couleur noire
        
        font = pygame.font.Font(None, 32)
        text = font.render("Chargement du jeu...", True, (255, 255, 255))  # Couleur blanche
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        pygame.display.update()
        pygame.time.wait(1000)  # Attendre 1 seconde

    async def game_loop(self):
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
    
            # Remplir l'écran avec la couleur d'arrière-plan
            self.screen.fill(WATER_COLOR)

            # Exécution de la logique du jeu
            self.level.run()
    
            # Vérifie si le joueur est mort et affiche l'écran de fin de partie
            if self.level.game_over_screen:
                game_over = True  # Définit le drapeau du jeu terminé sur True
    
            pygame.display.update()
            await asyncio.sleep(1 / FPS)

    def restart_game(self):
        self.level.player.dead = False
        self.level = Level()  # Crée un nouveau niveau
        self.level.game_over_screen = False

if __name__ == '__main__':
    game = Game()
    asyncio.run(game.run())
