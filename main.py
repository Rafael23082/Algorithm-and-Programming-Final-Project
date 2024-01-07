import pygame
import sys

pygame.init()

# The size for the pygame window, and setting the window
screen_width = 850
screen_height = 500
screen = pygame.display.set_mode((screen_width,screen_height))

# Importing buttons and scaling it
exit = pygame.image.load("exit.png").convert_alpha()
exit_scaled = pygame.transform.scale(exit,(150,70))

FPS = 60
font_size = 60

clock = pygame.time.Clock()

# It is the size for each block in the world (blocks, lava and doors)
tile_width = 30
tile_height = 30

left_mouse_clicks = 1

# The Image class helps displaying images and scaling it when necessary
class Image:
    
    def __init__(self, image, x, y, scale):
        self.image = image
        self.x = x
        self.y = y
        self.scale = scale
        self.image = pygame.transform.scale(self.image,(int(self.image.get_width()*self.scale),int(self.image.get_height()*self.scale)))
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
    
    def display(self):
        screen.blit(self.image,(self.x,self.y))

# The Scale_Player class is the class that animates the character, displaying the character, moving the character, and provides appropriate responses when colliding with tiles
class Scale_Player:

    # Initializing 
    def __init__(self,character, scale, x, y):
        self.character = character  
        self.scale = scale
        self.x = x
        self.y = y
        self.animations_container = []
        self.list_index = 0
        num_of_idle_images = 5
        self.action_index = 0
        self.vel_y = 0
        self.flip = False
        self.jump = False
        num_of_run_images = 0
        num_of_jump_images = 0
        num_of_fall_images = 0
        self.gravity = 0.75
        self.jump_status = False
        self.fall_status = False
        self.in_air = False
        self.alive = True

        # The action_list acts as a temporary list to append itself containing different actions into the self.animations_container. So the animation can change when the action changes as well.
        action_list = []

        # Storing scaled idle images according to the character chosen
        for i in range(num_of_idle_images):

            # My file names are numbers so it will make it easy storing it.
            img = pygame.image.load(f"{character}/idle/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            action_list.append(img)
        self.animations_container.append(action_list)

        # Both characters have different number of images for each action
        action_list = []
        if self.character == "character1":
            num_of_run_images = 8
            num_of_jump_images = 3
            num_of_fall_images = 3

        elif self.character == "character2":
            num_of_run_images = 6
            num_of_jump_images = 4
            num_of_fall_images = 2
 
        # The same concept as before but for run images.
        for i in range(num_of_run_images):

            img = pygame.image.load(f"{self.character}/run/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            action_list.append(img)
        self.animations_container.append(action_list)

        # For jump images.
        action_list = []
        for i in range(num_of_jump_images):
            img = pygame.image.load(f"{self.character}/jump/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            action_list.append(img)
        self.animations_container.append(action_list)

        # For fall images
        action_list = []
        for i in range(num_of_fall_images):
            img = pygame.image.load(f"{self.character}/fall/{i}.png")
            img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale)))
            action_list.append(img)
        self.animations_container.append(action_list)

        # Self.update_time helps to set a delay between images
        self.update_time = pygame.time.get_ticks()
        self.rect = img.get_rect(topleft = (x,y))

        # Self.image is according to the self.action_index and self.list_index.
        # Self.action_index represents the action, and the list_index represent the image in the list
        self.image = self.animations_container[self.action_index][self.list_index]
        self.height = self.image.get_height()
        self.width = self.image.get_width()

    # This method switches between images in a list inside the self.animations_list.
    def update_animation(self):

        # Time delay between images
        picture_transition_time = 100
        self.image = self.animations_container[self.action_index][self.list_index]

        # Self.update_time is continuously updated whenever the list_index is changed so there will be constant transition.
        if pygame.time.get_ticks() - self.update_time > picture_transition_time:
            self.update_time = pygame.time.get_ticks()
            self.list_index += 1

        # If the list_index is equal or more to the length of an action in the self.animations_list, the self.list_index is resetted to 0to continue the animation.
        if self.list_index >= len(self.animations_container[self.action_index]):
            self.list_index = 0

    # This method switches actions when needed. (When the upcoming action is different from the previous one E.g: From staying idle into running)
    def update_action(self, action):
            
        # Change the action
        if self.action_index != action:
            self.action_index = action

            # Reset the image index
            self.list_index = 0

            #Update the self.update_time so the image transition delay still exists
            self.update_time = pygame.time.get_ticks()
        

    def move(self,move_left,move_right):

        # At the end of the method, the values will be added to the player.rect. So it is set to 0.
        x_change = 0
        y_change = 0

        # for some reason the characters  move faster when jumping than running, so I added this extra code 
        if self.jump_status or self.fall_status:
            player_speed = 5
        elif self.jump_status == False or self.fall_status == False:
            player_speed = 8
        else:
            player_speed = 5

        # Edit the x_change if the player moves left / right
        if move_left:
            x_change = -player_speed
            self.flip = True
        elif move_right:
            x_change = player_speed
            self.flip = False
        else: 
            player_speed = 0

        # Playing the animation for running
        if move_left or move_right:
            self.update_action(1)
        else:
            self.update_action(0)
            
            
        if self.jump and self.in_air == False:

            # A negative number so there will be a transition when the character is jumping
            self.vel_y = -11
            self.jump = False

            # To prevent the player from jumping twice
            self.in_air = True

        # Make the character look like they have a transition when jumping, and causes them to fall when the self.vel.y becomes positive
        self.vel_y += self.gravity

        # Updates the y coordinates
        y_change += self.vel_y

        # There is a ground in the stage 1 from the wallpaper, I made this code so that the player can stand on the ground wallpaper.
        wallpaper_ground_x = 475
        if self.rect.bottom + y_change >= wallpaper_ground_x:
            y_change = 0
            self.fall_status = False
            self.in_air = False

        # Helps in updating the action
        if self.in_air and self.vel_y > 0:
            self.fall_status = True
            self.jump_status = False

        elif self.vel_y + self.gravity < 0:
            self.fall_status = False
            self.jump_status = True

        # Updates jumping and falling action
        if self.fall_status:
            self.update_action(3)
        if self.jump_status:
            self.update_action(2)

        # So we can access the world even though in different classes
        global world

        # Prevent the player from moving through the tiles
        for tile in world.block_list:
            if tile[1].colliderect(self.rect.x + x_change, self.rect.y, self.width, self.height):
                x_change = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + y_change, self.width, self.height):
                
                if self.vel_y > 0:
                    self.on_top_of_tile = True
                    y_change = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
                    self.fall_status = False
                    player_speed = 4
                
                if self.vel_y < 0:
                    y_change = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    player_speed = 4

        # Same as above but for lavas, but it will cause the player to die when colliding
        for tile in world.danger_list:
            
            if tile[1].colliderect(self.rect.x + x_change, self.rect.y, self.width, self.height):
                x_change = 0
                self.alive = False

            if tile[1].colliderect(self.rect.x, self.rect.y + y_change , self.width, self.height):
                
                if self.vel_y >= 0:
        
                    y_change = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
                    self.fall_status = False
                    player_speed = 4
                    self.alive = False
                
                if self.vel_y < 0:
                    y_change = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                    player_speed = 4
                    self.alive = False

        if self.alive == False:
            y_change = 0
            x_change = 0
                    
        # Finally updating the coordinates
        self.rect.x += x_change
        self.rect.y += y_change

    # This method displays the player
    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)

