import pygame

pygame.init()
window = pygame.display.set_mode((1280, 960))
clock = pygame.time.Clock()


pos = pygame.math.Vector2(634,480)
velocity = pygame.math.Vector2(2,0)

soccerball = pygame.transform.scale(pygame.image.load('soccerball.png'),(50,50))
image = soccerball.convert_alpha()

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pos += velocity 

    if pos.x + 25 >= 960 or pos.x - 25 <= 320:
        velocity.x *= -1
    if pos.y + 25 >= 960 or pos.y - 25 <= 320:
        velocity.y *= -1
           
    window.fill(0)
    #pygame.draw.lines(window, "gray", True, corner_points) 
    image_rect = image.get_rect(center = (pos.x,pos.y))
    window.blit(image, image_rect)
    pygame.display.update()

pygame.quit()
exit()