# ====================================
#         Snake Game Settings
#
# Author: Slick
# Date  :
# ====================================
import random as r
from position import Position


class Settings:
    def __init__(self):
        # Screen settings
        self.screen_size = (640, 480)
        self.screen_font = (None, 32)

        # Snake settings
        self.lives       = 3
        self.score       = 0
        self.is_dead     = False
        self.blocks      = []
        self.tick        = 250
        self.speed       = 250
        self.level       = 1
        self.berry_count = 0
        self.segments    = 1
        self.frame       = 0
        self.direction   = 0
        self.blocks.append(Position(20, 15))
        self.blocks.append(Position(19, 15))

        # Berry settings
        self._berry_x       = r.randint(1, 38)
        self._berry_y       = r.randint(1, 28)
        self.berry_position = Position(self._berry_x, self._berry_y)

    def load_map(self):
        with open("map_file.txt") as file:
            content = file.readlines()
        return content
