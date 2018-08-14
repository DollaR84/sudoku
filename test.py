"""
Test create sudoku.

Created on 13.08.2018

@author: Ruslan Dolovanyuk

"""

import copy
import random

from solver import solve_sudoku

from sudoku import Generator


def create_sudoku():
    """Generate and check sudoku."""
    gen = Generator()
    grid = gen.get_grid_2x(gen.mix(gen.get_base_grid()))
    flook = [[False for j in range(gen.size)] for i in range(gen.size)]
    iterator = 0
    difficult = gen.n ** 4
    while iterator < gen.n ** 4:
        i = random.randrange(gen.size)
        j = random.randrange(gen.size)
        if not flook[i][j]:
            flook[i][j] = True
            iterator += 1
            temp = grid[i][j]
            grid[i][j] = 0
            difficult -= 1
            grid_solution = copy.deepcopy(grid)
            solutions = 0
            for solution in solve_sudoku((gen.n, gen.n), grid_solution):
                solutions += 1
            if 1 != solutions:
                grid[i][j] = temp
                difficult += 1
    return grid, difficult


def show(grid, difficult):
    """Show sudoku."""
    print('Difficult: %d' % difficult)
    for row in grid:
        line = [str(value) for value in row]
        print(' '.join(line))


if '__main__' == __name__:
    show(*create_sudoku())
