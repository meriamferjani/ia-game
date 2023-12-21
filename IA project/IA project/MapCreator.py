from PIL import Image
import numpy as np


def generateMatrix(map):
    image = Image.open(map)
    width, height = image.size
    matrix = np.zeros((height, width))
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            if (pixel == (255, 255, 255) or pixel == (255, 255, 255, 255)):
                matrix[y][x] = 0
            elif (pixel == (255, 0, 0) or pixel == (255, 0, 0, 255)):
                matrix[y][x] = 2  # 2 for trap
            elif (pixel == (0, 255, 0) or pixel == (0, 255, 0, 255)):
                matrix[y][x] = 3  # 3 for node
            elif (pixel == (0, 0, 255) or pixel == (0, 0, 255, 255)):
                matrix[y][x] = 4  # 4 for treasure
            elif (pixel == (0, 0, 0) or pixel == (0, 0, 0, 255)):
                matrix[y][x] = 1
            else:
                matrix[y][x] = 1
    return matrix
