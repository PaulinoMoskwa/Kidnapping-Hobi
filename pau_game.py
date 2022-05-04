#------------------------------------------------------------------------------------------------
# INITIAL SETTINGS
#------------------------------------------------------------------------------------------------
import random
import pygame
import time

# Initialize pygame (now everything in pygame is up and running)
pygame.init()
pygame.mixer.music.load("music/boy_with_luv.mp3")

# Colors constants
white  = (255, 255, 255)
black  = (0, 0, 0)
green  = (0, 255, 0)
red    = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)

# Screen constants
WIDTH = 850
HEIGHT = 500

# Game variables
score     = 0
player_x  = 50
player_y  = 300
y_change  = 0
x_change  = 0
gravity   = 1
obstacles = [800, 1300, 1600] # initial obstacles positions
obstacle_speed = 3
active = False # you start stopped, with space bar you enable yourself

# Define the screen
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Title to the window
pygame.display.set_caption('Kidnapping Hobi')

# Background image and fps definition
background = pygame.image.load("images/background.jpg")
fps = 60

# Define fonts
font = pygame.font.Font('freesansbold.ttf', 22)
font_title = pygame.font.SysFont('Lucida Calligraphy', 48, italic=True)

# Define the timer
timer = pygame.time.Clock()

# Player image.png
player_image = pygame.image.load("images/player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (70, 80))

# Enemy image.png
enemy_image = pygame.image.load("images/enemy.png").convert_alpha()
enemy_image = pygame.transform.scale(enemy_image, (70, 80))

# Enemy image.png
enemyfly_image = pygame.image.load("images/enemyfly.png").convert_alpha()
enemyfly_image = pygame.transform.scale(enemyfly_image, (100, 60))

# Floor image.png
floor_image = pygame.image.load("images/floor.png").convert_alpha()
floor_image = pygame.transform.scale(floor_image, (WIDTH, 15))

#------------------------------------------------------------------------------------------------
# GAME DEFINITION
#------------------------------------------------------------------------------------------------
running = True
pygame.mixer.music.play()

while running:
    timer.tick(fps) # it controls the speed at which it runs
    screen.blit(background, (0,0))

    if not active:
        title = font_title.render(f'* Kidnapping Hobi *', True, white)
        screen.blit(title, (170,50))
        instruction_text = font.render(f'Space Bar to Start', True, white, black)
        screen.blit(instruction_text, (350, 150))
        instruction_text_2 = font.render(f'Up to Jump, Left/Right to Move', True, white, black)
        screen.blit(instruction_text_2, (280, 190))

    # Print score
    score_text = font.render(f'How many Paulos did Hobi avoid?: {score}', True, white, black)
    screen.blit(score_text, (250, 430)) # .blit() is the "draw something"-pygame instruction, what? score_text, in position (160, 250)

    # Create the floor
    screen.blit(floor_image, [0, 380])

    # Player definition
    player = screen.blit(player_image, [player_x, player_y])

    # Ground-obstacle definition
    obstacle_0 = screen.blit(enemy_image, [obstacles[0], 300]) # screen.blit(image, x_position, y_position)
    obstacle_1 = screen.blit(enemy_image, [obstacles[1], 300])
    obstacle_2 = screen.blit(enemyfly_image, [obstacles[2], 200])

    # Get anything that is going on in the computer (click/mouse position/pressed button)
    for event in pygame.event.get():

        # Ending condition (otherwise the computer explodes)
        if event.type == pygame.QUIT:
            running = False

        # Start the game
        if event.type == pygame.KEYDOWN and not active:
            if event.key == pygame.K_SPACE:

                # Re-starting music
                pygame.mixer.music.load("music/boy_with_luv.mp3")
                pygame.mixer.music.play()

                # Re-initialize obstacles, player position and score
                obstacles = [800, 1300, 1600]
                player_x = 50
                player_y = 300
                score = 0
                obstacle_speed = 3

                # Ready to play
                active = True

        # Key Press
        if event.type == pygame.KEYDOWN and active:
            if event.key == pygame.K_UP and y_change == 0:
                y_change = 25 # value of the jump
            if event.key == pygame.K_RIGHT:
                x_change = 2
            if event.key == pygame.K_LEFT:
                x_change = -2

        # Key Releas
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                x_change = 0
            if event.key == pygame.K_LEFT:
                x_change = 0

    # Obstacle movements
    for i in range(len(obstacles)):
        if active:
            obstacles[i] = obstacles[i] - obstacle_speed

            if obstacles[i] < -20:
                random_shift = random.randint(300, 1000)
                if i == 0:
                    obstacles[0] = obstacles[2] + random_shift
                if i == 1:
                    obstacles[1] = obstacles[0] + random_shift
                if i == 2:
                    obstacles[2] = obstacles[1] + random_shift
                score = score + 1

                # Change obstacle-speed if it's going well
                if obstacle_speed < 9:
                    obstacle_speed = obstacle_speed + 1/10

            if player.colliderect(obstacle_0) or player.colliderect(obstacle_1) or player.colliderect(obstacle_2):
                pygame.mixer.music.load("music/end.mp3")
                pygame.mixer.music.play()
                active = False

    # Horizontal movement (player)
    if 0 <= player_x <= 830: #boundary
        player_x = player_x + x_change

    # Boundary conditions (player)
    if player_x < 0:
        player_x = 0
    if player_x > 830:
        player_x = 830

    # |-------------------------- JUMP --------------------------|
    # | Comment about jumping: the position (0,0) is top left,   |
    # | if you move to the right it increases, if you move to    |
    # | the bottom it increases, so to jump you have to decrease |
    # | the vertical position to the character (it is a          |
    # | flipped down axis system). With the condition            |
    # | player_y < 300 we are checking if the player is below    |
    # | the floor (floor which is positioned at 300).            |
    # |----------------------------------------------------------|
    if y_change > 0 or player_y < 300:
        player_y = player_y - y_change # you have to subtract from player_y for it to go up
        y_change = y_change - gravity # while you're jumping the gravity will have an effect 
                                      # (at every moment it will subtract 1 of the jump because of gravity)

    # Check condition: if the player goes under the floor, put him back on the floor
    if player_y > 300:
        player_y = 300

    # Re-intialize the jump (to give the possibility to jump again)
    if player_y == 300 and y_change < 0:
        y_change = 0

    pygame.display.flip()
pygame.quit()
