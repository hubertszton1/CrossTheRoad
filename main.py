import pygame
import random
import time
import colors
import spritesheet

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
WIDTH_SCALE = 1920 / SCREEN_WIDTH
HEIGHT_SCALE = 1080 / SCREEN_HEIGHT
SCALE = min(WIDTH_SCALE, HEIGHT_SCALE)
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FONT = pygame.font.Font("font/ThaleahFat.ttf", int(52//SCALE))
GAME_OVER_FONT =pygame.font.Font("font/ThaleahFat.ttf", int(80//SCALE))

PLAYER_WIDTH = int(164 // SCALE)
PLAYER_HEIGHT = int(132 // SCALE)
CAR_WIDTH = int(300 // SCALE)
CAR_HEIGHT = int(120 // SCALE)
ROAD_HEIGHT = int(180 // SCALE)
CARS = 4
MIN_CAR_SPACING = int(280 // SCALE)  # Minimum space between cars in the same lane

# background images
backgrounds = [
    pygame.transform.scale(pygame.image.load('models/bg1.png'),(1920//SCALE, 1080//SCALE)),
    pygame.transform.scale(pygame.image.load('models/bg2.png'),(1920//SCALE, 1080//SCALE)),
    pygame.transform.scale(pygame.image.load('models/bg3.png'),(1920//SCALE, 1080//SCALE)),
]

bone_img = pygame.transform.scale(pygame.image.load('models/bone.png'), (70//SCALE, 70//SCALE))

# animation sprites
idle_img = pygame.image.load('models/dog/idle.png')
IDLE = spritesheet.SpriteSheet(idle_img).get_sheet(8, 164, 132, scale=SCALE)

walk_down_img = pygame.image.load("models/dog/walk_down.png")
WALK_DOWN = spritesheet.SpriteSheet(walk_down_img).get_sheet(8, 164, 132, scale=SCALE)

walk_down_left_img = pygame.image.load("models/dog/walk_down_left.png")
WALK_DOWN_LEFT = spritesheet.SpriteSheet(walk_down_left_img).get_sheet(8, 164, 132, scale=SCALE)

walk_down_right_img = pygame.image.load("models/dog/walk_down_right.png")
WALK_DOWN_RIGHT = spritesheet.SpriteSheet(walk_down_right_img).get_sheet(8, 164, 132, scale=SCALE)

walk_left_img = pygame.image.load("models/dog/walk_left.png")
WALK_LEFT = spritesheet.SpriteSheet(walk_left_img).get_sheet(8, 164, 132, scale=SCALE)

walk_right_img = pygame.image.load("models/dog/walk_right.png")
WALK_RIGHT = spritesheet.SpriteSheet(walk_right_img).get_sheet(8, 164, 132, scale=SCALE)

walk_up_img = pygame.image.load("models/dog/walk_up.png")
WALK_UP = spritesheet.SpriteSheet(walk_up_img).get_sheet(8, 164, 132, scale=SCALE)

walk_up_left_img = pygame.image.load("models/dog/walk_up_left.png")
WALK_UP_LEFT = spritesheet.SpriteSheet(walk_up_left_img).get_sheet(8, 164, 132, scale=SCALE)

walk_up_right_img = pygame.image.load("models/dog/walk_up_right.png")
WALK_UP_RIGHT = spritesheet.SpriteSheet(walk_up_right_img).get_sheet(8, 164, 132, scale=SCALE)

# cars sprites
cars_images = [
    [
        pygame.transform.scale(pygame.image.load("models/car/level1/white-car.png"), (220 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level1/green-car.png"), (220 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level1/blue-car.png"), (220 //SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level1/orange-car.png"), (220 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level1/red-car.png"), (220 // SCALE, 130 // SCALE)),
    ],
    [
        pygame.transform.scale(pygame.image.load("models/car/level10/blue-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level10/green-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level10/white-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level10/red-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level10/orange-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level10/yellow-pickup.png"), (246 // SCALE, 120 // SCALE)),
    ],
    [
        pygame.transform.scale(pygame.image.load("models/car/level20/blue-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level20/green-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level20/orange-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level20/purple-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level20/red-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load("models/car/level20/white-mustang.png"), (231 // SCALE, 130 // SCALE)),
    ]
]


# gameplay
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed=5):
        super().__init__()
        self.image = IDLE[0]  # Initial sprite image
        self.rect = self.image.get_rect()  # Get rect for positioning
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walk_count = 0
        self.mask = pygame.mask.from_surface(self.image)  # Create the initial mask
        self.bonus =False
        self.blink_counter = 0

    def update(self, keys):
        dx = 0
        dy = 0
        self.left = self.right = self.up = self.down = False
        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.left = True
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.right = True
        if keys[pygame.K_UP]:
            dy = -self.speed
            self.up = True
        if keys[pygame.K_DOWN]:
            dy = self.speed
            self.down = True

        # Movement and boundary checking
        self.rect.x = max(0, min(self.rect.x + dx, SCREEN_WIDTH - self.width))
        self.rect.y = max(0, min(self.rect.y + dy, SCREEN_HEIGHT - self.height))

        self.animate()

    def animate(self):
        # Animation logic based on direction
        if self.walk_count + 1 >= 40:
            self.walk_count = 0
        if self.left:
            if self.up:
                self.image = WALK_UP_LEFT[self.walk_count // 5]
            elif self.down:
                self.image = WALK_DOWN_LEFT[self.walk_count // 5]
            else:
                self.image = WALK_LEFT[self.walk_count // 5]
        elif self.right:
            if self.up:
                self.image = WALK_UP_RIGHT[self.walk_count // 5]
            elif self.down:
                self.image = WALK_DOWN_RIGHT[self.walk_count // 5]
            else:
                self.image = WALK_RIGHT[self.walk_count // 5]
        elif self.up:
            self.image = WALK_UP[self.walk_count // 5]
        elif self.down:
            self.image = WALK_DOWN[self.walk_count // 5]
        else:
            self.image = IDLE[self.walk_count // 5]

        # Update the mask and rect
        self.mask = pygame.mask.from_surface(self.image)
        self.walk_count += 1

    def reset_position(self):
        self.rect.x = ((SCREEN_WIDTH - PLAYER_WIDTH) // 2)
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - (10//SCALE)
    

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, car_set, image_index):
        super().__init__()
        self.image = cars_images[car_set][image_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH:
            self.rect.x = -self.rect.width  # Loop the car back
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WIDTH

class Bone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bone_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.display = random.randint(0, 99) < 50

def create_cars(level):
    cars = []
    if level < 30:
        car_set = level//10
    else:
        car_set = 2
    for i in range(CARS):  # NUMBER OF LANES
        y = (i + 1) * ROAD_HEIGHT + (20//SCALE)

        num_cars_in_lane = random.randint(1, 1 + level//10)  # Random number of cars in each lane

        # Generate a random speed for the entire lane
        lane_speed = random.randint(2, 6) + (level/20) - 1
        lane_speed = round(lane_speed/SCALE, 3)

        car_positions = []  # Store positions of cars in the current lane

        # Start generating car positions
        while len(car_positions) < num_cars_in_lane:
            # Generate a random x position within the screen width
            x_position = random.randint(0, SCREEN_WIDTH)

            # Ensure cars are spaced out enough
            if not any(abs(x_position - pos) < MIN_CAR_SPACING for pos in car_positions):
                car_positions.append(x_position)  # Add valid position
                image_index = random.randint(0, len(cars_images[car_set])-1)  # Randomly select a car image index
                car = Car(x_position, y, lane_speed, car_set, image_index)  # Pass image_index here
                cars.append(car)  # Store Car object directly, not a tuple

    return cars

def create_bone():
    x_posistion = random.randint(0, SCREEN_WIDTH)
    y_position = random.randint(ROAD_HEIGHT, SCREEN_HEIGHT - ROAD_HEIGHT)
    return Bone(x_posistion, y_position)

def render_text_with_outline(x, y,base, outline, size, surface):
    # top left
    surface.blit(outline, (x - size, y - size))
    # top right
    surface.blit(outline, (x + size, y - size))
    # bot left
    surface.blit(outline, (x - size, y + size))
    # bot right
    surface.blit(outline, (x + size, y + size))
    # base
    surface.blit(base, (x, y))

def game_over(surface, level, score):
    
    game_over_base = GAME_OVER_FONT.render("GAME OVER", True, colors.RED)
    game_over_outline = GAME_OVER_FONT.render("GAME OVER", True, colors.BLACK)
    level_base = GAME_OVER_FONT.render(f"LEVEL: {level}", True, colors.YELLOW)
    level_outline = GAME_OVER_FONT.render(f"LEVEL: {level}", True, colors.BLACK)
    score_base = GAME_OVER_FONT.render(f"SCORE: {score}", True, colors.YELLOW)
    score_outline = GAME_OVER_FONT.render(f"SCORE: {score}", True, colors.BLACK)
    play_again_base = FONT.render("Press any key to play again", True, colors.WHITE)
    play_again_outline = FONT.render("Press any key to play again", True, colors.BLACK)

    game_over_width = game_over_base.get_width()
    level_width = level_base.get_width()
    score_width = score_base.get_width()
    play_again_width = play_again_base.get_width()


    render_text_with_outline((SCREEN_WIDTH//2) - (game_over_width//2), (SCREEN_HEIGHT//2) - 50, game_over_base, game_over_outline, 3, surface)
    render_text_with_outline((SCREEN_WIDTH//2) - (level_width//2), (SCREEN_HEIGHT//2), level_base, level_outline, 3, surface)
    render_text_with_outline((SCREEN_WIDTH//2) - (score_width//2), (SCREEN_HEIGHT//2) + 50, score_base, score_outline, 3, surface)
    render_text_with_outline((SCREEN_WIDTH//2) - (play_again_width//2), (SCREEN_HEIGHT//2) + 100, play_again_base, play_again_outline, 2, surface)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()  # Zamknij grę
            if event.type == pygame.KEYDOWN:  # Sprawdza, czy dowolny klawisz został wciśnięty
                waiting = False  # Wyjdź z pętli po naciśnięciu klawisza
                return  # Powróć do funkcji game(), aby zresetować grę

def game():
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    level = 1
    score = 0

    # Player initialization
    player = Player((SCREEN_WIDTH - PLAYER_WIDTH) // 2, (SCREEN_HEIGHT - PLAYER_HEIGHT - 20), PLAYER_WIDTH, PLAYER_HEIGHT, round(5/SCALE))
    player_group = pygame.sprite.Group(player)  # Player sprite group
    cars = create_cars(level)
    car_group = pygame.sprite.Group()
    for car in cars:
        car_group.add(car)
    bone = create_bone()
    bone_group = pygame.sprite.Group(bone)
    running = True
    while running:
        clock.tick(FPS)
        if level < 30:
            SCREEN.blit(backgrounds[level//10], (0, 0))
        else:
            SCREEN.blit(backgrounds[2], (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        player.update(keys)
        player_group.draw(SCREEN)  # Draw player

        # Display the current level and score
        level_base_text = FONT.render(f"Level  {level}", True, colors.WHITE)
        level_outline_text = FONT.render(f"Level  {level}", True, colors.BLACK)
        render_text_with_outline(20, (SCREEN_HEIGHT - 100//SCALE), level_base_text, level_outline_text, 2, SCREEN)
        score_base_text = FONT.render(f"Score  {score}", True, colors.WHITE)
        score_outline_text = FONT.render(f"Score  {score}", True, colors.BLACK)
        render_text_with_outline(20, (SCREEN_HEIGHT - 60//SCALE), score_base_text, score_outline_text, 2, SCREEN)

        # Check if player reaches the top
        if player.rect.y <= 0:
            level_time = (pygame.time.get_ticks() - start_time) // 1000 # time taken to pass the level in seconds
            if player.bonus:
                score += level*100 + int((level*100)/level_time)*2
                player.bonus = False
            else:
                score += level*100 + int((level*100)/level_time)*2
            level += 1  # Go to the next level
            player.reset_position()  # Reset player position
            start_time = pygame.time.get_ticks()
            cars = create_cars(level)  # Create new cars for the new level
            car_group.empty()  # Clear previous cars
            for car in cars:
                car_group.add(car)
            bone = create_bone()
            bone_group = pygame.sprite.Group(bone)

        if bone.display:
            bone_group.draw(SCREEN)

        # Update and draw cars
        car_group.update()
        car_group.draw(SCREEN)

        # Collision detection using collide_mask
        if pygame.sprite.spritecollide(player, car_group, False, pygame.sprite.collide_mask):
            # Wywołaj funkcję game_over i poczekaj, aż użytkownik wciśnie przycisk
            game_over(SCREEN, level, score)
            # Zresetuj grę po Game Over (restart całej funkcji)
            return game()  # Restartuj grę, zamiast zamykać okno

        if pygame.sprite.spritecollide(player, bone_group, False, pygame.sprite.collide_mask):
            bone.display = False
            player.bonus = True


        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    game()
