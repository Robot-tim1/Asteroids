import pygame
from constants import *
from logger import log_state

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.time.Clock()
    dt = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")

        pygame.display.flip()

        dt = pygame.time.Clock().tick(60) 


if __name__ == "__main__":
    main()
