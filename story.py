import pygame
from pygame.locals import *

class Help(pygame.sprite.Sprite):
    """This class represents the helo dialogs that will appear on the level"""
    pos = [0, -320, -850, -3800]
    msg = ["Seems that you lost the sound and it's been scattered all over the place in the form of musical notes, you'll have to get them back!\nLook! You have the first one right there, so lucky!", \
           "Ohh! Fairies have appear, and they have different colours! \nMaybe shooting with the note you just got of the same colour, they'll die sooner and you'll get more points on your way.\n\n[Use the D and S keys to change the note as you keep gathering them.\nAnd the SPACE to shoot]",\
           "That stave blocks the way. \nSeems that it has some colour, do you have any idea?",\
           "That stave also has a colour... what can be done to get up there?",\
           ]
    def __init__(self, playerPos, screenSpeed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.font = pygame.font.Font(None, 20)
        self.font.set_italic(1)
        self.color = Color('white')
        self.rectSize = (250,200)
        self.image = pygame.Surface(self.rectSize, SRCALPHA)
        self.rect = self.image.get_rect(topleft=(400,200))
        self.playerPos = playerPos
        self.lastPlayerPos = playerPos
        self.speedX = screenSpeed+2
   
    def updatePlayerPos(self,playerPos):
        self.playerPos = playerPos

    def update(self):
        """Update the help dialogs depending on the positions of the player"""
        for i in range(len(self.pos)):
            if (self.playerPos <= self.pos[i]) and (self.playerPos >= self.pos[i]-15):
                rect = Rect(0,0,self.rectSize[0],self.rectSize[1])
                self.image = self.render(self.msg[i], self.font, self.color, rect)
                self.rect = self.image.get_rect(topleft=(-self.pos[i]+100,250))

        if not (self.playerPos == self.lastPlayerPos):
            if self.playerPos < self.lastPlayerPos:
                self.rect.move_ip(-self.speedX,0)
            else:
                self.rect.move_ip(self.speedX,0)
        self.lastPlayerPos = self.playerPos

    def render(self, string, font, text_color, rect, justification=0):
        """Returns a Surface from a given text. With the text correctly set on the place given"""
        final_lines = []
        requested_lines = string.splitlines()

        # Make the lines fit in the rectangle
        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                # If some word is too long to fit, exit
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        raise TextRectException, "The word" + word + " is too long to fit in the rect given."
                # New line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Create the new line while the words fit
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        # Write the text on the Surface
        surface = pygame.Surface(self.rectSize, SRCALPHA)

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect.height:
                raise TextRectException, "The text is too long to fit on the rect due to height."
            if line != "":
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise TextRectException, "Justification not valid: " + str(justification)
            accumulated_height += font.size(line)[1]

        return surface
