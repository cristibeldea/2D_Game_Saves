from pynput import mouse
from Settings import *
import pygame


class PlayerInputManagement:
    def __init__(self, posManage):
        self.player_input = 0
        self.currentMousePosition = pygame.mouse.get_pos()
        self.posManage = posManage
        self.last_tick = pygame.time.get_ticks()
        self.dustCloudSize = 75
        # pygame.mouse.set_pos([tileSize, tileSize])

        dustCloudImage1 = pygame.image.load("Tiles/dustCloud1.png")
        self.dustCloudImage1 = pygame.transform.scale(dustCloudImage1, (self.dustCloudSize, self.dustCloudSize))

        dustCloudImage2 = pygame.image.load("Tiles/dustCloud2.png")
        self.dustCloudImage2 = pygame.transform.scale(dustCloudImage2, (self.dustCloudSize, self.dustCloudSize))

        dustCloudImage3 = pygame.image.load("Tiles/dustCloud3.png")
        self.dustCloudImage3 = pygame.transform.scale(dustCloudImage3, (self.dustCloudSize, self.dustCloudSize))

        dustCloudImage4 = pygame.image.load("Tiles/dustCloud4.png")
        self.dustCloudImage4 = pygame.transform.scale(dustCloudImage4, (self.dustCloudSize, self.dustCloudSize))

        dustCloudImage5 = pygame.image.load("Tiles/dustCloud5.png")
        self.dustCloudImage5 = pygame.transform.scale(dustCloudImage5, (self.dustCloudSize, self.dustCloudSize))

    def checkMouseInput(self):
        self.currentMousePosition = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed(num_buttons=3) == (True, False, False) and not self.posManage.blockJustPlaced:
            self.last_tick = pygame.time.get_ticks()
            self.posManage.placeBlock(self.currentMousePosition)
            self.posManage.saveCoords()




        # for event in pygame.event.get():
        #     if event.type == pygame.MOUSEWHEEL:
        #         if event.y == 1:
        #
        #         elif event.y == -1:
        #             self.mapManage.tileSize = self.mapManage.tileSize // 2
    # def on_move(self, x, y):
    #     print('Pointer moved to {0}'.format(
    #         (x, y)))
    #
    # def on_click(self, x, y, button, pressed):
    #     print('{0} at {1}'.format(
    #         'Pressed' if pressed else 'Released',
    #         (x, y)))
    #     if not pressed:
    #         # Stop listener
    #         return False
    #
    # def on_scroll(self, x, y, dx, dy):
    #     print('Scrolled {0} at {1}'.format(
    #         'down' if dy < 0 else 'up',
    #         (x, y)))
    #
    # # Collect events until released
    #