# The enemy class displays the enemy character and moves it.
class Enemy:

    # Initializing
    def __init__(self, scale, min_x, max_x, x, y, image):
        self.image = image
        enemy = pygame.image.load(self.image).convert_alpha()
        self.scale = scale
        self.image = pygame.transform.scale(enemy,(int(enemy.get_width()*self.scale),int(enemy.get_height()*self.scale)))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.min_x = min_x
        self.max_x = max_x
        self.speed = 0.5
        self.flip = False
        self.height = self.image.get_height()

    def move(self):

        # Once the enemy reaches the max point (x coordinate) set, the enemy will move the oppsite way
        if self.rect.x >= self.max_x:
            self.speed = -0.6
            self.flip = True

        if self.rect.x <= self.min_x:
            self.speed = 0.6
            self.flip = False

        # Updating coordinates
        self.rect.x += self.speed

    # Displaying the enemy
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),self.rect)

class World:
    
    # Initializing
    def __init__(self, data):
        
        # stores the image and the rect(coordinates) according to the number in the list
        # I want to give different effects when the user collides with different blocks
        self.block_list = []
        self.danger_list = []
        self.door_list = []
        
        row_count = 0

        block_img = pygame.image.load("tile.png").convert_alpha()
        lava_img = pygame.image.load("lava.png").convert_alpha()
        door_img = pygame.image.load("door.png").convert_alpha()

        # goes through each list
        for row in data:
            col_count = 0
            # goes through each element in each list
            for tile in row:
                # if statements according to the numbers
                if tile == 1:
                    imagee = pygame.transform.scale(block_img, (tile_width, tile_height))
                    imagee_rect = imagee.get_rect()

                    # So there will be constant gap length between tiles
                    imagee_rect.x = col_count * tile_width
                    imagee_rect.y = row_count * tile_height
                    tile = (imagee, imagee_rect)
                    self.block_list.append(tile)
                if tile == 2:
                    imagee = pygame.transform.scale(lava_img,(tile_width,tile_height))
                    imagee_rect = imagee.get_rect()
                    imagee_rect.x = col_count * tile_width
                    imagee_rect.y = row_count * tile_height
                    tile = (imagee, imagee_rect)
                    self.danger_list.append(tile)
                if tile == 3:
                    imagee = pygame.transform.scale(door_img, (tile_width, tile_height))
                    imagee_rect = imagee.get_rect()
                    imagee_rect.x = col_count * tile_width
                    imagee_rect.y = row_count * tile_height
                    tile = (imagee, imagee_rect)
                    self.door_list.append(tile)

                # So the gap is continuously updated
                col_count += 1
            row_count += 1                    

    # Displaying the world structure (The blocks, lava, door.)
    def draw(self):

        # prints each tuple containing the image and the coordinates
        for tile in self.block_list:
            screen.blit(tile[0], tile[1])
        for tile in self.danger_list:
            screen.blit(tile[0],tile[1])
        for tile in self.door_list:
            screen.blit(tile[0], tile[1])

