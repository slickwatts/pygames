# ====================================
#            Berry Class
#
# Author: Slick
# Date  :
# ====================================
import pygame
import random as r


class Berry:
    def __init__(self, game):
        self.image     = pygame.image.load("berry.bmp")
        # Berry rectangle value
        self.rect      = self.image.get_rect()
        # Berry x value (screen can fit 40 units across)
        self.x         = r.randint(1, 38)
        # Berry y value (screen can fit 30 units vertical)
        self.y         = r.randint(1, 28)
        # Left side of berry value (times 16 because cell is 16x16)
        self.rect.left = self.x * 16
        # Top of berry cell value
        self.rect.top  = self.y * 16
