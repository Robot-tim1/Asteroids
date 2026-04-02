import pygame
import sys

from constants import *
from logger import log_state, log_event
from player import *
from asteroid import *
from asteroidfield import AsteroidField
from shot import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def main():
    pygame.init()
    font = pygame.font.SysFont('Arial', 32) 
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    field = AsteroidField()   
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    pygame.time.Clock()
    dt = 0
    score = 0
    while True:
        log_state()
        text_surface = font.render(f"Score: {str(score)}", False, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")
        
        updatable.update(dt)
        
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    add_score = asteroid.split()
                    score += add_score

        for things in drawable:    
            things.draw(screen)
        
        screen.blit(text_surface, (50, 50))
        pygame.display.flip()

        dt = pygame.time.Clock().tick(60) / 1000

if __name__ == "__main__":
    main()
