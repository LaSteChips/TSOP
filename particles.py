import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
    def __init__(self):
        self.frames = {
			# magic
			'flame': import_folder('graphics/particles/flame/frames'),
			'aura': import_folder('graphics/particles/aura'),
			'heal': import_folder('graphics/particles/heal/frames'),
			
			# attacks 
			'claw': import_folder('graphics/particles/claw'),
			'slash': import_folder('graphics/particles/slash'),
			'sparkle': import_folder('graphics/particles/sparkle'),
			'leaf_attack': import_folder('graphics/particles/leaf_attack'),
			'thunder': import_folder('graphics/particles/thunder'),
            'end' : import_folder('graphics/particles/end'),

			# monster deaths
			'squid': import_folder('graphics/particles/smoke_orange'),
			'king_cheese': import_folder('graphics/particles/explosion'),
			'spirit': import_folder('graphics/particles/nova'),
			'bamboo': import_folder('graphics/particles/bamboo'),
		}

    def reflect_images(self,frames):
        new_frames = []		
        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self,pos,groups):
        animation_frames = choice(self.frames['leaf'])
        ParticleEffect(pos,animation_frames,groups)

    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)
        

class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups): 
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]
            
    def update(self):
        self.animate()