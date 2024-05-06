import pygame 
from settings import *
from support import import_folder
from entity import Entity

class Player(Entity):
	def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_shield, destroy_shield, create_magic, destroy_magic):
		super().__init__(groups)
		# Charger l'image du joueur et la redimensionner
		self.original_image = pygame.image.load('graphics/player/right_idle/0.png').convert_alpha()
		self.image = self.original_image.copy()  # Créer une copie de l'image originale
		self.rect = self.image.get_rect(topleft=pos)
		self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
		
		# Redimensionner l'image du joueur
		self.scale_factor = 27  # Factor de redimensionnement (2 pour doubler la taille)
		self.resize_image()

		# Graphics setup
		self.import_player_assets()
		self.status = 'right'

		# Movement 
		self.attacking = False
		self.attack_cooldown = 400
		self.attack_time = None
		self.obstacle_sprites = obstacle_sprites

		# Weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]

		# Shield
		self.shielding = False
		self.create_shield = create_shield
		self.destroy_shield = destroy_shield
		self.shield_index = 0
		self.shield_cooldown = 400
		self.shield_time = None
		self.shield = list(shield_data.keys())[self.shield_index]

		# Magic
		self.cast_magic = False
		self.create_magic = create_magic
		self.destroy_magic = destroy_magic
		self.magic_index = 0
		self.magic_cooldown = 250
		self.magic_time = None
		self.magic = list(magic_data.keys())[self.magic_index]

		# Stats
		self.stats = {'health': 100, 'energy': 15, 'attack': 1, 'magic': 50, 'speed': 8, 'mana_gain_per_hit' : 5}
		self.max_stats = {'health': 150, 'energy': 50, 'attack': 2, 'magic' : 75, 'speed': 10}
		self.upgrade_cost = {'health': 100, 'energy': 100, 'attack': 100, 'magic' : 100, 'speed': 100}
		self.health = self.stats['health']
		self.energy = self.stats['energy']
		self.exp = 0
		self.speed = self.stats['speed']

		# Damage timer
		self.vulnerable = True
		self.hurt_time = None
		self.invulnerability_duration = 500

		# Import sound
		self.weapon_attack_sound = pygame.mixer.Sound('audio/sword.wav')
		self.weapon_attack_sound.set_volume(0.1)
		self.hit_attack_sound = pygame.mixer.Sound('audio/Fire.wav')
		self.hit_attack_sound.set_volume(0.4)

		self.right_pressed_once = False
		self.left_pressed_once = False
		self.prev_status = 'left'

	def resize_image(self):
		# Redimensionner l'image en conservant les proportions
		width = int(self.original_image.get_width() * self.scale_factor)
		height = int(self.original_image.get_height() * self.scale_factor)
		self.image = pygame.transform.scale(self.original_image, (width, height))
		self.rect = self.image.get_rect(center=self.rect.center)

	def import_player_assets(self):
		character_path = 'graphics/player/'
		self.animations = {'left': [], 'right': [],
			'right_idle':[], 'left_idle':[],
			'right_attack':[], 'left_attack':[],
			'right_shield':[], 'left_shield':[],
			'right_magic':[], 'left_magic':[],
			'left_death' : [], 'right_death' : [],
			'left_idle_death' : [], 'right_idle_death' : []}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_z] or keys[pygame.K_w]:
				self.direction.y = -1

				if keys[pygame.K_d]:
					self.direction.x = 1
					self.right_pressed_once = True
					self.left_pressed_once = False
					self.prev_status = 'right'
					self.status = 'right'
				elif keys[pygame.K_q] or keys[pygame.K_a]:
					self.direction.x = -1
					self.left_pressed_once = True
					self.right_pressed_once = False
					self.prev_status = 'left'
					self.status = 'left'
				else:
					self.direction.x = 0
					if self.direction.x == 0 and self.direction.y == -1 and not (self.right_pressed_once or self.left_pressed_once):
						self.status = 'left'
			elif keys[pygame.K_s]:
				self.direction.y = 1
				if keys[pygame.K_d]:
					self.direction.x = 1
					self.right_pressed_once = True
					self.left_pressed_once = False
					self.prev_status = 'right'
					self.status = 'right'
				elif keys[pygame.K_q] or keys[pygame.K_a]:
					self.direction.x = -1
					self.left_pressed_once = True
					self.right_pressed_once = False
					self.prev_status = 'left'
					self.status = 'left'
				else:
					self.direction.x = 0
					if self.direction.x == 0 and self.direction.y == 1 and not (self.right_pressed_once or self.left_pressed_once):
						self.status = 'left'
			elif keys[pygame.K_d]:
				self.direction.x = 1
				self.direction.y = 0
				if not self.right_pressed_once:
					self.status = 'right'
			elif keys[pygame.K_q] or keys[pygame.K_a]:
				self.direction.x = -1
				self.direction.y = 0
				if not self.left_pressed_once:
					self.status = 'left'
			else:
				self.direction.x = 0
				self.direction.y = 0

			if not keys[pygame.K_d]:
				self.right_pressed_once = False

			if not keys[pygame.K_q]:
				self.left_pressed_once = False

			if self.direction.x == 0 and self.direction.y == -1 and not (self.right_pressed_once or self.left_pressed_once):
				self.status = self.prev_status

			if self.direction.x == 0 and self.direction.y == 1 and not (self.right_pressed_once or self.left_pressed_once):
				self.status = self.prev_status

			# Attack input 
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_attack()
				self.weapon_attack_sound.play()

			# Magic input 
			if keys[pygame.K_o] and not self.cast_magic:  # Vérifie si la touche est enfoncée pour la première fois
				self.cast_magic = True
				self.attack_time = pygame.time.get_ticks()
				style = list(magic_data.keys())[self.magic_index]
				strength = list(magic_data.values())[self.magic_index]['strength'] + self.stats['magic']
				cost = list(magic_data.values())[self.magic_index]['cost']
				self.create_magic(style, strength, cost)
			elif not keys[pygame.K_o]:  # Si la touche est relâchée
				self.cast_magic = False  # Réinitialise la variable de contrôle

			# Shield input 
			if keys[pygame.K_p]:
				if not self.shielding:
					self.shielding = True
					self.shield_time = pygame.time.get_ticks()

	def death(self):
		if self.stats['health'] <= 0:
			self.dead = True

	def get_status(self):
		# Attack status
		if self.direction.x == 0 and self.direction.y == 0:
			if not ('idle' in self.status or 'attack' in self.status or 'shield' in self.status or 'magic' in self.status):
				self.status = self.status + '_idle'

		# Shield status
		if self.shielding:
			self.direction.x = 0
			self.direction.y = 0
			if not 'shield' in self.status and not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle', '_shield')
				else:
					self.status = self.status + '_shield'
			elif 'attack' in self.status:
				self.status = self.status.replace('_attack', '_shield')
			elif 'magic' in self.status:
				self.status = self.status.replace('_magic', '_shielding')
		else:
			if 'shield' in self.status:
				self.status = self.status.replace('_shield', '')

		# Attack status
		if self.attacking and not self.shielding:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle', '_attack')
				elif 'shield' in self.status:
					self.status = self.status.replace('_shield', '_idle')
				elif 'magic' in self.status:
					self.status = self.status.replace('_magic', '_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:   
				self.status = self.status.replace('_attack', '')

		if self.cast_magic and not self.shielding and not self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'magic' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle', '_magic')
				elif 'shield' in self.status:
					self.status = self.status.replace('_shield', '_magic')
				elif 'attack' in self.status:
					self.status = self.status.replace('_attack', '_magic')
				else:
					self.status = self.status + '_magic'
		else:
			if '_magic' in self.status:
				self.status = self.status.replace('_magic', '')

		# Death status
		if self.dead:
			self.direction.x = 0
			self.direction.y = 0
			if self.dead:
				self.status = 'left_death' if self.direction.x < 0 else 'right_death'

	def cooldowns(self):
		current_time = pygame.time.get_ticks()
		
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown + weapon_data[self.weapon]['cooldown']:
				self.attacking = False
				self.destroy_attack()
		
		if self.shielding and self.shield_time is not None and shield_data[self.shield]['cooldown'] is not None:
			if current_time - self.shield_time >= self.shield_cooldown + shield_data[self.shield]['cooldown']:
				self.shielding = False
				self.destroy_shield()
		
		if self.cast_magic and self.magic_time is not None and magic_data[self.magic]['cooldown'] is not None:
			if current_time - self.magic_time >= self.magic_cooldown + magic_data[self.magic]['cooldown']:
				self.cast_magic = False
				self.destroy_magic()

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True

	def animate(self):
		animation = self.animations[self.status]

		# Si l'animation de la mort est en cours
		if self.status.endswith('_death'):
			# Vérifiez si self.frame_index dépasse la taille de la liste animation
			if int(self.frame_index) >= len(animation):
				# Si l'animation de mort s'est jouée une fois
				self.frame_index = len(animation) - 1  # Assurez-vous que l'index reste dans les limites
				self.status = 'left_idle_death' if self.direction.x < 0 else 'right_idle_death'
			else:
				# Set the image
				self.image = animation[int(self.frame_index)]
				self.frame_index += self.animation_speed / 1.5  # Ralentissement de l'animation

		else:
			self.frame_index += self.animation_speed / 0.75  # Ralentissement de l'animation
			# Assurez-vous que self.frame_index reste dans les limites de la liste animation
			if int(self.frame_index) >= len(animation):
				self.frame_index = 0  # Revenez au début de l'animation

			# Set the image
			self.image = animation[int(self.frame_index)]

		self.rect = self.image.get_rect(center=self.hitbox.center)

		# Flicker 
		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def get_full_weapon_damage(self):
		base_damage = self.stats['attack']
		weapon_damage = weapon_data[self.weapon]['damage']
		return base_damage + weapon_damage

	def get_full_magic_damage(self):
		base_damage = self.stats['magic']
		spell_damage = magic_data[self.magic]['strength']
		return base_damage + spell_damage

	def get_value_by_index(self, index):
		return list(self.stats.values())[index]

	def get_cost_by_index(self, index):
		return list(self.upgrade_cost.values())[index]

	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.stats['speed'])

		# Si le joueur est mort
		if self.dead:
			if not hasattr(self, 'death_start_time'):
				self.death_start_time = pygame.time.get_ticks()  # Enregistrer le temps auquel la mort a commencé
			else:
				# Vérifier si 5 seconde s'est écoulée depuis le début de la mort
				if pygame.time.get_ticks() - self.death_start_time >= 3000:  
					self.dead = False  # Réinitialiser l'état du joueur à vivant
					self.health = self.stats['health'] * 0.1  # Réinitialiser la santé
					# D'autres réinitialisations peuvent être nécessaires en fonction de votre logique de jeu
					self.death_start_time = None  # Réinitialiser le temps de début de la mort