# This class displays coins and responses if the player collides with the coinse
class Coins:

    # Initializing
    def __init__(self, x, y):
        coin_image = pygame.image.load("coin.png").convert_alpha()
        self.coin_image_scaled = pygame.transform.scale(coin_image,(int(coin_image.get_width()*0.08),int(coin_image.get_height()*0.08)))
        self.rect = self.coin_image_scaled.get_rect(topleft = (x, y))

    def draw(self):

        screen.blit(self.coin_image_scaled,(self.rect.x, self.rect.y))

        # So the score value can be accessed from other methods
        global score

        if player_rectangle.colliderect(self.rect):

            # Move the coin out of screen when colliding and adding the score
            self.rect.x += 1000
            score += 10

# This function is displayed when the program is executed. It displays the main menu.
def main_menu():
    
    yellow = (255,255,0)

    run = True

    # Inserting necessary images, caption and logo
    pygame.display.set_caption("THE CRUSADERS")
    logo = pygame.image.load("logo.png").convert_alpha()
    pygame.display.set_icon(logo)

    background = pygame.image.load("bg.png").convert_alpha()
    background_scaled = pygame.transform.scale(background,(850,500))

    play = pygame.image.load("play.png").convert_alpha()
    play_scaled = pygame.transform.scale(play,(150,70))

    game_logo = pygame.image.load("gamelogo.png").convert_alpha()
    game_logo_scaled = pygame.transform.scale(game_logo,(60,90))

    font = pygame.font.Font("Minecraftia-Regular.ttf",font_size)
    display_text1 = font.render("THE", True, yellow)
    display_text2 = font.render("CRUSADERS", True, yellow)

    while run:

        screen.fill((0,0,0))

        # Displaying Images
        background_image = Image(background_scaled,0,0,1)
        background_image.display()

        play_image = Image(play_scaled,195,320,1)
        play_image.display()

        exit_image = Image(exit_scaled,485,320,1)
        exit_image.display()

        game_logo_image = Image(game_logo_scaled, 385,220,1)
        game_logo_image.display()

        screen.blit(display_text1,(345,40))
        screen.blit(display_text2,(221,120))

        mouse_position = pygame.mouse.get_pos()

        # Provide responses when the mouse is clicked on the buttons.        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == left_mouse_clicks:
                    if exit_image.rect.collidepoint(mouse_position):
                        comfirm_quit()
                    if play_image.rect.collidepoint(mouse_position):
                        choose_character()

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

