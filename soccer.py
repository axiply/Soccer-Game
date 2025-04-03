import pygame
from pygame import mixer
from pygame.locals import *
import sys
import random

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

def level_screen():
    # define fonts and text
    font = pygame.font.SysFont("monospace", 40)
    text = font.render(status, True, pygame.Color("white"))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    # display the message and wait for a key press
    screen.fill(background_color)
    screen.blit(text, text_rect)
    pygame.display.flip()

    start_time = pygame.time.get_ticks()  # Get current time in milliseconds
    waiting = True

    # wait 2 seconds or press key to continue
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # Exit loop when a key is pressed

        # check if 2 seconds (2000 milliseconds) have passed
        if pygame.time.get_ticks() - start_time >= 2000:
            waiting = False  # exit loop after 2 seconds

        clock.tick(30)

# settings & images for animation
pos = pygame.math.Vector2(346,480)
velocity = pygame.math.Vector2(4,0)
i_soccerball = pygame.transform.scale(pygame.image.load('soccer_ball.png'),(50,50)) 
soccerball_image = i_soccerball.convert_alpha()

# function to draw starting animation
def loading_animation():
    global pos 
    waiting = True

    while waiting: 
        pos += velocity 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Ensure program exits cleanly

        pos += velocity  # Move the soccer ball

        if pos.x + 25 >= 960:  # When animation reaches the end
            waiting = False  # Stop loop
            velocity.x = 0  # Stop movement
            screen.fill(0)
            pygame.display.update()
            return  # Exit the function cleanly

        # Continue animating
        screen.fill(0)
        image_rect = soccerball_image.get_rect(center=(pos.x, pos.y))
        screen.blit(soccerball_image, image_rect)
        pygame.display.update()
        clock.tick(40)


levels = ["Level 1","Level 2","Level 3","Level 4","Level 5"]
status = "loading screen"

if status == "loading screen":
    #starting loading animation
    loading_animation()
    # Display loading screen and wait for key press
    loading_screen()
    status = "Level 1"

if status in levels:
    level_screen()
# **** alterations of above code will have to take place after with more code

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
