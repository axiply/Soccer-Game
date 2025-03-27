import pygame
pygame.font.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
FREESANS_32 = pygame.font.Font('freesansbold.ttf', 25)

pygame.init()
window = pygame.display.set_mode((1280, 960))
clock = pygame.time.Clock()

pos = pygame.math.Vector2(346,480)
velocity = pygame.math.Vector2(2,0)

soccerball = pygame.transform.scale(pygame.image.load('soccerball.png'),(50,50))
image = soccerball.convert_alpha()

status = "start screen"

def start(SCREEN):
    """
    Instruction screen shown at the start of the game
    Args:
        screen (Surface)
    """
    # Set screen as black with white text. 
    SCREEN.fill((0,0,0))
    font = FREESANS_32

    # Create text object, with associated rectangle in centre of screen
    text1 = font.render('Press enter to begin', True, (255,255,255))
    textRect1 = text1.get_rect()
    textRect1.center = SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 45

    # blit needed for it to be placed on the surface, then display updated for it to show up.
    SCREEN.blit(text1, textRect1)

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pos += velocity 

    if pos.x + 25 >= 960:
        velocity.x = 0
        window.fill(0)
        pygame.display.update()
    else:
        window.fill(0)
        image_rect = image.get_rect(center = (pos.x,pos.y))
        window.blit(image, image_rect)
        pygame.display.update()

    if status == "start screen":
        start(window)

pygame.quit()
exit()