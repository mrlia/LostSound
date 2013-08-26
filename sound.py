import os.path
import pygame
from pygame.locals import *

#Create the relative path to the data
main_dir = os.path.split(os.path.abspath(__file__))[0]

class noSound:
    """This class is in case the sound fails."""
    def play(self): pass

def load_sound(file):
    """Load a sound file"""
    if not pygame.mixer: return noSound()
    file = os.path.join(main_dir, 'data', file)
    try:
        sound = pygame.mixer.Sound(file)
        return sound
    except pygame.error:
        print ('The sound %s can not be loaded' % file)
    return noSound()

def load_sounds(*files):
    """Load several sounds and returns a list."""
    sounds = []
    for file in files:
        sounds.append(load_sound(file))
    return sounds
