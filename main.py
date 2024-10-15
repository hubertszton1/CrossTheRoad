import pygame
import random
import colors
import spritesheet

pygame.init()

SCALE = 1.5

# Screen dimensions
SCREEN_WIDTH = int(1920 // SCALE)
SCREEN_HEIGHT = int(1080 // SCALE)
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font("font/ka1.ttf", int(30//SCALE))

PLAYER_WIDTH = 164 // SCALE
PLAYER_HEIGHT = 132 // SCALE
CAR_WIDTH = 300 // SCALE
CAR_HEIGHT = 120 // SCALE
ROAD_HEIGHT = 180 // SCALE
CARS = 4
MIN_CAR_SPACING = 350 // SCALE  # Minimum space between cars in the same lane

# background images
bg1 = pygame.transform.scale(pygame.image.load('models/bg1.png'),(1920//SCALE, 1080//SCALE))

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
        self.freeze = False
        self.freeze_timer = 0
        self.blink_counter = 0

    def update(self, keys):
        if not self.freeze:
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

    def start_freeze(self, duration):
        self.freeze = True
        self.freeze_timer = pygame.time.get_ticks() + duration

    def check_freeze(self):
        if self.freeze and pygame.time.get_ticks() > self.freeze_timer:
            self.freeze = False

    def animate(self):
        if not self.freeze:
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
        else:
            self.image = IDLE[0]
            self.blink_counter += 1
            if self.blink_counter % 20 < 10:  # Every 10 frames, toggle visibility
                self.image.set_alpha(0)  # Invisible
            else:
                self.image.set_alpha(255) 

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


def create_cars(level):
    cars = []
    if level < 9:
        car_set = level//3
    else:
        car_set = 2
    for i in range(CARS):  # NUMBER OF LANES
        y = (i + 1) * ROAD_HEIGHT + (30//SCALE)

        num_cars_in_lane = random.randint(1 + level//15, 2 + level//10)  # Random number of cars in each lane

        # Generate a random speed for the entire lane
        lane_speed = random.randint(2, 5) + level/10 - 1

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


def game():
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()

    # Player initialization
    player = Player((SCREEN_WIDTH - PLAYER_WIDTH) // 2, (SCREEN_HEIGHT - PLAYER_HEIGHT - 20), PLAYER_WIDTH, PLAYER_HEIGHT)
    player_group = pygame.sprite.Group(player)  # Player sprite group

    level = 1
    score = 0
    cars = create_cars(level)

    # Car sprites group
    car_group = pygame.sprite.Group()
    for car in cars:  # No need for tuples anymore, just add Car objects
        car_group.add(car)

    running = True
    while running:
        clock.tick(FPS)
        SCREEN.blit(bg1, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        player.check_freeze()
        player.update(keys)
        player_group.draw(SCREEN)  # Draw player

        # Display the current level
        level_text = font.render(f"Level  {level}", True, colors.BLACK)
        SCREEN.blit(level_text, (20, 20))
        score_text = font.render(f"Score  {score}", True, colors.BLACK)
        SCREEN.blit(score_text, (20, 50))

        # Check if player reaches the top
        if player.rect.y <= 0 and not player.freeze:
            level_time = (pygame.time.get_ticks() - start_time) // 1000 # time taken to pass the level in seconds
            score += level*10 + int((level*10)/level_time)
            level += 1  # Go to the next level
            player.reset_position()  # Reset player position
            player.start_freeze(1000)

            start_time = pygame.time.get_ticks()
            cars = create_cars(level)  # Create new cars for the new level
            car_group.empty()  # Clear previous cars
            for car in cars:
                car_group.add(car)

        # Update and draw cars
        car_group.update()
        car_group.draw(SCREEN)

        # Collision detection using collide_mask
        if pygame.sprite.spritecollide(player, car_group, False, pygame.sprite.collide_mask):
            level = 1  # Go to the next level
            cars = create_cars(level)  # Create new cars for the new level
            car_group.empty()  # Clear previous cars
            for car in cars:
                car_group.add(car)
            player.reset_position()  # Reset player position
            player.start_freeze(500)

        # Update display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game()
