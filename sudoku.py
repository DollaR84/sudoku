"""
Module generator base grid and random mixing.

Created on 11.08.2018

@author: Ruslan Dolovanyuk

"""

import random

from copy import copy


class Generator:
    """Main generator for sudoku."""
    n = property(lambda self: self.__N)
    size = property(lambda self: self.__size)

    def __init__(self, n=3):
        """Initialize generator."""
        self.__N = n
        self.__size = self.n * self.n
        random.seed()

        self.__generate_base_grid()

    def __generate_base_grid(self):
        """Generate base grid."""
        std_row = [num for num in range(1, self.size+1)]
        self.__base_grid = []
        for block in range(self.n):
            for row in range(self.n):
                self.__base_grid.extend(std_row[row*3+block:]+std_row[:row*3+block])

    def get_base_grid(self):
        """Return base grid."""
        return copy(self.__base_grid)

    def transposing(self, grid):
        """Transposing grid 9x9."""
        rows = self.size
        cols = self.size
        transpose_grid = [0]*rows*cols
        for row in range(rows):
            for col in range(cols):
                transpose_grid[col*cols+row] = grid[row*rows+col]
        return transpose_grid

    def swap_rows(self, grid):
        """Swap random beside rows in grid 9x9."""
        area = random.randrange(self.n)
        line1, line2 = random.sample(range(self.n), 2)
        start1 = (area * self.n * self.size) + (line1 * self.size)
        start2 = (area * self.n * self.size) + (line2 * self.size)
        for index in range(self.size):
            grid[start1+index], grid[start2+index] = grid[start2+index], grid[start1+index]
        return grid

    def swap_cols(self, grid):
        """Swap random beside cols in grid 9x9."""
        return self.transposing(self.swap_rows(self.transposing(grid)))

    def swap_area_horizontal(self, grid):
        """Swap random beside area on horizontal in grid 9x9."""
        area1, area2 = random.sample(range(self.n), 2)
        start1 = area1 * self.n * self.size
        start2 = area2 * self.n * self.size
        for row in range(self.n):
            row = row * self.size
            for index in range(self.size):
                grid[start1+row+index], grid[start2+row+index] = grid[start2+row+index], grid[start1+row+index]
        return grid

    def swap_area_vertical(self, grid):
        """Swap random beside area vertical in grid 9x9."""
        return self.transposing(self.swap_area_horizontal(self.transposing(grid)))

    def mix(self, grid, amt=10):
        """Random mix functions shuffle grid 9x9.
           amt - set steps for mix.
        """
        mix_func = (
                    self.transposing,
                    self.swap_rows,
                    self.swap_cols,
                    self.swap_area_horizontal,
                    self.swap_area_vertical
                   )

        for i in range(amt):
            grid = random.choice(mix_func)(grid)
        return grid

    def get_grid_2x(self, grid):
        """Return mixed grid view lists in list."""
        return [[grid[self.size*row+col] for col in range(self.size)] for row in range(self.size)]


def test_base_grid():
    """Test print base grid."""
    gen = Generator()
    grid = gen.get_base_grid()
    print('='*15)
    print('Base grid:')
    for row in range(gen.size):
        row_str = [str(grid[row*gen.size+col]) for col in range(gen.size)]
        print(' '.join(row_str))
    print('='*15)


def test_transpose_grid():
    """Test print transpose grid."""
    gen = Generator()
    grid = gen.transposing(gen.get_base_grid())
    print('='*15)
    print('Transpose grid:')
    for row in range(gen.size):
        row_str = [str(grid[row*gen.size+col]) for col in range(gen.size)]
        print(' '.join(row_str))
    print('='*15)


def test_mix_grid():
    """Test print mix grid."""
    gen = Generator()
    grid = gen.mix(gen.get_base_grid())
    print('='*15)
    print('Mix grid:')
    for row in range(gen.size):
        row_str = [str(grid[row*gen.size+col]) for col in range(gen.size)]
        print(' '.join(row_str))
    print('='*15)


if "__main__" == __name__:
    test_base_grid()
    test_transpose_grid()
    test_mix_grid()
