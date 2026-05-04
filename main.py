import pygame
import sys
import time

from constants import *
from logger import log_state, log_event
from player import *
from asteroid import *
from asteroidfield import AsteroidField
from shot import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    pygame.mixer.pre_init(frequency=24000, size=-16, channels=2, buffer=512)
    pygame.init()
    pygame.time.Clock()
    death_sound = pygame.mixer.Sound("assets/sounds/30360796_8-bit-death-sound_by_alexander_blu_preview.wav")
    death_sound.set_volume(0.2)

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
    while True:

        field = AsteroidField()   
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        forward = pygame.Vector2(0, 1).rotate(180)
        right = pygame.Vector2(0, 1).rotate(180 + 90) * 15 / 1.5
        a = (145, 87) + forward * 15
        b = (145, 87) - forward * 15 - right
        c = (145, 87) - forward * 15 + right
        triangle = [a,b,c]
        
        dt = 0
        score = 0
        lives = 3
        life_reward = 2500
        gamestate = "RUNNING"
        while True:
            log_state()
            text_surface = font.render(f"Score {str(score)}", True, (255, 255, 255))
            text_surface_lives = font.render(f"Lives {str(lives)}", True, (255, 255, 255))
            text_surface_gameover = font.render("Game over", True, (255, 255, 255)) 
            text_surface_playagain = font.render("Press R to Restart", True, (255, 255, 255))
            text_surface_quit = font.render("Press Q to Quit", True, (255, 255, 255)) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(1)
            
            screen.fill("black")

            if gamestate == "GAMEOVER":               
                screen.blit(text_surface_gameover, (SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 2 - 100))
                screen.blit(text_surface_playagain, (SCREEN_WIDTH / 2 / 2 - 30, SCREEN_HEIGHT / 2))
                screen.blit(text_surface_quit, (SCREEN_WIDTH / 2 + 60, SCREEN_HEIGHT / 2))
                pygame.display.flip()
                if pygame.key.get_pressed()[pygame.K_r]:
                    player.kill()
                    field.kill()
                    for shot in shots:
                        shot.kill()
                    for asteroid in asteroids:
                        asteroid.kill()
                    break
                if pygame.key.get_pressed()[pygame.K_q]:
                    sys.exit(1)
            
            if gamestate == "RUNNING":
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
                    if player.collides_with(asteroid):
                        log_event("player_hit")               
                        if lives == 0:
                            death_sound.play(fade_ms=100)
                            gamestate = "GAMEOVER"
                        else:
                            lives -= 1
                            player.kill()
                            player = Dead_Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                            death_sound.play(fade_ms=100)
                    for shot in shots:
                        if shot.collides_with(asteroid):
                            log_event("asteroid_shot")
                            shot.kill()
                            add_score = asteroid.split()
                            score += add_score
                            if score > life_reward:
                                lives += 1
                                if life_reward == 10000:
                                    life_reward = 12500
                                life_reward *= 2

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
