import random

from circleshape import *
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (176, 144, 112), self.position, self.radius, 0)
        pygame.draw.circle(screen, (146, 114, 82), self.position, self.radius, 3)

    def update(self, dt):
        self.position += (self.velocity * dt)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return 100
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        vel1 = self.velocity.rotate(angle)
        vel2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position[0], self.position[1], new_radius)
        asteroid2 = Asteroid(self.position[0], self.position[1], new_radius)
        
        asteroid1.velocity = vel1 * 1.2
        asteroid2.velocity = vel2 * 1.2

        if self.radius == ASTEROID_MIN_RADIUS * 2:
            return 50
        else:
            return 25