# ====================================
#       Snake Game [Main]
#
# Author: Slick
# Date  : 2020-08-17
# ====================================
import pygame
import sys
from settings import Settings
from berry import Berry
from snake import Snake
from wall import Wall
from position import Position


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.settings  = Settings()
        self.fps_clock = pygame.time.Clock()
        self.surface   = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption("Snake")
        self.center_x  = self.surface.get_width() / 2
        self.center_y  = self.surface.get_height() / 2
        self.font      = pygame.font.Font(None, 32)

        self.quit_game = False
        self.is_playing = (self.settings.lives >= 0)
        self.snake_map = self.settings.load_map()
        self.berry = Berry(self)
        self.snake_head_pos = self.settings.blocks[0]
        self.snake_speed = 45
        self.wall_bricks = []

    def draw_game_over(self):
        text1 = self.font.render("GAME OVER BITCH", 1, (255, 0, 0))
        text2 = self.font.render("SPACE to play again or Q to quit", 1, (0, 255, 255))
        text1_pos = text1.get_rect(centerx=self.center_x, top=self.center_y - 48)
        text2_pos = text2.get_rect(centerx=self.center_x, top=self.center_y)
        self.surface.blit(text1, text1_pos)
        self.surface.blit(text2, text2_pos)

    def draw_game_objects(self):
        self._draw_walls(self.surface, Wall().image, self.settings.load_map())
        self.surface.blit(self.berry.image, self.berry.rect)
        self._draw_snake(self.surface, Snake().image, self.settings)
        self._draw_data()

    def _draw_walls(self, surface, image, map_):
        row = 0
        for line in map_:
            col = 0
            for char in line:
                if char == "1":
                    width = image.get_width()
                    height = image.get_height()
                    img_rect = pygame.Rect(col, row, width, height)
                    self.wall_bricks.append((col, row))
                    img_rect.left = col * 16
                    img_rect.top  = row * 16
                    surface.blit(image, img_rect)
                col += 1
            row += 1

    def _draw_snake(self, surface, image, game_data):
        first = True
        for block in game_data.blocks:
            dest = (block.x * 16, block.y * 16, 16, 16)
            if first:
                first = False
                src = (((self.settings.direction * 2) + self.settings.frame) * 16, 0, 16, 16)
            else:
                src = (8 * 16, 0, 16, 16)
            self.surface.blit(image, dest, src)

    def _draw_data(self):
        text = self.font.render(f"Lives: {self.settings.lives} || Level: {self.settings.level} || Score: {self.settings.score}", 1, (255, 255, 255))
        text_pos = text.get_rect(centerx=self.center_x, top=self.surface.get_rect().top + 50)
        self.surface.blit(text, text_pos)

    def _handle_events(self):
        if self.settings.lives < 0:
            self.draw_game_over()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                self.is_playing = True
                self._reset_snake()
                self.settings.lives = 3
                self.settings.score = 0
                self.settings.level = 1
                self._reposition_berry()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            # mouse click is for testing
            elif event.type == pygame.MOUSEBUTTONDOWN:  # if mouse clicked lose life
                self.settings.lives -= 1
            self._handle_direction_change(event)

    def _handle_direction_change(self, event):
        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] and self.settings.direction != 1:
                self.settings.direction = 0
            elif keys[pygame.K_LEFT] and self.settings.direction != 0:
                self.settings.direction = 1
            elif keys[pygame.K_UP] and self.settings.direction != 3:
                self.settings.direction = 2
            elif keys[pygame.K_DOWN] and self.settings.direction != 2:
                self.settings.direction = 3

    def _reset_snake(self):
        self.settings.blocks = self.settings.blocks[:2]
        self.settings.direction = 0
        self.snake_head_pos.x = 20
        self.snake_head_pos.y = 15
        self.snake_speed = 60

    def _collision_check(self):
        self._hit_berry_check()
        self._hit_wall_check()
        self._hit_self_check()

    def _hit_berry_check(self):
        """Checks if snake hits berry, if it does, add block to snake"""
        # If snake head collides with berry
        if self.snake_head_pos.x == self.berry.x and self.snake_head_pos.y == self.berry.y and self.settings.lives >= 0:
            self._reposition_berry()
            self.snake_speed += 10
            self.settings.score += 5
            self.settings.berry_count += 1
            # Adding the extra block to the snake after berry eaten
            if self.settings.direction == 1:
                self.settings.blocks.append(Position(self.settings.blocks[-1].x + 1, self.settings.blocks[-1].y))
            elif self.settings.direction == 0:
                self.settings.blocks.append(Position(self.settings.blocks[-1].x - 1, self.settings.blocks[-1].y))
            elif self.settings.direction == 2:
                self.settings.blocks.append(Position(self.settings.blocks[-1].x, self.settings.blocks[-1].y + 1))
            elif self.settings.direction == 3:
                self.settings.blocks.append(Position(self.settings.blocks[-1].x, self.settings.blocks[-1].y - 1))
            # Gain level every 5 berries eaten
            if self.settings.berry_count % 5 == 0:
                self.settings.level += 1
                self.settings.score += 100
        # If game over
        elif self.settings.lives < 0 and self.snake_head_pos.x == self.berry.x and self.snake_head_pos.y == self.berry.y:
            self._reposition_berry()

    def _hit_wall_check(self):
        for brick in self.wall_bricks:
            if self.snake_head_pos.x == brick[0] and self.snake_head_pos.y == brick[1] and self.settings.lives >= 0:
                self.settings.lives -= 1
                self._reset_snake()
            elif self.snake_head_pos.x == brick[0] and self.snake_head_pos.y == brick[1] and self.settings.lives < 0:
                self._reset_snake()
                self.settings.lives = -1

    def _hit_self_check(self):
        for block in self.settings.blocks[1:]:
            if self.snake_head_pos.x == block.x and self.snake_head_pos.y == block.y:
                self.settings.lives -= 1
                self._reset_snake()

    def _reposition_berry(self):
        self.berry = None
        self.berry = Berry(self)

    def update_game(self, settings, game_time):
        settings.tick -= game_time
        if settings.tick < 0:
            settings.tick += settings.speed
            settings.frame += 1
            settings.frame %= 2
            if settings.direction == 0:
                move = (1, 0)
            elif settings.direction == 1:
                move = (-1, 0)
            elif settings.direction == 2:
                move = (0, -1)
            else:
                move = (0, 1)
            new_pos = Position(self.snake_head_pos.x + move[0], self.snake_head_pos.y + move[1])
            for block in settings.blocks:
                temp = Position(block.x, block.y)
                block.x = new_pos.x
                block.y = new_pos.y
                new_pos = Position(temp.x, temp.y)

    def run_game(self):
        while self.is_playing:
            self.surface.fill((0, 0, 0))
            self._handle_events()
            self._collision_check()
            self.update_game(self.settings, self.snake_speed)
            self.draw_game_objects()
            pygame.display.update()
            self.fps_clock.tick(30)


if __name__ == "__main__":
    game = SnakeGame()
    game.run_game()
    game.draw_game_over()
