import pygame
import random
import colors
import spritesheet

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
FPS = 60
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

PLAYER_WIDTH = 164
PLAYER_HEIGHT = 132
CAR_WIDTH = 300
CAR_HEIGHT = 120
ROAD_HEIGHT = 180
CARS = 4
MIN_CAR_SPACING = 300  # Minimum space between cars in the same lane

# background images
bg1 = pygame.image.load('models/bg1.png')

# animation sprites
idle_img = pygame.image.load("models/dog/idle.png")
idle_rect = idle_img.get_rect()
idle_mask = pygame.mask.from_surface(idle_img)
mask_img = idle_mask.to_surface()
IDLE = spritesheet.SpriteSheet(idle_img).get_sheet(8, 164, 136, colors.BLUE)

walk_down_img = pygame.image.load("models/dog/walk_down.png")
WALK_DOWN = spritesheet.SpriteSheet(walk_down_img).get_sheet(8, 164, 136, colors.BLUE)

walk_down_left_img = pygame.image.load("models/dog/walk_down_left.png")
WALK_DOWN_LEFT = spritesheet.SpriteSheet(walk_down_left_img).get_sheet(8, 164, 136, colors.BLUE)

walk_down_right_img = pygame.image.load("models/dog/walk_down_right.png")
WALK_DOWN_RIGHT = spritesheet.SpriteSheet(walk_down_right_img).get_sheet(8, 164, 136, colors.BLUE)

walk_left_img = pygame.image.load("models/dog/walk_left.png")
WALK_LEFT = spritesheet.SpriteSheet(walk_left_img).get_sheet(8, 164, 136, colors.BLUE)

walk_right_img = pygame.image.load("models/dog/walk_right.png")
WALK_RIGHT = spritesheet.SpriteSheet(walk_right_img).get_sheet(8, 164, 136, colors.BLUE)

walk_up_img = pygame.image.load("models/dog/walk_up.png")
WALK_UP = spritesheet.SpriteSheet(walk_up_img).get_sheet(8, 164, 136, colors.BLUE)

walk_up_left_img = pygame.image.load("models/dog/walk_up_left.png")
WALK_UP_LEFT = spritesheet.SpriteSheet(walk_up_left_img).get_sheet(8, 164, 136, colors.BLUE)

walk_up_right_img = pygame.image.load("models/dog/walk_up_right.png")
WALK_UP_RIGHT = spritesheet.SpriteSheet(walk_up_right_img).get_sheet(8, 164, 136, colors.BLUE)

# cars sprites
cars_images = [
    pygame.image.load("models/car/white-car.png"),
    pygame.image.load("models/car/blue-car.png"),
    pygame.image.load("models/car/red-car.png"),
    pygame.image.load("models/car/green-car.png"),
    pygame.image.load("models/car/orange-car.png")
]
# Preload font for better performance
font = pygame.font.Font(None, 36)


