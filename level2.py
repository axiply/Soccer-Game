def level_2():
    level_screen("Level 2")
    # add player_image and other required variables to global
    global player_score, opponent_score, coins, soccer_ball, player, ronaldo, player_goalie, other_goalie, player_image, player_image_original, ronaldo_image, x_ball_speed, y_ball_speed

    
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

    #ball speed changes
    x_ball_speed = 10 * random.choice((1, -1))
    y_ball_speed = 10 * random.choice((1, -1))

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
                    game_over_screen()
            
            # limited powerups allowed
            if event.type == powerup_running:
                if len(powerups) < 5: 
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
        
        pygame.display.flip()
        clock.tick(60)