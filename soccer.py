'''
Pygame Soccer Game
ICS3U
Authors: Swanish and Selina
Purpose: Create a soccer pong game with power-ups and coins for Mohammed. The first level is basic with a Ronaldo and the player, with a few powerups here and there. The second level has a faster ball speed, one ronaldo and more powerups. The third level has one more ronaldo along with some more powerups, and finally, the last level has 3 Ronaldos and even more powerups! On the ending screen, the student wins a lamborghini.
Date: 2025-04-17

Functions:
moving_ball()
player_out()
ronaldo_movement()
goalie_movement()
screen_switcher()
loading_animation()
loading_screen()
level_screen()
bal_restart()
clock_time()
check_goal()
create_power()
create_powersforlevel2()
create_coin()
initialize_game()
level_transition_screen()
level_1()
level_2()
level_3()
create_powerupslevel3()
create_mud_puddle()
create_obstacle()
move_second_enemy()
move_third_enemy()
level_4()
create_powerupslevel4()
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
    """
    Moves the soccer ball and handles collisions, boundaries, and goal checks.

    Parameters:
        None (uses global variables and objects)

    Returns:
        None

    By: Swanish and Selina
    """
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
def player_out():
    """
    Keeps the player within the screen boundaries.

    Parameters:
        None

    Returns:
        None

    By: Swanish and Selina
    """
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
    """
    Moves Ronaldo towards the soccer ball automatically (super cool bot movement)

    Parameters:
        None

    Returns:
        None

    By: Swanish and Selina
    """
    ronaldo_limit_x = screen_width * 3//5

    if ronaldo.x < soccer_ball.x and ronaldo.x < ronaldo_limit_x:
        ronaldo.x += speed_ronaldo
        
    if ronaldo.x > soccer_ball.x:
        ronaldo.x -= speed_ronaldo

    if ronaldo.y < soccer_ball.y:
        ronaldo.y += speed_ronaldo

    if ronaldo.y > soccer_ball.y:
        ronaldo.y -= speed_ronaldo

# moving teh goalies
def goalie_movement(goalie, where):
    """
    Moves the goalie up or down on the screen by itself

    Parameters:
        goalie (Rect): The goalie object to move.
        where (str): Direction to move ('up' or 'down').

    Returns:
        None

    By: Swanish and Selina
    """
    if goalie.top <= 0:
        goalie.top = 0

    if goalie.bottom >= screen_height:
        goalie.bottom = screen_height

    # keeping the goalie in bounds, by moving it back slightly
    if where == 'up' and goalie.top > 0:
        goalie.y -= 4

    if where == 'down' and goalie.bottom < screen_height:
        goalie.y += 4

# add the screen switcher
level1 = True
def screen_switcher():
    """
    Switches to the appropriate level screen based on what the current level is 

    Parameters:
        None

    Returns:
        None
    
    By: Swanish and Selina
    """
    if level1:
        level_1()
    elif level2:
        level_2()
    elif level3:
        level_3()
    elif level4:
        level_4()
    elif level5:
        level_5()
    else:
        pygame.quit()
        sys.exit()

# function to draw loading animation
def loading_animation():
    """
    Displays a loading animation with a moving soccer ball until it reaches the end of the screen.

    Parameters:
        None

    Returns:
        None

    By: Swanish and Selina
    """
     
    positionn = pygame.math.Vector2(346,480)
    velocity = pygame.math.Vector2(4,0)
    i_soccerball = pygame.transform.scale(pygame.image.load('soccer_ball.png'),(50,50)) 
    soccerball_image = i_soccerball.convert_alpha()

    waiting = True

    while waiting: 
        positionn += velocity 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  

        positionn += velocity  # move the soccer ball

        if positionn.x + 25 >= 960:  # when animation reaches the end
            waiting = False  
            velocity.x = 0  
            screen.fill(0)
            pygame.display.update()
            return  

        # continue animating
        screen.fill(0)
        image_rect = soccerball_image.get_rect(center=(positionn.x, positionn.y))
        screen.blit(soccerball_image, image_rect)
        pygame.display.update()
        clock.tick(40)

# function for the loading screen
def loading_screen():
    """
    Displays a loading screen with a soccer background image and title.
    Waits for the player to press any key to continue.

    Parameters:
        None

    Returns:
        None

    By: Swanish and Selina
    """

    # load background image
    background_img = pygame.image.load("soccer_field.jpg")
    background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
    
    # set up title text
    title_font = pygame.font.SysFont("monospace", 60)
    title_text = title_font.render("Soccer Legends", True, pygame.Color("black"))
    title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 3))
    
    # set up continue text
    continue_font = pygame.font.SysFont("monospace", 40)
    continue_text = continue_font.render("Press any key to continue...", True, pygame.Color("gray"))
    continue_rect = continue_text.get_rect(center=(screen_width // 2, screen_height * 2 // 3))

    # show the text
    screen.blit(background_img, (0, 0))
    screen.blit(title_text, title_rect)
    screen.blit(continue_text, continue_rect)
    pygame.display.flip()

    # wait for mohammed to press a key before continuign
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
    """
    Displays the current level on screen and waits 2 seconds or for a key press to continue.

    Parameters:
        level (str): The level text to display.

    Returns:
        None

    By: Swanish and Selina
    """
    # define fonts and text
    font = pygame.font.SysFont("monospace", 40)
    text = font.render(level, True, pygame.Color("white"))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    # brief descriptions for each level
    desc_font = pygame.font.SysFont("monospace", 20)
    if level == "Level 1: The Beginnings":
        description = desc_font.render("This is your first game against Ronaldo!", True, pygame.Color("white")) 
        description2 = desc_font.render("There are many objects on the field to help you!",True, pygame.Color("white"))
    
    if level == "Level 2: The Faster One":
        description = desc_font.render("Oh no! The ball is getting faster!", True, pygame.Color("white")) 
        description2 = desc_font.render("There are many objects on the field to help you!",True, pygame.Color("white"))

    if level == "Level 3: Double Trouble":
        description = desc_font.render("There are more of them?!?!", True, pygame.Color("white")) 
        description2 = desc_font.render("Careful: Is that rain??",True, pygame.Color("white"))

    if level == "Level 4: Triple Fun":
        description = desc_font.render("No way! Three of them??", True, pygame.Color("white")) 
        description2 = desc_font.render("Not all objects on the field will help you!",True, pygame.Color("white"))

    description_rect = description.get_rect(center=(screen_width // 2, screen_height // 2+100))
    description2_rect = description2.get_rect(center=(screen_width // 2, screen_height // 2+125))

    # display the message and wait for a key press
    screen.fill(background_color)
    screen.blit(text, text_rect)
    screen.blit(description,description_rect)
    screen.blit(description2,description2_rect)

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
    """
    Resets the ball to the center with new random speed if no goal was scored.

    Parameters:
        None

    Returns:
        None

    By: Swanish and Selina
    """

    global x_ball_speed, y_ball_speed, goal_scored
    
    # only restart the ball if we're not in a goal animation
    if not goal_scored:
        soccer_ball.center = (screen_width/2, screen_height/2)
        x_ball_speed = 7 * random.choice((1, -1))
        y_ball_speed = 7 * random.choice((1, -1))

# format the time correctly
def clock_time(seconds):
    """
    Converts a given time in seconds to a formatted string

    Parameters:
        seconds (int): The time in seconds to convert.

    Returns:
        str: The formatted time as a string in MM:SS format.

    By: Swanish and Selina
    """
    
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
    
    """
    Checks if a goal has been scored and updates scores, game state, and transitions to the next level if necessary.

    Parameters:
        None

    Returns:
        None (or triggers a level transition if a player reaches 5 points)

    By: Swanish and Selina
    """

    global player_score, opponent_score, goal_scored, goal_time, goal_side, current_l, next_l
    
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
        level_transition_screen(current_l, next_l) 
        return

# create a POWERUP! for level 1
def create_powerup():
    """
    Creates a random power-up with a random type and position.

    Parameters:
        None

    Returns:
        dict: A dictionary containing the power-up's 'rect' (position and size) and 'type' (either 'size' or 'speed').

    By: Swanish and Selina
    """

    powerup_type = random.choice(['size', 'speed'])
    power_x = random.randint(100, screen_width - 100)
    power_y = random.randint(100, screen_height - 100)
    
    powerup_box = pygame.Rect(power_x, power_y, 30, 30)
    return {'rect': powerup_box, 'type': powerup_type}

# create ht powerups for level 2
def create_powersforlevel2():
    """
    Creates a random power-up for level 2 with a random type and position.

    Parameters:
        None

    Returns:
        dict: A dictionary containing the power-up's 'rect' (position and size) and 'type' (either 'size', 'speed', or 'ball-back').
   
    By: Swanish and Selina
     """
    powerup_type = random.choice(['size','speed','ball-back'])
    power_x = random.randint(100, screen_width - 100)
    power_y = random.randint(100, screen_height - 100)

    powerup_box = pygame.Rect(power_x,power_y, 30, 30)
    return {'rect': powerup_box, 'type': powerup_type}

# make the coin (remember to add shop as student requested shop)
def create_coin():
    """
    Creates a coin at a random position on the screen.

    Parameters:
        None

    Returns:
        Rect: A pygame.Rect representing the coin's position and size.

    By: Swanish and Selina
    """

    coin_x = random.randint(100, screen_width - 100)
    coin_y = random.randint(100, screen_height - 100)
    
    coin_box = pygame.Rect(coin_x, coin_y, 20, 20)
    return coin_box

def initialize_game():
    """
    Initializes the game by setting up the screen, background, objects, and global variables.

    Parameters:
        None

    Returns:
        clock: The pygame clock object used for controlling the game frame rate.

    By: Swanish and Selina
    """
    # initialize pygame and create global variables
    global screen_width, screen_height, screen, background_image, background_color, x_ball_speed, y_ball_speed, speed_ronaldo, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, ronaldo_image, player_image_original, grey_color, timer_font, timer_color, score_font, player_score, opponent_score, coins

    pygame.init()
    
    # define the screen size
    screen_width = 1280
    screen_height = 960
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mohammed's Soccer")

    # setting up the background and scaling the images
    background_image = pygame.image.load('soccerfields/1.png') 
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
    """
    Displays the level transition screen, showing level completion, score, coins, countdown, 
    and the option to skip to the next level.

    Parameters:
        current_level (str): The current level that was completed.
        next_level (str): The next level to start after the transition.

    Returns:
        None

    By: Swanish and Selina
    """

    # define all the globals
    global level1, level2, level3, level4, level5, player_score, opponent_score, current_l, next_l
    
    font_LARGEE = pygame.font.SysFont("monospace", 40)
    font_smal = pygame.font.SysFont("monospace", 30)
    
    countdown_seconds = 10
    countdown_event = pygame.USEREVENT + 10
    pygame.time.set_timer(countdown_event, 1000)
    
    # display the text
    level_completed_text = font_LARGEE.render(f"Level {current_level} Completed!", True, pygame.Color("white"))
    score_text = font_smal.render(f"Score: {opponent_score} - {player_score}", True, pygame.Color("white"))
    
    # add who won text
    if player_score > opponent_score:
        winner_text = font_smal.render("OMG YOU WON!!!", True, pygame.Color("green"))
    else:
        winner_text = font_smal.render("THE RONALDO(S) WON!?!", True, pygame.Color("red"))
    
    
    coins_text = font_smal.render(f"Coins: {coins}", True, pygame.Color("gold"))
    next_level_text = font_smal.render(f"Next Level in: {countdown_seconds}", True, pygame.Color("white"))
    skip_text = font_smal.render("Press any key to skip", True, pygame.Color("gray"))

    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # display the countdown 
            if event.type == countdown_event:
                countdown_seconds -= 1
                next_level_text = font_smal.render(f"Next Level in: {countdown_seconds}", True, pygame.Color("white"))
                if countdown_seconds <= 0:
                    waiting = False
                    pygame.time.set_timer(countdown_event, 0)
            
            if event.type == pygame.KEYDOWN: # if key down, start the next level 
                waiting = False
                pygame.time.set_timer(countdown_event, 0)
        
        # put the stuff on screen
        screen.fill(background_color)
        screen.blit(level_completed_text, (screen_width//2 - level_completed_text.get_width()//2, screen_height//2 - 100))
        screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, screen_height//2 - 50))
        # Add the winner text below the score
        screen.blit(winner_text, (screen_width//2 - winner_text.get_width()//2, screen_height//2 - 20))
        screen.blit(coins_text, (screen_width//2 - coins_text.get_width()//2, screen_height//2 + 10))
        screen.blit(next_level_text, (screen_width//2 - next_level_text.get_width()//2, screen_height//2 + 50))
        screen.blit(skip_text, (screen_width//2 - skip_text.get_width()//2, screen_height//2 + 100))
        pygame.display.flip()
        clock.tick(60)
    
    # make sire that no other levels are on when we are switiching the screen 
    if next_level == "1":
        level1 = True
        level2 = level3 = level4 = level5 = False
    elif next_level == "2":
        level2 = True
        level1 = level3 = level4 = level5 = False
    elif next_level == "3":
        level3 = True
        level1 = level2 = level4 = level5 = False
    elif next_level == "4":
        level4 = True 
        level1 = level2 = level3 = level5 = False
    elif next_level == "5":
        level5 = True
        level1 = level2 = level3 = level4 = False
    else:
        level1 = level2 = level3 = level4 = level5 = False
        pygame.quit()
        sys.exit()
    
    screen_switcher()

# level one function
def level_1():
    """
    Runs the gameplay for Level 1 of the game. This includes managing player movements, power-ups, 
    coin collection, goal-scoring events, and the countdown timer. 

    Returns:
        None

    By: Swanish and Selina
    """
    level_screen("Level 1: The Beginnings")
    # add player_image and other required variables to global
    global player_score, opponent_score, coins, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, player_image_original, ronaldo_image, goal_scored, goal_time, goal_side, current_l, next_l

    current_l = "1"
    next_l = "2"
    
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
                    level_transition_screen("1","2") 
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
        player_out()
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

def level_2():
    """
    Starts and manages Level 2 of the soccer game.

    Handles game logic including player movement, powerups, coin collection, ball movement, and scoring.
    It also updates the screen with the current state and displays the timer, score, and active powerups.

    Parameters:
        None

    Returns:
        None

    By: Swanish and Selina
    """
    level_screen("Level 2: The Faster One")
    # add player_image and other required variables to global
    global player_score, opponent_score, coins, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, player_image_original, ronaldo_image, level_num, x_ball_speed, y_ball_speed, goal_scored, goal_time, goal_side, current_l, next_l
    # level 2 specific settings
    current_l = "2"
    next_l = "3"

    x_ball_speed = 0
    y_ball_speed = 0
    soccer_ball.center = (screen_width/2, screen_height/2)
    ball_activated = False
    
    background_image = pygame.image.load('soccerfields/2.png') 
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height)) 

    game_length_time = 120

    #resetting
    player_score = 0
    opponent_score = 0
    coins = 0
    ball_activated = False
    
    # set up timers
    timer_running = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_running, 1000)

    powerup_running = pygame.USEREVENT + 2
    pygame.time.set_timer(powerup_running, 5000)  # new powerup every 5 seconds

    coin_running = pygame.USEREVENT + 3
    pygame.time.set_timer(coin_running, 5000)  # new coin every 5 seconds


    # game variables
    running = True
    time_remaining = game_length_time

    # powerup variables
    powerups = []
    time_left_size_boost = 0
    time_left_speed_boost = 0
    time_left_ball_back_text = 0
    normal_player_speed = 8
    boosted_player_speed = 14
    size_on = False
    speed_on = False
    ball_back = False

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
                    level_transition_screen(2,3)
                    return
            
            # limited powerups allowed
            if event.type == powerup_running:
                if len(powerups) < 5: 
                    powerups.append((create_powersforlevel2()))
                    
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
            current_speed = 8

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

        if ball_back and current_time > time_left_ball_back_text:
            ball_back = False

        # call the moving ball funcitons
        if ball_activated or key_down or key_up or key_left or key_right:
            if not ball_activated:
                # Initialize ball speed only once when first key is pressed
                x_ball_speed = 9 * random.choice((2, -2, -1, 1))
                y_ball_speed = 9 * random.choice((1, -1, 2, -2))
                ball_activated = True
            moving_ball()

        
        player.x += speed_player_x
        player.y += speed_player_y
        player_out()
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

                 # if the player touches a BALL BACK powerup, the ball goes to their position
                elif powerup['type'] == 'ball-back':
                    ball_back = True
                    time_left_ball_back_text = current_time + 2
                    soccer_ball.x = player.x+5
                    soccer_ball.y = player.y

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
            elif powerup['type'] == 'ball-back':
                pygame.draw.rect(screen, (138,43,226), powerup['rect']) # blue for ball to come back to player
        
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

        if ball_back:
            back_text = timer_font.render("You have the ball!", True, (0, 0, 255))
            screen.blit(back_text,(20,100))

        # handle goal animation and delayed respawn
        if goal_scored:
            current_time = pygame.time.get_ticks()
            time_since_goal = current_time - goal_time
            
            # flash the appropriate goalie
            if time_since_goal < 5000:  # during the 5 second delay
                flash_index = (time_since_goal // flash_interval) % 2
                flash_color = flash_colors[flash_index]
                
                if goal_side == "left":
                    # left goal was scored on, flash the left goalie
                    pygame.draw.rect(screen, flash_color, other_goalie)
                else:
                    # right goal was scored on, flash the right goalie
                    pygame.draw.rect(screen, flash_color, player_goalie)
                    
                # show text
                goal_font = pygame.font.SysFont("monospace", 80)
                goal_text = goal_font.render("GOAL!", True, (255, 0, 0))
                screen.blit(goal_text, (screen_width//2 - goal_text.get_width()//2, screen_height//2 - 40))
            else:
                # reset ball after 5 secs
                goal_scored = False
                ball_restart()
                x_ball_speed = 10 * random.choice((1, -1))
                y_ball_speed = 10 * random.choice((1, -1))
        
        pygame.display.flip()
        clock.tick(60)

def level_3():
    """
    Initializes and runs Level 3 of the game with power-ups, obstacles, and random events.
    
    Parameters:
        None
    
    Returns:
        None

    By: Swanish and Selina
    """

    level_screen("Level 3: Double Trouble")
    
    # initialize the global variables
    global player_score, opponent_score, coins, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, player_image_original, ronaldo_image, x_ball_speed, y_ball_speed, goal_scored, goal_time, goal_side, current_l, next_l
    
    # initialize the level specific variables
    current_l = "3"
    next_l = "4"

    # restart the player scores 
    player_score = 0
    opponent_score = 0
    coins = 0
    ball_activated = False

    # initialize the speeds and the locatiosn
    x_ball_speed = 0
    y_ball_speed = 0
    soccer_ball.center = (screen_width/2, screen_height/2)

    # check if goal scored for the flash funciton
    goal_scored = False
    goal_time = 0
    goal_side = ""
    flash_interval = 200  
    flash_colors = [(255, 255, 255), grey_color] 

    # start background
    background_image = pygame.image.load("soccerfields/3.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    game_length_time = 240 # game length initialize
    
    # set up events
    timer_running = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_running, 1000)
    
    powerup_running = pygame.USEREVENT + 2
    pygame.time.set_timer(powerup_running, 8000)
    
    coin_running = pygame.USEREVENT + 3
    pygame.time.set_timer(coin_running, 5000)
    
    puddle_timer = pygame.USEREVENT + 4
    pygame.time.set_timer(puddle_timer, 15000)
    
    weather_timer = pygame.USEREVENT + 5
    pygame.time.set_timer(weather_timer, 10000)
    
    fan_cheer_timer = pygame.USEREVENT + 6
    pygame.time.set_timer(fan_cheer_timer, 12000)
    
    # game variables
    running = True
    time_remaining = game_length_time
    
    # initialize other variables
    powerups = []
    time_left_size_boost = 0
    time_left_speed_boost = 0
    time_left_slow_effect = 0
    time_left_freeze_enemies = 0
    normal_player_speed = 7
    boosted_player_speed = 14
    slowed_player_speed = 3

    # checking if the poewrups are on
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
    
    # key tracking
    key_down = False
    key_up = False
    key_left = False
    key_right = False
    
    # create the second enemy
    second_enemy = pygame.Rect(screen_width // 2, screen_height//2 - 50, 100, 100)
    second_enemy_image = pygame.image.load("ronaldo.png")
    second_enemy_image = pygame.transform.scale(second_enemy_image, (100, 100))
    second_enemy_speed = 3
    
    # while its running
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # code to make the timer owrk
            if event.type == timer_running:
                time_remaining -= 1
                if time_remaining <= 0:
                    level_transition_screen("3","4") 
                    return
            
            # code to make the powerup work for each level
            if event.type == powerup_running:
                if len(powerups) < 2:
                    powerups.append(create_powerup_level3())
            
            # code to create the coins
            if event.type == coin_running:
                if len(coin_object) < 3:
                    coin_object.append(create_coin())
            
            # code to create the mud puddls
            if event.type == puddle_timer:
                if len(mud_puddles) < 4:
                    mud_puddles.append(create_mud_puddle())
            
            # code to create the distracting rain
            if event.type == weather_timer:
                if not rain_effect:
                    rain_effect = True
                    rain_end_time = current_time + 15
                    x_ball_speed *= 0.8
                    y_ball_speed *= 0.8
                
            # fan cheering effect
            if event.type == fan_cheer_timer and random.random() > 0.5:
                fan_cheering = True
                fan_end_time = current_time + 5
                if random.random() > 0.5:
                    player_score += 1
                else:
                    obstacles.append(create_obstacle())

            # check if the keys are pressed
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
        # reset the speeds
        speed_player_x = 0
        speed_player_y = 0

        # adjust speeds according to the boosts
        if player_slowed:
            current_speed = slowed_player_speed
        elif speed_on:
            current_speed = boosted_player_speed
        else:
            current_speed = normal_player_speed

        # check if the keys are down 
        if key_down:
            speed_player_y = current_speed
        if key_up:
            speed_player_y = -current_speed
        if key_left:
            speed_player_x = -current_speed
        if key_right:
            speed_player_x = current_speed

        # turn off the size boost
        if size_on and current_time > time_left_size_boost:
            size_on = False
            original_center = player.center
            player_image = player_image_original.copy()
            player.width, player.height = 100, 100
            player.center = original_center

        # turn off the speed boost
        if speed_on and current_time > time_left_speed_boost:
            speed_on = False

        # turn off the slow effect
        if player_slowed and current_time > time_left_slow_effect:
            player_slowed = False
            
        # turn off the freeze effect
        if enemies_frozen and current_time > time_left_freeze_enemies:
            enemies_frozen = False
        
        #t turn off the rain effect
        if rain_effect and current_time > rain_end_time:
            rain_effect = False
            x_ball_speed /= 0.8
            y_ball_speed /= 0.8
        
        # turn off the fan cheering
        if fan_cheering and current_time > fan_end_time:
            fan_cheering = False

        
        if ball_activated or key_down or key_up or key_left or key_right:
            if not ball_activated:
                # initialize ball speed only once when first key is pressed
                x_ball_speed = 7 * random.choice((2, -2, -1, 1))
                y_ball_speed = 7 * random.choice((1, -1, 2, -2))
                ball_activated = True
            moving_ball()
        
        player.x += speed_player_x
        player.y += speed_player_y
        player_out() # reset the player if they go out of bounds 
        
        # reset the movements when not frozen
        if not enemies_frozen:
            ronaldo_movement()
            move_second_enemy(second_enemy)

        # remove the powerups 
        powerups_to_remove = []

        # poweruos
        for i, powerup in enumerate(powerups):
            if player.colliderect(powerup['rect']):
                if powerup['type'] == 'size': # add size if touched
                    size_on = True
                    time_left_size_boost = current_time + 30
                    original_center = player.center
                    player_image = pygame.transform.scale(player_image_original, (150, 150))
                    player.width, player.height = 150, 150
                    player.center = original_center
                    
                elif powerup['type'] == 'speed': # add speed if touched
                    speed_on = True
                    time_left_speed_boost = current_time + 30
                    
                elif powerup['type'] == 'invincible': # add invincibility if touched 
                    player_slowed = False
                    time_left_slow_effect = 0
                    
                elif powerup['type'] == 'freeze': # add freeze if touched 
                    enemies_frozen = True
                    time_left_freeze_enemies = current_time + 10
                
                # remove the powerup
                powerups_to_remove.append(i)
        
        for i in sorted(powerups_to_remove, reverse=True):
            powerups.pop(i)
        
        # remove the coins
        coins_to_remove = []
        for i, coin in enumerate(coin_object):
            if player.colliderect(coin):
                coins += 1
                coins_to_remove.append(i)
        
        for i in sorted(coins_to_remove, reverse=True):
            coin_object.pop(i)
        
        # remove the puddles
        puddles_to_remove = []
        for i, puddle in enumerate(mud_puddles):
            if player.colliderect(puddle):
                player_slowed = True
                time_left_slow_effect = current_time + 5
                puddles_to_remove.append(i)
        
        for i in sorted(puddles_to_remove, reverse=True):
            mud_puddles.pop(i)
        
        # remove the obstacles
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

        # check if the ball hits the other enemy and change its direction
        if soccer_ball.colliderect(second_enemy):
            x_ball_speed *= -1
            soccer_ball.x = second_enemy.right
            y_ball_speed += random.choice([-1, 1]) * 2

        # goalie movements
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
        
        # draw the blue box thing if enemies are forzen
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
        
        # draw a bunch of random lines to distract the player
        if rain_effect:
            for i in range(100):
                pygame.draw.line(screen, (200, 200, 255), 
                                (random.randint(0, screen_width), random.randint(0, screen_height)), 
                                (random.randint(0, screen_width), random.randint(0, screen_height)), 1)
                
        # if the fan is cheering 
        if fan_cheering:
            cheer_text = timer_font.render("CROWD GOES WILD OMG AHH!", True, (255, 215, 0))
            screen.blit(cheer_text, (screen_width//2 - 100, screen_height - 50))
        
        # timer display
        timer_text = timer_font.render(f"Time: {clock_time(time_remaining)}", True, timer_color)
        screen.blit(timer_text, (screen_width//2 - 70, 20))
        
        # score display
        score_text = score_font.render(f"{opponent_score} - {player_score}", True, timer_color)
        screen.blit(score_text, (screen_width//2 - 60, 60))
        
        # coin text display
        coin_text = timer_font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(coin_text, (screen_width - 200, 20))
        
        # display active powerups
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

        # handle goal animation and delayed respawn
        if goal_scored:
            current_time = pygame.time.get_ticks()
            time_since_goal = current_time - goal_time
            
            # flash the appropriate goalie
            if time_since_goal < 5000:  # during the 5 second delay
                flash_index = (time_since_goal // flash_interval) % 2
                flash_color = flash_colors[flash_index]
                
                if goal_side == "left":
                    # left goal was scored on, flash the left goalie
                    pygame.draw.rect(screen, flash_color, other_goalie)
                else:
                    # right goal was scored on, flash the right goalie
                    pygame.draw.rect(screen, flash_color, player_goalie)
                    
                # display "GOAL!" text
                goal_font = pygame.font.SysFont("monospace", 80)
                goal_text = goal_font.render("GOAL!", True, (255, 0, 0))
                screen.blit(goal_text, (screen_width//2 - goal_text.get_width()//2, screen_height//2 - 40))
            else:
                # after 5 seconds, reset the ball and clear the goal state
                goal_scored = False
                ball_restart()
        
        pygame.display.flip()
        clock.tick(60)

def create_powerup_level3():
    """
    Creates a random power-up for level 3 with random position and type.
    
    Parameters:
        None
    
    Returns:
        dict: A dictionary containing the power-up's 'rect' (position and size) and 'type' (e.g., 'size', 'speed', 'invincible', 'freeze').
   
    
    By: Swanish and Selina
    """

    # create the powerups
    powerup_type = random.choice(['size', 'speed', 'invincible', 'freeze'])
    power_x = random.randint(100, screen_width - 100)
    power_y = random.randint(100, screen_height - 100)
    
    powerup_box = pygame.Rect(power_x, power_y, 30, 30)
    return {'rect': powerup_box, 'type': powerup_type}

def create_mud_puddle():

    """
    Creates a random mud puddle at a random position on the screen.
    
    Parameters:
        None
    
    Returns:
        pygame.Rect: A rectangle representing the position and size of the mud puddle.

    By: Swanish and Selina
    """

    # define the mud puddle
    # create the mud puddle
    puddle_x = random.randint(100, screen_width - 100)
    puddle_y = random.randint(100, screen_height - 100)
    
    puddle_box = pygame.Rect(puddle_x, puddle_y, 50, 50)
    return puddle_box


def create_obstacle():

    """
    Creates a random obstacle at a random position on the screen.
    
    Parameters:
        None
    
    Returns:
        pygame.Rect: A rectangle representing the position and size of the obstacle.

    By: Swanish and Selina
    """

    # create the obstacles
    obstacle_x = random.randint(100, screen_width - 100)
    obstacle_y = random.randint(100, screen_height - 100)
    
    obstacle_box = pygame.Rect(obstacle_x, obstacle_y, 40, 40)
    return obstacle_box

def move_second_enemy(second_enemy):

    """
    Moves the second enemy towards the soccer ball and the middle of the screen.
    
    Parameters:
        second_enemy (pygame.Rect): The rectangle representing the second enemy's position and size.
    
    Returns:
        None

    By: Swanish and Selina
    """
    
    # move the second enemy
    if soccer_ball.y < second_enemy.y:
        second_enemy.y -= 3
    if soccer_ball.y > second_enemy.y:
        second_enemy.y += 3
        
    middle_x = screen_width // 2
    
    if second_enemy.x < middle_x - 100:
        second_enemy.x += 3
    if second_enemy.x > middle_x + 100:
        second_enemy.x -= 3


# move the third enemy
def move_third_enemy(third_enemy):

    """
    Moves the third enemy towards the soccer ball and the middle of the screen.
    
    Parameters:
        third_enemy (pygame.Rect): The rectangle representing the third enemy's position and size.
    
    Returns:
        None]

    By: Swanish and Selina
    """

    if soccer_ball.y < third_enemy.y:
        third_enemy.y -= 2
    if soccer_ball.y > third_enemy.y:
        third_enemy.y += 2
    
    middle_x = screen_width // 2

    if third_enemy.x < middle_x - 100:
        third_enemy.x += 2
    if third_enemy.x > middle_x + 100:
        third_enemy.x -= 2


def level_4():
    level_screen("Level 4: Triple Fun")

    """
    Starts Level 4, managing player movements, enemies, power-ups, obstacles, and coin collection.

    Parameters:
    None

    Returns:
    None

    By: Swanish and Selina
    """
    
     # define global variables 
    global player_score, opponent_score, coins, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, player_image_original, ronaldo_image, x_ball_speed, y_ball_speed, goal_scored, goal_time, goal_side, current_l, next_l
    
    # initialize the level specific variables
    current_l = "4"
    next_l = "5"

    # restart the player scores
    player_score = 0
    opponent_score = 0
    coins = 0
    ball_activated = False
    
    # initialize the speeds and the locatiosn
    x_ball_speed = 0
    y_ball_speed = 0
    soccer_ball.center = (screen_width/2, screen_height/2)

    # check if goal scored for the flash funciton
    goal_scored = False
    goal_time = 0
    goal_side = ""
    flash_interval = 200  
    flash_colors = [(255, 255, 255), grey_color] 
    
    #load background
    background_image = pygame.image.load("soccerfields/4.png")
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

    game_length_time = 240
    
    # set up events
    timer_running = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_running, 1000)
    
    powerup_running = pygame.USEREVENT + 2
    pygame.time.set_timer(powerup_running, 8000)
    
    coin_running = pygame.USEREVENT + 3
    pygame.time.set_timer(coin_running, 5000)
    
    puddle_timer = pygame.USEREVENT + 4
    pygame.time.set_timer(puddle_timer, 15000)
    
    fan_cheer_timer = pygame.USEREVENT + 6
    pygame.time.set_timer(fan_cheer_timer, 12000)
    
    # game variables
    running = True
    time_remaining = game_length_time
    
    powerups = []
    time_left_size_boost = 0
    time_left_speed_boost = 0
    time_left_slow_effect = 0
    time_left_freeze_enemies = 0
    time_left_coin_lose_text = 0
    time_left_goal_lose_text = 0

    # initialize other variables
    normal_player_speed = 7
    boosted_player_speed = 14
    slowed_player_speed = 3
    size_on = False
    speed_on = False
    coin_lose = False
    goal_lose = False

    # check if the poewrups are on
    player_slowed = False
    enemies_frozen = False
    
    coin_object = []
    
    mud_puddles = []
    
    fan_cheering = False
    fan_end_time = 0
    
    obstacles = []
    
    # key tracking
    key_down = False
    key_up = False
    key_left = False
    key_right = False
    
    # enemy speeds
    second_enemy = pygame.Rect(screen_width // 2, screen_height//2 - 50, 100, 100)
    second_enemy_image = pygame.image.load("ronaldo.png")
    second_enemy_image = pygame.transform.scale(second_enemy_image, (100, 100))
    second_enemy_speed = 3

    third_enemy = pygame.Rect(screen_width // 2 - 100, screen_height//2 - 50, 100, 100)
    third_enemy_image = pygame.image.load("ronaldo.png")
    third_enemy_image = pygame.transform.scale(third_enemy_image, (100,100))
    third_enemy_speed = 2
    
    # while game runs 
    while running:
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == timer_running: # timer running
                time_remaining -= 1
                if time_remaining <= 0:
                    level_transition_screen("4","5") 
                    return
            
            if event.type == powerup_running: # create poewrups
                if len(powerups) < 2:
                    powerups.append(create_powerup_level4())
                    
            if event.type == coin_running: # create coins
                if len(coin_object) < 3:
                    coin_object.append(create_coin())
            
            if event.type == puddle_timer: # create those puddles
                if len(mud_puddles) < 4:
                    mud_puddles.append(create_mud_puddle())

            # fan cheering effect
            if event.type == fan_cheer_timer and random.random() > 0.5:
                fan_cheering = True
                fan_end_time = current_time + 5
                if random.random() > 0.5:
                    player_score += 1
                else:
                    obstacles.append(create_obstacle())

            # check if the keys are pressed
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

        # player speed initialize
        speed_player_x = 0
        speed_player_y = 0

        # adjust speeds according to the boosts
        if player_slowed:
            current_speed = slowed_player_speed
        elif speed_on:
            current_speed = boosted_player_speed
        else:
            current_speed = normal_player_speed

       # check if the keys are down
        if key_down:
            speed_player_y = current_speed
        if key_up:
            speed_player_y = -current_speed
        if key_left:
            speed_player_x = -current_speed
        if key_right:
            speed_player_x = current_speed

        # turn off the size boost
        if size_on and current_time > time_left_size_boost:
            size_on = False
            original_center = player.center
            player_image = player_image_original.copy()
            player.width, player.height = 100, 100
            player.center = original_center
        
        # turn off the speed boost
        if speed_on and current_time > time_left_speed_boost:
            speed_on = False

        # turn off the slow effect
        if player_slowed and current_time > time_left_slow_effect:
            player_slowed = False
        # turn off the freeze effect
        if enemies_frozen and current_time > time_left_freeze_enemies:
            enemies_frozen = False
        #   turn off the rain effect 
        if fan_cheering and current_time > fan_end_time:
            fan_cheering = False
    # turn off the goal lose effect
        if goal_lose and current_speed > time_left_goal_lose_text:
            goal_lose = False
        # turn off the coin lose effect
        if coin_lose and current_speed > time_left_coin_lose_text:
            coin_lose = False

        # NOTE TO SELF: ONLY IMPLENETED BECAUSE THE BALL KEPT MOVING BEFORE THE PLAYER PLAYED
        if ball_activated or key_down or key_up or key_left or key_right:
            if not ball_activated:
                # initialize ball speed only once when first key is pressed
                x_ball_speed = 7 * random.choice((2, -2, -1, 1))
                y_ball_speed = 7 * random.choice((1, -1, 2, -2))
                ball_activated = True
            moving_ball()
        
        # move the player
        player.x += speed_player_x
        player.y += speed_player_y
        player_out() # reset the player if they go out of bounds
        
        # reset the movements when not frozen
        if not enemies_frozen:
            ronaldo_movement()
            move_second_enemy(second_enemy)
            move_third_enemy(third_enemy)

        # remove the powerups
        powerups_to_remove = []
        for i, powerup in enumerate(powerups):
            if player.colliderect(powerup['rect']):
                if powerup['type'] == 'size': # add size if touched
                    size_on = True
                    time_left_size_boost = current_time + 30
                    original_center = player.center
                    player_image = pygame.transform.scale(player_image_original, (150, 150))
                    player.width, player.height = 150, 150
                    player.center = original_center
                    
                elif powerup['type'] == 'speed': # add speed if touched
                    speed_on = True
                    time_left_speed_boost = current_time + 30
                    
                elif powerup['type'] == 'invincible': # add invincibility if touched
                    player_slowed = False
                    time_left_slow_effect = 0
                    
                elif powerup['type'] == 'freeze': # add freeze if touched
                    enemies_frozen = True
                    time_left_freeze_enemies = current_time + 10
                
                elif powerup['type'] == 'coin-lose': # add coin lose if touched
                    coin_lose = True
                    time_left_coin_lose_text = current_time + 2
                    coins -= 1
                
                elif powerup['type'] == 'goal-lose': # add goal lose if touched
                    goal_lose = True 
                    time_left_goal_lose_text = current_time + 2
                    player_score -= 1
                    
                powerups_to_remove.append(i)
        
        # remove the powerup and coins
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

        # check if the ball hits the other enemy and change its direction
        if soccer_ball.colliderect(second_enemy):
            x_ball_speed *= -1
            soccer_ball.x = second_enemy.right
            y_ball_speed += random.choice([-1, 1]) * 2
        
        # check if th eball hits the third enemy and change the directioj
        if soccer_ball.colliderect(third_enemy):
            x_ball_speed *= -1
            soccer_ball.x = third_enemy.right
            y_ball_speed += random.choice([-1, 1]) * 2

        # move the goalies 
        if soccer_ball.y > other_goalie.centery:
            goalie_movement(other_goalie, 'down')
        else:
            goalie_movement(other_goalie, 'up')

        if soccer_ball.y > player_goalie.centery:
            goalie_movement(player_goalie, 'down')
        else:
            goalie_movement(player_goalie, 'up')

        screen.blit(background_image, (0, 0))

        # for each pwoerup drawe them 
        for powerup in powerups:
            if powerup['type'] == 'size':
                pygame.draw.rect(screen, (255, 0, 0), powerup['rect'])
            elif powerup['type'] == 'speed':
                pygame.draw.rect(screen, (0, 255, 0), powerup['rect'])
            elif powerup['type'] == 'freeze':
                pygame.draw.rect(screen, (0, 255, 255), powerup['rect'])
            elif powerup['type'] == 'coin-lose':
                pygame.draw.rect(screen, (0,0,0), powerup['rect'])
            elif powerup['type'] == 'goal-lose':
                pygame.draw.rect(screen, (0,0,1), powerup['rect'])
        

        # for each coin just draw them 
        for coin in coin_object:
            pygame.draw.ellipse(screen, (255, 215, 0), coin)
            
        # for each mud puddle just draw them 
        for puddle in mud_puddles:
            pygame.draw.ellipse(screen, (139, 69, 19), puddle)
        
        # draw each obstacle
        for obstacle in obstacles:
            pygame.draw.rect(screen, (200, 20, 20), obstacle)

        # create the player and the enemies
        screen.blit(player_image, player)
        screen.blit(ronaldo_image, ronaldo)
        
        # create the bolue box things when enemies are frozen
        if enemies_frozen:
            frozen_overlay = pygame.Surface((second_enemy.width, second_enemy.height), pygame.SRCALPHA)
            frozen_overlay.fill((0, 255, 255, 128))
            screen.blit(second_enemy_image, second_enemy)
            screen.blit(frozen_overlay, second_enemy)

            frozen_overlay = pygame.Surface((third_enemy.width, third_enemy.height), pygame.SRCALPHA)
            frozen_overlay.fill((0, 255, 255, 128))
            screen.blit(third_enemy_image, third_enemy)
            screen.blit(frozen_overlay, third_enemy)
            
            frozen_overlay = pygame.Surface((ronaldo.width, ronaldo.height), pygame.SRCALPHA)
            frozen_overlay.fill((0, 255, 255, 128))
            screen.blit(frozen_overlay, ronaldo)
        else:
            screen.blit(second_enemy_image, second_enemy)
            screen.blit(third_enemy_image,third_enemy)
            
        pygame.draw.rect(screen, grey_color, player_goalie)
        pygame.draw.rect(screen, grey_color, other_goalie)
        pygame.draw.ellipse(screen, grey_color, soccer_ball)
        pygame.draw.aaline(screen, grey_color, (screen_width/2, 0), (screen_width/2, screen_height))
        
        # if the fans are cheering displaytext
        if fan_cheering:
            cheer_text = timer_font.render("CROWD GOES WILD AHHH OMGGGG!!!", True, (255, 215, 0))
            screen.blit(cheer_text, (screen_width//2 - 100, screen_height - 50))
        
        timer_text = timer_font.render(f"Time: {clock_time(time_remaining)}", True, timer_color)
        screen.blit(timer_text, (screen_width//2 - 70, 20))
        
        score_text = score_font.render(f"{opponent_score} - {player_score}", True, timer_color)
        screen.blit(score_text, (screen_width//2 - 60, 60))
        
        coin_text = timer_font.render(f"Coins: {coins}", True, (255, 215, 0))
        screen.blit(coin_text, (screen_width - 200, 20))
        
        # display powerup text
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
        
        if coin_lose:
            coin_lose_text = timer_font.render("You lost a coin!", True, (0,0,0))
            screen.blit(coin_lose_text, (20, 180))

        if goal_lose:
            goal_lose_text = timer_font.render("You lost a goal!", True, (0,0,0))
            screen.blit(goal_lose_text,(20, 200))
            
        # handle goal animation and delayed respawn
        if goal_scored:
            current_time = pygame.time.get_ticks()
            time_since_goal = current_time - goal_time
            
            # flash the appropriate goalie
            if time_since_goal < 5000:  # during the 5 second delay
                flash_index = (time_since_goal // flash_interval) % 2
                flash_color = flash_colors[flash_index]
                
                if goal_side == "left":
                    # left goal was scored on, flash the left goalie
                    pygame.draw.rect(screen, flash_color, other_goalie)
                else:
                    # right goal was scored on, flash the right goalie
                    pygame.draw.rect(screen, flash_color, player_goalie)
                    
                # show goal
                goal_font = pygame.font.SysFont("monospace", 80)
                goal_text = goal_font.render("GOALALA!!", True, (255, 0, 0))
                screen.blit(goal_text, (screen_width//2 - goal_text.get_width()//2, screen_height//2 - 40))
            else:
                # After 5 seconds, reset the ball and clear the goal state
                goal_scored = False
                ball_restart()
        
        pygame.display.flip()
        clock.tick(60)

# function to create the powerups for the final level
def create_powerup_level4():
    """
    Generates a random power-up for Level 4 with a random type and position.

    Parameters:
    None

    Returns:
    dict: A dictionary containing the power-up's rectangle ('rect') and type ('type').

    By: Swanish and Selina
    """
    powerup_type = random.choice(['size', 'speed', 'invincible', 'freeze','coin-lose','goal-lose'])
    power_x = random.randint(100, screen_width - 100)
    power_y = random.randint(100, screen_height - 100)
    
    powerup_box = pygame.Rect(power_x, power_y, 30, 30)
    return {'rect': powerup_box, 'type': powerup_type}

def level_5():
    global current_l, next_l

    current_l = "5"
    next_l = "6"

    # define the colors
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
    color_index = 0
    
    # remember the font
    font = pygame.font.SysFont("monospace", 35)
    
    running = True
    clock = pygame.time.Clock()
    
    # Add a start time to track elapsed time
    start_time = pygame.time.get_ticks()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # auto-exit after 5 secosnds
        current_time = pygame.time.get_ticks()
        if current_time - start_time >= 5000:
            pygame.quit()
            sys.exit()
        
        # clear the screen and put a black background
        screen.fill((0, 0, 0))
        
        # display thanks message with changing colors
        text = font.render("THANK YOU FOR PLAYING!! WE HOPE YOU HAD A BLAST :)", True, colors[color_index])
        text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(text, text_rect)

        text2 = font.render("You have won a lamborghini!!!", True, colors[color_index])
        text2_rect = text2.get_rect(center=(screen_width/2, screen_height/2+50))
        screen.blit(text2, text2_rect)

        lambo_image = pygame.image.load('lambo.png') 
        lambo_image = pygame.transform.scale(lambo_image, (300, 150)) 
        image_rect = lambo_image.get_rect(center=(screen_width/2, screen_height/2 - 150))
        screen.blit(lambo_image, image_rect)
        
        small_font = pygame.font.SysFont("monospace", 24)
        exit_text = small_font.render("Exiting in " + str(5 - int((current_time - start_time)/1000)) + " seconds...", True, (255, 255, 255))
        exit_rect = exit_text.get_rect(center=(screen_width/2, screen_height/2 + 100))
        screen.blit(exit_text, exit_rect)
        
        # change color every 500 milliseconds
        if pygame.time.get_ticks() % 500 == 0:
            color_index = (color_index + 1) % len(colors)
        
        pygame.display.flip()
        clock.tick(60)
    
    return

clock = initialize_game()
loading_animation()
loading_screen()
#level_1()
level_2()
level_3()
level_4()
level_5()
