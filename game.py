import pygame
import numpy as np
from pygame import Rect
from pygame.font import Font
from pygame.sprite import Sprite, AbstractGroup, Group

import random


class Tile(Sprite):
    def __init__(self, size: int, margin: int, position: tuple[int, int], value_count: int, *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.size = size
        self.margin = margin
        self.position = position  # row, col (y, x)
        self.value_count = value_count
        self.value = random.randint(0, self.value_count-1)
        self.color_value = 50*((self.value+1)/self.value_count)
        self.neighbours: list[Tile] = []
        self.font = Font(None, 36)

        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.y = self.position[0]*self.size + \
            (self.margin*(self.position[0]+1))
        self.rect.x = self.position[1]*self.size + \
            (self.margin*(self.position[1]+1))

        self.update_image()

    def __str__(self):
        return f"Tile at {self.position} with value {self.value}"

    def __repr__(self):
        return f"{self.value}"

    def update_image(self):
        text_surface = self.font.render(
            str(self.value+1), True, pygame.Color(255, 255, 255))
        c = pygame.Color(0, 0, 0)
        c.hsva = (0.0, 0.0, self.color_value, 1.0)
        self.image.fill(c)
        self.image.blit(text_surface, Rect(37, 37, 13, 24))

    def change_value(self):
        self.value += 1
        self.value %= self.value_count
        self.color_value = 50*((self.value+1)/self.value_count)

    def rotate_tile(self):
        self.change_value()
        self.update_image()

        for neighbour in self.neighbours:
            neighbour.change_value()
            neighbour.update_image()

    def update(self, mouse_pos):
        # mouse_pos -> x, y
        if self.rect.left <= mouse_pos[0] <= self.rect.right and self.rect.top <= mouse_pos[1] <= self.rect.bottom:
            self.rotate_tile()


class Game:
    def __init__(self, grid_size, value_count) -> None:
        pygame.init()

        self.grid_size = grid_size
        self.value_count = value_count
        self.cell_size = 90
        self.cell_margin = 10

        ws = self.grid_size * \
            (self.cell_size+self.cell_margin) + self.cell_margin
        self.window_size = (ws, ws)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Arrow Puzzle")
        self.font = Font(None, 36)
        self.bg_color = pygame.Color(68, 70, 84)

        self.grid: list[list[Tile]] = []
        self.click_counts = np.ndarray(shape=(4, 4), dtype=np.int8)
        self.click_counts.fill(0)
        self.board = Group()
        self.create_board()
        self.starting_grid = self.grid.copy()

    def create_board(self):
        for i in range(self.grid_size):
            row: list[Tile] = []
            for j in range(self.grid_size):
                row.append(Tile(self.cell_size, self.cell_margin,
                           (i, j), self.value_count))
                # self.board.add(Tile(self.cell_size, self.cell_margin, (i, j)))
            self.grid.append(row)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                current_tile = self.grid[i][j]
                for m in range(-1, 2):
                    if not (0 <= i + m < self.grid_size):
                        continue
                    for n in range(-1, 2):
                        if not (0 <= j + n < self.grid_size):
                            continue
                        if m == 0 and n == 0:
                            continue
                        neighbour_tile = self.grid[i + m][j + n]
                        current_tile.neighbours.append(neighbour_tile)
                self.board.add(current_tile)

    def check_win(self):
        pygame.event.pump()
        for tile in self.board.sprites():
            tile: Tile
            if tile.value != 0:
                return False
        return True

    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.board.update(pos)
                    # print(self.grid)

            # Clear the screen
            self.screen.fill(self.bg_color)
            self.board.draw(self.screen)

            # Check if the game has been won
            if self.check_win():
                text = self.font.render(
                    "You win!", True, (pygame.Color(255, 255, 255)))
                text_rect = text.get_rect(
                    center=(self.window_size[0] // 2, self.window_size[1] // 2))
                self.screen.blit(text, text_rect)
                self.board = Group()

            # Update the screen
            pygame.display.flip()

        pygame.quit()

    def _draw(func):
        def inner(self: "Game", *args):
            pygame.event.pump()
            func(self, *args)
            self.screen.fill(self.bg_color)
            self.board.draw(self.screen)
            pygame.display.flip()
        return inner

    @_draw
    def start_drawing(self, *args):
        pass

    @_draw
    def click(self, x: int, y: int):
        self.grid[x][y].rotate_tile()
        self.click_counts[x, y] += 1

    def pause(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    running = False

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    game = Game(grid_size=4, value_count=4)
    game.main_loop()
