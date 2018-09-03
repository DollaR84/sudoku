"""
Player for sudoku.

Created on 14.08.2018

@author: Ruslan Dolovanyuk

"""

import pygame

from constants import Colors


class Player:
    """Player class for sudoku."""

    def __init__(self, board, speech, phrases):
        """Initialize player class."""
        self.board = board
        self.speech = speech
        self.phrases = phrases
        self.color = Colors.BLUE
        self.index = 0

    def draw(self):
        """Draw method for player."""
        left = self.board.cells[self.index].left
        top = self.board.cells[self.index].top
        size = self.board.cells[self.index].size
        pygame.draw.rect(self.board.board, self.color, (left, top, size, size), 1)

    def move(self, x, y):
        """Move player on board."""
        current_row, current_col = self.get_coord_2x()
        if -1 == y:
            if 0 < current_row:
                current_row += y
            else:
                self.speech.speak(self.phrases['border'])
        elif 1 == y:
            if self.board.ROWS-1 > current_row:
                current_row += y
            else:
                self.speech.speak(self.phrases['border'])
        if -1 == x:
            if 0 < current_col:
                current_col += x
            else:
                self.speech.speak(self.phrases['border'])
        elif 1 == x:
            if self.board.COLS-1 > current_col:
                current_col += x
            else:
                self.speech.speak(self.phrases['border'])

        self.index = (current_row * self.board.COLS) + current_col
        self.speak()

    def speak(self):
        """Speak information for moving cell."""
        cell = self.board.cells[self.index]
        if 0 == cell.status:
            self.speech.speak(self.phrases['empty'])
        else:
            self.speech.speak(str(cell.status))

    def get_coord_2x(self):
        """Return row and col from index."""
        row = self.index // self.board.COLS
        col = self.index % self.board.COLS
        return row, col
