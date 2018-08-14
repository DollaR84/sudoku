"""
Cell on board sudoku.

Created on 14.08.2018

@author: Ruslan Dolovanyuk

"""

import pygame

from constants import Colors


class Cell:
    """Cell class on board for sudoku."""

    def __init__(self, left, top, size, status):
        """Initialize cell class."""
        self.left = left
        self.top = top
        self.size = size
        self.status = status
        self.read_only = False if 0 == self.status else True
        self.color = Colors.SILVER if 0 == self.status else Colors.GREEN

        if 0 != self.status:
            self.set_text()

    def draw(self, board):
        """Draw method for cell."""
        pygame.draw.rect(board, self.color, (self.left, self.top, self.size, self.size))
        if 0 != self.status:
            board.blit(self.textSurfaceObj, self.textRectObj)

    def set_status(self, status):
        """Set status for cell."""
        if not self.read_only:
            self.status = status
            self.color = Colors.SILVER if 0 == self.status else Colors.YELLOW
            if 0 != self.status:
                self.set_text()

    def set_text(self):
        """Set number text on cell draw."""
        fontObj = pygame.font.SysFont('arial', 24)
        self.textSurfaceObj = fontObj.render(str(self.status), True, Colors.BLUE)
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.center = (self.left+(self.size//2), self.top+(self.size//2))
