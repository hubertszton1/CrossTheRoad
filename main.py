import pygame
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

PLAYER_SIZE = 30
CAR_WIDTH = 60
CAR_HEIGHT = 30
ROAD_HEIGHT = 100
CARS = 5
FPS = 60
MIN_CAR_SPACING = 150  # Minimum space between cars in the same lane

# Preload font for better performance
font = pygame.font.Font(None, 36)

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_SIZE - 10
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.color = BLUE
        self.speed = 4

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.width, self.height))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.x = max(0, min(self.x, SCREEN_WIDTH - self.width))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - self.height))

    def reset_position(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - PLAYER_SIZE - 10

class Car:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.color = RED
        self.speed = speed

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (self.x, self.y, self.width, self.height))

    def move(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.x = -self.width  # Loop the car back
        if self.x < -self.width:  # Add this line to handle leftward movement
            self.x = SCREEN_WIDTH

def create_cars(level):
    cars = []
    for i in range(CARS):  #NUMBER OF LANES
        y = (i + 1) * ROAD_HEIGHT + 20
        num_cars_in_lane = random.randint(2, 5)  # Random number of cars in each lane (2 to 5)

        # Generate a random speed for the entire lane
        lane_speed = random.randint(2, 5) + (level/10 - 1)

        # Position the cars in the lane without overlap
        car_positions = []
        x_position = random.randint(-SCREEN_WIDTH, 0)

        for _ in range(num_cars_in_lane):
            # Ensure cars are spaced out enough
            while x_position in car_positions or (car_positions and abs(x_position - car_positions[-1]) < MIN_CAR_SPACING):
                x_position = random.randint(-SCREEN_WIDTH+200, SCREEN_WIDTH-200)

            car = Car(x_position, y, lane_speed)
            cars.append(car)
            car_positions.append(x_position)

    return cars

def game():
    clock = pygame.time.Clock()
    player = Player()
    level = 1

    cars = create_cars(level)

    running = True
    while running:
        clock.tick(FPS)
        SCREEN.fill(WHITE)

        # Draw roads
        for i in range(CARS):
            pygame.draw.rect(SCREEN, BLACK, (0, (i + 1) * ROAD_HEIGHT, SCREEN_WIDTH, ROAD_HEIGHT))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement
        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_RIGHT]:
            dx = player.speed
        if keys[pygame.K_UP]:
            dy = -player.speed
        if keys[pygame.K_DOWN]:
            dy = player.speed
        player.move(dx, dy)

        # Move and draw cars
        for car in cars:
            car.move()
            car.draw()

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