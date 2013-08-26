import pygame

class Step(pygame.sprite.Sprite):
    """This class represents the static steps the player can jump on to"""
    def __init__(self,id,pos,playerPos,screenSpeed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[id]
        self.rect = self.image.get_rect(topleft=pos)
        self.playerPos = playerPos
        self.lastPlayerPos = playerPos
        self.speedX = screenSpeed+2

    def updatePlayerPos(self,playerPos):
        self.playerPos = playerPos

    def update(self):
        """Update the step position"""
        if not (self.playerPos == self.lastPlayerPos):
            if self.playerPos < self.lastPlayerPos:
                self.rect.move_ip(-self.speedX,0)
            else:
                self.rect.move_ip(self.speedX,0)
        self.lastPlayerPos = self.playerPos

class StepMove(pygame.sprite.Sprite):
    """This class represents the moving steps the player can jump on to"""
    def __init__(self,id,pos,playerPos,screenRect,screenSpeed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.id = id
        self.image = self.images[id]
        self.rect = self.image.get_rect(topleft=pos)
        self.playerPos = playerPos
        self.lastPlayerPos = playerPos
        self.active = 0
        self.facingY = -1
        self.screenRect = screenRect
        self.speedX = screenSpeed+2
        self.speedY = 4

    def updatePlayerPos(self,playerPos):
        self.playerPos = playerPos

    def update(self):
        """Update the step position"""
        if self.active:
            self.rect.move_ip(0, self.facingY*self.speedY)
            if self.rect.top <= self.screenRect.top:
                self.facingY = -self.facingY
            elif self.rect.bottom >= self.screenRect.bottom-50:
                self.facingY = -self.facingY
        
        if not (self.playerPos == self.lastPlayerPos):
            if self.playerPos < self.lastPlayerPos:
                self.rect.move_ip(-self.speedX,0)
            else:
                self.rect.move_ip(self.speedX,0)
        self.lastPlayerPos = self.playerPos

    def activate(self):
        """Activates the movement of the step"""
        self.active = 1
        self.facingY = -1

class Block(pygame.sprite.Sprite):
    """This class represents the objects that will block the way"""
    def __init__(self,id,pos,playerPos,screenSpeed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[id]
        self.id = id
        self.rect = self.image.get_rect(topleft=pos)
        self.playerPos = playerPos
        self.lastPlayerPos = playerPos
        self.speedX = screenSpeed+2

    def updatePlayerPos(self,playerPos):
        self.playerPos = playerPos

    def update(self):
        """Update the object position"""
        if not (self.playerPos == self.lastPlayerPos):
            if self.playerPos < self.lastPlayerPos:
                self.rect.move_ip(-self.speedX,0)
            else:
                self.rect.move_ip(self.speedX,0)
        self.lastPlayerPos = self.playerPos
