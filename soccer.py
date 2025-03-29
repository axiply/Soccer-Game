import pygame
from pygame import mixer
from pygame.locals import *
import sys
import random

# clock initialized
clock = pygame.time.Clock()

def ball_movement():
    global soccer_ball_speed_x, soccer_ball_speed_y

    # check for collision with goalkeepers before moving the ball
    if soccer_ball.colliderect(opposing_goalie):
        soccer_ball_speed_x *= -1
        soccer_ball.x = opposing_goalie.right  # move ball away from goalie
        soccer_ball_speed_y += random.choice([-1, 1]) * 2  

    if soccer_ball.colliderect(player_goalie):
        soccer_ball_speed_x *= -1
        soccer_ball.x = player_goalie.left - soccer_ball.width  # move ball away from goalie
        soccer_ball_speed_y += random.choice([-1, 1]) * 2 

    # now move the ball based on its current speed
    soccer_ball.x += soccer_ball_speed_x
    soccer_ball.y += soccer_ball_speed_y

    # check for ball going out of bounds
    if soccer_ball.top <= 0 or soccer_ball.bottom >= screen_height:
        soccer_ball_speed_y *= -1
    
    if soccer_ball.left <= 0 or soccer_ball.right >= screen_width:
        ball_restart()

    # colliding with players
    if soccer_ball.colliderect(opposing_player):
        soccer_ball_speed_x *= -1
        soccer_ball.x = opposing_player.right  # move ball away from the player

    if soccer_ball.colliderect(player):
        soccer_ball_speed_x *= -1
        soccer_ball.x = player.left - soccer_ball.width  # move ball away from the player

def teleport_player():
    # ensure the player doesn't go outside the screen boundaries
    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height
    if player.left <= 0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def opponent_movement():
    # make the opposing player follow the ball
    if opposing_player.x < soccer_ball.x:
        opposing_player.x += speed_opposing_player
    if opposing_player.x > soccer_ball.x:
        opposing_player.x -= speed_opposing_player
    if opposing_player.y < soccer_ball.y:
        opposing_player.y += speed_opposing_player
    if opposing_player.y > soccer_ball.y:
        opposing_player.y -= speed_opposing_player

def goalie_movement(goalie, direction):
    # goalies move up and down within their bounds
    if goalie.top <= 0:
        goalie.top = 0
    if goalie.bottom >= screen_height:
        goalie.bottom = screen_height
    if direction == 'up' and goalie.top > 0:
        goalie.y -= 4  # move up
    if direction == 'down' and goalie.bottom < screen_height:
        goalie.y += 4  # move down

def ball_restart():
    global soccer_ball_speed_x, soccer_ball_speed_y
    # restart the ball in the center with a random direction and speed
    soccer_ball.center = (screen_width/2, screen_height/2)
    soccer_ball_speed_x = 7 * random.choice((1, -1))
    soccer_ball_speed_y = 7 * random.choice((1, -1))

def loading_screen():
    # Define fonts and text
    font = pygame.font.SysFont("monospace", 40)
    text = font.render("Press any key to continue...", True, pygame.Color("white"))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    # Display the message and wait for a key press
    screen.fill(background_color)
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Wait for a key press to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # exit the loop when a key is pressed
        clock.tick(30)

# setting up the game
pygame.init()
clock = pygame.time.Clock()

# setting up the main window
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Soccer Pong")

# speeds
soccer_ball_speed_x = 7 * random.choice((2, -2, -1, 1))
soccer_ball_speed_y = 7 * random.choice((1, -1, 2, -2))
speed_player_x = 0
speed_player_y = 0
speed_opposing_player = 4

# objects
soccer_ball = pygame.Rect(screen_width/2 - 16, screen_height/2 - 16, 32, 32)
player = pygame.Rect(screen_width - 60, screen_height/2 - 50, 50, 50)
opposing_player = pygame.Rect(10, screen_height/2 - 50, 50, 50)
player_goalie = pygame.Rect(screen_width - 90, screen_height/2 - 80, 30, 160)  # right side goalie
opposing_goalie = pygame.Rect(60, screen_height/2 - 80, 30, 160)  # left side goalie

# load custom player images
player_image = pygame.image.load("character.png")  
opposing_player_image = pygame.image.load("ronaldo.png")  

# scale the images
player_image = pygame.transform.scale(player_image, (100, 100))
opposing_player_image = pygame.transform.scale(opposing_player_image, (100, 100))

background_color = pygame.Color("grey11")
grey_color = (205, 205, 200)

# music
try:
    mixer.music.load("football_chant.wav")
    mixer.music.play(-1)
except pygame.error:
    print("Warning, there is no sound file loaded!")

# Display loading screen and wait for key press
loading_screen()

# Start the game after loading screen
running = True
while running:
    # handling events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # player movement controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                speed_player_y += 7
            if event.key == pygame.K_UP:
                speed_player_y -= 7
            if event.key == pygame.K_LEFT:
                speed_player_x -= 7
            if event.key == pygame.K_RIGHT:
                speed_player_x += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                speed_player_y -= 7
            if event.key == pygame.K_UP:
                speed_player_y += 7
            if event.key == pygame.K_LEFT:
                speed_player_x += 7
            if event.key == pygame.K_RIGHT:
                speed_player_x -= 7

    # ball movement logic
    ball_movement()
    
    # player movement
    player.x += speed_player_x
    player.y += speed_player_y
    teleport_player()
    opponent_movement()

    # goalie movements (left goalie moves up and down)
    if soccer_ball.y > opposing_goalie.centery:
        goalie_movement(opposing_goalie, 'down')
    else:
        goalie_movement(opposing_goalie, 'up')

    if soccer_ball.y > player_goalie.centery:
        goalie_movement(player_goalie, 'down')
    else:
        goalie_movement(player_goalie, 'up')

    # draw everything on the screen
    screen.fill(background_color)

    # draw custom images for the players and goalies
    screen.blit(player_image, player)  # player
    screen.blit(opposing_player_image, opposing_player)  # opposing player
    pygame.draw.rect(screen, grey_color, player_goalie)  # player's goalie
    pygame.draw.rect(screen, grey_color, opposing_goalie)  # opposing goalie's goalie
    pygame.draw.ellipse(screen, grey_color, soccer_ball)  # soccer ball
    pygame.draw.aaline(screen, grey_color, (screen_width/2, 0), (screen_width/2, screen_height))  # middle line
    
    # update the window
    pygame.display.flip()
    clock.tick(60)
