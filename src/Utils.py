import random
import pygame
import time

def printTable(table):
    for i in range(len(table)):
        if i == 0:
            print("-------------------------------")
        for j in range(len(table[i])):
            if j == 0:
                print("|", end="")
            print(" "+(("_" if (table[i][j] == 0)
                  else str(table[i][j])) + " "), end="")
            if (j+1) % 3 == 0:
                print("|", end="")
        print()
        if (i+1) % 3 == 0:
            print("-------------------------------")


def initialize(table, empty):
    fill(table)
    removeDigit(table, empty)


def solve(table, gridDisplay, empty, font, grid_node_width, grid_node_height,start):
    #time.sleep(0.25)
    box = 0
    if check(table):
        return True
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] != 0:
                continue
            box = generateBoxNumber(i, j)
            for num in range(9):
                if checkUsed(i, j, box, num+1, table):
                    table[i][j] = num+1
                    visualizeGrid(gridDisplay, table, empty, font,
                                  grid_node_width, grid_node_height,start)
                    if solve(table, gridDisplay, empty, font, grid_node_width, grid_node_height,start):
                        return True
                    table[i][j] = 0
                    visualizeGrid(gridDisplay, table, empty, font,
                                  grid_node_width, grid_node_height,start)
            return False
    return False


def checkUsed(i, j, box, number, table):
    if checkBox(number, box, table):
        if checkHorizontal(i, number, table):
            if checkVertical(j, number, table):
                return True
    return False


def check(table):
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] == 0:
                return False
    return True


def checkHorizontal(i, number, table):
    for j in range(len(table[i])):
        if number == table[i][j]:
            return False
    return True


def checkVertical(j, number, table):
    for i in range(len(table)):
        if number == table[i][j]:
            return False
    return True


def generateBoxNumber(i, j):
    if i >= 0 and i <= 2:
        if j >= 0 and j <= 2:
            return 1
        if j >= 3 and j <= 5:
            return 2
        return 3
    if i >= 3 and i <= 5:
        if j >= 0 and j <= 2:
            return 4
        if j >= 3 and j <= 5:
            return 5
        return 6
    if j >= 0 and j <= 2:
        return 7
    if j >= 3 and j <= 5:
        return 8
    return 9


def checkBox(number, box, table):
    match box:
        case 1:
            for i in range(3):
                for j in range(3):
                    if table[i][j] == number:
                        return False
        case 2:
            for i in range(3):
                for j in range(3, 6):
                    if table[i][j] == number:
                        return False
        case 3:
            for i in range(3):
                for j in range(6, 9):
                    if table[i][j] == number:
                        return False
        case 4:
            for i in range(3, 6):
                for j in range(3):
                    if table[i][j] == number:
                        return False
        case 5:
            for i in range(3, 6):
                for j in range(3, 6):
                    if table[i][j] == number:
                        return False
        case 6:
            for i in range(3, 6):
                for j in range(6, 9):
                    if table[i][j] == number:
                        return False
        case 7:
            for i in range(6, 9):
                for j in range(3):
                    if table[i][j] == number:
                        return False
        case 8:
            for i in range(6, 9):
                for j in range(3, 6):
                    if table[i][j] == number:
                        return False
        case 9:
            for i in range(6, 9):
                for j in range(6, 9):
                    if table[i][j] == number:
                        return False
    return True


def gensolve(table):
    box = 0
    if check(table):
        return True
    for i in range(len(table)):
        for j in range(len(table[i])):
            if table[i][j] != 0:
                continue
            box = generateBoxNumber(i, j)
            for num in range(9):
                if checkUsed(i, j, box, num+1, table):
                    table[i][j] = num+1
                    if gensolve(table):
                        return True
                    table[i][j] = 0
            return False
    return False


def fill(table):
    while check(table) == False:
        for i in range(len(table)):
            for j in range(len(table[i])):
                if table[i][j] != 0:
                    continue
                table[i][j] = random.randint(1, 9)
                if not gensolve(table):
                    table[i][j] = 0


def removeDigit(table, empty):
    count = int(
        input("Enter how many digits should be missing(max is 81):"))
    while count > 81 and count < 1:
        count = int(input("Enter a number between 1 and 81"))
    k = count
    while k >= 0:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if table[i][j] != 0:
            table[i][j] = 0
            empty.append((i, j))
            k -= 1
    printTable(table)
    print("Empty = "+str(count))


def createNumber(gridDisplay, font, x, y, num, color):
    if num == 0:
        return
    text = font.render(str(num), False, color)
    gridDisplay.blit(text, (x, y))


def visualizeGrid(gridDisplay, table, empty, font, grid_node_width, grid_node_height, start):
    pygame.event.get()
    pygame.display.get_surface().fill((255, 255, 255))
    size = gridDisplay.get_size()[0]
    for i in range(0, size, grid_node_width):
        x = i
        y = i
        pygame.draw.line(gridDisplay, (211, 211, 211), (x, 0), (x, size), 2)
        pygame.draw.line(gridDisplay, (211, 211, 211), (0, y), (size, y), 2)
    for i in range(0, size, grid_node_height*3):
        x = i
        y = i
        pygame.draw.line(gridDisplay, (0, 0, 0), (x, 0), (x, size), 5)
        pygame.draw.line(gridDisplay, (0, 0, 0), (0, y), (size, y), 5)
    y = (grid_node_height/2)-5
    for i in range(len(table)):
        x = (grid_node_height/2)-5
        for j in range(len(table)):
            if (i, j) in empty:
                text = font.render("_", False, (0, 0, 0))
                gridDisplay.blit(text, (x, y))
            if (i, j) in empty:
                createNumber(gridDisplay, font, x, y,
                             table[i][j], (119, 0, 200))
            else:
                createNumber(gridDisplay, font, x, y, table[i][j], (0, 0, 0))
            x += grid_node_width
        y += grid_node_height
    pygame.display.update()
