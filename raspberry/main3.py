import pygame
import random
from gpiozero import Button
import os
import colors
import spritesheet
os.chdir(os.path.dirname(__file__))

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
WIDTH_SCALE = 1920 / SCREEN_WIDTH
HEIGHT_SCALE = 1080 / SCREEN_HEIGHT
SCALE = min(WIDTH_SCALE, HEIGHT_SCALE)
FPS = 50
SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.mouse.set_visible(False)

FONT = pygame.font.Font("font/ThaleahFat.ttf", int(52 / SCALE))
END_SCREEN_FONT = pygame.font.Font("font/ThaleahFat.ttf", int(80 / SCALE))

PLAYER_WIDTH = int(164 / SCALE)
PLAYER_HEIGHT = int(132 / SCALE)
CAR_WIDTH = int(300 / SCALE)
CAR_HEIGHT = int(120 / SCALE)
ROAD_HEIGHT = int(180 / SCALE)
LANES = 4
MIN_CAR_SPACING = int(300 / SCALE)

keys = {
    'up': Button(19),
    'down': Button(13),
    'left': Button(26),
    'right': Button(6)
}


exit_img = pygame.transform.scale(pygame.image.load(
    'exit.png'), (30 // SCALE, 30 // SCALE))
bone_img = pygame.transform.scale(pygame.image.load(
    'models/bone.png'), (70 // SCALE, 70 // SCALE))

idle_img = pygame.image.load('models/dog/idle.png')
IDLE = spritesheet.SpriteSheet(idle_img).get_sheet(8, 164, 132, scale=SCALE)

walk_down_img = pygame.image.load("models/dog/walk_down.png")
WALK_DOWN = spritesheet.SpriteSheet(
    walk_down_img).get_sheet(8, 164, 132, scale=SCALE)

walk_down_left_img = pygame.image.load("models/dog/walk_down_left.png")
WALK_DOWN_LEFT = spritesheet.SpriteSheet(
    walk_down_left_img).get_sheet(8, 164, 132, scale=SCALE)

walk_down_right_img = pygame.image.load("models/dog/walk_down_right.png")
WALK_DOWN_RIGHT = spritesheet.SpriteSheet(
    walk_down_right_img).get_sheet(8, 164, 132, scale=SCALE)

walk_left_img = pygame.image.load("models/dog/walk_left.png")
WALK_LEFT = spritesheet.SpriteSheet(
    walk_left_img).get_sheet(8, 164, 132, scale=SCALE)

walk_right_img = pygame.image.load("models/dog/walk_right.png")
WALK_RIGHT = spritesheet.SpriteSheet(
    walk_right_img).get_sheet(8, 164, 132, scale=SCALE)

walk_up_img = pygame.image.load("models/dog/walk_up.png")
WALK_UP = spritesheet.SpriteSheet(
    walk_up_img).get_sheet(8, 164, 132, scale=SCALE)

walk_up_left_img = pygame.image.load("models/dog/walk_up_left.png")
WALK_UP_LEFT = spritesheet.SpriteSheet(
    walk_up_left_img).get_sheet(8, 164, 132, scale=SCALE)

walk_up_right_img = pygame.image.load("models/dog/walk_up_right.png")
WALK_UP_RIGHT = spritesheet.SpriteSheet(
    walk_up_right_img).get_sheet(8, 164, 132, scale=SCALE)

backgrounds = [
    pygame.transform.scale(pygame.image.load(
        'models/bg1.png'), (1920 // SCALE, 1080 // SCALE)),
    pygame.transform.scale(pygame.image.load(
        'models/bg2.png'), (1920 // SCALE, 1080 // SCALE)),
    pygame.transform.scale(pygame.image.load(
        'models/bg3.png'), (1920 // SCALE, 1080 // SCALE)),
]

cars_images = [
    [
        pygame.transform.scale(pygame.image.load(
            "models/car/level1/white-car.png"), (220 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level1/green-car.png"), (220 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level1/blue-car.png"), (220 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level1/orange-car.png"), (220 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level1/red-car.png"), (220 // SCALE, 130 // SCALE)),
    ],
    [
        pygame.transform.scale(pygame.image.load(
            "models/car/level10/blue-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level10/green-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level10/white-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level10/red-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level10/orange-pickup.png"), (246 // SCALE, 120 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level10/yellow-pickup.png"), (246 // SCALE, 120 // SCALE)),
    ],
    [
        pygame.transform.scale(pygame.image.load(
            "models/car/level20/blue-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level20/green-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level20/orange-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level20/purple-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level20/red-mustang.png"), (231 // SCALE, 130 // SCALE)),
        pygame.transform.scale(pygame.image.load(
            "models/car/level20/white-mustang.png"), (231 // SCALE, 130 // SCALE)),
    ]
]


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed=5):
        super().__init__()
        self.image = IDLE[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.directions = {'left': False,
                           'right': False, 'up': False, 'down': False}
        self.walk_count = 0
        self.bonus = False

    def handle_buttons(self, keys):
        self.directions['left'] = keys['left'].is_pressed
        self.directions['right'] = keys['right'].is_pressed
        self.directions['up'] = keys['up'].is_pressed
        self.directions['down'] = keys['down'].is_pressed

    def update(self, keys):
        self.handle_buttons(keys)
        dx = dy = 0
        if self.directions['left']:
            dx -= self.speed
        if self.directions['right']:
            dx += self.speed
        if self.directions['up']:
            dy -= self.speed
        if self.directions['down']:
            dy += self.speed
        self.rect.x = max(
            0, min(self.rect.x + dx, SCREEN_WIDTH - self.width))
        self.rect.y = max(
            0, min(self.rect.y + dy, SCREEN_HEIGHT - self.height))
        self.animate()

    def animate(self):
        if self.walk_count + 1 >= 40:
            self.walk_count = 0
        # eliminate the conflict when a player presses two opposing buttons at the same time
        effective_left = self.directions['left'] and not self.directions['right']
        effective_right = self.directions['right'] and not self.directions['left']
        effective_up = self.directions['up'] and not self.directions['down']
        effective_down = self.directions['down'] and not self.directions['up']
        if not (effective_left or effective_right or effective_up or effective_down):
            self.image = IDLE[self.walk_count // 5]
        else:
            if effective_left:
                if effective_up:
                    self.image = WALK_UP_LEFT[self.walk_count // 5]
                elif effective_down:
                    self.image = WALK_DOWN_LEFT[self.walk_count // 5]
                else:
                    self.image = WALK_LEFT[self.walk_count // 5]
            elif effective_right:
                if effective_up:
                    self.image = WALK_UP_RIGHT[self.walk_count // 5]
                elif effective_down:
                    self.image = WALK_DOWN_RIGHT[self.walk_count // 5]
                else:
                    self.image = WALK_RIGHT[self.walk_count // 5]
            elif effective_up:
                self.image = WALK_UP[self.walk_count // 5]
            elif effective_down:
                self.image = WALK_DOWN[self.walk_count // 5]
        self.walk_count += 1
        self.mask = pygame.mask.from_surface(self.image)


    def reset_position(self):
        self.rect.x = ((SCREEN_WIDTH - PLAYER_WIDTH) // 2)
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT


class Car(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, direction, car_set, image_index):
        super().__init__()
        self.image_original = cars_images[car_set][image_index]
        self.image = pygame.transform.flip(self.image_original, direction == -1, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.direction = direction
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.direction == 1 and self.rect.x > SCREEN_WIDTH:
            self.rect.x = -self.rect.width
        elif self.direction == -1 and self.rect.x < -self.rect.width:
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
        car_set = level // 10
    else:
        car_set = 2

    for i in range(LANES):
        y = (i + 1) * ROAD_HEIGHT + (20 // SCALE)
        num_cars_in_lane = random.randint(1, 1 + level // 10)
        lane_speed = random.randint(2, 5) + (level / 10) - 1
        car_positions = []

        direction = 1 if i % 2 == 0 else -1  # Kierunek: naprzemiennie prawo/lewo

        while len(car_positions) < num_cars_in_lane:
            x_position = random.randint(0, SCREEN_WIDTH)

            if not any(abs(x_position - pos) < MIN_CAR_SPACING for pos in car_positions):
                car_positions.append(x_position)
                image_index = random.randint(0, len(cars_images[car_set]) - 1)
                car = Car(x_position, y, lane_speed, direction, car_set, image_index)
                cars.append(car)

    return cars


def create_bone():
    x_posistion = random.randint(0, SCREEN_WIDTH)
    y_position = random.randint(ROAD_HEIGHT, SCREEN_HEIGHT - ROAD_HEIGHT)
    return Bone(x_posistion, y_position)


def render_text_with_outline(x, y, base, outline, size, surface):
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


def end_screen(surface, level, score, win):
    if win:
        result_base = END_SCREEN_FONT.render("YOU WIN", True, colors.BLUE)
        result_outline = END_SCREEN_FONT.render("YOU WIN", True, colors.YELLOW)
    else:
        result_base = END_SCREEN_FONT.render("GAME OVER", True, colors.RED)
        result_outline = END_SCREEN_FONT.render(
            "GAME OVER", True, colors.BLACK)
    level_base = END_SCREEN_FONT.render(f"LEVEL: {level}", True, colors.YELLOW)
    level_outline = END_SCREEN_FONT.render(
        f"LEVEL: {level}", True, colors.BLACK)
    score_base = END_SCREEN_FONT.render(f"SCORE: {score}", True, colors.YELLOW)
    score_outline = END_SCREEN_FONT.render(
        f"SCORE: {score}", True, colors.BLACK)
    play_again_base = FONT.render(
        "Press any key to play again", True, colors.WHITE)
    play_again_outline = FONT.render(
        "Press any key to play again", True, colors.BLACK)

    game_over_width = result_base.get_width()
    level_width = level_base.get_width()
    score_width = score_base.get_width()
    play_again_width = play_again_base.get_width()

    render_text_with_outline((SCREEN_WIDTH//2) - (game_over_width//2),
                             (SCREEN_HEIGHT//2) - 50, result_base, result_outline, 3, surface)
    render_text_with_outline((SCREEN_WIDTH//2) - (level_width//2),
                             (SCREEN_HEIGHT//2), level_base, level_outline, 3, surface)
    render_text_with_outline((SCREEN_WIDTH//2) - (score_width//2),
                             (SCREEN_HEIGHT//2) + 50, score_base, score_outline, 3, surface)
    render_text_with_outline((SCREEN_WIDTH//2) - (play_again_width//2),
                             (SCREEN_HEIGHT//2) + 100, play_again_base, play_again_outline, 2, surface)

    pygame.display.flip()
    pygame.time.delay(500)
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        for button in keys:
            keys[button].wait_for_release()
        for button in keys:
            if keys[button].is_pressed:
                waiting = False
                return


def game():
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    level = 1
    score = 0

    player = Player((SCREEN_WIDTH - PLAYER_WIDTH) // 2, (SCREEN_HEIGHT -
                    PLAYER_HEIGHT), PLAYER_WIDTH, PLAYER_HEIGHT, round(7/SCALE))
    player_group = pygame.sprite.Group(player)
    cars = create_cars(level)
    car_group = pygame.sprite.Group()
    for car in cars:
        car_group.add(car)
    bone = create_bone()
    bone_group = pygame.sprite.Group(bone)
    exit_button_rect = pygame.Rect(
        SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20, 20, 20)
    running = True
    while running:
        clock.tick(FPS)
        if level < 30:
            SCREEN.blit(backgrounds[level//10], (0, 0))
        else:
            SCREEN.blit(backgrounds[2], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and exit_button_rect.collidepoint(event.pos):
                running = False

        player.update(keys)
        player_group.draw(SCREEN)

        SCREEN.blit(exit_img, exit_button_rect)

        level_base_text = FONT.render(f"Level  {level}", True, colors.WHITE)
        level_outline_text = FONT.render(f"Level  {level}", True, colors.BLACK)
        render_text_with_outline(
            20, (SCREEN_HEIGHT - 100//SCALE), level_base_text, level_outline_text, 2, SCREEN)
        score_base_text = FONT.render(f"Score  {score}", True, colors.WHITE)
        score_outline_text = FONT.render(f"Score  {score}", True, colors.BLACK)
        render_text_with_outline(
            20, (SCREEN_HEIGHT - 60//SCALE), score_base_text, score_outline_text, 2, SCREEN)

        if player.rect.y <= 0:
            if level == 30:
                end_screen(SCREEN, level, score, win=True)
            level_time = (pygame.time.get_ticks() - start_time) / 1000
            if player.bonus:
                score += level*100 + int((level*100)/level_time)*2
                player.bonus = False
            else:
                score += level*100 + int((level*100)/level_time)
            level += 1
            player.reset_position()        
            start_time = pygame.time.get_ticks()
            cars = create_cars(level)
            car_group.empty()
            for car in cars:
                car_group.add(car)
            bone = create_bone()
            bone_group = pygame.sprite.Group(bone)

        if bone.display:
            bone_group.draw(SCREEN)

        car_group.update()
        car_group.draw(SCREEN)

        if pygame.sprite.spritecollide(player, car_group, False, pygame.sprite.collide_mask):
            end_screen(SCREEN, level, score, win=False)
            return game()

        if pygame.sprite.spritecollide(player, bone_group, False, pygame.sprite.collide_mask):
            bone.display = False
            player.bonus = True

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    game()
