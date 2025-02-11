import os
import pygame
from game_pack.params import *

x, y = 240, 150  
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}"
class Figure(pygame.sprite.Sprite):

    def __init__(self, filename, r, c, side, board):
        pygame.sprite.Sprite.__init__(self)
        original_image = pygame.image.load(os.path.dirname(__file__) + '/' + filename).convert_alpha()
        self.image = pygame.transform.smoothscale(original_image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect(topleft=(c * CELL_SIZE, r * CELL_SIZE))
        self.row = r
        self.col = c
        self.side = side
        self.board = board
        self.is_drop = False

    def set_pos(self, r, c):
        self.row = r
        self.col = c
        self.rect.left = c * CELL_SIZE
        self.rect.top = r * CELL_SIZE

    @staticmethod
    def is_valid_pos(r, c):
        if 0 <= r <= 7 and 0 <= c <= 7:
            return True
        else:
            return False



class King(Figure):

    def __init__(self, r, c, side, board):
        Figure.__init__(self, 'sprites/' + side + 'King.png', r, c, side, board)

    def get_actions(self):
        result = []
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

        for delta_row, delta_col in offsets:
            r1 = self.row + delta_row
            c1 = self.col + delta_col
            if not self.is_valid_pos(r1, c1):
                continue
            result.append((r1, c1))
        return result


class Queen(Figure):

    def __init__(self, r, c, side, board):
        Figure.__init__(self, 'sprites/' + side + 'Queen.png', r, c, side, board)

    def get_actions(self):
        result = []
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1), (-1, 1), (1, 1), (1, -1), (-1, -1)]

        for delta_row, delta_col in offsets:
            mul = 0
            while True:
                mul += 1
                r1 = self.row + mul * delta_row
                c1 = self.col + mul * delta_col
                if not self.is_valid_pos(r1, c1):
                    break
                result.append((r1, c1))
                figure = self.board.get_figure(r1, c1)
                if figure is not None:
                    break

        return result


class Rook(Figure):

    def __init__(self, r, c, side, board):
        Figure.__init__(self, 'sprites/' + side + 'Rook.png', r, c, side, board)

    def get_actions(self):
        result = []
        offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]

        for delta_row, delta_col in offsets:
            mul = 0
            while True:
                mul += 1
                r1 = self.row + mul * delta_row
                c1 = self.col + mul * delta_col
                if not self.is_valid_pos(r1, c1):
                    break
                result.append((r1, c1))
                figure = self.board.get_figure(r1, c1)
                if figure is not None:
                    break

        return result


class Bishop(Figure):

    def __init__(self, r, c, side, board):
        Figure.__init__(self, 'sprites/' + side + 'Bishop.png', r, c, side, board)

    def get_actions(self):
        result = []
        offsets = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

        for delta_row, delta_col in offsets:
            mul = 0
            while True:
                mul += 1
                r1 = self.row + mul * delta_row
                c1 = self.col + mul * delta_col
                if not self.is_valid_pos(r1, c1):
                    break
                result.append((r1, c1))
                figure = self.board.get_figure(r1, c1)
                if figure is not None:
                    break
        return result


class Knight(Figure):

    def __init__(self, r, c, side, board):
        Figure.__init__(self, 'sprites/' + side + 'Knight.png', r, c, side, board)

    def get_actions(self):
        result = []

        offsets = [(-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        for delta_row, delta_col in offsets:
            r1 = self.row + delta_row
            c1 = self.col + delta_col
            if not self.is_valid_pos(r1, c1):
                continue
            result.append((r1, c1))
        return result


class Pawn(Figure):

    def __init__(self, r, c, side, board):
        Figure.__init__(self, 'sprites/' + side + 'Pawn.png', r, c, side, board)

        if self.row == 1:
            self.direction = 1
        if self.row == 6:
            self.direction = -1

    def get_actions(self, *args):
        result = []

        if PAWN_MOVES in args or not args:
            r1 = self.row + self.direction
            c = self.col
            if self.is_valid_pos(r1, c):
                if self.board.get_figure(r1, c) is None:
                    result.append((r1, c))

            if self.row == 1 or self.row == 6:
                r2 = self.row + 2 * self.direction
                if self.is_valid_pos(r2, c):
                    if self.board.get_figure(r1, c) is None and self.board.get_figure(r2, c) is None:
                        result.append((r2, c))

        if PAWN_TAKES in args or not args:
            offsets = (-1, 1)
            r1 = self.row + self.direction
            for offset in offsets:
                c1 = self.col + offset
                if not self.is_valid_pos(r1, c1):
                    continue
                result.append((r1, c1))
        return result
