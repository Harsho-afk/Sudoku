import numpy as np
import pygame
from Utils import *

table = np.zeros((9, 9), int)
empty = []
initialize(table, empty)
# table = [[0, 0, 0, 0, 0, 6, 0, 0, 3],
#          [0, 0, 0, 0, 1, 0, 4, 0, 0],
#          [0, 4, 0, 8, 0, 0, 0, 7, 9],
#          [8, 0, 9, 0, 7, 0, 0, 6, 0],
#          [0, 6, 0, 0, 8, 0, 0, 0, 5],
#          [0, 5, 7, 0, 3, 0, 8, 0, 0],
#          [2, 0, 0, 1, 0, 9, 0, 0, 0],
#          [0, 0, 0, 5, 0, 3, 0, 0, 0],
#          [0, 0, 0, 0, 0, 0, 6, 0, 0]]
empty = []
for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 0:
                empty.append((i,j))

pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 50)
gridDisplay = pygame.display.set_mode((900, 900))
grid_node_width = 100
grid_node_height = 100
start = 50

solving = True
while solving:
    if check(table):
        solving = False
    visualizeGrid(gridDisplay, table, empty, font,
                  grid_node_width, grid_node_height, start)
    solve(table, gridDisplay, empty, font, grid_node_width, grid_node_height,start)
    visualizeGrid(gridDisplay, table, empty, font,
                  grid_node_width, grid_node_height, start)

printTable(table)
time.sleep(10)
pygame.quit()
