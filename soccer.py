'''
Pygame Soccer Pong Game
ICS3U
Authors: Swanish and Selina
Purpose: Create a soccer pong game with power-ups and coins
Date: 2025-04-17
'''

# install the necessary libraries
import pygame
from pygame import mixer
from pygame.locals import *
import sys
import random
import time


# initialize the clock 
clock = pygame.time.Clock()

# start the ball movement
def moving_ball():
    global x_ball_speed, y_ball_speed

    if goal_scored:
        return

    # handling the cases where the ball hits either goalie
    if soccer_ball.colliderect(other_goalie):
        x_ball_speed *= -1
        soccer_ball.x = other_goalie.right
        y_ball_speed = random.randint(-7, 7)  

    if soccer_ball.colliderect(player_goalie):
        x_ball_speed *= -1
        soccer_ball.x = player_goalie.left - soccer_ball.width
        y_ball_speed = random.randint(-7, 7) 

    # adding the speeds
    soccer_ball.x += x_ball_speed
    soccer_ball.y += y_ball_speed

    # Check if ball is completely out of bounds
    if soccer_ball.x < -100 or soccer_ball.x > screen_width + 100 or soccer_ball.y < -100 or soccer_ball.y > screen_height + 100:
        soccer_ball.center = (screen_width/2, screen_height/2)
        x_ball_speed = 7 * random.choice((2, -2, -1, 1))
        y_ball_speed = 7 * random.choice((1, -1, 2, -2))

    # handling the cases where the ball hits the top or bottom of the screen
    if soccer_ball.top <= 0 or soccer_ball.bottom >= screen_height:
        y_ball_speed *= -1
    
    if soccer_ball.left <= 0 or soccer_ball.right >= screen_width:
        check_goal()

    # handling the cases where the ball hits the player or opposing player
    if soccer_ball.colliderect(ronaldo):
        x_ball_speed *= -1
        soccer_ball.x = ronaldo.right
        y_ball_speed = random.randint(-7, 7)

    if soccer_ball.colliderect(player):
        x_ball_speed *= -1
        soccer_ball.x = player.left - soccer_ball.width
        y_ball_speed = random.randint(-7, 7)

# function for if player leaves the screen
def player_out_of_bounds():
    if player.top <= 0:
        player.top = 0

    if player.bottom >= screen_height:
        player.bottom = screen_height

    if player.left <= 0:
        player.left = 0

    if player.right >= screen_width:
        player.right = screen_width

# function for the moving of the goalie
def ronaldo_movement():
    ronaldo_limit_x = screen_width * 3//5

    if ronaldo.x < soccer_ball.x and ronaldo.x < ronaldo_limit_x:
        ronaldo.x += speed_ronaldo
        
    if ronaldo.x > soccer_ball.x:
        ronaldo.x -= speed_ronaldo

    if ronaldo.y < soccer_ball.y:
        ronaldo.y += speed_ronaldo

    if ronaldo.y > soccer_ball.y:
        ronaldo.y -= speed_ronaldo

def boss_spawner():
    # spawn the boss
    boss_x = random.randint(100, screen_width - 100)
    boss_y = random.randint(100, screen_height - 100)
    
    boss_box = pygame.Rect(boss_x, boss_y, 200, 200)
    return boss_box

def boss_movement():
    if ronaldo.x < soccer_ball.x:
        ronaldo.x += speed_ronaldo
        
    if ronaldo.x > soccer_ball.x:
        ronaldo.x -= speed_ronaldo

    if ronaldo.y < soccer_ball.y:
        ronaldo.y += speed_ronaldo

    if ronaldo.y > soccer_ball.y:
        ronaldo.y -= speed_ronaldo

# moving teh goalies
def goalie_movement(goalie, where):
    if goalie.top <= 0:
        goalie.top = 0

    if goalie.bottom >= screen_height:
        goalie.bottom = screen_height

    # keeping the goalie in bounds, by moving it back slightly
    if where == 'up' and goalie.top > 0:
        goalie.y -= 4

    if where == 'down' and goalie.bottom < screen_height:
        goalie.y += 4

