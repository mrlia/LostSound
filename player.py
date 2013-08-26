import pygame

class Player(pygame.sprite.Sprite):
    """This class represents the player and its methods"""
    jumpSpeed = -1
    notes = []
    def __init__(self,speedX,floorrect):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.notes = []
        self.imageCont = 0
        self.imageNum = 1
        self.image = self.images[self.imageNum]
        self.floor = floorrect
        self.rect = self.image.get_rect(bottom=self.floor.bottom)
        self.reloading = 0
        self.climbed = 0
        self.climbedB = 0
        self.jumping = 0
        self.jumpBase = self.floor.bottom
        self.speedX = speedX
        self.speedY = 0
        self.origtop = self.rect.top
        self.facingX = 1
        self.selectedNote = -1
        self.noteIndex = -1
        self.changing = 0

    def move(self,directionX,time):
        """Move the player, based on the direction, speed and time"""
        displacementX = directionX*self.speedX*time
        displacementY = self.speedY*time
        self.rect.move_ip(displacementX,displacementY)
        self.rect = self.rect.clamp(self.floor)

        if self.imageCont == 3:
            if directionX < 0:
                if self.imageNum <= 3 or self.imageNum >=7:
                    self.imageNum = 4
                else:
                    self.imageNum = self.imageNum+1
                self.image = self.images[self.imageNum]
                self.facingX = directionX
            elif directionX > 0:
                if self.imageNum >= 3:
                    self.imageNum = 0
                else:
                    self.imageNum = self.imageNum+1
                self.image = self.images[self.imageNum]
                self.facingX = directionX
            self.imageCont = 0
        else:
            self.imageCont = self.imageCont +1

    def position(self,pos):
        """Modify the player position"""
        self.rect.move_ip(pos)
        
    def setJumpBase(self,base):
        """Set the base of the players jump"""
        self.jumpBase = base

    def setSpeed(self,x,y):
        """Set the speed x and y"""
        self.speedX = x
        self.speedY = y

    def gravity(self,x,y):
        """Create the gravity effect"""
        self.speedX = self.speedX + x
        self.speedY = self.speedY + y

    def gunPos(self):
        """Calculate the position from where the shot will start"""
        if self.facingX >0:
            pos = self.rect.midright
        elif self.facingX <0:
            pos = self.rect.midleft
        return pos

    def insertNote(self,note):
        """Insert obtained notes"""
        inserted = 0
        if len(self.notes) > 1:
            if note < self.notes[0]:
                self.notes.insert(0,note)
                inserted = 1
            else:            
                for i in range(len(self.notes)-1):
                    if note > self.notes[i] and note < self.notes[i+1]:
                        self.notes.insert(i+1,note)
                        inserted = 1
            if not inserted:
                self.notes.append(note)
        elif len(self.notes) == 1:
            if note > self.notes[0]:
                self.notes.append(note)
            else:
                self.notes.insert(0,note)
        elif len(self.notes) == 0:
            self.notes.append(note)
            
    def selectNote(self,up,down):
        """Select the note to shoot"""
        if len(self.notes) != 0:
            if self.noteIndex == -1:
                self.noteIndex = 0
            else:
                if down and not (self.noteIndex == 0):
                    self.noteIndex = self.noteIndex-1
                elif up and not (self.noteIndex == 6):
                    if not (self.noteIndex+2 > len(self.notes)):
                        self.noteIndex = self.noteIndex+1
            self.selectedNote = self.notes[self.noteIndex]
            
    def gameEnded(self):
        """Check if the player has the 7 notes and so the level ends"""
        end = 0
        if len(self.notes) == 7:
            end = 1
        return end
        
class Shot(pygame.sprite.Sprite):
    """This class represents the player shot"""
    speed = 11
    def __init__(self, pos, facingX, id, screenRect):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.imageCont = 0
        self.image = self.images[id]
        self.id = id
        self.rect = self.image.get_rect(midbottom=pos)
        self.facing = facingX
        if self.facing < 0:
            self.image = pygame.transform.flip(self.images[id], 1, 0)
        elif self.facing > 0:
            self.image = self.images[id]
        self.screenRect = screenRect

    def update(self):
        """Update the status, position and image of the shot"""
        if self.imageCont == 6:
            if self.facing >0:
                self.image = pygame.transform.rotate(self.image, 90)
                if self.rect.left >= self.screenRect.right:
                    self.kill()
            elif self.facing <0:
                self.image = pygame.transform.rotate(self.image, -90)
                if self.rect.right <= self.screenRect.left:
                    self.kill()
            self.imageCont = 0
        else:
            self.imageCont = self.imageCont +1
        self.rect.move_ip(self.facing*self.speed, 0)

class Note(pygame.sprite.Sprite):
    """This class represents the notes the player has to gather"""
    def __init__(self,noteNum,pos,playerPos,screenSpeed):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.id = noteNum
        self.image = self.images[noteNum]
        self.rect = self.image.get_rect(topleft=pos)
        self.playerPos = playerPos
        self.lastPlayerPos = playerPos
        self.speedX = screenSpeed+2

    def updatePlayerPos(self,playerPos):
        self.playerPos = playerPos

    def update(self):
        """Update the position"""
        if not (self.playerPos == self.lastPlayerPos):
            if self.playerPos < self.lastPlayerPos:
                self.rect.move_ip(-self.speedX,0)
            else:
                self.rect.move_ip(self.speedX,0)
        self.lastPlayerPos = self.playerPos

    def kill(self):
        """Returns the id of the note once it's obtained"""
        pygame.sprite.Sprite.kill(self)
        return self.id
