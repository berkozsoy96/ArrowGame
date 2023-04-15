import pygame
from pygame import Rect
from pygame.font import Font
from pygame.sprite import Sprite, AbstractGroup, Group

import random


class Tile(Sprite):
    _possible_values = [0, 1, 2, 3]
    _colors = {
        "0": pygame.Color(10, 10, 10),
        "1": pygame.Color(25, 25, 25),
        "2": pygame.Color(50, 50, 50),
        "3": pygame.Color(75, 75, 75),
        "4": pygame.Color(100, 100, 100),
        "5": pygame.Color(125, 125, 125)
    }

    def __init__(self, size: int, margin: int, position: tuple[int, int], *groups: AbstractGroup) -> None:
        super().__init__(*groups)
        self.size = size
        self.margin = margin
        self.position = position  # row, col (y, x)
        self.value = random.choice(Tile._possible_values)
        self.color = Tile._colors[str(self.value)]
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
        return f"Tile at {self.position} with value {self.value}"

    def update_image(self):
        text_surface = self.font.render(
            str(self.value+1), True, pygame.Color(255, 255, 255))
        self.image.fill(self.color)
        self.image.blit(text_surface, Rect(37, 37, 13, 24))

    def change_value(self):
        self.value += 1
        self.value %= len(Tile._possible_values)
        self.color = Tile._colors[str(self.value)]

    def update(self, mouse_pos):
        # mouse_pos -> x, y
        if self.rect.left <= mouse_pos[0] <= self.rect.right and self.rect.top <= mouse_pos[1] <= self.rect.bottom:
            self.change_value()
            self.update_image()

            for neighbour in self.neighbours:
                neighbour.change_value()
                neighbour.update_image()


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.window_size = (410, 410)
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("Arrow Puzzle")
        self.font = Font(None, 36)
        self.bg_color = pygame.Color(68, 70, 84)

        self.grid_size = 4
        self.cell_size = 90
        self.cell_margin = 10

        self.board = Group()
        self.create_board()

    def create_board(self):
        grid: list[list[Tile]] = []
        for i in range(self.grid_size):
            row: list[Tile] = []
            for j in range(self.grid_size):
                row.append(Tile(self.cell_size, self.cell_margin, (i, j)))
                # self.board.add(Tile(self.cell_size, self.cell_margin, (i, j)))
            grid.append(row)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                for m in range(-1, 2):
                    if not (0 <= i + m < self.grid_size):
                        continue
                    for n in range(-1, 2):
                        if not (0 <= j + n < self.grid_size):
                            continue
                        if m == 0 and n == 0:
                            continue
                        grid[i][j].neighbours.append(grid[i + m][j + n])
                self.board.add(grid[i][j])

    def check_win(self):
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


if __name__ == "__main__":
    game = Game()
    game.main_loop()
