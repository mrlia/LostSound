import random
import pygame
from pygame.locals import *
from image import *
from sound import *
from player import *
from enemy import *
from score import *
from steps import *
from story import *

# Constantes
SCREENRECT = Rect(0, 0, 800, 600)
FLOORRECT = Rect(200, 0, 400, 550)
BEGIN_LVL = -10
END_LVL = -9200
SCREEN_SPEED = 10
PLAYER_SPEEDX = 0.4
PLAYER_POS = 0
MAX_SHOTS = 2

def main(winstyle = 0):
    """Funcion principal del juego. Inicializar las variables necesarias y hacer el bucle principal."""
    pygame.init()
    # Try to init the sound
    if pygame.mixer and not pygame.mixer.get_init():
        print ('Error, no hay sonido')
        pygame.mixer = None
    
    # Set the screen mode
    winstyle = RESIZABLE # FULLSCREEN for fullscreen
    bestColorDepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestColorDepth)
    
    # Load the images of the Sprite classes
    Player.images = assembleSprite('rubia.gif', (42,60), (4,2))
    Fairy.images = assembleSprites((40,40), (3,1), 'hadaDO.gif', 'hadaRE.gif', 'hadaMI.gif', 'hadaFA.gif', 'hadaSOL.gif', 'hadaLA.gif', 'hadaSI.gif')
    Step.images = load_images('pent_flores.gif', 'pent1.gif', 'pent2.gif', 'pent3.gif', 'pent4.gif', 'pent5.gif', 'pent6.gif')
    StepMove.images = [load_image('pent1_mover.gif')]
    Block.images = load_images('bloque_pent1.gif', 'bloque_pent2.gif', 'bloque_pent3.gif', 'bloque_pent4.gif', 'bloque_pent5.gif')
    Note.images = load_images('do.gif', 're.gif', 'mi.gif', 'fa.gif', 'sol.gif', 'la.gif', 'si.gif')
    Score.notesImages = load_images('do2.gif', 're2.gif', 'mi2.gif', 'fa2.gif', 'sol2.gif', 'la2.gif', 'si2.gif', 'borde.gif')
    Shot.images = load_images('do2.gif', 're2.gif', 'mi2.gif', 'fa2.gif', 'sol2.gif', 'la2.gif', 'si2.gif', 'ruido.gif')
    
    
    # Create the visualization window
    pygame.display.set_icon(load_image('icon.gif'))
    pygame.display.set_caption('Lost Sound')
    
    # Greate the background
    bgdImage  = load_image('background.bmp')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.blit(bgdImage, (0, 0))

    screen.blit(background, (0,0))
    pygame.display.flip()
    
    # Load the sound
    if pygame.mixer:
        sounds = load_sounds('do.wav', 're.wav', 'mi.wav', 'fa.wav', 'sol.wav', 'la.wav', 'si.wav', 'ruido.wav')
        dead_sound = load_sound('morir.wav')
        dead_sound.set_volume(0.5)
        for s in sounds:
            s.set_volume(0.8)
        sounds[7].set_volume(0.2)

    # Load the music    
    if pygame.mixer:
        file = os.path.join(main_dir, 'data', 'I_Talk_to_the_Rain.mp3')
        pygame.mixer.music.load(file)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1) # Makes the music sound a number of times. -1 infinite
    
    # Init the sprites Groups
    fairies = pygame.sprite.Group()
    steps = pygame.sprite.Group()
    stepsM = pygame.sprite.Group()
    blocks = pygame.sprite.Group()
    notes = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    all = pygame.sprite.Group()
    
    # Assign Sprites to the Groups
    Player.containers = all
    Fairy.containers = fairies, all
    Step.containers = steps, all
    StepMove.containers = stepsM, all
    Block.containers = blocks, all
    Note.containers = notes, all
    Shot.containers = shots, all
    Score.containers = all
    ScoreF.containers = all
    Help.containers = all
    
    # Variables needed
    clock = pygame.time.Clock()
    SELECTED_NOTE = -1
    SCORE = 0

    # Init the Sprites
    player = Player(PLAYER_SPEEDX,FLOORRECT)
    PLAYER_POS = player.rect.left

    Note(0,(500, 100),PLAYER_POS,SCREEN_SPEED)
    Note(1,(2350, 150),PLAYER_POS,SCREEN_SPEED)
    Note(2,(4000, 10),PLAYER_POS,SCREEN_SPEED)
    Note(3,(6450, 120),PLAYER_POS,SCREEN_SPEED)
    Note(4,(7250, 20),PLAYER_POS,SCREEN_SPEED)
    Note(5,(8700, 30),PLAYER_POS,SCREEN_SPEED)
    Note(6,(10150, 200),PLAYER_POS,SCREEN_SPEED)
    
    Step(0,(400,350),PLAYER_POS,SCREEN_SPEED)
    Step(3,(2400,350),PLAYER_POS,SCREEN_SPEED)
    Step(2,(3500,350),PLAYER_POS,SCREEN_SPEED)
    Step(4,(4250,250),PLAYER_POS,SCREEN_SPEED)
    Step(1,(4850,200),PLAYER_POS,SCREEN_SPEED)
    Step(5,(5670,350),PLAYER_POS,SCREEN_SPEED)
    Step(6,(6450,200),PLAYER_POS,SCREEN_SPEED)
    Step(3,(6950,200),PLAYER_POS,SCREEN_SPEED)
    Step(2,(7550,300),PLAYER_POS,SCREEN_SPEED)
    Step(1,(9150,200),PLAYER_POS,SCREEN_SPEED)
    Step(2,(10500,200),PLAYER_POS,SCREEN_SPEED)
    Step(3,(11200,350),PLAYER_POS,SCREEN_SPEED)

    StepMove(0,(8600,400),PLAYER_POS,SCREENRECT,SCREEN_SPEED)
    
    Block(0,(2200, 50),PLAYER_POS,SCREEN_SPEED)
    Block(2,(6350, 0),PLAYER_POS,SCREEN_SPEED)

    Fairy(0,(1100, 200),PLAYER_POS,SCREENRECT,SCREEN_SPEED)
    for j in range(1200,10300,150):
            i = random.randrange(0,7)
            k = random.randrange(j,j+150)
            l = random.randrange(200,450)
            appear = random.choice((0,1))
            if appear:
                Fairy(i,(k, l),PLAYER_POS,SCREENRECT,SCREEN_SPEED)
    
    score = Score((20,50),SCREEN_SPEED)
    scoreF = ScoreF()
    if pygame.font:
        all.add(scoreF)
        
    help = Help(PLAYER_POS,SCREEN_SPEED)
    
    while player.alive():
        # Set the fps
        timePassed = clock.tick(50)

        # Check if the player wants to quit and get the key pressed
        for event in pygame.event.get():
            if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
                    return
        keystate = pygame.key.get_pressed()
        
        # Clear the Sprites from the screen
        all.clear(screen, background)
        SELECTED_NOTE = player.selectedNote

        # updated all the Sprites status
        all.update()
        
        # Read the inputs and update the status variables
        directionX = keystate[K_RIGHT] - keystate[K_LEFT]
        jumpState = keystate[K_UP]
        firing = keystate[K_SPACE]
        noteUP = keystate[K_d]
        noteDOWN = keystate[K_s]

        if (noteUP or noteDOWN) and not player.changing:
            player.changing = 1
            player.selectNote(noteUP,noteDOWN)
        elif (not noteUP and not noteDOWN) and player.changing:
            player.changing = 0
                               
        if not player.reloading and firing and len(shots) < MAX_SHOTS:
            Shot(player.gunPos(), player.facingX, player.selectedNote, SCREENRECT)
            sounds[player.selectedNote].play()
        player.reloading = firing        

        # Create the effect of the player jump
        if not player.jumping and jumpState:
            player.setJumpBase(player.rect.bottom)
            player.jumping = 1
            player.setSpeed(player.speedX,player.jumpSpeed)
        else:
            if player.jumping and (player.jumpBase <= player.rect.bottom):
                player.jumping = 0
            elif player.jumping and player.climbed:
                player.setJumpBase(player.rect.bottom)
                player.jumping = 0
            elif player.jumping and player.climbedB:
                player.setJumpBase(player.rect.bottom)
                player.jumping = 0

        # Update the player and move it
        player.setSpeed(PLAYER_SPEEDX,player.speedY)
        player.gravity(0,0.05)
        player.move(directionX,timePassed)

        # Create the effect of movement in the screen
        directionX = -directionX
        # If the player has reached the end and has all the notes, the screen freezes
        if (player.gameEnded() == 1) and (PLAYER_POS <= END_LVL+20):
            pass
        elif (player.rect.left == FLOORRECT.left or player.rect.right == FLOORRECT.right) and PLAYER_POS >= END_LVL:
            if PLAYER_POS <= BEGIN_LVL:
                PLAYER_POS = PLAYER_POS+SCREEN_SPEED*directionX
            elif PLAYER_POS >= BEGIN_LVL and directionX == -1:
                PLAYER_POS = PLAYER_POS+SCREEN_SPEED*directionX
        elif PLAYER_POS <= END_LVL and directionX == 1:
            PLAYER_POS = PLAYER_POS+SCREEN_SPEED*directionX

        # Update the player position for the other Sprites
        for note in notes:
            note.updatePlayerPos(PLAYER_POS)
        for fairy in fairies:
            fairy.updatePlayerPos(PLAYER_POS)
        for step in steps:
            step.updatePlayerPos(PLAYER_POS)
        for step in stepsM:
            step.updatePlayerPos(PLAYER_POS)
        for block in blocks:
            block.updatePlayerPos(PLAYER_POS)
        help.updatePlayerPos(PLAYER_POS)

        # Check collisions between the obstacles and the player
        player.climbed = 0 
        for step in pygame.sprite.spritecollide(player, steps, 0):
            if step.rect.top <= player.rect.bottom and step.rect.bottom <> player.rect.bottom and step.rect.centery > player.rect.bottom:
                player.setSpeed(player.speedX,0)
                player.position((0,-1))
                player.climbed = 1

        player.climbedB = 0 
        for step in pygame.sprite.spritecollide(player, stepsM, 0):
            if step.rect.top <= player.rect.bottom and step.rect.bottom <> player.rect.bottom and step.rect.centery > player.rect.bottom:
                player.setSpeed(player.speedX,0)
                player.position((0,5*step.facingY))
                player.climbedB = 1
                
        for block in pygame.sprite.spritecollide(player, blocks, 0):
            if block.rect.left <= player.rect.right:
                player.setSpeed(0,player.speedY)
                player.position((-11,0))

        # Check collisions with the notes
        for note in pygame.sprite.spritecollide(player, notes, 0):
            # Hacer un sonido
            id = note.kill()
            player.insertNote(id)
            score.addNote(id)
            scoreF.addPoints(100)

        # Check collisions between the blocks and the shots
        for shot, block in pygame.sprite.groupcollide(shots, blocks, 1, 0).items():
            if block[0].id == shot.id:
                block[0].kill()

        for shot, step in pygame.sprite.groupcollide(shots, stepsM, 1, 0).items():
            if step[0].id == shot.id:
                step[0].activate()
            
        # Check collisions with the fairies
        for fairy in pygame.sprite.spritecollide(player, fairies, 1):
            dead_sound.play()
            player.kill()

        # Check collisions between the fairies and the shots
        for shot, fairy in pygame.sprite.groupcollide(shots, fairies, 1, 0).items():
            if fairy[0].id == shot.id:
                fairy[0].kill()
                dead_sound.play()
                scoreF.addPoints(10)
            else:
                fairy[0].lives = fairy[0].lives-1
                if fairy[0].lives == 0:
                    dead_sound.play()
                    scoreF.addPoints(1)
            
        background.blit(bgdImage, (PLAYER_POS,0))
        screen.blit(background, (0,0))

        # Check if the player has reached the end and has all the notes
        if (player.gameEnded() == 1) and (PLAYER_POS <= END_LVL+20):
            result = game_end(scoreF.getScore())
            result[1].center = screen.get_rect().center
            screen.blit(result[0], result[1])
            
        # Draw the updated Sprites
        dirty = all.draw(screen)
        pygame.display.flip()

        # Check if the end has ended
        if (player.gameEnded() == 1) and (PLAYER_POS <= END_LVL+20):        
            pygame.time.wait(3000)
            return
        
    # Stop the music and quit
    if pygame.mixer:
        pygame.mixer.music.stop()
    pygame.time.wait(1000)
    pygame.quit()
    
    
# Call the main if the script executed from command line
if __name__ == '__main__': main()


