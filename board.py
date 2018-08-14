"""
Board for sudoku.

Created on 14.08.2018

@author: Ruslan Dolovanyuk

"""

import pygame

from cell import Cell

from constants import Colors


class Board:
    """Board class for sudoku."""

    def __init__(self, config, screen):
        """Initialize board class."""
        self.config = config
        self.screen = screen

        self.ROWS = 9
        self.COLS = 9
        self.size_cell = self.config.getint('board', 'size_cell')
        self.cells = []

        self.board = pygame.Surface(self.get_sizes())
        self.calc_offset()

    def get_sizes(self):
        """Return calculated sizes x and y."""
        return (self.COLS*self.size_cell, self.ROWS*self.size_cell)

    def calc_offset(self):
        """Calculate position board on screen."""
        screen_x = self.config.getint('screen', 'size_x')
        screen_y = self.config.getint('screen', 'size_y')
        board_sizes = self.get_sizes()
        board_x = board_sizes[0]
        board_y = board_sizes[1]

        offset_x = (screen_x - board_x) // 2
        offset_y = (screen_y - board_y) // 2

        self.offset = (offset_x, offset_y)

    def draw(self):
        """Draw method for board."""
        self.screen.blit(self.board, self.offset)
        for cell in self.cells:
            cell.draw(self.board)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                pygame.draw.rect(self.board, Colors.WHITE, (col*self.size_cell, row*self.size_cell, self.size_cell, self.size_cell), 1)

    def init_cells(self, grid):
        """Initialize cells from grid."""
        self.cells.clear()
        for row in range(self.ROWS):
            for col in range(self.COLS):
                self.cells.append(Cell(col*self.COLS, row*self.ROWS, self.size_cell, grid[row][col]))