# gameplay
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed=5):
        super().__init__()
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.width = width
        self.height = height
        self.speed = speed
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walk_count = 0
        self.hitbox = None

    def draw(self):
        if self.walk_count + 1 >= 40:
            self.walk_count = 0
        if self.left:
            if self.up:
                SCREEN.blit(WALK_UP_LEFT[self.walk_count // 5], (self.x, self.y))
                self.hitbox = pygame.mask.from_surface(WALK_UP_LEFT[self.walk_count // 5])
            elif self.down:
                SCREEN.blit(WALK_DOWN_LEFT[self.walk_count // 5], (self.x, self.y))
                self.hitbox = pygame.mask.from_surface(WALK_DOWN_LEFT[self.walk_count // 5])
            else:
                SCREEN.blit(WALK_LEFT[self.walk_count // 5], (self.x, self.y))
                self.hitbox = pygame.mask.from_surface(WALK_LEFT[self.walk_count // 5])
            self.walk_count += 1
        elif self.right:
            if self.up:
                SCREEN.blit(WALK_UP_RIGHT[self.walk_count // 5], (self.x, self.y))
                self.hitbox = pygame.mask.from_surface(WALK_UP_RIGHT[self.walk_count // 5])
            elif self.down:
                SCREEN.blit(WALK_DOWN_RIGHT[self.walk_count // 5], (self.x, self.y))
                self.hitbox = pygame.mask.from_surface(WALK_DOWN_RIGHT[self.walk_count // 5])
            else:
                SCREEN.blit(WALK_RIGHT[self.walk_count // 5], (self.x, self.y))
                self.hitbox = pygame.mask.from_surface(WALK_RIGHT[self.walk_count // 5])
            self.walk_count += 1
        elif self.up:
            SCREEN.blit(WALK_UP[self.walk_count // 5], (self.x, self.y))
            self.hitbox = pygame.mask.from_surface(WALK_UP[self.walk_count // 5])
            self.walk_count += 1
        elif self.down:
            SCREEN.blit(WALK_DOWN[self.walk_count // 5], (self.x, self.y))
            self.hitbox = pygame.mask.from_surface(WALK_DOWN[self.walk_count // 5])
            self.walk_count += 1
        else:
            #SCREEN.blit(IDLE[self.walk_count // 5], (self.x, self.y))
            self.hitbox = pygame.mask.from_surface(IDLE[self.walk_count // 5])
            hitbox_img = self.hitbox.to_surface(setcolor=colors.BLUE)
            hitbox_img.set_colorkey(colors.BLACK)
            SCREEN.blit(hitbox_img, (self.x, self.y))
            self.walk_count += 1
        pygame.display.update()

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

    def reset_position(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10


class Car:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.speed = speed
        self.hitbox = None

    def draw(self, index):
        #SCREEN.blit(cars_images[index], (self.x, self.y))
        self.hitbox = pygame.mask.from_surface(cars_images[index])
        hitbox_img = self.hitbox.to_surface(setcolor=colors.RED)
        hitbox_img.set_colorkey(colors.BLACK)
        SCREEN.blit(hitbox_img, (self.x, self.y))

    def move(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.x = -self.width  # Loop the car back
        if self.x < -self.width:  # Add this line to handle leftward movement
            self.x = SCREEN_WIDTH


def create_cars(level):
    cars = []
    for i in range(CARS):  # NUMBER OF LANES
        y = (i + 1) * ROAD_HEIGHT + 30
        num_cars_in_lane = random.randint(1, 3)  # Random number of cars in each lane (2 to 5)

        # Generate a random speed for the entire lane
        lane_speed = random.randint(2, 5) + (level / 2 - 1)

        car_positions = []  # Store positions of cars in the current lane

        # Start generating car positions
        while len(car_positions) < num_cars_in_lane:
            # Generate a random x position within the screen width
            x_position = random.randint(0, SCREEN_WIDTH)

            # Ensure cars are spaced out enough
            if not any(abs(x_position - pos) < MIN_CAR_SPACING for pos in car_positions):
                car_positions.append(x_position)  # Add valid position
                car = Car(x_position, y, lane_speed)
                cars.append((car, random.randint(0, 4)))

    return cars


def game():
    clock = pygame.time.Clock()
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    level = 1

    cars = create_cars(level)

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
        dx = 0
        dy = 0
        player.left = False
        player.right = False
        player.up = False
        player.down = False
        if keys[pygame.K_LEFT]:
            dx = -player.speed
            player.left = True
            player.right = False
        if keys[pygame.K_RIGHT]:
            dx = player.speed
            player.right = True
            player.left = False
        if keys[pygame.K_UP]:
            dy = -player.speed
            player.up = True
            player.down = False
        if keys[pygame.K_DOWN]:
            dy = player.speed
            player.down = True
            player.up = False
        player.move(dx, dy)

        # Display the current level
        level_text = font.render(f"Level: {level}", True, colors.BLACK)
        SCREEN.blit(level_text, (10, 10))

        # Check if player reaches the top
        if player.y <= 0:
            level += 1  # Go to the next level
            player.reset_position()  # Reset player position
            cars = create_cars(level)  # Create new cars for the new level

        for car, index in cars:
            car.move()
            car.draw(index)

            # Calculate offsets
            offset_x = player.x - car.x
            offset_y = player.y - car.y
            if player.hitbox and car.hitbox:
                if player.hitbox.overlap(car.hitbox, (offset_x, offset_y)) is not None:
                    running = False  # End the game if collision occurs

        player.draw()

        # Update display
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    game()
