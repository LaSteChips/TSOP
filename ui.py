import pygame
from settings import *

class UI:
    def __init__(self):
        # general
        self.display_surface = pygame.display.get_surface()
        self.front = pygame.font.Font(UI_FONT, UI_FONT_SIZE)

        # bar setup
        self.health_bar_rect = pygame.Rect(10, 10, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10, 34, ENERGY_BAR_WIDTH, BAR_HEIGHT)

        # convert magic dictionary
        self.magic_graphics = []
        for magic in magic_data.values():
            magic_image = pygame.image.load(magic['graphic']).convert_alpha()
            self.magic_graphics.append(magic_image)

        self.weapon_graphics = []
        for weapon in weapon_data.values():
            weapon_image = pygame.image.load(weapon['graphic']).convert_alpha()
            self.weapon_graphics.append(weapon_image)

        self.shield_graphics = []
        for shield in shield_data.values():
            shield_image = pygame.image.load(shield['graphic']).convert_alpha()
            self.shield_graphics.append(shield_image)

    def show_bar(self, current, max_amount, bg_rect, color):
        # draw the bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        # converting stats to pixel
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # drawing the bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_exp(self, exp):
        text_surf = self.front.render(str(int(exp)), False, TEXT_COLOR)
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 20))
        self.display_surface.blit(text_surf, text_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 20), 3)

    def magic_overlay(self, magic_index):
        # Nouvelle taille du carré noir
        box_size = 60  # Vous pouvez ajuster la taille du carré noir ici
        border_thickness = 10  # Épaisseur de la bordure sombre

        # Espacement du bord de la fenêtre
        spacing_from_edge = 10

        # Position de l'image en haut à droite
        left = self.display_surface.get_size()[0] - box_size - spacing_from_edge
        top = spacing_from_edge

        # Crée le rectangle pour le premier carré noir
        bg_rect = pygame.Rect(left, top, box_size, box_size)

        # Dessine la bordure sombre autour du premier carré noir
        border_color = (50, 50, 50)  # Couleur sombre pour la bordure
        pygame.draw.rect(self.display_surface, border_color, bg_rect)  
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect.inflate(-border_thickness, -border_thickness))

        # Dessine l'image centrée à l'intérieur du premier carré noir
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(magic_surf, magic_rect)

        # Crée un deuxième carré au-dessus du premier
        second_box_size = 30  # Ajustez la taille du deuxième carré
        second_box_border_thickness = 7.5  # Épaisseur de la bordure sombre du deuxième carré
        second_box_rect = pygame.Rect(left - second_box_size, top + box_size - second_box_size, second_box_size, second_box_size)

        # Ajustez l'emplacement du deuxième carré noir en modifiant les valeurs de left et top
        left_second_box = left - second_box_size + 15 # Ajustez cette valeur pour changer l'emplacement horizontal
        top_second_box = top + box_size - second_box_size + 10 # Ajustez cette valeur pour changer l'emplacement vertical

        second_box_rect = pygame.Rect(left_second_box, top_second_box, second_box_size, second_box_size)

        # Dessine la bordure sombre autour du deuxième carré
        pygame.draw.rect(self.display_surface, border_color, second_box_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, second_box_rect.inflate(-second_box_border_thickness, -second_box_border_thickness))

        # Dessine une image à l'intérieur du deuxième carré (à titre d'exemple)
        second_box_image = pygame.Surface((second_box_rect.width - 2 * second_box_border_thickness, second_box_rect.height - 2 * second_box_border_thickness))

        # Dessine une image à l'intérieur du deuxième carré (à titre d'exemple)
        second_box_image = pygame.image.load('graphics/objects/O_ui.png').convert_alpha()
        second_box_image_rect = second_box_image.get_rect(center=second_box_rect.center)

        # Dessine la bordure sombre autour du deuxième carré
        pygame.draw.rect(self.display_surface, border_color, second_box_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, second_box_rect.inflate(-second_box_border_thickness, -second_box_border_thickness))

        # Blitte l'image centrée à l'intérieur du deuxième carré
        self.display_surface.blit(second_box_image, second_box_image_rect)

    def weapon_overlay(self, magic_index):
        # Nouvelle taille du carré noir
        box_size = 60  # Vous pouvez ajuster la taille du carré noir ici
        border_thickness = 10  # Épaisseur de la bordure sombre

        # Espacement du bord de la fenêtre
        spacing_from_edge = 90
        spacing_from_edge_top = 10

        # Position de l'image en haut à droite
        left = self.display_surface.get_size()[0] - box_size - spacing_from_edge
        top = spacing_from_edge_top

        # Crée le rectangle pour le premier carré noir
        bg_rect = pygame.Rect(left, top, box_size, box_size)

        # Dessine la bordure sombre autour du premier carré noir
        border_color = (50, 50, 50)  # Couleur sombre pour la bordure
        pygame.draw.rect(self.display_surface, border_color, bg_rect)  
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect.inflate(-border_thickness, -border_thickness))

        # Dessine l'image centrée à l'intérieur du premier carré noir
        weapon_surf = self.weapon_graphics[magic_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(weapon_surf, weapon_rect)

        # Crée un deuxième carré au-dessus du premier
        second_box_size = 30  # Ajustez la taille du deuxième carré
        second_box_border_thickness = 7.5  # Épaisseur de la bordure sombre du deuxième carré
        second_box_rect = pygame.Rect(left - second_box_size, top + box_size - second_box_size, second_box_size, second_box_size)

        # Ajustez l'emplacement du deuxième carré noir en modifiant les valeurs de left et top
        left_second_box = left - second_box_size + 15 # Ajustez cette valeur pour changer l'emplacement horizontal
        top_second_box = top + box_size - second_box_size + 10 # Ajustez cette valeur pour changer l'emplacement vertical

        second_box_rect = pygame.Rect(left_second_box, top_second_box, second_box_size, second_box_size)

        # Dessine la bordure sombre autour du deuxième carré
        pygame.draw.rect(self.display_surface, border_color, second_box_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, second_box_rect.inflate(-second_box_border_thickness, -second_box_border_thickness))

        # Dessine une image à l'intérieur du deuxième carré (à titre d'exemple)
        second_box_image = pygame.Surface((second_box_rect.width - 2 * second_box_border_thickness, second_box_rect.height - 2 * second_box_border_thickness))

        # Dessine une image à l'intérieur du deuxième carré (à titre d'exemple)
        second_box_image = pygame.image.load('graphics/objects/Space_bar.png').convert_alpha()
        second_box_image_rect = second_box_image.get_rect(center=second_box_rect.center)

        # Dessine la bordure sombre autour du deuxième carré
        pygame.draw.rect(self.display_surface, border_color, second_box_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, second_box_rect.inflate(-second_box_border_thickness, -second_box_border_thickness))

        # Blitte l'image centrée à l'intérieur du deuxième carré
        self.display_surface.blit(second_box_image, second_box_image_rect)
        
    def shield_overlay(self, magic_index):
        # Nouvelle taille du carré noir
        box_size = 60  # Vous pouvez ajuster la taille du carré noir ici
        border_thickness = 10  # Épaisseur de la bordure sombre

        # Espacement du bord de la fenêtre
        spacing_from_edge = 180
        spacing_from_edge_top = 10

        # Position de l'image en haut à droite
        left = self.display_surface.get_size()[0] - box_size - spacing_from_edge
        top = spacing_from_edge_top

        # Crée le rectangle pour le premier carré noir
        bg_rect = pygame.Rect(left, top, box_size, box_size)

        # Dessine la bordure sombre autour du premier carré noir
        border_color = (50, 50, 50)  # Couleur sombre pour la bordure
        pygame.draw.rect(self.display_surface, border_color, bg_rect)  
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect.inflate(-border_thickness, -border_thickness))

        # Dessine l'image centrée à l'intérieur du premier carré noir
        shield_surf = self.shield_graphics[magic_index]
        shield_rect = shield_surf.get_rect(center=bg_rect.center)
        self.display_surface.blit(shield_surf, shield_rect)

        # Crée un deuxième carré au-dessus du premier
        second_box_size = 30  # Ajustez la taille du deuxième carré
        second_box_border_thickness = 7.5  # Épaisseur de la bordure sombre du deuxième carré
        second_box_rect = pygame.Rect(left - second_box_size, top + box_size - second_box_size, second_box_size, second_box_size)

        # Ajustez l'emplacement du deuxième carré noir en modifiant les valeurs de left et top
        left_second_box = left - second_box_size + 15 # Ajustez cette valeur pour changer l'emplacement horizontal
        top_second_box = top + box_size - second_box_size + 10 # Ajustez cette valeur pour changer l'emplacement vertical

        second_box_rect = pygame.Rect(left_second_box, top_second_box, second_box_size, second_box_size)

        # Dessine la bordure sombre autour du deuxième carré
        pygame.draw.rect(self.display_surface, border_color, second_box_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, second_box_rect.inflate(-second_box_border_thickness, -second_box_border_thickness))

        # Dessine une image à l'intérieur du deuxième carré (à titre d'exemple)
        second_box_image = pygame.Surface((second_box_rect.width - 2 * second_box_border_thickness, second_box_rect.height - 2 * second_box_border_thickness))

        # Dessine une image à l'intérieur du deuxième carré (à titre d'exemple)
        second_box_image = pygame.image.load('graphics/objects/P_ui.png').convert_alpha()
        second_box_image_rect = second_box_image.get_rect(center=second_box_rect.center)

        # Dessine la bordure sombre autour du deuxième carré
        pygame.draw.rect(self.display_surface, border_color, second_box_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, second_box_rect.inflate(-second_box_border_thickness, -second_box_border_thickness))

        # Blitte l'image centrée à l'intérieur du deuxième carré
        self.display_surface.blit(second_box_image, second_box_image_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats['energy'], self.energy_bar_rect, ENERGY_COLOR)

        self.show_exp(player.exp)

        self.magic_overlay(player.magic_index)
        self.weapon_overlay(player.weapon_index)
        self.shield_overlay(player.shield_index)