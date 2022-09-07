import time
import pygame as pg
import numpy as np


WIDTH = 550
HEIGHT = 650
background_colour = "#bde0fe"
grid = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]
buffer = 5


def number_is_possible(row, col, n):
    global grid
    # check if the number is already in the row
    for i in range(0, 9):
        if grid[row][i] == n:
            return False

    # check if the number is already in the column
    for i in range(0, 9):
        if grid[i][col] == n:
            return False

    # getting values for the grid to be checked
    row_grid = (row // 3) * 3
    col_grid = (col // 3) * 3

    # checking if the value is in the grid
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[row_grid + i][col_grid + j] == n:
                return False

    return True


def solve_grid(win):
    global grid
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for n in range(1, 10):
                    if number_is_possible(row, col, n):
                        grid[row][col] = n
                        solve_grid(win)
                        grid[row][col] = 0
                return
    time.sleep(2)
    populate_grid(win)
    input("More Solutions?")


def populate_grid(win):
    global grid
    myfont = pg.font.SysFont("Comic Sans MS", 35)
    x, y = 50, 50
    for i in range(9):
        for j in range(9):
            value = myfont.render(str(grid[i][j]), True, (0, 0, 0))
            win.blit(value, (x + 50 * j + 15, y))
            pg.display.update()
        y += 50


def insert(win, position):
    i, j = position[1], position[0]
    myfont = pg.font.SysFont("Comic Sans MS", 35)
    global grid
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

            if event.type == pg.KEYDOWN:
                if event.key == 48 or 8:
                    grid[i - 1][j - 1] = event.key - 48
                    pg.draw.rect(
                        win,
                        background_colour,
                        (
                            position[0] * 50 + buffer,
                            position[1] * 50 + buffer,
                            50 - 2 * buffer,
                            50 - 2 * buffer,
                        ),
                    )
                    pg.display.update()
                if 0 < event.key - 48 < 10:
                    pg.draw.rect(
                        win,
                        background_colour,
                        (
                            position[0] * 50 + buffer,
                            position[1] * 50 + buffer,
                            50 - 2 * buffer,
                            50 - 2 * buffer,
                        ),
                    )
                    value = myfont.render(str(event.key - 48), True, (0, 0, 0))
                    win.blit(value, (position[0] * 50 + 15, position[1] * 50))
                    grid[i - 1][j - 1] = event.key - 48
                    pg.display.update()
                    # print(np.matrix(grid))
                return
            return


def main():
    isSolved = False
    pg.init()
    myfont = pg.font.SysFont("Arial", 20)
    win = pg.display.set_mode((WIDTH, HEIGHT))
    win.fill(background_colour)
    pg.display.set_caption("Sudoku Solver")

    # creating button
    text_value = "Solve" if isSolved == False else "Solved"
    color_value = "#e76f51" if isSolved == False else "#2a9d8f"
    text = myfont.render(text_value, True, (0, 0, 0))
    pg.draw.rect(win, (color_value), (225, 550, 100, 30))
    win.blit(text, (225 + 25, 550 + 3))

    for i in range(0, 10):
        linewidth = 4 if (i) % 3 == 0 else 2
        pg.draw.line(win, (0, 0, 0), (50 + 50 * i, 50),
                     (50 + 50 * i, 500), (linewidth))
        pg.draw.line(win, (0, 0, 0), (50, 50 + 50 * i),
                     (500, 50 + 50 * i), (linewidth))

    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if (225 <= pos[0] <= 325) and (550 <= pos[1] <= 580):
                    isSolved = True
                    solve_grid(win)

            if event.type == pg.MOUSEBUTTONUP and event.button == 1:
                pos = pg.mouse.get_pos()
                if pos[0] < 50 or pos[0] > 500:
                    break
                if pos[1] < 50 or pos[1] > 500:
                    break
                insert(win, (pos[0] // 50, pos[1] // 50))

            if event.type == pg.QUIT:
                pg.quit()
                return


main()