# This function is displayed when the user clicks the exit button in the main menu. It re-confirms with the user.
def comfirm_quit():

    run = True

    yellow = (255,255,0)

    # Loading in images and font styles
    background = pygame.image.load("bg.png").convert_alpha()
    background_scaled = pygame.transform.scale(background,(850,500))
    font = pygame.font.Font("Minecraftia-Regular.ttf",font_size)
    confirm_text = font.render("CONFIRM EXIT", True, yellow)

    while run:

        screen.fill((0,0,0))

        # Displaying objects
        background_image = Image(background_scaled,0,0,1)
        background_image.display()

        exit_image = Image(exit_scaled,485,320,1)
        exit_image.display()

        cancel_image = pygame.image.load("cancel.png").convert_alpha()
        cancel_image_scaled = pygame.transform.scale(cancel_image,(150,70))

        cancel_button = Image(cancel_image_scaled, 195,320, 1)
        cancel_button.display()
    
        screen.blit(confirm_text,(180,170))

        mouse_position = pygame.mouse.get_pos()

        # Providing responses when the mouse button is clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == left_mouse_clicks:
                    if exit_image.rect.collidepoint(mouse_position):
                        run = False
                    if cancel_button.rect.collidepoint(mouse_position):
                        main_menu()

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit() 

# This function is where the user chooses their character
def choose_character():

    yellow = (255,255,0)

    run = True

    # Loading in images, font styles and captions
    pygame.display.set_caption("CHOOSE YOUR CHARACTER")
    font = pygame.font.Font("Minecraftia-Regular.ttf", font_size)
    display_text3 = font.render("CHOOSE CHARACTER", True, yellow)

    background = pygame.image.load("bg.png").convert_alpha()
    background_scaled = pygame.transform.scale(background, (850, 500))

    character_1_image = pygame.image.load("character1/idle/0.png").convert_alpha()
    character_1 = Image(character_1_image, 225, 150, 5)

    character_2_image = pygame.image.load("character2/idle/0.png").convert_alpha()
    character_2 = Image(character_2_image, 520, 160, 5.5)

    select_button = pygame.image.load("select.png").convert_alpha()
    select_button_scaled = pygame.transform.scale(select_button, (int(select_button.get_width() * 0.4), int(select_button.get_height() * 0.4)))

    select_button1_x, select_button1_y = 210,390
    select_button2_x, select_button2_y = 525,390

    select_button1 = Image(select_button_scaled, select_button1_x, select_button1_y, 1)
    select_button2 = Image(select_button_scaled, select_button2_x, select_button2_y, 1)

    while run:

        # Displaying background, characters and buttons
        screen.blit(background_scaled, (0, 0))
        screen.blit(display_text3, (80, 50))

        character_1.display()
        character_2.display()

        select_button1.display()
        select_button2.display()

        mouse_position = pygame.mouse.get_pos()

        # Responds according to the button clicked
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == left_mouse_clicks:
                    if select_button1.rect.collidepoint(mouse_position):
                        level_1("character1")
                    if select_button2.rect.collidepoint(mouse_position):
                        level_1("character2")

        pygame.display.update()

    pygame.quit()
    sys.exit()

