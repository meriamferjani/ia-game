import pygame
import time
import tkinter as tk
from tkinter import messagebox
import numpy as np
from MapCreator import generateMatrix

RESOLUTION = 30

# init level details
leveMatrix = generateMatrix("./assets/sprites/map2.png")
num_rows, num_cols = leveMatrix.shape
width, height = num_cols, num_rows

# Load the images to be user
wallImage = pygame.image.load("./assets/sprites/wall30.png")
grassImage = pygame.image.load("./assets/sprites/grass.png")
playerImage = pygame.image.load("./assets/sprites/player30.png")
treasureImage = pygame.image.load("./assets/sprites/treasure30.png")
skeletonImage = pygame.image.load("./assets/sprites/skeleton30.png")
nodeImage = pygame.image.load("./assets/sprites/node.png")
doorImage = pygame.image.load("./assets/sprites/door.png")
solvedDoorImage = pygame.image.load("./assets/sprites/solved.png")
unsolvedDoorImage = pygame.image.load("./assets/sprites/unsolved.png")

# Initialize Pygame
pygame.init()

# Create a screen
screen = pygame.display.set_mode((width * RESOLUTION, height * RESOLUTION))

# Maze class
class Maze:
    def __init__(self, width, height, mazeMatrix):
        self.width = width
        self.height = height
        self.end_rect = [np.where(mazeMatrix[:] == 4)[
            0][0], np.where(mazeMatrix[:] == 4)[1][0]]
        self.doors =[[3,0],[19,24],[19,4],[0,34]]
        self.solvedDoors =[]
        self.unsolvedDoors =[]
        self.start_rect = [-1,-1]
        self.cells = mazeMatrix
        self.visited = [[False for x in range(width)] for y in range(height)]
        self.path = []

    def solve(self, x, y):
        self.path.append((x, y))
        draw_maze(self)
        pygame.display.flip()
        pygame.event.pump()
        time.sleep(0.1)
        if x == self.end_rect[1] and y == self.end_rect[0]:
            return True

        directions = list(range(4))  # list of directions
        np.random.shuffle(directions)  # randomly shuffle the directions

        dx = [0, 1, 0, -1]
        dy = [-1, 0, 1, 0]
        for dir in directions:  # use shuffled directions here
            nx, ny = x + dx[dir], y + dy[dir]
            if nx >= 0 and ny >= 0 and nx < self.width and ny < self.height:
                if (self.cells[ny][nx] == 0 or self.cells[ny][nx] == 3 or self.cells[ny][nx] == 4) and (nx, ny) not in self.path:
                    if self.solve(nx, ny):
                        return True

        self.path.remove((x, y))

        draw_maze(self)
        pygame.display.flip()
        time.sleep(0.1)

        return False

# Draw the maze
def draw_maze(maze):
    for y in range(maze.height):
        for x in range(maze.width):
            rect = pygame.Rect(x * RESOLUTION, y *
                               RESOLUTION, RESOLUTION, RESOLUTION)
            if maze.cells[y][x] == 1:
                screen.blit(wallImage, rect)
            elif maze.cells[y][x] == 2:
                screen.blit(skeletonImage, rect)
            elif maze.cells[y][x] == 3:
                screen.blit(nodeImage, rect)
            elif maze.cells[y][x] == 4:
                screen.blit(treasureImage, rect)
            else:
                screen.blit(grassImage, rect)
            if len(maze.path) and (x, y) == maze.path[len(maze.path) - 1]:
                screen.blit(playerImage, rect)
    for y,x in maze.doors:
        rect = pygame.Rect(x * RESOLUTION, y * RESOLUTION, RESOLUTION, RESOLUTION)
        screen.blit(doorImage, rect)
    for y,x in maze.unsolvedDoors:
        rect = pygame.Rect(x * RESOLUTION, y * RESOLUTION, RESOLUTION, RESOLUTION)
        screen.blit(unsolvedDoorImage, rect)
    for y,x in maze.solvedDoors:
        rect = pygame.Rect(x * RESOLUTION, y * RESOLUTION, RESOLUTION, RESOLUTION)
        screen.blit(solvedDoorImage, rect)
    pygame.display.flip()


# Create and draw the maze
maze = Maze(width, height, leveMatrix)

# Game loop
running = True
while running:
    draw_maze(maze)
    maze.start_rect = [-1,-1]
    maze.path = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Left mouse button (1) is clicked
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]//RESOLUTION
            mouse_y = mouse_pos[1]//RESOLUTION
            if([mouse_y,mouse_x] in maze.doors):
                maze.start_rect[1] = mouse_pos[0]//RESOLUTION 
                maze.start_rect[0] = mouse_pos[1]//RESOLUTION   
    if(maze.start_rect[0]!=-1 and maze.start_rect[1]!=-1):
        solved = maze.solve(maze.start_rect[1], maze.start_rect[0])
        if solved:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(
                "Maze Solved", "The path to the exit has been found!")
            root.destroy()
            if(not (maze.start_rect in maze.solvedDoors)):
                maze.solvedDoors.append(maze.start_rect)
        else:
            root = tk.Tk()
            root.withdraw()
            messagebox.showinfo(
                "Maze unsolvable", "The path to the exit doesnt exist!")
            root.destroy()
            if(not (maze.start_rect in maze.unsolvedDoors)):
                maze.unsolvedDoors.append(maze.start_rect)
    

pygame.quit()
