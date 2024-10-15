import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

    def get_image(self, frame, width, height, color=(0, 255, 255), scale=1):
        image = pygame.Surface((width, height))
        image.fill(color=color)
        image.blit(self.sheet,(0,0), (frame*width, 0, width, height))
        image.set_colorkey(color)
        image = pygame.transform.scale(image, (width // scale, height // scale))
        return image

    def get_sheet(self, size, width, height, color=(0, 255, 255), scale=1):
        sheet = []
        for x in range(size):
            sheet.append(self.get_image(x, width, height, color, scale))
        return sheet