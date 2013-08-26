import pygame, random

MAX_FAIRY_LIVES = 3

class Fairy(pygame.sprite.Sprite):
    """This class represents the enemies of the game. 
    Receives its position, the players position, the screen Rect and screen speed."""
    def __init__(self, id, pos, playerPos, screenRect, screenSpeed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.id = id
        self.imageCont = 0
        self.imageNum = id*3
        self.imageNumMin = self.imageNum
        self.imageNumMax = self.imageNum+2
        self.image = self.images[self.imageNum]
        self.rect = self.image.get_rect(topleft=pos)
        self.playerPos = playerPos
        self.lastPlayerPos = playerPos
        self.facingY = random.choice((-1,1))
        self.lives = MAX_FAIRY_LIVES
        self.killed = 0
        self.screenRect = screenRect
        self.speedX = screenSpeed+2
        self.speedY = 8
   
    def updatePlayerPos(self,playerPos):
        self.playerPos = playerPos

    def update(self):
        """Update the status, position and image of the enemies."""
        self.rect.move_ip(0, self.facingY*self.speedY)
        if self.rect.top <= self.screenRect.top:
            self.facingY = -self.facingY
        elif self.rect.bottom >= self.screenRect.bottom-50:
            self.facingY = -self.facingY

        if self.imageCont == 6:                
            if self.imageNum == self.imageNumMax:
                self.imageNum = self.imageNumMin
            else:
                self.imageNum = self.imageNum+1
            self.image = self.images[self.imageNum]
            self.imageCont = 0
        else:
            self.imageCont = self.imageCont +1

        if not (self.playerPos == self.lastPlayerPos):
            if self.playerPos < self.lastPlayerPos:
                self.rect.move_ip(-self.speedX,0)
            else:
                self.rect.move_ip(self.speedX,0)
        self.lastPlayerPos = self.playerPos

        if self.lives == 0: self.kill()

        if self.killed and (self.rect.bottom >= self.screenRect.bottom-50):
            pygame.sprite.Sprite.kill(self)

    def kill(self):
        """Modify the enemy speed while dying."""
        self.speedY = 3
        self.facingY = 1
        self.killed = 1
