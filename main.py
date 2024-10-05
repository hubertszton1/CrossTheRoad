import pygame
import random
import spritesheet

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)

PLAYER_WIDTH = 164
PLAYER_HEIGHT = 132
CAR_WIDTH = 300
CAR_HEIGHT = 120
ROAD_HEIGHT = 180
CARS = 4
FPS = 60
MIN_CAR_SPACING = 300  # Minimum space between cars in the same lane

# background images
bg1 = pygame.image.load('models/bg1.png')

#animation sprites
idle_img = pygame.image.load("models/dog/idle.png")
IDLE = spritesheet.SpriteSheet(idle_img).get_sheet(8, 164, 136, BLUE)

walk_down_img = pygame.image.load("models/dog/walk_down.png")
WALK_DOWN = spritesheet.SpriteSheet(walk_down_img).get_sheet(8, 164, 136, GREEN)

walk_down_left_img = pygame.image.load("models/dog/walk_down_left.png")
WALK_DOWN_LEFT = spritesheet.SpriteSheet(walk_down_left_img).get_sheet(8, 164, 136, GREEN)

walk_down_right_img = pygame.image.load("models/dog/walk_down_right.png")
WALK_DOWN_RIGHT = spritesheet.SpriteSheet(walk_down_right_img).get_sheet(8, 164, 136, GREEN)

walk_left_img = pygame.image.load("models/dog/walk_left.png")
WALK_LEFT = spritesheet.SpriteSheet(walk_left_img).get_sheet(8, 164, 136, GREEN)

walk_right_img = pygame.image.load("models/dog/walk_right.png")
WALK_RIGHT = spritesheet.SpriteSheet(walk_right_img).get_sheet(8, 164, 136, GREEN)

walk_up_img = pygame.image.load("models/dog/walk_up.png")
WALK_UP = spritesheet.SpriteSheet(walk_up_img).get_sheet(8, 164, 136, GREEN)

walk_up_left_img = pygame.image.load("models/dog/walk_up_left.png")
WALK_UP_LEFT = spritesheet.SpriteSheet(walk_up_left_img).get_sheet(8, 164, 136, GREEN)

walk_up_right_img = pygame.image.load("models/dog/walk_up_right.png")
WALK_UP_RIGHT = spritesheet.SpriteSheet(walk_up_right_img).get_sheet(8, 164, 136, GREEN)

# cars sprites
cars_images = [
    pygame.image.load("models/car/WhiteCar.png"),
    pygame.image.load("models/car/BlueCar.png"),
    pygame.image.load("models/car/redcar.png"),
    pygame.image.load("models/car/greencar.png"),
    pygame.image.load("models/car/orangecar.png")
]
# Preload font for better performance
font = pygame.font.Font(None, 36)

# gameplay
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.color = BLUE
        self.speed = 4
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.walk_count = 0

    def draw(self):
        if self.walk_count + 1 >= 64:
            self.walk_count = 0
        if self.left:
            if self.up:
                SCREEN.blit(WALK_UP_LEFT[self.walk_count//8], (self.x, self.y))
            elif self.down:
                SCREEN.blit(WALK_DOWN_LEFT[self.walk_count//8], (self.x, self.y))
            else:
                SCREEN.blit(WALK_LEFT[self.walk_count//8], (self.x, self.y))
            self.walk_count += 1
        elif self.right:
            if self.up:
                SCREEN.blit(WALK_UP_RIGHT[self.walk_count//8], (self.x, self.y))
            elif self.down:
                SCREEN.blit(WALK_DOWN_RIGHT[self.walk_count//8], (self.x, self.y))
            else:
                SCREEN.blit(WALK_RIGHT[self.walk_count//8], (self.x, self.y))
            self.walk_count += 1
        elif self.up:
            SCREEN.blit(WALK_UP[self.walk_count//8], (self.x, self.y))
            self.walk_count += 1
        elif self.down:
            SCREEN.blit(WALK_DOWN[self.walk_count//8], (self.x, self.y))
            self.walk_count += 1
        else:
            SCREEN.blit(IDLE[self.walk_count//8], (self.x, self.y))
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
        self.color = RED
        self.speed = speed

    def draw(self, index):
        SCREEN.blit(cars_images[index], (self.x, self.y))
        #pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.width, self.height))

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
        num_cars_in_lane = random.randint(2, 3)  # Random number of cars in each lane (2 to 5)

        # Generate a random speed for the entire lane
        lane_speed = random.randint(2, 5) + (level / 2 - 1)

        car_positions = []  # Store positions of cars in the current lane

        # Start generating car positions
        while len(car_positions) < num_cars_in_lane:
            # Generate a random x position within the screen width
            x_position = random.randint(-CAR_WIDTH, SCREEN_WIDTH)
            
            # Ensure cars are spaced out enough
            if not any(abs(x_position - pos) < MIN_CAR_SPACING for pos in car_positions):
                car_positions.append(x_position)  # Add valid position
                car = Car(x_position, y, lane_speed)
                cars.append((car, random.randint(0, 4)))

    return cars
    # cars = []
    # for i in range(CARS):  #NUMBER OF LANES
    #     y = (i + 1) * ROAD_HEIGHT + 30
    #     num_cars_in_lane = random.randint(2, 5)  # Random number of cars in each lane (2 to 5)

    #     # Generate a random speed for the entire lane
    #     lane_speed = random.randint(2, 5) + (level/2 - 1)

    #     # Position the cars in the lane without overlap
    #     car_positions = []
    #     x_position = random.randint(-SCREEN_WIDTH, 0)

    #     for _ in range(num_cars_in_lane):
    #         # Ensure cars are spaced out enough
    #         while x_position in car_positions or (car_positions and abs(x_position - car_positions[-1]) < MIN_CAR_SPACING):
    #             x_position = random.randint(-SCREEN_WIDTH+600, SCREEN_WIDTH-600)

    #         car = Car(x_position, y, lane_speed)
    #         cars.append((car, random.randint(0, 4)))
    #         car_positions.append(x_position)

    # return cars

def game():
    clock = pygame.time.Clock()
    player = Player()
    level = 1
    global wa

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

        # Move and draw cars
        for car, index in cars:
            car.move()
            car.draw(index)

            # Check collision with the player
            if (player.x < car.x + car.width and
                player.x + player.width > car.x and
                player.y < car.y + car.height and
                player.y + player.height > car.y):
                running = False  # End the game if collision occurs

        # Check if player reaches the top
        if player.y <= 0:
            level += 1  # Go to the next level
            player.reset_position()  # Reset player position
            cars = create_cars(level)  # Create new cars for the new level

        # Draw player
        player.draw()

        # Display the current level
        level_text = font.render(f"Level: {level}", True, BLACK)
        SCREEN.blit(level_text, (10, 10))

        # Update display
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    game()