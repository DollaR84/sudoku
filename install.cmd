pyinstaller -F --noconsole ^
--add-binary board.pyd;. ^
--add-binary cell.pyd;. ^
--add-binary constants.pyd;. ^
--add-binary game.pyd;. ^
--add-binary player.pyd;. ^
--add-binary solver.pyd;. ^
--add-binary speech.pyd;. ^
--add-binary sudoku.pyd;. ^
--hidden-import pygame ^
main.pyw
