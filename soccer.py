'''
ICS3U - Python Project
Name: soccer.py 
Date: April idk
Description: Basically soccer (watched youtube tutorial)
'''


import pygame
import sys  # sys.exit() to quit the game
import random

def ball_movement():
    global soccer_ball_speed_horizontal, soccer_ball_speed_vertical
    # making the ball move
    soccer_ball.x += soccer_ball_speed_horizontal
    soccer_ball.y += soccer_ball_speed_vertical

    # ensuring the ball doesnt go out of bounds
    if soccer_ball.bottom <= 0 or soccer_ball.top >= screen_height:
        soccer_ball_speed_vertical *= -1
    
    if soccer_ball.left <= 0 or soccer_ball.right >= screen_width:
        ball_restart()
        
    # colliding with the rectangles
    if soccer_ball.colliderect(opposing_player) or soccer_ball.colliderect(player):
        soccer_ball_speed_horizontal *= -1

def teleport_player():
    # placed back at border if goes out of bounds
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height

def opponent_movement():
    # opposing player movement
    if opposing_player.top < soccer_ball.y:
        opposing_player.top += speed_opposing_player
    if opposing_player.bottom > soccer_ball.y:
        opposing_player.bottom -= speed_opposing_player
    if opposing_player.top <= 0:
        opposing_player.top = 0
    if opposing_player.bottom >= screen_height:
        opposing_player.bottom = screen_height

def ball_restart():
    global soccer_ball_speed_horizontal, soccer_ball_speed_vertical
    soccer_ball.center = (screen_width/2, screen_height/2)
    soccer_ball_speed_horizontal *= random.choice((1, -1))
    soccer_ball_speed_vertical *= random.choice((1, -1))

# setting up the game
pygame.init()
clock = pygame.time.Clock()

# setting up the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_width))
pygame.display.set_caption("Soccer Pong")

# speeds
soccer_ball_speed_horizontal = 7 * random.choice((1, -1))
soccer_ball_speed_vertical = 7 * random.choice((1, -1))
speed_player = 0
speed_opposing_player = 7

# objects
soccer_ball = pygame.Rect(screen_width/2 - 16, screen_height/2 - 16, 32,32)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opposing_player = pygame.Rect(10, screen_height/2 - 70, 10, 140)

background_color = pygame.Color("grey11")
grey_color = (205, 205, 200)

while True:
    # handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # player movement
        if event.type == pygame.KEYDOWN: # when keys are down
            if event.key == pygame.K_DOWN:
                speed_player += 7
            if event.key == pygame.K_UP:
                speed_player -= 7
        if event.type == pygame.KEYUP: # when keys are up
            if event.key == pygame.K_DOWN:
                speed_player -= 7
            if event.key == pygame.K_UP:
                speed_player += 7

    # ball movement
    ball_movement()

    player.y += speed_player
    teleport_player()
    opponent_movement()

    # drawing the objects
    screen.fill(background_color)
    pygame.draw.rect(screen, grey_color, player) # player
    pygame.draw.rect(screen, grey_color, opposing_player) # opposing player
    pygame.draw.ellipse(screen, grey_color, soccer_ball) # soccer
    pygame.draw.aaline(screen, grey_color, (screen_width/2, 0), (screen_width/2, screen_height)) # middle line  # aaline is anti-aliased line       
    

    # update the window
    pygame.display.flip()
    clock.tick(60) 

     
