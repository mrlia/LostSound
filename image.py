import os.path
import pygame
from pygame.locals import *

# Check if we can load more than BMP
if not pygame.image.get_extended():
    raise SystemExit("Error: Module needed to extend the image")

# Create the relative path to the data
main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    """Load an image and returns a Surface."""
    file = os.path.join(main_dir, 'data', file)
    print(file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        print ('No se puede cargar la imagen %s' % file)
    return surface.convert()

def load_images(*files):
    """Load several images and returns a list."""
    images = []
    for file in files:
        images.append(load_image(file))
    return images

def assembleSprite(filename, size, matrix):
    """Returns a list with the images of the file.
    The size is the size of each image in pixels inside the file.
    The matrix indicates how the images are positionate (nCol,nRow)"""
    width = size[0]
    height = size[1]
    file = os.path.join(main_dir, 'data', filename)
    spritesheet = pygame.image.load(file)
    sprites = []
    for y in range(matrix[1]):
        for x in range(matrix[0]):
            image = pygame.Surface((width,height))
            w = x*width
            w2 = (x+1)*width
            h = y*height
            h2 = (y+1)*height
            rect = (w, h, w2, h2)
            image.blit(spritesheet, (0,0), rect)
            image = image.convert()
            colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
            sprites.append(image)
    return sprites

def assembleSprites(size, matrix, *files):
    """Returns a list with the images of several files.
    The size is the size of each image in pixels inside the files.
    The matrix indicates how the images are positionate (nCol,nRow)"""
    sprites = []
    for file in files:
        sprites.extend(assembleSprite(file, size, matrix))
    return sprites

