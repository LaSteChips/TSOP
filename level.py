import pygame
from settings import *
from tile import Tile
from player import Player
from support import *
from random import randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
import sqlite3
from datetime import datetime

class Level:
	def __init__(self):
		# Obtenez la surface d'affichage
		self.display_surface = pygame.display.get_surface()
		self.game_paused = False

		# Configuration des groupes de sprites
		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		# Sprites d'attaque
		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		# Sprites de bouclier
		self.current_shield = None

		# Sprites de magie
		self.current_magic = None

		# Configuration des sprites
		self.create_map()

		# Interface utilisateur
		self.ui = UI()
		self.upgrade = Upgrade(self.player)

		# Particules
		self.animation_player = AnimationPlayer()
		self.magic_player = MagicPlayer(self.animation_player)

		# Écran de fin de jeu
		self.game_over_screen = False
		self.game_over_text_position = None

		# Indicateur de fin de jeu
		self.end = False

		# Indicateur pour suivre si les données ont déjà été enregistrées
		self.data_imported = False

	def create_map(self):
		layouts = {
			'boundary': import_csv_layout('graphics/tilemap/map_border.csv'),
			'object': import_csv_layout('graphics/tilemap/map_Tree.csv'),
			'entities': import_csv_layout('graphics/tilemap/map_enemy.csv')
		}
		graphics = {
			'objects': import_folder('graphics/Objects')
		}

		for style,layout in layouts.items():
			for row_index,row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x,y),[self.obstacle_sprites],'invisible')

						if style == 'object':
							surf = graphics['objects'][int(col)]
							Tile((x,y),[self.visible_sprites,self.obstacle_sprites],'object',surf)

						if style == 'entities':
							if col == '394':
								self.player = Player(
								(x,y),
								[self.visible_sprites],
								self.obstacle_sprites,
								self.create_attack,
								self.destroy_attack,
								self.create_shield,
								self.destroy_shield,
								self.create_magic,
								self.destroy_magic)
							else:
								if col == '390': monster_name = 'bamboo'
								elif col == '391': monster_name = 'spirit'
								elif col == '392': monster_name = 'king_cheese'
								elif col == '393': monster_name = 'squid'
								else: monster_name = 'end'
								Enemy(
									monster_name,
									(x,y),
									[self.visible_sprites,self.attackable_sprites],
									self.obstacle_sprites,
									self.damage_player,
									self.trigger_death_particles,
									self.add_exp)

	def create_attack(self):
		self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

	def create_magic(self, style, strength, cost):
		if style == 'heal':
			self.magic_player.heal(self.player, strength, cost, [self.visible_sprites])

	def destroy_magic(self):
		if self.current_magic:
			self.current_magic.kill()
		self.current_magic = None

	def create_shield(self):
		self.player.shielding = True
		self.player.shield_time = pygame.time.get_ticks()

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def destroy_shield(self):
		self.player.shielding = False
		if self.current_shield:
			self.current_shield.kill()
		self.current_shield = None

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							pos = target_sprite.rect.center
							offset = pygame.math.Vector2(0, 5)
							for leaf in range(randint(3, 6)):
								self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
							target_sprite.kill()
						else:
							target_sprite.get_damage(self.player, attack_sprite.sprite_type)
							# Ajoute du mana lorsque le joueur inflige des dégâts
							mana_gain = self.player.stats['mana_gain_per_hit']
							self.player.energy += mana_gain
							if self.player.energy > self.player.stats['energy']:
								self.player.energy = self.player.stats['energy']  # Limite la quantité de mana au maximum

	def damage_player(self, amount, attack_type):
		if self.player.vulnerable:
			if self.player.shielding:
				amount *= 0.8
			self.player.vulnerable = False
			self.player.health -= amount
			self.player.hurt_time = pygame.time.get_ticks()
			self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])
			if self.player.health <= 0:  # Met à jour self.player.dead si la santé est <= 0
				self.player.dead = True
				self.game_over()  # Appel de la méthode game_over lorsque le joueur est mort

	def trigger_death_particles(self, pos, particle_type):
		self.animation_player.create_particles(particle_type, pos, self.visible_sprites)

	def add_exp(self, amount):
		self.player.exp += amount

	def toggle_menu(self):
		self.game_paused = not self.game_paused

	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.ui.display(self.player)
		if not self.game_paused:
			self.visible_sprites.update()
			self.visible_sprites.enemy_update(self.player)
			self.player_attack_logic()
		# debug(self.player.status) # à retirer
		self.game_over()

		if self.player.dead:
			self.remove_enemies()

	def game_over(self):
		self.game_over_screen = True
		self.game_over_text_position = (640, 300)
		bar_position = (640, 275)  # Position manuellement réglable de la barre noire
		if self.player.dead or self.end:  # Si le joueur est mort ou a touché "end"
			font = pygame.font.SysFont('arial', 36)
			game_over_text = font.render("Game Over", True, (255, 0, 0))
			text_rect = game_over_text.get_rect(center=self.game_over_text_position)  # Utiliser la position spécifiée

			# Dessiner un rectangle noir en dessous du texte
			bar_height = 50
			bar_rect = pygame.Rect(0, bar_position[1], self.display_surface.get_width(), bar_height)
			pygame.draw.rect(self.display_surface, (0, 0, 0), bar_rect)

			self.display_surface.blit(game_over_text, text_rect)
			pygame.display.flip()  # Assurez-vous de rafraîchir l'écran après avoir dessiné le texte

			# Enregistrer les données dans la base de données si le joueur est mort ou a touché "end"
			if not self.data_imported:
				self.import_data(self.player)
				self.data_imported = True

	def remove_enemies(self):
		# Supprime tous les ennemis de la liste de sprites
		enemy_sprites = [sprite for sprite in self.visible_sprites.sprites() if isinstance(sprite, Enemy)]
		for enemy in enemy_sprites:
			enemy.kill()

	def end(self):
		# Fait en sorte que, si player touche "end", alors l'événement fin = true
		self.end = True

	def import_data(self, player):
		# Connexion à la base de données
		connection = sqlite3.connect("data.db")
		cursor = connection.cursor()

		# Obtention de la date actuelle
		current_date = datetime.now().strftime("%Y%m%d")

		# Vérifiez la valeur maximale actuelle de l'ID
		cursor.execute("SELECT MAX(id) FROM game_data")
		max_id = cursor.fetchone()[0]

		# Si la table est vide, commencez à partir de 1, sinon à partir de max_id + 1
		next_id = max_id + 1 if max_id is not None else 1

		# Insertion des données d'expérience dans la table game_data avec l'ID ajusté
		cursor.execute("INSERT INTO game_data (id, score, date) VALUES (?, ?, ?)", (next_id, player.exp, current_date))

		# Commit et fermeture de la connexion
		connection.commit()
		connection.close()


class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):

		# general setup
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

		# creating the floor
		self.floor_surf = pygame.image.load('graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	def custom_draw(self,player):

		#getting the offset
		self.offset.x = player.rect.centerx - self.half_width
		self.offset.y = player.rect.centery - self.half_height

		# draw the floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf,floor_offset_pos)

		# for sprite in self.sprites():
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image,offset_pos)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
		for enemy in enemy_sprites:
			enemy.enemy_update(player)