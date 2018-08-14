"""
Main module for running sudoku game.

Created on 11.08.2018

@author: Ruslan Dolovanyuk

"""

import copy
import json
import pickle
import random
import time

import pygame

from configparser import ConfigParser

from board import Board

from constants import Colors

from player import Player

from solver import solve_sudoku

from speech import Speech

from sudoku import Generator


class Game:
    """Main running class for game."""

    def __init__(self):
        """Initialize running class."""
        self.config = ConfigParser()
        self.config.read('settings.ini')
        self.size_x = self.config.getint('screen', 'size_x')
        self.size_y = self.config.getint('screen', 'size_y')

        with open('languages.json', 'r', encoding='utf8') as json_file:
            self.phrases = json.load(json_file)[self.config.get('total', 'language')]

        self.speech = Speech(self.config)
        self.speech.speak(self.phrases['start'])

        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((self.size_x, self.size_y))
        pygame.display.set_caption('Sudoku')

        self.board = Board(self.config, self.screen)
        self.player = Player(self.board, self.speech, self.phrases)
        self.game_over = True
        self.win = False
        self.handle_numbers = {'K_'+str(num): num for num in range(10)}
        self.handle_numbers.update({'K_KP'+str(num): num for num in range(10)})

        self.fontObj = pygame.font.SysFont('arial', 50)
        self.clock = pygame.time.Clock()

        self.gen = Generator()
        self.new_game()
        try:
            save_file = open('autosave.dat', 'rb')
        except IOError as e:
            pass
        else:
            with save_file:
                data = pickle.load(save_file)
                self.grid = data['grid']
                self.origin = data['origin']
                self.board.cells = data['cells']
                for cell in self.board.cells:
                    if 0 != cell.status:
                        cell.set_text()
                self.speech.speak(self.phrases['load'])
                self.player.speak()

    def mainloop(self):
        """Run main loop game."""
        self.running = True
        while self.running:
            self.handle_events()
            self.draw()

            self.clock.tick(15)
            pygame.display.flip()

        with open('autosave.dat', 'wb') as save_file:
            data = {'cells': self.board.cells, 'grid': self.grid, 'origin': self.origin}
            pickle.dump(data, save_file)
            self.speech.speak(self.phrases['save'])
        self.speech.speak(self.phrases['finish'])
        pygame.quit()

    def handle_events(self):
        """Check all game events."""
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                self.running = False
            elif pygame.KEYDOWN == event.type:
                if pygame.K_ESCAPE == event.key:
                    self.running = False
                elif pygame.K_F1 == event.key:
                    self.help()
                elif pygame.K_F5 == event.key:
                    self.new_game()
                elif pygame.K_F6 == event.key:
                    self.grid = copy.deepcopy(self.origin)
                    self.board.init_cells(self.grid)
                    self.speech.speak(self.phrases['repeat'])
                elif pygame.K_LEFT == event.key:
                    if not self.game_over:
                        self.player.move(-1, 0)
                elif pygame.K_RIGHT == event.key:
                    if not self.game_over:
                        self.player.move(1, 0)
                elif pygame.K_UP == event.key:
                    if not self.game_over:
                        self.player.move(0, -1)
                elif pygame.K_DOWN == event.key:
                    if not self.game_over:
                        self.player.move(0, 1)
                elif pygame.K_q == event.key:
                    if not self.game_over:
                        row, col = self.player.get_coord_2x()
                        top_x = self.gen.n * (row // self.gen.n)
                        top_y = self.gen.n * (col // self.gen.n)
                        nums = [str(self.grid[x][y]) for x in range(top_x, top_x+self.gen.n) for y in range(top_y, top_y+self.gen.n) if 0 != self.grid[x][y]]
                        self.speech.speak(' '.join(nums))
                elif pygame.K_w == event.key:
                    if not self.game_over:
                        row, col = self.player.get_coord_2x()
                        nums = [str(value) for value in self.grid[row] if 0 != value]
                        self.speech.speak(' '.join(nums))
                elif pygame.K_e == event.key:
                    if not self.game_over:
                        row, col = self.player.get_coord_2x()
                        nums = [str(row[col]) for row in self.grid if 0 != row[col]]
                        self.speech.speak(' '.join(nums))
                elif pygame.K_c == event.key:
                    row, col = self.player.get_coord_2x()
                    self.speech.speak('%s; %s' % (str(col+1), str(row+1)))
                for key, num in self.handle_numbers.items():
                    if getattr(pygame, key) == event.key:
                        if not self.game_over:
                            row, col = self.player.get_coord_2x()
                            self.grid[row][col] = num
                            self.board.cells[self.player.index].set_status(num)
                            self.player.speak()
                            if 0 == num:
                                self.open_cells -= 1
                            else:
                                self.open_cells += 1
                                self.check_game_status()

    def draw(self):
        """Main draw function."""
        self.screen.fill(Colors.GRAY)
        self.board.draw()
        if self.game_over:
            if self.win:
                textSurfaceObj = self.fontObj.render(self.phrases['win'], True, Colors.GREEN)
            else:
                textSurfaceObj = self.fontObj.render(self.phrases['game_over'], True, Colors.RED)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (self.size_x//2, self.size_y//2)
            self.screen.blit(textSurfaceObj, textRectObj)
        else:
            self.player.draw()

    def new_game(self):
        """Start new game."""
        self.speech.speak(self.phrases['new_game'])
        self.game_over = False
        self.create_sudoku()
        self.player.index = 0
        self.player.speak()

    def help(self):
        """Speak help for keys control game."""
        file_name = 'help_' + self.config.get('total', 'language') + '.txt'
        with open(file_name, 'r', encoding='utf8') as help_file:
            data = help_file.readlines()
            for line in [line for line in data if '\n' != line]:
                self.speech.speak(line)
                time.sleep(0.1)

    def create_sudoku(self):
        """Generate and check sudoku."""
        self.origin = self.gen.get_grid_2x(self.gen.mix(self.gen.get_base_grid()))
        self.grid = copy.deepcopy(self.origin)
        flook = [[False for j in range(self.gen.size)] for i in range(self.gen.size)]
        iterator = 0
        self.open_cells = self.gen.n ** 4
        while iterator < self.gen.n ** 4:
            i = random.randrange(self.gen.size)
            j = random.randrange(self.gen.size)
            if not flook[i][j]:
                flook[i][j] = True
                iterator += 1
                temp = self.grid[i][j]
                self.grid[i][j] = 0
                self.open_cells -= 1
                grid_solution = copy.deepcopy(self.grid)
                solutions = 0
                for solution in solve_sudoku((self.gen.n, self.gen.n), grid_solution):
                    solutions += 1
                if 1 != solutions:
                    self.grid[i][j] = temp
                    self.open_cells += 1
        self.board.init_cells(self.grid)

    def check_game_status(self):
        """Check status win or game over."""
        if (self.gen.n ** 4) == self.open_cells:
            self.game_over = True
            result = [self.grid[x][y] == self.origin[x][y] for x in range(self.gen.size) for y in range(self.gen.size)]
            self.win = all(result)
            for index, cell in self.board.cells:
                if not cell.read_only:
                    cell.color = Colors.GREEN if result[index] else Colors.RED


if __name__ == '__main__':
    game = Game()
    game.mainloop()