# when the game ends
def game_over_screen():

    # text
    font = pygame.font.SysFont("monospace", 60)

    # show who won?!?
    if player_score >= 5:
        text = font.render("You Win!", True, pygame.Color("green"))

    elif opponent_score >= 5:
        text = font.render("OMG RONALDO WINS!!!!!!", True, pygame.Color("red"))
    else:
        text = font.render("WHAT?? YOU TIED!??!", True, pygame.Color("yellow"))

    # displaying the score
    text_box_thing = text.get_rect(center=(screen_width // 2, screen_height // 2))
    show_score = font.render(f"{opponent_score} - {player_score}", True, pygame.Color("white"))
    score_box = show_score.get_rect(center=(screen_width // 2, screen_height // 2 + 80))
    
    coin_display = font.render(f"Coins: {coins}", True, pygame.Color("gold"))
    coin_box = coin_display.get_rect(center=(screen_width // 2, screen_height // 2 + 160))

    # display teh text
    screen.fill(background_color)  
    screen.blit(text, text_box_thing)
    screen.blit(show_score, score_box)
    screen.blit(coin_display, coin_box)
    pygame.display.flip()

    # wait to let the user read it for 3 sec befor exiting
    pygame.time.delay(3000)  
    pygame.quit()
    sys.exit()

def screen_switcher():
    if level1:
        level_1()
    elif level2:
        level_2()
    elif level3:
        level_3()
    elif level4:
        level_4()
    else:
        level_5()


# function to draw loading animation
def loading_animation():
    pos = pygame.math.Vector2(346,480)
    velocity = pygame.math.Vector2(4,0)
    i_soccerball = pygame.transform.scale(pygame.image.load('soccer_ball.png'),(50,50)) 
    soccerball_image = i_soccerball.convert_alpha()

    waiting = True

    while waiting: 
        pos += velocity 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  

        pos += velocity  # move the soccer ball

        if pos.x + 25 >= 960:  # when animation reaches the end
            waiting = False  
            velocity.x = 0  
            screen.fill(0)
            pygame.display.update()
            return  

        # continue animating
        screen.fill(0)
        image_rect = soccerball_image.get_rect(center=(pos.x, pos.y))
        screen.blit(soccerball_image, image_rect)
        pygame.display.update()
        clock.tick(40)

# function for the loading screen
def loading_screen():
    # define fonts and text
    font = pygame.font.SysFont("monospace", 40)
    text = font.render("Press any key to continue...", True, pygame.Color("white"))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    # display the message and wait for a key press
    screen.fill(background_color)
    screen.blit(text, text_rect)
    pygame.display.flip()

    # wait for a key press to continue
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False  # exit the loop when a key is pressed
        clock.tick(30)

# function for screen in between levels
def level_screen(level):
    # define fonts and text
    font = pygame.font.SysFont("monospace", 40)
    text = font.render(level, True, pygame.Color("white"))
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

# function to restart the ball
def ball_restart():
    global x_ball_speed, y_ball_speed, goal_scored
    
    # only restart the ball if we're not in a goal animation
    if not goal_scored:
        soccer_ball.center = (screen_width/2, screen_height/2)
        x_ball_speed = 7 * random.choice((1, -1))
        y_ball_speed = 7 * random.choice((1, -1))

# format the time correctly
def clock_time(seconds):
    # note to self: bit inefficient, fix later

    minutes = int(seconds / 60) 
    remaining = seconds - (minutes * 60) 
    result = ""

    if minutes < 10:
        result += "0" + str(minutes)
    else:
        result += str(minutes)

    result += ":"

    if remaining < 10:
        result += "0" + str(remaining)
    else:
        result += str(remaining)

    return result

# check if the ball is in a goal
def check_goal():
    global player_score, opponent_score, goal_scored, goal_time, goal_side
    
    if soccer_ball.left <= 0:
        player_score += 1
        goal_scored = True
        goal_time = pygame.time.get_ticks()
        goal_side = "left"  
        
    if soccer_ball.right >= screen_width:
        opponent_score += 1
        goal_scored = True
        goal_time = pygame.time.get_ticks()
        goal_side = "right" 
    
    if player_score >= 5 or opponent_score >= 5:
        level_transition_screen(1, 3) 
        return

# create a POWERUP!
def create_powerup():
    powerup_type = random.choice(['size', 'speed'])
    power_x = random.randint(100, screen_width - 100)
    power_y = random.randint(100, screen_height - 100)
    
    powerup_box = pygame.Rect(power_x, power_y, 30, 30)
    return {'rect': powerup_box, 'type': powerup_type}

# make the coin (remember to add shop as student requested shop)
def create_coin():
    coin_x = random.randint(100, screen_width - 100)
    coin_y = random.randint(100, screen_height - 100)
    
    coin_box = pygame.Rect(coin_x, coin_y, 20, 20)
    return coin_box

def init_game():
    # initialize pygame and create global variables
    global screen_width, screen_height, screen, background_image, background_color, x_ball_speed, y_ball_speed, speed_ronaldo, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, ronaldo_image, player_image_original, grey_color, timer_font, timer_color, score_font, player_score, opponent_score, coins

    pygame.init()
    
    # define the screen size
    screen_width = 1280
    screen_height = 960
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mohammed's Soccer")

    # setting up the background and scaling the images
    background_image = pygame.image.load('/Users/swanishbaweja/Pygame project (NEW)/soccerfields/1.png') 
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height)) 

    # ball speeds
    x_ball_speed = 7 * random.choice((2, -2, -1, 1))
    y_ball_speed = 7 * random.choice((1, -1, 2, -2))
    speed_ronaldo = 4

    # get the rectangles
    soccer_ball = pygame.Rect(screen_width/2 - 16, screen_height/2 - 16, 32, 32)
    player = pygame.Rect(screen_width - 111, screen_height/2 - 49, 100, 100)
    ronaldo = pygame.Rect(10, screen_height/2 - 53, 100, 100)
    boss = pygame.Rect(10, screen_height/2 - 53, 200, 200)
    player_goalie = pygame.Rect(screen_width - 91, screen_height/2 - 80, 30, 160)
    other_goalie = pygame.Rect(60, screen_height/2 - 80, 30, 160)

    # upload the IMAGES
    player_image = pygame.image.load("character.png")  
    ronaldo_image = pygame.image.load("ronaldo.png")  
    #boss_image = pygame.image.load("boss.png")

    # resize they images because they were too bigg
    player_image = pygame.transform.scale(player_image, (100, 100))
    player_image_original = player_image.copy()
    ronaldo_image = pygame.transform.scale(ronaldo_image, (100, 100))

    # get the specific shad of gray and stuff for the vbackground
    background_color = pygame.Color("grey11")
    grey_color = (205, 205, 200)

    # fonts
    timer_font = pygame.font.SysFont("monospace", 36)
    timer_color = pygame.Color("white")
    score_font = pygame.font.SysFont("monospace", 70)

    # initialize the scoring and stuff
    player_score = 0
    opponent_score = 0
    coins = 0
    
    # check for the music (added because i had an error)
    try:
        mixer.music.load("fifa.mp3")
        mixer.music.play(-1)
    except pygame.error:
        print("Warning, there is no sound file loaded!")
    
    return clock

def level_transition_screen(current_level, next_level):
    global level1, level2, level3, level4, level5
    
    font_large = pygame.font.SysFont("monospace", 40)
    font_small = pygame.font.SysFont("monospace", 30)
    
    countdown_seconds = 10
    player_score = 0
    opponent_score = 0
    countdown_event = pygame.USEREVENT + 10
    pygame.time.set_timer(countdown_event, 1000)
    
    level_completed_text = font_large.render(f"Level {current_level} Completed!", True, pygame.Color("white"))
    score_text = font_small.render(f"Score: {opponent_score} - {player_score}", True, pygame.Color("white"))
    coins_text = font_small.render(f"Coins: {coins}", True, pygame.Color("gold"))
    next_level_text = font_small.render(f"Next Level in: {countdown_seconds}", True, pygame.Color("white"))
    skip_text = font_small.render("Press any key to skip", True, pygame.Color("gray"))

    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == countdown_event:
                countdown_seconds -= 1
                next_level_text = font_small.render(f"Next Level in: {countdown_seconds}", True, pygame.Color("white"))
                if countdown_seconds <= 0:
                    waiting = False
                    pygame.time.set_timer(countdown_event, 0)
            
            if event.type == pygame.KEYDOWN:
                waiting = False
                pygame.time.set_timer(countdown_event, 0)
        
        screen.fill(background_color)
        screen.blit(level_completed_text, (screen_width//2 - level_completed_text.get_width()//2, screen_height//2 - 100))
        screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 - 50))
        screen.blit(coins_text, (screen_width//2 - coins_text.get_width()//2, screen_height//2))
        screen.blit(next_level_text, (screen_width//2 - next_level_text.get_width()//2, screen_height//2 + 50))
        screen.blit(skip_text, (screen_width//2 - skip_text.get_width()//2, screen_height//2 + 100))
        pygame.display.flip()
        clock.tick(60)
    
    if next_level == 1:
        level1 = True
        level2 = level3 = level4 = level5 = False
    elif next_level == 2:
        level2 = True
        level1 = level3 = level4 = level5 = False
    elif next_level == 3:
        level3 = True
        level1 = level2 = level4 = level5 = False
    elif next_level == 4:
        level4 = True 
        level1 = level2 = level3 = level5 = False
    elif next_level == 5:
        level5 = True
        level1 = level2 = level3 = level4 = False
    
    screen_switcher()
    

# level one function
def level_1():
    level_screen("Level 1: The Beginnings")
    # add player_image and other required variables to global
    global player_score, opponent_score, coins, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, player_image_original, ronaldo_image, goal_scored, goal_time, goal_side

    
    # level 1 specific settings
    game_length_time = 300
    
    # set up timers
    timer_running = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_running, 1000)

    powerup_running = pygame.USEREVENT + 2
    pygame.time.set_timer(powerup_running, 10000)  # new powerup every 10 seconds

    coin_running = pygame.USEREVENT + 3
    pygame.time.set_timer(coin_running, 5000)  # new coin every 5 seconds

    # game variables
    running = True
    time_remaining = game_length_time

    # powerup variables
    powerups = []
    time_left_size_boost = 0
    time_left_speed_boost = 0
    normal_player_speed = 7
    boosted_player_speed = 14
    size_on = False
    speed_on = False

    # input tracking (added to mitigate randomly moving error)
    key_down = False
    key_up = False
    key_left = False
    key_right = False

    # initialize the delayed ball spawning 
    goal_scored = False
    goal_time = 0
    goal_side = ""
    flash_interval = 200  # milliseconds between flashes
    flash_colors = [(255, 255, 255), grey_color]  # White and original color

    # coins
    coin_object = []
    
    # while its running
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # timer
            if event.type == timer_running:
                time_remaining -= 1
                if time_remaining <= 0:
                    level_transition_screen(1, 3) 
                    return
            
            # limited powerups allowed
            if event.type == powerup_running:
                if len(powerups) < 3: 
                    powerups.append(create_powerup())
                    
            if event.type == coin_running:
                if len(coin_object) < 5:  
                    coin_object.append(create_coin())

# tracking the buttons pressed on the user's keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    key_down = True

                if event.key == pygame.K_UP:
                    key_up = True

                if event.key == pygame.K_LEFT:
                    key_left = True

                if event.key == pygame.K_RIGHT:
                    key_right = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    key_down = False

                if event.key == pygame.K_UP:
                    key_up = False

                if event.key == pygame.K_LEFT:
                    key_left = False

                if event.key == pygame.K_RIGHT:
                    key_right = False

        speed_player_x = 0
        speed_player_y = 0

        # if speed boost is on, set the speed to the boosted speed
        if speed_on:
            current_speed = boosted_player_speed
        else:
            current_speed = 7

        # if the key is down, make him move on the speed it is currently on
        if key_down:
            speed_player_y = current_speed

        if key_up:
            speed_player_y = -current_speed

        if key_left:
            speed_player_x = -current_speed

        if key_right:
            speed_player_x = current_speed

        if size_on and current_time > time_left_size_boost:
            size_on = False
            
            original_center = player.center
            
            player_image = player_image_original.copy()
            
            # reset back to normla dimension
            player.width, player.height = 100, 100
            
            player.center = original_center

        # if the speed boost is on for more than the alloted time, turn it off
        if speed_on and current_time > time_left_speed_boost:
            speed_on = False

        # call the moving ball funcitons
        moving_ball()
        
        player.x += speed_player_x
        player.y += speed_player_y
        player_out_of_bounds()
        ronaldo_movement()

        powerups_to_remove = []
        for i, powerup in enumerate(powerups):
            if player.colliderect(powerup['rect']):

                # if the player touches a SIZING poweruo they get bigger
                if powerup['type'] == 'size':
                    size_on = True
                    time_left_size_boost = current_time + 30
                    
                    original_center = player.center
                    
                    player_image = pygame.transform.scale(player_image_original, (150, 150))
                    
                    # make the collision box match the larger image 150x150
                    player.width, player.height = 150, 150
                    
                    player.center = original_center
                    
                # if the player touches a SPEED powerup they get faster
                elif powerup['type'] == 'speed':
                    speed_on = True
                    time_left_speed_boost = current_time + 30
                powerups_to_remove.append(i)
        
        for i in sorted(powerups_to_remove, reverse=True):
            powerups.pop(i)
        
        coins_to_remove = []
        for i, coin in enumerate(coin_object):
            if player.colliderect(coin):
                coins += 1
                coins_to_remove.append(i)
        
        # remove collected coins
        for i in sorted(coins_to_remove, reverse=True):
            coin_object.pop(i)

        if soccer_ball.y > other_goalie.centery:
            goalie_movement(other_goalie, 'down')
        else:
            goalie_movement(other_goalie, 'up')

        if soccer_ball.y > player_goalie.centery:
            goalie_movement(player_goalie, 'down')
        else:
            goalie_movement(player_goalie, 'up')

        screen.blit(background_image, (0, 0))

        # draw powerups
        for powerup in powerups:
            if powerup['type'] == 'size':
                pygame.draw.rect(screen, (255, 0, 0), powerup['rect'])  # red for size
            elif powerup['type'] == 'speed':
                pygame.draw.rect(screen, (0, 255, 0), powerup['rect'])  # green for speed
        
        # draw coins
        for coin in coin_object:
            pygame.draw.ellipse(screen, (255, 215, 0), coin)  # Gold color for coins

        # draw everything
        screen.blit(player_image, player)
        screen.blit(ronaldo_image, ronaldo)
        pygame.draw.rect(screen, grey_color, player_goalie)
        pygame.draw.rect(screen, grey_color, other_goalie)
        pygame.draw.ellipse(screen, grey_color, soccer_ball)
        pygame.draw.aaline(screen, grey_color, (screen_width/2, 0), (screen_width/2, screen_height))
        
        # have the timer text displayed
        timer_text = timer_font.render(f"Time: {clock_time(time_remaining)}", True, timer_color)
        screen.blit(timer_text, (screen_width//2 - 70, 20))
        
        score_text = score_font.render(f"{opponent_score} - {player_score}", True, timer_color)
        screen.blit(score_text, (screen_width//2 - 60, 60))
        
        # display coin count
        coin_text = timer_font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(coin_text, (screen_width - 200, 20))
        
        # display active powerups
        if size_on:
            size_text = timer_font.render("Size Boost!", True, (255, 0, 0))
            screen.blit(size_text, (20, 20))
        
        if speed_on:
            speed_text = timer_font.render("Speed Boost!", True, (0, 255, 0))
            screen.blit(speed_text, (20, 60))

        # Handle goal animation and delayed respawn
        if goal_scored:
            current_time = pygame.time.get_ticks()
            time_since_goal = current_time - goal_time
            
            # Flash the appropriate goalie
            if time_since_goal < 5000:  # During the 5 second delay
                flash_index = (time_since_goal // flash_interval) % 2
                flash_color = flash_colors[flash_index]
                
                if goal_side == "left":
                    # Left goal was scored on, flash the left goalie
                    pygame.draw.rect(screen, flash_color, other_goalie)
                else:
                    # Right goal was scored on, flash the right goalie
                    pygame.draw.rect(screen, flash_color, player_goalie)
                    
                # Display "GOAL!" text
                goal_font = pygame.font.SysFont("monospace", 80)
                goal_text = goal_font.render("GOAL!", True, (255, 0, 0))
                screen.blit(goal_text, (screen_width//2 - goal_text.get_width()//2, screen_height//2 - 40))
            else:
                # After 5 seconds, reset the ball and clear the goal state
                goal_scored = False
                ball_restart()
        
        
        
        pygame.display.flip()
        clock.tick(60)

def level_3():
    level_screen("Level 3 - Double Trouble")
    
    global player_score, opponent_score, coins, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, player_image_original, ronaldo_image, x_ball_speed, y_ball_speed, goal_scored, goal_time, goal_side
    
    player_score = 0
    opponent_score = 0
    coins = 0
    ball_activated = False

    x_ball_speed = 0
    y_ball_speed = 0
    soccer_ball.center = (screen_width/2, screen_height/2)

    goal_scored = False
    goal_time = 0
    goal_side = ""
    flash_interval = 200  
    flash_colors = [(255, 255, 255), grey_color] 

    background_image = pygame.image.load("/Users/swanishbaweja/Pygame project (NEW)/soccerfields/3.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    game_length_time = 240
    
    timer_running = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_running, 1000)
    
    powerup_running = pygame.USEREVENT + 2
    pygame.time.set_timer(powerup_running, 8000)
    
    coin_running = pygame.USEREVENT + 3
    pygame.time.set_timer(coin_running, 5000)
    
    puddle_timer = pygame.USEREVENT + 4
    pygame.time.set_timer(puddle_timer, 15000)
    
    weather_timer = pygame.USEREVENT + 5
    pygame.time.set_timer(weather_timer, 20000)
    
    fan_cheer_timer = pygame.USEREVENT + 6
    pygame.time.set_timer(fan_cheer_timer, 12000)
    
    running = True
    time_remaining = game_length_time
    
    powerups = []
    time_left_size_boost = 0
    time_left_speed_boost = 0
    time_left_slow_effect = 0
    time_left_freeze_enemies = 0
    normal_player_speed = 7
    boosted_player_speed = 14
    slowed_player_speed = 3
    size_on = False
    speed_on = False
    player_slowed = False
    enemies_frozen = False
    
    coin_object = []
    
    mud_puddles = []
    
    rain_effect = False
    rain_end_time = 0
    
    fan_cheering = False
    fan_end_time = 0
    
    obstacles = []
    
    key_down = False
    key_up = False
    key_left = False
    key_right = False
    
    second_enemy = pygame.Rect(screen_width // 2, screen_height//2 - 50, 100, 100)
    second_enemy_image = pygame.image.load("ronaldo.png")
    second_enemy_image = pygame.transform.scale(second_enemy_image, (100, 100))
    second_enemy_speed = 3
    
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == timer_running:
                time_remaining -= 1
                if time_remaining <= 0:
                    level_transition_screen(1, 3) 
                    return
            
            if event.type == powerup_running:
                if len(powerups) < 2:
                    powerups.append(create_powerup_level3())
                    
            if event.type == coin_running:
                if len(coin_object) < 3:
                    coin_object.append(create_coin())
            
            if event.type == puddle_timer:
                if len(mud_puddles) < 4:
                    mud_puddles.append(create_mud_puddle())
                    
            if event.type == weather_timer:
                if not rain_effect:
                    rain_effect = True
                    rain_end_time = current_time + 15
                    x_ball_speed *= 0.8
                    y_ball_speed *= 0.8
                    
            if event.type == fan_cheer_timer and random.random() > 0.5:
                fan_cheering = True
                fan_end_time = current_time + 5
                if random.random() > 0.5:
                    player_score += 1
                else:
                    obstacles.append(create_obstacle())

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    key_down = True
                if event.key == pygame.K_UP:
                    key_up = True
                if event.key == pygame.K_LEFT:
                    key_left = True
                if event.key == pygame.K_RIGHT:
                    key_right = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    key_down = False
                if event.key == pygame.K_UP:
                    key_up = False
                if event.key == pygame.K_LEFT:
                    key_left = False
                if event.key == pygame.K_RIGHT:
                    key_right = False

        speed_player_x = 0
        speed_player_y = 0

        if player_slowed:
            current_speed = slowed_player_speed
        elif speed_on:
            current_speed = boosted_player_speed
        else:
            current_speed = normal_player_speed

        if key_down:
            speed_player_y = current_speed
        if key_up:
            speed_player_y = -current_speed
        if key_left:
            speed_player_x = -current_speed
        if key_right:
            speed_player_x = current_speed

        if size_on and current_time > time_left_size_boost:
            size_on = False
            original_center = player.center
            player_image = player_image_original.copy()
            player.width, player.height = 100, 100
            player.center = original_center

        if speed_on and current_time > time_left_speed_boost:
            speed_on = False

        if player_slowed and current_time > time_left_slow_effect:
            player_slowed = False
            
        if enemies_frozen and current_time > time_left_freeze_enemies:
            enemies_frozen = False
            
        if rain_effect and current_time > rain_end_time:
            rain_effect = False
            x_ball_speed /= 0.8
            y_ball_speed /= 0.8
            
        if fan_cheering and current_time > fan_end_time:
            fan_cheering = False


        
        if ball_activated or key_down or key_up or key_left or key_right:
            if not ball_activated:
                # Initialize ball speed only once when first key is pressed
                x_ball_speed = 7 * random.choice((2, -2, -1, 1))
                y_ball_speed = 7 * random.choice((1, -1, 2, -2))
                ball_activated = True
            moving_ball()
        
        player.x += speed_player_x
        player.y += speed_player_y
        player_out_of_bounds()
        
        if not enemies_frozen:
            ronaldo_movement()
            move_second_enemy(second_enemy)

        powerups_to_remove = []
        for i, powerup in enumerate(powerups):
            if player.colliderect(powerup['rect']):
                if powerup['type'] == 'size':
                    size_on = True
                    time_left_size_boost = current_time + 30
                    original_center = player.center
                    player_image = pygame.transform.scale(player_image_original, (150, 150))
                    player.width, player.height = 150, 150
                    player.center = original_center
                    
                elif powerup['type'] == 'speed':
                    speed_on = True
                    time_left_speed_boost = current_time + 30
                    
                elif powerup['type'] == 'invincible':
                    player_slowed = False
                    time_left_slow_effect = 0
                    
                elif powerup['type'] == 'freeze':
                    enemies_frozen = True
                    time_left_freeze_enemies = current_time + 10
                    
                powerups_to_remove.append(i)
        
        for i in sorted(powerups_to_remove, reverse=True):
            powerups.pop(i)
        
        coins_to_remove = []
        for i, coin in enumerate(coin_object):
            if player.colliderect(coin):
                coins += 1
                coins_to_remove.append(i)
        
        for i in sorted(coins_to_remove, reverse=True):
            coin_object.pop(i)
            
        puddles_to_remove = []
        for i, puddle in enumerate(mud_puddles):
            if player.colliderect(puddle):
                player_slowed = True
                time_left_slow_effect = current_time + 5
                puddles_to_remove.append(i)
        
        for i in sorted(puddles_to_remove, reverse=True):
            mud_puddles.pop(i)
            
        obstacles_to_remove = []
        for i, obstacle in enumerate(obstacles):
            if soccer_ball.colliderect(obstacle):
                x_ball_speed *= -1
                obstacles_to_remove.append(i)
            if player.colliderect(obstacle):
                player_slowed = True
                time_left_slow_effect = current_time + 3
                obstacles_to_remove.append(i)
        
        for i in sorted(obstacles_to_remove, reverse=True):
            obstacles.pop(i)

        if soccer_ball.colliderect(second_enemy):
            x_ball_speed *= -1
            soccer_ball.x = second_enemy.right
            y_ball_speed += random.choice([-1, 1]) * 2

        if soccer_ball.y > other_goalie.centery:
            goalie_movement(other_goalie, 'down')
        else:
            goalie_movement(other_goalie, 'up')

        if soccer_ball.y > player_goalie.centery:
            goalie_movement(player_goalie, 'down')
        else:
            goalie_movement(player_goalie, 'up')

        screen.blit(background_image, (0, 0))

        for powerup in powerups:
            if powerup['type'] == 'size':
                pygame.draw.rect(screen, (255, 0, 0), powerup['rect'])
            elif powerup['type'] == 'speed':
                pygame.draw.rect(screen, (0, 255, 0), powerup['rect'])
            elif powerup['type'] == 'invincible':
                pygame.draw.rect(screen, (0, 0, 255), powerup['rect'])
            elif powerup['type'] == 'freeze':
                pygame.draw.rect(screen, (0, 255, 255), powerup['rect'])
        
        for coin in coin_object:
            pygame.draw.ellipse(screen, (255, 215, 0), coin)
            
        for puddle in mud_puddles:
            pygame.draw.ellipse(screen, (139, 69, 19), puddle)
            
        for obstacle in obstacles:
            pygame.draw.rect(screen, (200, 20, 20), obstacle)

        screen.blit(player_image, player)
        screen.blit(ronaldo_image, ronaldo)
        
        if enemies_frozen:
            frozen_overlay = pygame.Surface((second_enemy.width, second_enemy.height), pygame.SRCALPHA)
            frozen_overlay.fill((0, 255, 255, 128))
            screen.blit(second_enemy_image, second_enemy)
            screen.blit(frozen_overlay, second_enemy)
            
            frozen_overlay = pygame.Surface((ronaldo.width, ronaldo.height), pygame.SRCALPHA)
            frozen_overlay.fill((0, 255, 255, 128))
            screen.blit(frozen_overlay, ronaldo)
        else:
            screen.blit(second_enemy_image, second_enemy)
            
        pygame.draw.rect(screen, grey_color, player_goalie)
        pygame.draw.rect(screen, grey_color, other_goalie)
        pygame.draw.ellipse(screen, grey_color, soccer_ball)
        pygame.draw.aaline(screen, grey_color, (screen_width/2, 0), (screen_width/2, screen_height))
        
        if rain_effect:
            for _ in range(100):
                pygame.draw.line(screen, (200, 200, 255), 
                                (random.randint(0, screen_width), random.randint(0, screen_height)), 
                                (random.randint(0, screen_width), random.randint(0, screen_height)), 1)
        
        if fan_cheering:
            cheer_text = timer_font.render("CROWD GOES WILD!", True, (255, 215, 0))
            screen.blit(cheer_text, (screen_width//2 - 100, screen_height - 50))
        
        timer_text = timer_font.render(f"Time: {clock_time(time_remaining)}", True, timer_color)
        screen.blit(timer_text, (screen_width//2 - 70, 20))
        
        score_text = score_font.render(f"{opponent_score} - {player_score}", True, timer_color)
        screen.blit(score_text, (screen_width//2 - 60, 60))
        
        coin_text = timer_font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(coin_text, (screen_width - 200, 20))
        
        if size_on:
            size_text = timer_font.render("Size Boost!", True, (255, 0, 0))
            screen.blit(size_text, (20, 20))
        
        if speed_on:
            speed_text = timer_font.render("Speed Boost!", True, (0, 255, 0))
            screen.blit(speed_text, (20, 60))
            
        if player_slowed:
            slow_text = timer_font.render("Slowed Down!", True, (139, 69, 19))
            screen.blit(slow_text, (20, 100))
            
        if enemies_frozen:
            freeze_text = timer_font.render("Enemies Frozen!", True, (0, 255, 255))
            screen.blit(freeze_text, (20, 140))
            
        if rain_effect:
            rain_text = timer_font.render("Rainy Weather!", True, (200, 200, 255))
            screen.blit(rain_text, (20, 180))

        # Handle goal animation and delayed respawn
        if goal_scored:
            current_time = pygame.time.get_ticks()
            time_since_goal = current_time - goal_time
            
            # Flash the appropriate goalie
            if time_since_goal < 5000:  # During the 5 second delay
                flash_index = (time_since_goal // flash_interval) % 2
                flash_color = flash_colors[flash_index]
                
                if goal_side == "left":
                    # Left goal was scored on, flash the left goalie
                    pygame.draw.rect(screen, flash_color, other_goalie)
                else:
                    # Right goal was scored on, flash the right goalie
                    pygame.draw.rect(screen, flash_color, player_goalie)
                    
                # Display "GOAL!" text
                goal_font = pygame.font.SysFont("monospace", 80)
                goal_text = goal_font.render("GOAL!", True, (255, 0, 0))
                screen.blit(goal_text, (screen_width//2 - goal_text.get_width()//2, screen_height//2 - 40))
            else:
                # After 5 seconds, reset the ball and clear the goal state
                goal_scored = False
                ball_restart()
        
        pygame.display.flip()
        clock.tick(60)

def create_powerup_level3():
    powerup_type = random.choice(['size', 'speed', 'invincible', 'freeze'])
    power_x = random.randint(100, screen_width - 100)
    power_y = random.randint(100, screen_height - 100)
    
    powerup_box = pygame.Rect(power_x, power_y, 30, 30)
    return {'rect': powerup_box, 'type': powerup_type}

def create_mud_puddle():
    puddle_x = random.randint(100, screen_width - 100)
    puddle_y = random.randint(100, screen_height - 100)
    
    puddle_box = pygame.Rect(puddle_x, puddle_y, 50, 50)
    return puddle_box

def create_obstacle():
    obstacle_x = random.randint(100, screen_width - 100)
    obstacle_y = random.randint(100, screen_height - 100)
    
    obstacle_box = pygame.Rect(obstacle_x, obstacle_y, 40, 40)
    return obstacle_box

def move_second_enemy(second_enemy):
    if soccer_ball.y < second_enemy.y:
        second_enemy.y -= 3
    if soccer_ball.y > second_enemy.y:
        second_enemy.y += 3
        
    middle_x = screen_width // 2
    
    if second_enemy.x < middle_x - 100:
        second_enemy.x += 3
    if second_enemy.x > middle_x + 100:
        second_enemy.x -= 3

def main():
    clock = init_game()
    loading_animation()
    loading_screen()
    level_1()
    level_3()
    level_5()
    

if __name__ == "__main__":
    main()
