import logic
import pygame
from sys import exit
import math

mm = logic.Mastermind()

pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 450, 950


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mastermind")
pygame.display.set_icon(pygame.image.load("Mastermind/assets/images/mastermind_icon.png"))
clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill(("#252525"))
    
    pygame.display.update()
    clock.tick(60)