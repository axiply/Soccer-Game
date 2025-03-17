import pygame

pygame.init()
window = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

corner_points = [(100, 100), (300, 300), (300, 100), (100, 300)]
pos = corner_points[0]
speed = 2

def move(pos, speed, points):
    direction = pygame.math.Vector2(points[0]) - pos
    if direction.length() <= speed:
        pos = points[0]
        points.append(points[0])
        points.pop(0)
    else:
        direction.scale_to_length(speed)
        new_pos = pygame.math.Vector2(pos) + direction
        pos = (new_pos.x, new_pos.y) 
    return pos

soccerball = pygame.transform.scale(pygame.image.load('soccerball.png'),(50,50))
image = soccerball.convert_alpha()

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pos = move(pos, speed, corner_points)
    image_rect = image.get_rect(center = pos)
           
    window.fill(0)
    #pygame.draw.lines(window, "gray", True, corner_points) 
    window.blit(image, image_rect)
    pygame.display.update()

pygame.quit()
exit()