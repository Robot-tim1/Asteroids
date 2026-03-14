import pygame
from constants import *
from logger import log_state
from player import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    pygame.time.Clock()
    dt = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")
        
        player.update(dt)
        player.draw(screen)

        pygame.display.flip()

        dt = pygame.time.Clock().tick(60) / 1000

if __name__ == "__main__":
    main()
