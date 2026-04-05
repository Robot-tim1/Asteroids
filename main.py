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
    respawned = pygame.sprite.Group()
    dead = pygame.sprite.Group()

    Dead_Player.containers = (updatable, dead)
    Respawned_Player.containers = (updatable, drawable, respawned)
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (shots, updatable, drawable)

    field = AsteroidField()   
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    forward = pygame.Vector2(0, 1).rotate(180)
    right = pygame.Vector2(0, 1).rotate(180 + 90) * 15 / 1.5
    a = (145, 87) + forward * 15
    b = (145, 87) - forward * 15 - right
    c = (145, 87) - forward * 15 + right
    triangle = [a,b,c]
    
    pygame.time.Clock()
    dt = 0
    score = 0
    lives = 3
    while True:
        log_state()
        text_surface = font.render(f"Score {str(score)}", True, (255, 255, 255))
        text_surface_lives = font.render(f"Lives {str(lives)}", True, (255, 255, 255)) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")

        updatable.update(dt)
        
        if player in dead:
            if player.respawn_cooldown <= 0:
                player.kill()
                player = Respawned_Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

        if player in respawned:
            if player.i_frames <= 0:
                player.kill()
                player = Player(player.position[0], player.position[1], player.rotation, player.cooldown)
        
        for asteroid in asteroids:
            if player not in dead:
                if player.collides_with(asteroid):
                    log_event("player_hit")               
                    if lives == 0:
                        print("Game over!")
                        sys.exit()
                    else:
                        lives -= 1
                        player.kill()
                        player = Dead_Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    shot.kill()
                    add_score = asteroid.split()
                    score += add_score

        for things in drawable:    
            things.draw(screen)
        screen.blit(text_surface_lives, (30, 70))
        screen.blit(text_surface, (30, 20))
        pygame.draw.polygon(screen, "black", triangle, 0)
        pygame.draw.polygon(screen, "white", triangle, 3)
        
        pygame.display.flip()

        dt = pygame.time.Clock().tick(60) / 1000

if __name__ == "__main__":
    main()
