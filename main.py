import threading

import pygame, sys

import PerlinNoiseManagement
import PositionManagement
import MapManagement
import Player
import PlayerInputManagement
import ElevationManagement
from Settings import *
from pynput import mouse


class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.clock = pygame.time.Clock()

        self.noiseManage = PerlinNoiseManagement.PerlinNoiseManagement()
        self.mapManage = MapManagement.MapManagement(self.noiseManage)
        self.player = Player.Player(self.mapManage.tileSize)
        self.posManage = PositionManagement.PositionManagement(self.mapManage, self.noiseManage, self.player)
        self.inputManage = PlayerInputManagement.PlayerInputManagement(self.posManage)
        #self.elevationManage = ElevationManagement.ElevationManagement(self.noiseManage, self.posManage)

        self.counter = 0
        self.counter_2 = 0

        self.firstVar = True
        self.secondVar = False

        self.wonGame = False

        self.tileSize = self.mapManage.tileSize
        self.chunkSize = self.mapManage.chunkSize
        self.widthTiles = self.mapManage.widthTiles
        self.heightTiles = self.mapManage.heightTiles
        self.step = self.mapManage.step

    def checkPlayerHasQuitted(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.posManage.setPlayerCollisionBounds()
        self.keyPressed = pygame.key.get_pressed()
        self.posManage.setDirection(self.keyPressed)

        self.posManage.move()

        self.posManage.checkAndChangePosition()
        self.inputManage.checkMouseInput()

        # self.checkKeyTaken()
        # self.checkOpenedDoor()
        # self.checkExitMaze()
        # self.checkWinnedGame()
        threading.Thread(target=self.drawScreen())

        pygame.display.update()
        self.clock.tick(FPS)

    def run(self):
        self.posManage.generateFirstChunks()
        while self.running:
            self.checkPlayerHasQuitted()
            ####################

            ###################
            self.update()

    def drawSelectionArea(self):
        # print(self.posManage.selectionDecalationX, self.posManage.selectionDecalationY)
        [self.selectionX, self.selectionY] = self.posManage.getSelectionPosition(self.inputManage.currentMousePosition)

        if self.counter % 40 == 0:
            self.firstVar = True
            self.secondVar = False

        if self.counter % 80 == 0:
            self.secondVar = True
            self.firstVar = False
            self.counter = 0
        self.counter += 1

        if self.firstVar:
            self.screen.blit(self.mapManage.selectionV1, (self.selectionX, self.selectionY))
        elif self.secondVar:
            self.screen.blit(self.mapManage.selectionV2, (self.selectionX, self.selectionY))

    #def drawAddedBlocks(self):

    def drawMap(self):
        for i in range(-1, self.heightTiles + 1):
            for j in range(-1, self.widthTiles + 1):
                # currentTileToDraw = self.mapManage.getTile(i+1, j+1)
                currentTileToDraw = self.posManage.tileMap[i + self.posManage.realative_position[1] - self.heightTiles // 2][j + self.posManage.realative_position[0] - self.widthTiles // 2]
                self.screen.blit(currentTileToDraw.image, (j * self.tileSize - self.posManage.insideTileX, i * self.tileSize - self.posManage.insideTileY))

        #self.drawAddedBlocks()
            # print("\n"
    def drawPlayer(self):
        # position_toDraw = self.posManage.getDetailedPosition()
        # self.screen.blit(self.player.playerTile.image, (position_toDraw[0] * self.tileSize, position_toDraw[1] * self.tileSize) )
        if (self.posManage.lastDirection == "down"):
            if (self.posManage.front < self.posManage.changeRate):
                self.player.changePlayerImage("frontRightFoot")

            elif (self.posManage.front >= self.posManage.changeRate):
                self.player.changePlayerImage("frontLeftFoot")

            self.posManage.front += 1
            if (self.posManage.front == 2 * self.posManage.changeRate):
                self.posManage.front = 0

        elif self.posManage.lastDirection == "left":
            if self.posManage.left < self.posManage.changeRate:
                self.player.changePlayerImage("left1")

            elif self.posManage.changeRate <= self.posManage.left < self.posManage.changeRate + 10:
                self.player.changePlayerImage("left3")

            elif self.posManage.left >= self.posManage.changeRate + 10 and self.posManage.left < 2* self.posManage.changeRate + 10:
                self.player.changePlayerImage("left2")

            elif self.posManage.left >= 2 * self.posManage.changeRate + 10:
                self.player.changePlayerImage("left3")

            self.posManage.left += 1
            if (self.posManage.left == 2 * self.posManage.changeRate + 20):
                self.posManage.left = 0

        elif self.posManage.lastDirection == "up":
            if self.posManage.back < self.posManage.changeRate:
                self.player.changePlayerImage("backRightFoot")

            elif self.posManage.back >= self.posManage.changeRate:
                self.player.changePlayerImage("backLeftFoot")

            self.posManage.back += 1
            if (self.posManage.back == 2 * self.posManage.changeRate):
                self.posManage.back = 0

        elif self.posManage.lastDirection == "right":
            if self.posManage.right < self.posManage.changeRate:
                self.player.changePlayerImage("right1")

            elif self.posManage.changeRate <= self.posManage.right < self.posManage.changeRate + 10:
                self.player.changePlayerImage("right3")

            elif self.posManage.changeRate + 10 <= self.posManage.right <= 2* self.posManage.changeRate + 10:
                self.player.changePlayerImage("right2")

            elif 2* self.posManage.changeRate + 10 < self.posManage.right:
                self.player.changePlayerImage("right3")

            self.posManage.right += 1
            if self.posManage.right == 2 * self.posManage.changeRate + 20:
                self.posManage.right = 0

        else:
            self.player.changePlayerImage("standing")
        self.screen.blit(self.player.playerTile.image, screenCenter)

    # def drawWinScreen(self):
    #     winImage = pygame.image.load("Tiles/win.png")
    #     winImage = pygame.transform.scale(winImage, (4 * self.tileSize, 2 * self.tileSize))
    #     self.screen.fill((0,0,0))
    #     self.screen.blit(winImage,
    #                      ((screenWidth - 4*self.tileSize) / 2, (screenHeight - 2*self.tileSize) / 2))

    def drawDustCloud(self, x, y):
        if self.counter_2 < 10:
            self.screen.blit(self.inputManage.dustCloudImage1, (x, y))
        elif 7 <= self.counter_2 < 14:
            self.screen.blit(self.inputManage.dustCloudImage2, (x, y))
        elif 14 <= self.counter_2 < 21:
            self.screen.blit(self.inputManage.dustCloudImage3, (x, y))
        elif 21 <= self.counter_2 < 28:
            self.screen.blit(self.inputManage.dustCloudImage4, (x, y))
        elif 28 <= self.counter_2 < 35:
            self.screen.blit(self.inputManage.dustCloudImage5, (x, y))
        elif self.counter_2 == 35:
            self.counter_2 = 0
            self.posManage.blockJustPlaced = False

        self.counter_2 += 1

        print("DUST CLOUD DRAWN AT: ", x, y)
    def drawScreen(self):
        self.screen.fill((0, 0, 0))
        # draw map
        self.drawMap()
        if self.posManage.blockJustPlaced:
            [x, y] = self.posManage.getDustCloudPosition()
            print(x, y)
            self.drawDustCloud(x * self.tileSize - self.posManage.insideTileX - 12, y * self.tileSize - self.posManage.insideTileY - 12)
        self.drawPlayer()
        self.drawSelectionArea()


        # self.drawWinScreen()
        # draw player

        # draw movable objects


if __name__ == "__main__":
    gameManagement = Game()
    gameManagement.run()