# Function that displays the first level
def level_1(character):

    pygame.display.set_caption("MAIN GAME")
    font = pygame.font.Font("Minecraftia-Regular.ttf", 20)

    # Loading in the world structure that will run in the World class
    world_structure = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,1,1,1,1,2,2,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1],
    [1,3,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

    global world

    # World_structure is went through
    world = World(world_structure)

    # Both characters have different sizes, so this is necessary
    player_x = 50
    if character == "character1":
        scale = 2
        player_y = 403
    if character == "character2":
        scale = 2.2
        player_y = 407

    # Setting up initial coordinates and sizes
    player = Scale_Player(character, scale, player_x, player_y)
    
    enemy_scale = 0.15
    enemy1_minimum_x, enemy1_maximum_x, enemy1_x, enemy1_y = 200, 210, 200, 195 
    enemy2_minimum_x, enemy2_maximum_x, enemy2_x, enemy2_y = 480, 530, 480, 405 

    enemy1 = Enemy(enemy_scale, enemy1_minimum_x, enemy1_maximum_x, enemy1_x, enemy1_y, "guard.png")
    enemy2 = Enemy(enemy_scale, enemy2_minimum_x, enemy2_maximum_x, enemy2_x, enemy2_y,"guard.png")

    coin1, coin2, coin3, coin4, coin5, coin6, coin7 = Coins(314,320), Coins(500,320), Coins(779,323), Coins (540,175), Coins(390, 85), Coins(270, 115), Coins(90,235)

    moving_left = False
    moving_right = False

    background = pygame.transform.scale(pygame.image.load("game_wallpaper.jpg").convert_alpha(),(850,500))
    caution_img = pygame.image.load("caution.png").convert_alpha()
    caution_img_scaled = pygame.transform.scale(caution_img,(int(caution_img.get_width()*0.07),int(caution_img.get_height()*0.07)))
    
    run = True

    # so it can be accessed from the coins class to add the score when collisions occur
    global score
    score = 0   

    # The stage number (level)
    stage = 1
    stage_text = font.render(f"Stage: {stage}", True, (255,255,0))

    while run:

        # To remove trails
        screen.fill((0, 0, 0))

        # Displaying images
        screen.blit(background,(0,0))
        screen.blit(caution_img_scaled,(160,416))
        
        # Update player action
        player.update_action(player.action_index)

        # Draw the world_structure
        world.draw()

        # Displaying texts
        score_text = font.render(f"Score: {score}", True, (255,255,0))
        screen.blit(score_text,(10,10))
        screen.blit(stage_text, (750,10))

        # Update player animation
        player.update_animation()   

        # Moves the player according to the key pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: 
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w and player.in_air == False:
                    player.jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    player.jump = False

        # Moving and drawing the player and enemies
        player.move(moving_left, moving_right), player.draw()
        enemy1.move(), enemy1.draw()
        enemy2.move(), enemy2.draw()

        # Make a rectangle to check collisions more accurately
        global player_rectangle
        player_rectangle_width, enemy_rectangle_width = 50,23

        # Setting up rectangles (If not, player may collide with enemies even though it does not)
        player_rectangle = pygame.Rect(player.rect.x , player.rect.y, player_rectangle_width , player.height)
        enemy1_rectangle = pygame.Rect(enemy1.rect.x, enemy1.rect.y, enemy_rectangle_width, enemy1.height)      
        enemy2_rectangle = pygame.Rect(enemy2.rect.x , enemy2.rect.y, enemy_rectangle_width , enemy2.height)

        # Display coins
        coin1.draw(), coin2.draw(), coin3.draw(), coin4.draw(), coin5.draw(), coin6.draw(), coin7.draw()

        # Kill player if colliding with enemies
        if player_rectangle.colliderect(enemy2_rectangle) or player_rectangle.colliderect(enemy1_rectangle):
            player.alive = False

        # To give a short delay after dying
        time_delay_after_death = 300

        # Redirecting to another function after dying
        if player.alive == False:
            pygame.time.delay(time_delay_after_death)
            you_died(player.character)

        # if the player reaches the door, it redirects to the next level
        for tile in world.door_list:
            if player_rectangle.colliderect(tile[1]):
                level_2(player.character)

        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()
    sys.exit()

# Function that displays the second level
def level_2(character):

    # Comments are similar to the function above

    pygame.display.set_caption("MAIN GAME")
    font = pygame.font.Font("Minecraftia-Regular.ttf", 20)

    player_x = 50

    world_structure = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
    [1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,2],
    [1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,2],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,0,0,0,0,0,0,0,0,2],
    [1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,1,1,0,0,0,0,0,0,2,2],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,0,3,0,1,1,1,0,0,0,0,0,0,2,2],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,1,0,0,0,2,2],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,2,2],
    [2,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2],
    [2,2,1,1,0,0,1,1,1,0,0,1,1,1,1,0,0,1,0,0,1,0,1,1,1,2,2,2,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
    ]

    global world
    world = World(world_structure)

    if character == "character1":
        scale = 2
        player_y = 103
    if character == "character2":
        scale = 2.2
        player_y = 107

    enemy1_scale, enemy1_minimum_x, enemy1_maximum_x, enemy1_x, enemy1_y = 0.3, 200, 250, 200, 105
    enemy2_scale, enemy2_minimum_x, enemy2_maximum_x, enemy2_x, enemy2_y = 0.3, 480, 800, 480, 105
    enemy3_scale, enemy3_minimum_x, enemy3_maximum_x, enemy3_x, enemy3_y = 0.15, 680, 730, 690, 405

    player = Scale_Player(character, scale, player_x, player_y)
    enemy1 = Enemy(enemy1_scale, enemy1_minimum_x, enemy1_maximum_x, enemy1_x , enemy1_y,"guard2.png")
    enemy2 = Enemy(enemy2_scale ,enemy2_minimum_x, enemy2_maximum_x, enemy2_x, enemy2_y,"guard2.png")
    enemy3 = Enemy(enemy3_scale, enemy3_minimum_x, enemy3_maximum_x, enemy3_x, enemy3_y,"guard.png" )

    coin1, coin2, coin3, coin4, coin5, coin6 = Coins(330,390), Coins(507,330), Coins(781,264), Coins(540,175), Coins(93, 390), Coins(210,175)

    moving_left = False
    moving_right = False

    background = pygame.transform.scale(pygame.image.load("game_wallpaper.jpg").convert_alpha(),(850,500))

    stage = 2
    stage_text = font.render(f"Stage: {stage}", True, (255,255,0))

    run = True

    while run:

        screen.fill((0, 0, 0))
        screen.blit(background,(0,0))
        
        player.update_action(player.action_index)

        world.draw()

        score_text = font.render(f"Score: {score}", True, (255,255,0))
        screen.blit(score_text,(10,10))
        screen.blit(stage_text, (750,10))

        player.update_animation()   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: 
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w and player.in_air == False:
                    player.jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    player.jump = False

        player.move(moving_left, moving_right)
      
        player.draw()

        # make a rectangle to check collisions more accurately
        global player_rectangle
        
        player_rectangle = pygame.Rect(player.rect.x , player.rect.y, 50 , player.height)
        enemy1_rectangle = pygame.Rect(enemy1.rect.x, enemy1.rect.y, 23, enemy1.height)
        enemy2_rectangle = pygame.Rect(enemy2.rect.x , enemy2.rect.y, 23 , enemy2.height)
        enemy3_rectangle = pygame.Rect(enemy3.rect.x, enemy3.rect.y, 23, enemy3.height)

        enemy1.move(), enemy1.draw()
        enemy2.move(), enemy2.draw()
        enemy3.move(), enemy3.draw()

        coin1.draw(), coin2.draw(), coin3.draw(), coin4.draw(), coin5.draw(), coin6.draw()
 
        if player_rectangle.colliderect(enemy2_rectangle) or player_rectangle.colliderect(enemy1_rectangle) or player_rectangle.colliderect(enemy3_rectangle):
            player.alive = False

        if player.alive == False:
            pygame.time.delay(300)
            you_died(player.character)

        # if the player reaches the door
        for tile in world.door_list:
            if player_rectangle.colliderect(tile[1]):
                level_3(character)

        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()
    sys.exit()

