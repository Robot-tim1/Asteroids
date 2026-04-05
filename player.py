import pygame
from constants import *
from circleshape import *
from shot import *

class Player(CircleShape):
    
    cooldown = 0
    
    def __init__(self, x, y, rotation=0):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = rotation
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "green", self.triangle(), 0)
        pygame.draw.polygon(screen, (0,160,0), self.triangle(), 3)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt    

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
    
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.cooldown -= dt
        forward = pygame.K_w
        left = pygame.K_a
        right = pygame.K_d
        back = pygame.K_s

        if keys[forward] and keys[back] or not keys[forward] and not keys[back]:
            if keys[left]:
                self.rotate(-dt)
            if keys[right]:
                self.rotate(dt) 
        
        elif keys[forward]:
            self.move(dt)        
            if keys[left]:
                self.rotate(-dt)
            if keys[right]:
                self.rotate(dt)    
        
        elif keys[back]: 
            self.move(-dt)
            if keys[left]:
                self.rotate(dt)
            if keys[right]:
                self.rotate(-dt)     
        
        if keys[pygame.K_SPACE]:
            if self.cooldown > 0:
                pass
            else:
                self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS    
                self.shoot()

    def shoot(self):
        position_vector = pygame.Vector2(self.position[0], self.position[1])
        offset_vector = pygame.Vector2(0, 20)
        rotated_offset = offset_vector.rotate(self.rotation)
        position_vector += rotated_offset
        shot = Shot(position_vector[0], position_vector[1])
        
        vector = pygame.Vector2(0, 1)
        rotated = vector.rotate(self.rotation)
        speed = rotated * PLAYER_SHOOT_SPEED
        shot.velocity += speed

class Respawned_Player(Player):
    def __init__(self, x, y):
        super().__init__(x, y, 0)
        self.i_frames = PLAYER_DEATH_COOLDOWN_SECONDS
        self.count = 0
    
    def update(self, dt):
        super().update(dt)
        self.i_frames -= dt

    def collides_with(self, other):
        pass
    
    def draw(self, screen):
        self.count += 1
        if self.i_frames < 0.5:
            pygame.draw.polygon(screen, "green", self.triangle(), 0)
            pygame.draw.polygon(screen, (0,160,0), self.triangle(), 3)
        elif self.count < 2:
            pygame.draw.polygon(screen, "green", self.triangle(), 0)
            pygame.draw.polygon(screen, (0,160,0), self.triangle(), 3)
        elif self.count >= 3:
            self.count = 0

class Dead_Player(Player):
    def __init__(self, x, y):
        super().__init__(x, y, 0)
        self.respawn_cooldown = 1

    def collides_with(self, other):
        pass
    
    def update(self, dt):
        self.respawn_cooldown -= dt