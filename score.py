import pygame
from pygame.locals import *

class Score(pygame.sprite.Sprite):
    """This class represents the notes the player has obtained"""
    notesImages = []
    def __init__(self,pos,screenSpeed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((100,410), SRCALPHA)
        self.rect = self.image.get_rect(topleft=pos)
        self.speedX = screenSpeed+2

    def addNote(self,id):
        """Insert a new note on the list"""
        pos = (10,id*60)
        self.image.blit(self.notesImages[id],pos)            
        
class ScoreF(pygame.sprite.Sprite):
    """This class represents the player score"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('white')
        self.lastscore = -1
        self.update()
        self.rect = self.image.get_rect().move(20, 20)

    def addPoints(self,points):
        self.score = self.score + points

    def getScore(self):
        return self.score

    def update(self):
        """Update the player score"""
        if self.score != self.lastscore:
            self.lastscore = self.score
            msg = "Puntuacion: %d" % self.score
            self.image = self.font.render(msg, 0, self.color)

def game_end(score):
    font = pygame.font.Font(None, 40)
    font.set_italic(1)
    color = Color('white')
    msg = "The 7 notes have been gathered!!! Final score: %d" % score
    text = font.render(msg, 1, color)
    textPos = text.get_rect()
    return text, textPos