# Function that displays the third level
def level_3(character):

    # Comments are similar too

    pygame.display.set_caption("MAIN GAME")
    font = pygame.font.Font("Minecraftia-Regular.ttf", 20)

    player_x = 330

    world_structure = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1],
    [1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,3,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,2,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1],
    [1,1,2,2,2,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,2,2,1,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,1,1,1,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
    [1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,2,2,1,1,1,0,0,0,0,0,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

    global world
    world = World(world_structure)

    if character == "character1":
        scale = 2
        player_y = 167
    if character == "character2":
        scale = 2.2
        player_y = 171

    enemy1_scale, enemy1_minimum_x, enemy1_maximum_x, enemy1_x, enemy1_y = 0.3, 100, 240, 100, 105
    enemy2_scale, enemy2_minimum_x, enemy2_maximum_x, enemy2_x, enemy2_y = 0.3, 540, 670, 540, 155
    enemy3_scale, enemy3_minimum_x, enemy3_maximum_x, enemy3_x, enemy3_y = 0.15, 300, 400, 300, 375
    enemy4_scale, enemy4_minimum_x, enemy4_maximum_x, enemy4_x, enemy4_y = 0.1, 120, 180, 120, 220

    player = Scale_Player(character, scale, player_x, player_y)
    enemy1 = Enemy(enemy1_scale ,enemy1_minimum_x, enemy1_maximum_x , enemy1_x, enemy1_y,"guard2.png")
    enemy2 = Enemy(enemy2_scale, enemy2_minimum_x, enemy2_maximum_x, enemy2_x, enemy2_y ,"guard2.png")
    enemy3 = Enemy(enemy3_scale, enemy3_minimum_x , enemy3_maximum_x, enemy3_x, enemy3_y,"guard.png")
    enemy4 = Enemy(enemy4_scale, enemy4_minimum_x, enemy4_maximum_x, enemy4_x, enemy4_y, "guard3.png")

    coin1, coin2, coin3, coin4, coin5, coin6 = Coins(345,300), Coins(507,300), Coins(570,175), Coins(690,175), Coins(663, 360), Coins(210,175)

    moving_left = False
    moving_right = False

    background = pygame.transform.scale(pygame.image.load("game_wallpaper.jpg").convert_alpha(),(850,500))

    run = True
    player.flip = True

    stage = 3
    stage_text = font.render(f"Stage: {stage}", True, (255,255,0))

    while run:

        screen.fill((0, 0, 0))
        screen.blit(background,(0,0))
        
        player.update_action(player.action_index)

        world.draw()

        score_text = font.render(f"Score: {score}", True, (255,255,0))
        screen.blit(score_text,(10,10))
        screen.blit(stage_text, (750,10))

        player.update_animation()   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: 
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w and player.in_air == False:
                    player.jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    player.jump = False

        player.move(moving_left, moving_right)
      
        player.draw()

        # make a rectangle to check collisions more accurately
        global player_rectangle
        
        player_rectangle = pygame.Rect(player.rect.x , player.rect.y, 50 , player.height)
        enemy1_rectangle = pygame.Rect(enemy1.rect.x, enemy1.rect.y, 23, enemy1.height)
        enemy2_rectangle = pygame.Rect(enemy2.rect.x , enemy2.rect.y, 23 , enemy2.height)
        enemy3_rectangle = pygame.Rect(enemy3.rect.x, enemy3.rect.y, 23, enemy3.height)
        enemy4_rectangle = pygame.Rect(enemy4.rect.x, enemy4.rect.y, 23, enemy4.height)

        enemy1.move(), enemy1.draw()
        enemy2.move(), enemy2.draw()
        enemy3.move(), enemy3.draw()
        enemy4.move(), enemy4.draw()

        coin1.draw(), coin2.draw(), coin3.draw(), coin4.draw(), coin5.draw(), coin6.draw()
 
        if player_rectangle.colliderect(enemy2_rectangle) or player_rectangle.colliderect(enemy1_rectangle) or player_rectangle.colliderect(enemy3_rectangle) or player_rectangle.colliderect(enemy4_rectangle):
            player.alive = False

        if player.alive == False:
            pygame.time.delay(300)
            you_died(player.character)

        # if the player reaches the door
        for tile in world.door_list:
            if player_rectangle.colliderect(tile[1]):
                level_4(player.character)

        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()
    sys.exit()

# Function thst displays the final level
def level_4(character):

    # Comments are similar

    pygame.display.set_caption("MAIN GAME")
    font = pygame.font.Font("Minecraftia-Regular.ttf", 20)

    player_x = 30

    world_structure = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    ]

    global world
    world = World(world_structure)

    if character == "character1":
        scale = 2
        player_y = 330
    if character == "character2":
        scale = 2.2
        player_y = 334

    player = Scale_Player(character, scale, player_x, player_y)
    enemy1 = Enemy(0.15,60,790,170,317,"guard.png")
    enemy2 = Enemy(0.15,60,790, 300, 317,"guard.png")
    enemy3 = Enemy(0.15, 60,790, 430, 317,"guard.png")
    enemy4 = Enemy(0.15, 60, 790, 550, 317, "guard.png")
    enemy5 = Enemy(0.15, 60, 790, 670, 317, "guard.png")
    enemy6 = Enemy(0.15, 60, 790, 789, 317, "guard.png")

    moving_left = False
    moving_right = False

    background = pygame.transform.scale(pygame.image.load("game_wallpaper.jpg").convert_alpha(),(850,500))

    run = True

    stage = 4
    stage_text = font.render(f"Stage: {stage}", True, (255,255,0))

    while run:

        screen.fill((0, 0, 0))
        screen.blit(background,(0,0))
        
        player.update_action(player.action_index)

        world.draw()

        score_text = font.render(f"Score: {score}", True, (255,255,0))
        screen.blit(score_text,(10,10))
        screen.blit(stage_text, (750,10))

        player.update_animation()   

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a: 
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w and player.in_air == False:
                    player.jump = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    player.jump = False

        player.move(moving_left, moving_right)
      
        player.draw()

        # make a rectangle to check collisions more accurately
        global player_rectangle
        
        player_rectangle = pygame.Rect(player.rect.x , player.rect.y, 50 , player.height)
        enemy1_rectangle = pygame.Rect(enemy1.rect.x, enemy1.rect.y, 23, enemy1.height)
        enemy2_rectangle = pygame.Rect(enemy2.rect.x , enemy2.rect.y, 23 , enemy2.height)
        enemy3_rectangle = pygame.Rect(enemy3.rect.x, enemy3.rect.y, 23, enemy3.height)
        enemy4_rectangle = pygame.Rect(enemy4.rect.x, enemy4.rect.y, 23, enemy4.height)
        enemy5_rectangle = pygame.Rect(enemy5.rect.x, enemy5.rect.y, 23, enemy5.height)
        enemy6_rectangle = pygame.Rect(enemy6.rect.x, enemy6.rect.y, 23, enemy6.height)

        enemy1.move(), enemy1.draw()
        enemy2.move(), enemy2.draw()
        enemy3.move(), enemy3.draw()
        enemy4.move(), enemy4.draw()
        enemy5.move(), enemy5.draw()
        enemy6.move(), enemy6.draw()
 
        if player_rectangle.colliderect(enemy2_rectangle) or player_rectangle.colliderect(enemy1_rectangle) or player_rectangle.colliderect(enemy3_rectangle) or player_rectangle.colliderect(enemy4_rectangle) or player_rectangle.colliderect(enemy5_rectangle) or player_rectangle.colliderect(enemy6_rectangle):
            player.alive = False

        if player.alive == False:
            pygame.time.delay(300)
            you_died(player.character)

        # if the player reaches the door, the game is finished
        for tile in world.door_list:
            if player_rectangle.colliderect(tile[1]):
                game_finished()

        clock.tick(FPS)
        pygame.display.update()

    pygame.quit()
    sys.exit()

# Function when the player dies
def you_died(character):

    run = True

    # Setting images and texts
    background = pygame.image.load("bg.png").convert_alpha()
    background_scaled = pygame.transform.scale(background,(850,500))
    font = pygame.font.Font("Minecraftia-Regular.ttf",font_size)
    confirm_text = font.render("YOU DIED", True, (255,255,0))

    while run:

        screen.fill((0,0,0))

        # Displaying images and texts
        background_image = Image(background_scaled,0,0,1)
        background_image.display()

        exit_image = Image(exit_scaled,485,320,1)
        exit_image.display()

        retry_image = pygame.image.load("retry.png").convert_alpha()
        retry_image_scaled = pygame.transform.scale(retry_image,(150,70))

        retry_button = Image(retry_image_scaled, 195,320,1)
        retry_button.display()
    
        screen.blit(confirm_text,(250,170))

        mouse_position = pygame.mouse.get_pos()

        # Provides a choice to the player to exit or retry
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if exit_image.rect.collidepoint(mouse_position):

                        # Exit
                        run = False
                    if retry_button.rect.collidepoint(mouse_position):

                        # Retry
                        level_1(character)

        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit() 

# Function if the player wins, it either goes back to the main menu or exit
def game_finished():

    yellow = (255,255,0)

    run = True

    # Loading in images and texts
    pygame.display.set_caption("YOU WON!")
    font = pygame.font.Font("Minecraftia-Regular.ttf", font_size)
    display_text3 = font.render("YOU WON!", True, yellow)

    background = pygame.image.load("bg.png").convert_alpha()
    background_scaled = pygame.transform.scale(background, (850, 500))

    back_button_x, back_button_y = 210,340
    exit_button_x, exit_button_y = 525,340

    back_button = pygame.image.load("back.png").convert_alpha()
    back_button_scaled = pygame.transform.scale(back_button,(160,80))
    back_button_rect = back_button_scaled.get_rect(topleft = (back_button_x, back_button_y))

    exit_button = pygame.image.load("exit.png").convert_alpha()
    exit_button_scaled = pygame.transform.scale(exit_button,(160,80))
    exit_button_rect = exit_button_scaled.get_rect(topleft = (exit_button_x, exit_button_y))

    select_button1 = Image(back_button_scaled, back_button_x, back_button_y, 1)
    select_button2 = Image(exit_button_scaled, exit_button_x, exit_button_y, 1)

    while run:

        # Displaying images
        screen.blit(background_scaled, (0, 0))
        screen.blit(display_text3, (280, 80))

        select_button1.display()
        select_button2.display()

        mouse_position = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == left_mouse_clicks:
                    if exit_button_rect.collidepoint(mouse_position):

                        # Exits
                        run = False
                    if back_button_rect.collidepoint(mouse_position):

                        # Back to main menu
                        main_menu()

        pygame.display.update()

    pygame.quit()
    sys.exit()  

# Executing the code
if __name__ == "__main__":
    main_menu()
