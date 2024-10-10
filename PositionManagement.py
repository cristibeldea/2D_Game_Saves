from math import floor

import numpy as np
import pygame
from Settings import *
import AlteredBlock
import AlteredChunk
from Tile import Tile


class PositionManagement:
    def __init__(self, mapManage, noiseManage, player):
        self.lastBlockX = 0
        self.lastBlockY = 0
        self.mouseXTile = 0
        self.mouseYTile = 0
        self.blockX = 0
        self.blockY = 0
        self.block_X_inChunk = 0
        self.block_Y_inChunk = 0

        self.mapManage = mapManage
        self.noiseManage = noiseManage
        self.tileSize = self.mapManage.tileSize
        self.chunkSize = self.mapManage.chunkSize
        self.widthTiles = self.mapManage.widthTiles
        self.heightTiles = self.mapManage.heightTiles
        self.player = player

        self.insideTileX = self.tileSize - 1
        self.insideTileY = self.tileSize - 1
        self.selectionXOffset = self.tileSize - self.insideTileX
        self.selectionYOffset = self.tileSize - self.insideTileY
        self.insideChunkX = self.chunkSize // 2
        self.insideChunkY = self.chunkSize // 2

        self.player_position = [0, 0]
        self.realative_position = [3 * self.chunkSize // 2, 3 * self.chunkSize // 2]
        print(self.realative_position)
        self.chunk_position = [0, 0]

        self.front = 0
        self.back = 0
        self.right = 0
        self.left = 0

        self.leftBarrier = 0
        self.rightBarrier = 0
        self.topBarrier = 0
        self.bottomBarrier = 0
        self.playerWidth = 0.6 * self.tileSize
        self.playerHeight = 0.7 * self.tileSize
        self.lastDirection = "none "

        self.changeRate = 17

        self.currentMap = []
        self.tileMap = []
        self.currentChunks = []

        self.seed = 2
        self.step = self.mapManage.step

        self.alteredChunks = []
        self.alteredBlocks = []

        self.selectionX = -1
        self.selectionY = -1

        self.blockJustPlaced = False
        self.blocksAround = []

    def getTile(self, i, j):

        currentNumericalTile = self.currentMap[i][j][0]

        tile = self.mapManage.grassTile
        if currentNumericalTile <= 0.25:
            tile = self.mapManage.sharpStones
        elif 0.25 < currentNumericalTile < 0.5:
            tile = self.mapManage.sandTile
        elif 0.5 <= currentNumericalTile <= 1:
            tile = self.mapManage.grassTile
        elif 1 < currentNumericalTile != 10:
            tile = self.mapManage.stoneTile
        elif currentNumericalTile == 10:
            tile = self.mapManage.woodenWall

        return tile

    def assignTileMap(self):
        self.tileMap = []
        for i in range(len(self.currentMap)):
            row = []
            for j in range(len(self.currentMap[i])):
                row.append(self.getTile(i, j))
            self.tileMap.append(row)

            # row.append(self.getTile(i, j))
            # self.tileMap.append(row)

        # self.applyTransitionsAndEffects()

        # for i in range(len(self.currentMap) - 1):
        #     for j in range(len(self.currentMap[i]) - 1):
        #         if self.tileMap[i][j] != self.mapManage.transitionTile and ((self.tileMap[i][j+1] != self.mapManage.transitionTile and self.tileMap[i][j] != self.tileMap[i][j+1]) or (self.tileMap[i+1][j] != self.mapManage.transitionTile and self.tileMap[i][j] != self.tileMap[i+1][j])):
        #             self.tileMap[i][j] = self.mapManage.transitionTile

        ####PRINTING#####
        # for i in range(3*self.chunkSize):
        #     for j in range(3*self.chunkSize):
        #         print(self.tileMap[i][j].name, end=' ')
        #     print("\n")

    # def applyTransitionsAndEffects(self):
    #     for y in range(len(self.tileMap)):
    #         for x in range(len(self.tileMap)):

    # def canMove(self, keyPressed):
    #     if keyPressed[pygame.K_w]:
    #         upperTile = self.translateIntoTile(self.player_position[0], self.player_position[1] - 1)
    #         print(self.player_position)
    #         if upperTile.isSolid and self.insideTileY < self.tileSize / 3:
    #             return False
    #         else:
    #             return True
    #
    #     elif keyPressed[pygame.K_a]:
    #         leftTile = self.translateIntoTile(self.player_position[0] - 1, self.player_position[1])
    #         if leftTile.isSolid and self.insideTileX < self.tileSize / 2:
    #             return False
    #         else:
    #             return True
    #
    #     elif keyPressed[pygame.K_s]:
    #         lowerTile = self.translateIntoTile(self.player_position[0], self.player_position[1] + 1)
    #         if lowerTile.isSolid and self.insideTileY > self.tileSize / 3:
    #             return False
    #         else:
    #             return True
    #
    #     elif keyPressed[pygame.K_d]:
    #         rightTile = self.translateIntoTile(self.player_position[0] + 1, self.player_position[1])
    #         if rightTile.isSolid and self.insideTileX > self.tileSize / 2:
    #             return False
    #         else:
    #             return True

    def setBlocksAround(self):
        self.blocksAround[0] = self.tileMap[self.realative_position[0]][self.realative_position[1]].isSolid
        self.blocksAround[1] = self.tileMap[self.realative_position[0] - 1][self.realative_position[1] - 1].isSolid
        self.blocksAround[2] = self.tileMap[self.realative_position[0]][self.realative_position[1] - 1].isSolid
        self.blocksAround[3] = self.tileMap[self.realative_position[0] + 1][self.realative_position[1] - 1].isSolid
        self.blocksAround[4] = self.tileMap[self.realative_position[0] + 1][self.realative_position[1]].isSolid
        self.blocksAround[5] = self.tileMap[self.realative_position[0] + 1][self.realative_position[1] + 1].isSolid
        self.blocksAround[6] = self.tileMap[self.realative_position[0]][self.realative_position[1] + 1].isSolid
        self.blocksAround[7] = self.tileMap[self.realative_position[0] - 1][self.realative_position[1] + 1].isSolid
        self.blocksAround[8] = self.tileMap[self.realative_position[0] - 1][self.realative_position[1]].isSolid


    def canMove(self):
        result = True
        if self.blocksAround:
            result = False
        # if self.lastDirection == "left":
        #     nearTile = self.tileMap[self.realative_position[1]][self.realative_position[0] - 1]
        #     nearTileElevation = self.currentMap[self.realative_position[1]][self.realative_position[0] - 1][1]
        #     nearLowerTile = self.tileMap[self.realative_position[1] + 1][self.realative_position[0] - 1]
        #     nearLowerTileElevation = self.currentMap[self.realative_position[1] - 1][self.realative_position[0] - 1][1]
        #
        #     if self.insideTileX <= 3/2 * self.tileSize // 5:
        #         if nearTile.isSolid:  # and nearTileElevation <= self.player.elevation:
        #             result = False
        #         if nearLowerTile.isSolid:
        #             if self.tileSize // 2 + self.step < self.insideTileY < self.tileSize:
        #                 result = False
        #
        #             # print("relative:", self.realative_position[0] - 1, "barrier:", self.leftBarrier)
        #             # if self.realative_position[0] < self.leftBarrier:
        #             #     result = True
        #             # else:
        #             #     result = False
        #
        #         # if nearLowerTile.isSolid:
        #         #     if self.bottomBarrier * self.tileSize < (self.realative_position[1] + 1.2) * self.tileSize:
        #         #         result = True
        #         #     else:
        #         #         result = False
        #
        #         # if self.topBarrier * self.tileSize > (self.realative_position[1] + 0.5) * self.tileSize:
        #         #     result = True
        #         # else:
        #         #     result = False
        #
        # if self.lastDirection == "right":
        #     nearTile = self.tileMap[self.realative_position[1]][self.realative_position[0] + 1]
        #     nearTileElevation = self.currentMap[self.realative_position[1]][self.realative_position[0] + 1][1]
        #     nearLowerTile = self.tileMap[self.realative_position[1] + 1][self.realative_position[0] + 1]
        #     nearLowerTileElevation = self.currentMap[self.realative_position[1] - 1][self.realative_position[0] + 1][1]
        #
        #     if self.insideTileX >= self.tileSize - (3/2 * self.tileSize//5):
        #         if nearTile.isSolid:  # and nearTileElevation <= self.player.elevation:
        #             result = False
        #         if nearLowerTile.isSolid:
        #             if self.tileSize // 2 + self.step <= self.insideTileY < self.tileSize:
        #                 result = False
        #
        # if self.lastDirection == "up":
        #     nearTile = self.tileMap[self.realative_position[1] - 1][self.realative_position[0]]
        #     nearTileElevation = self.currentMap[self.realative_position[1] - 1][self.realative_position[0]][1]
        #     nearLeftTile = self.tileMap[self.realative_position[1] - 1][self.realative_position[0] - 1]
        #     nearLeftTileElevation = self.currentMap[self.realative_position[1] - 1][self.realative_position[0] - 1][1]
        #     nearRightTile = self.tileMap[self.realative_position[1] - 1][self.realative_position[0] + 1]
        #     nearRightTileElevation = self.currentMap[self.realative_position[1] - 1][self.realative_position[0] + 1][1]
        #
        #     if self.insideTileY <= self.tileSize / 15:
        #         if nearTile.isSolid:
        #             result = False
        #         if nearLeftTile.isSolid:
        #             if self.insideTileX <= 3 / 2 * self.tileSize / 5:
        #                 result = False
        #         if nearRightTile.isSolid:
        #             if self.insideTileX >= self.tileSize - (3/2 * self.tileSize /5):
        #                 result = False
        #
        # if self.lastDirection == "down":
        #     nearTile = self.tileMap[self.realative_position[1] + 1][self.realative_position[0]]
        #     nearTileElevation = self.currentMap[self.realative_position[1] + 1][self.realative_position[0]][1]
        #     nearLeftTile = self.tileMap[self.realative_position[1] + 1][self.realative_position[0] - 1]
        #     nearLeftTileElevation = self.currentMap[self.realative_position[1] + 1][self.realative_position[0] - 1][1]
        #     nearRightTile = self.tileMap[self.realative_position[1] + 1][self.realative_position[0] + 1]
        #     nearRightTileElevation = self.currentMap[self.realative_position[1] + 1][self.realative_position[0] + 1][1]
        #
        #     if self.insideTileY >= self.tileSize // 2:
        #         if nearTile.isSolid:
        #             result = False
        #         if nearLeftTile.isSolid:
        #             if self.insideTileX <= self.tileSize // 3:
        #                 result = False
        #         if nearRightTile.isSolid:
        #             if self.insideTileX > 2 * self.tileSize // 3:
        #                 result = False
        #

        return result

    def move(self):
        if self.lastDirection == "up":  # and self.canMove(keysPressed):
            self.insideTileY -= self.step

        elif self.lastDirection == "left":  # and self.canMove(keysPressed):
            self.insideTileX -= self.step

        elif self.lastDirection == "down":  # and self.canMove(keysPressed):
            self.insideTileY += self.step

        elif self.lastDirection == "right":  # and self.canMove(keysPressed):
            self.insideTileX += self.step

        elif self.lastDirection == "up_left":
            self.insideTileY -= self.step
            self.insideTileX -= self.step

        elif self.lastDirection == "up_right":
            self.insideTileY -= self.step
            self.insideTileX += self.step

        elif self.lastDirection == "down_left":
            self.insideTileY += self.step
            self.insideTileX -= self.step

        elif self.lastDirection == "down_right":
            self.insideTileY += self.step
            self.insideTileX += self.step


    def setDirection(self, keysPressed):
        if keysPressed[pygame.K_a] and keysPressed[pygame.K_w]:
            self.lastDirection = "up_left"
        elif keysPressed[pygame.K_d] and keysPressed[pygame.K_w]:
            self.lastDirection = "up_right"
        elif keysPressed[pygame.K_a] and keysPressed[pygame.K_s]:
            self.lastDirection = "down_left"
        elif keysPressed[pygame.K_d] and keysPressed[pygame.K_s]:
            self.lastDirection = "down_right"
        elif keysPressed[pygame.K_a]:
            self.lastDirection = "left"
        elif keysPressed[pygame.K_d]:
            self.lastDirection = "right"
        elif keysPressed[pygame.K_w]:
            self.lastDirection = "up"
        elif keysPressed[pygame.K_s]:
            self.lastDirection = "down"
        else:
            self.lastDirection = "none"
        print(self.lastDirection)

    # def playerNotOutOfMap(self):
    #     if(self.player_position[0] < widthTiles and self.player_position[0] > 0):
    #         if(self.player_position[1] < heightTiles and self.player_position[1] > 0):
    #             return True
    #         else:
    #             return False
    def changeRelativePosition(self, xIncrement, yIncrement):
        self.realative_position[0] += xIncrement
        self.realative_position[1] += yIncrement

    def resetRelativePosition(self, xDelta, yDelta):
        if xDelta == -1:
            self.realative_position[0] += self.chunkSize
            self.insideTileX = self.tileSize
            self.insideChunkX = self.chunkSize - 1
        elif xDelta == 1:
            self.realative_position[0] -= self.chunkSize
            self.insideTileX = 0
            self.insideChunkX = 0

        if yDelta == -1:
            self.realative_position[1] += self.chunkSize
            self.insideTileY = self.tileSize
            self.insideChunkY = self.chunkSize - 1
        elif yDelta == 1:
            self.realative_position[1] -= self.chunkSize
            self.insideTileY = 0
            self.insideChunkY = 0

    def changePosition(self, xIncrement, yIncrement):
        self.player_position[0] += xIncrement
        self.player_position[1] += yIncrement
        self.insideChunkX += xIncrement
        self.insideChunkY += yIncrement
        self.changeRelativePosition(xIncrement, yIncrement)

    def checkAndChangePosition(self):
        xIncrement = 0
        yIncrement = 0
        if self.insideTileX < 0:
            self.insideTileX = self.tileSize
            xIncrement = -1
        elif self.insideTileX >= self.tileSize:
            self.insideTileX = 0
            xIncrement = 1

        if self.insideTileY < 0:
            self.insideTileY = self.tileSize
            yIncrement = -1
        elif self.insideTileY >= self.tileSize:
            self.insideTileY = 0
            yIncrement = 1

        if xIncrement != 0 or yIncrement != 0:
            self.changePosition(xIncrement, yIncrement)
            self.checkAndChangeChunk()

    def getDetailedPosition(self):
        position = [0, 0]
        position[0] = self.realative_position[0] + self.insideTileX / self.tileSize
        position[1] = self.realative_position[1] + self.insideTileY / self.tileSize

        return position

    def setPlayerCollisionBounds(self):

        position = self.getDetailedPosition()
        self.leftBarrier = position[0] - 0.3
        self.rightBarrier = position[0] + 0.3
        self.topBarrier = position[1]
        self.bottomBarrier = position[1] + 0.5

    # def isAltered_relative(self, index):
    #     [x, x_junk, y, y_junk] = self.translateIndexToPosition(index)
    #     for element in self.alteredChunks:
    #         if element[0][0] == x and element[0][1] == y:
    #             return True

    def isAltered(self, chunkX, chunkY):
        for i in range(len(self.alteredChunks)):
            if self.alteredChunks[i].x == chunkX and self.alteredChunks[i].y == chunkY:
                return i
        return -1

    def isAltered_index(self, index):
        [x, x_junk, y, y_junk] = self.translateIndexToPosition(index)
        x = x // self.chunkSize
        y = y // self.chunkSize
        # print("INDEX_VERIFICATION: ", index, "X and Y VERIFICATION: ", x, y)
        # print("CHUNK ALTERAT (translation): ", x, y)
        return self.isAltered(x, y)

    def addAlteredBlocks(self, index):
        i = self.isAltered_index(index)
        for block in self.alteredChunks[i].alteredBlocks:
            print("DRAWING block (i, j): ", block.y, block.x, " in chunk (x, y): ", self.alteredChunks[i].x,
                  self.alteredChunks[i].y)
            self.currentChunks[index][block.y][block.x][0] = block.num
            # print("ADAUGAT CUB la poz: ", block.x, block.y)

    def changeCurrentChunks(self, xDelta, yDelta):
        # print("E AICI")
        if xDelta == -1:
            print("CHUNK NOU")
            self.currentChunks[3] = self.currentChunks[2]
            self.currentChunks[4] = self.currentChunks[0]
            self.currentChunks[5] = self.currentChunks[6]

            self.currentChunks[2] = self.currentChunks[1]
            self.currentChunks[0] = self.currentChunks[8]
            self.currentChunks[6] = self.currentChunks[7]

            self.currentChunks[1] = self.generateChunk(1)
            self.currentChunks[8] = self.generateChunk(8)
            self.currentChunks[7] = self.generateChunk(7)

        elif xDelta == 1:
            print("CHUNK NOU")
            self.currentChunks[1] = self.currentChunks[2]
            self.currentChunks[8] = self.currentChunks[0]
            self.currentChunks[7] = self.currentChunks[6]

            self.currentChunks[2] = self.currentChunks[3]
            # print("INAINTE: ", self.currentChunks[4])
            self.currentChunks[0] = self.currentChunks[4]
            # print("DUPA :", self.currentChunks[0])
            self.currentChunks[6] = self.currentChunks[5]
            # print("SCADERE: ")
            # print(self.currentChunks[4] - self.currentChunks[0])
            self.currentChunks[3] = self.generateChunk(3)
            self.currentChunks[4] = self.generateChunk(4)
            self.currentChunks[5] = self.generateChunk(5)

        if yDelta == -1:
            print("CHUNK NOU")
            self.currentChunks[7] = self.currentChunks[8]
            self.currentChunks[6] = self.currentChunks[0]
            self.currentChunks[5] = self.currentChunks[4]

            self.currentChunks[8] = self.currentChunks[1]
            self.currentChunks[0] = self.currentChunks[2]
            self.currentChunks[4] = self.currentChunks[3]

            self.currentChunks[1] = self.generateChunk(1)
            self.currentChunks[2] = self.generateChunk(2)
            self.currentChunks[3] = self.generateChunk(3)


        elif yDelta == 1:
            print("CHUNK NOU")
            self.currentChunks[1] = self.currentChunks[8]
            self.currentChunks[2] = self.currentChunks[0]
            self.currentChunks[3] = self.currentChunks[4]

            self.currentChunks[8] = self.currentChunks[7]
            self.currentChunks[0] = self.currentChunks[6]
            self.currentChunks[4] = self.currentChunks[5]

            self.currentChunks[7] = self.generateChunk(7)
            self.currentChunks[6] = self.generateChunk(6)
            self.currentChunks[5] = self.generateChunk(5)

        for i in range(9):
            if self.isAltered_index(i) != -1:
                self.addAlteredBlocks(i)

    def changeChunkPosition(self, xIncrement, yIncrement):
        self.chunk_position[0] += xIncrement
        self.chunk_position[1] += yIncrement

        self.resetRelativePosition(xIncrement, yIncrement)
        self.changeCurrentChunks(xIncrement, yIncrement)
        self.createCurrentMap()

    def checkAndChangeChunk(self):
        xIncrement = 0
        yIncrement = 0
        if self.insideChunkX < 0:
            self.insideChunkX = self.chunkSize - 1
            xIncrement = -1
        elif self.insideChunkX > self.chunkSize - 1:
            self.insideChunkX = 0
            xIncrement = 1

        if self.insideChunkY < 0:
            self.insideChunkY = self.chunkSize - 1
            yIncrement = -1
        elif self.insideChunkY > self.chunkSize - 1:
            self.insideChunkY = 0
            yIncrement = 1

        if xIncrement != 0 or yIncrement != 0:
            self.changeChunkPosition(xIncrement, yIncrement)

    def translateIndexToPosition(self, chunkIndex):
        x_start = 0
        y_start = 0
        x_end = 0
        y_end = 0
        if chunkIndex == 0:
            x_start = self.chunk_position[0]
            x_end = self.chunk_position[0] + 1
            y_start = self.chunk_position[1]
            y_end = self.chunk_position[1] + 1

        elif chunkIndex == 1:
            x_start = self.chunk_position[0] - 1
            x_end = self.chunk_position[0]
            y_start = self.chunk_position[1] - 1
            y_end = self.chunk_position[1]

        elif chunkIndex == 2:
            x_start = self.chunk_position[0]
            x_end = self.chunk_position[0] + 1
            y_start = self.chunk_position[1] - 1
            y_end = self.chunk_position[1]

        elif chunkIndex == 3:
            x_start = self.chunk_position[0] + 1
            x_end = self.chunk_position[0] + 2
            y_start = self.chunk_position[1] - 1
            y_end = self.chunk_position[1]

        elif chunkIndex == 4:
            x_start = self.chunk_position[0] + 1
            x_end = self.chunk_position[0] + 2
            y_start = self.chunk_position[1]
            y_end = self.chunk_position[1] + 1

        elif chunkIndex == 5:
            x_start = self.chunk_position[0] + 1
            x_end = self.chunk_position[0] + 2
            y_start = self.chunk_position[1] + 1
            y_end = self.chunk_position[1] + 2

        elif chunkIndex == 6:
            x_start = self.chunk_position[0]
            x_end = self.chunk_position[0] + 1
            y_start = self.chunk_position[1] + 1
            y_end = self.chunk_position[1] + 2

        elif chunkIndex == 7:
            x_start = self.chunk_position[0] - 1
            x_end = self.chunk_position[0]
            y_start = self.chunk_position[1] + 1
            y_end = self.chunk_position[1] + 2

        elif chunkIndex == 8:
            x_start = self.chunk_position[0] - 1
            x_end = self.chunk_position[0]
            y_start = self.chunk_position[1]
            y_end = self.chunk_position[1] + 1

        x_start = x_start * self.chunkSize
        x_end = x_end * self.chunkSize
        y_start = y_start * self.chunkSize
        y_end = y_end * self.chunkSize

        return [x_start, x_end, y_start, y_end]

    def generateChunk(self, chunkIndex):
        finalMatrix = []
        [x_start, x_end, y_start, y_end] = self.translateIndexToPosition(chunkIndex)
        biomeMatrix = self.noiseManage.generate_perlin_noise_matrix(x_start, x_end, y_start, y_end, self.seed)
        elevationMatrix = self.noiseManage.generate_perlin_noise_matrix(x_start, x_end, y_start, y_end, self.seed + 1)
        for i in range(len(elevationMatrix)):
            for j in range(len(elevationMatrix[0])):
                elevationMatrix[i][j] = floor(elevationMatrix[i][j])

        for i in range(len(elevationMatrix)):
            row = []
            for j in range(len(elevationMatrix[0])):
                row.append([biomeMatrix[i][j], elevationMatrix[i][j]])
            finalMatrix.append(row)

        return finalMatrix

    def generateFirstChunks(self):
        for chunkIndex in range(9):
            self.currentChunks.append(self.generateChunk(chunkIndex))
            if self.isAltered_index(chunkIndex) != -1:
                self.addAlteredBlocks(chunkIndex)

        self.createCurrentMap()

    def createCurrentMap(self):
        self.currentMap = []
        for i in range(len(self.currentChunks[1])):
            line = []
            line.extend(self.currentChunks[1][i])
            line.extend(self.currentChunks[2][i])
            line.extend(self.currentChunks[3][i])
            self.currentMap.append(line)

        for i in range(len(self.currentChunks[8])):
            line = []
            line.extend(self.currentChunks[8][i])
            line.extend(self.currentChunks[0][i])
            line.extend(self.currentChunks[4][i])
            self.currentMap.append(line)

        for i in range(len(self.currentChunks[7])):
            line = []
            line.extend(self.currentChunks[7][i])
            line.extend(self.currentChunks[6][i])
            line.extend(self.currentChunks[5][i])
            self.currentMap.append(line)

        self.assignTileMap()
        # print("MAP:", self.currentMap)

    def getSelectionPosition(self, currentMousePosition):
        self.selectionXOffset = self.tileSize - self.insideTileX
        self.selectionYOffset = self.tileSize - self.insideTileY
        self.selectionX = self.selectionXOffset + (
                currentMousePosition[0] - self.selectionXOffset) // self.tileSize * self.tileSize
        self.selectionY = self.selectionYOffset + (
                currentMousePosition[1] - self.selectionYOffset) // self.tileSize * self.tileSize

        return [self.selectionX, self.selectionY]

    def getMousePositionInTiles(self, currentMousePosition):
        tileXOffset = self.tileSize - self.insideTileX
        tileYOffset = self.tileSize - self.insideTileY
        self.mouseXTile = (currentMousePosition[0] - tileXOffset) // self.tileSize
        self.mouseYTile = (currentMousePosition[1] - tileYOffset) // self.tileSize
        return [self.mouseXTile, self.mouseYTile]

    def getBlockPositionOnMap(self, currentMousePosition):
        [mouseXTile, mouseYTile] = self.getMousePositionInTiles(currentMousePosition)
        # print("CHUNKS SIZE:", self.chunkSize)
        dx = self.chunkSize - (self.widthTiles // 2 - self.insideChunkX)
        dy = self.chunkSize - (self.heightTiles // 2 - self.insideChunkY)
        blockX = dx + mouseXTile + 1
        blockY = dy + mouseYTile + 1
        # print("BLocuri pe mapa: ", blockX, blockY)
        return [blockX, blockY]

    def findAlteredChunk_andBlocks(self, blockX, blockY):
        if blockX < self.chunkSize:
            if blockY < self.chunkSize:
                return [self.chunk_position[0] - 1, self.chunk_position[1] - 1, blockX, blockY]

            elif self.chunkSize <= blockY < 2 * self.chunkSize:
                return [self.chunk_position[0] - 1, self.chunk_position[1], blockX, blockY - self.chunkSize]

            elif blockY >= 2 * self.chunkSize:
                return [self.chunk_position[0] - 1, self.chunk_position[1] + 1, blockX, blockY - 2 * self.chunkSize]

        elif self.chunkSize <= blockX < 2 * self.chunkSize:
            print("BLOCK Y: ", blockY)
            if blockY < self.chunkSize:
                return [self.chunk_position[0], self.chunk_position[1] - 1, blockX - self.chunkSize, blockY]

            elif self.chunkSize <= blockY < 2 * self.chunkSize:
                return [self.chunk_position[0], self.chunk_position[1], blockX - self.chunkSize,
                        blockY - self.chunkSize]

            elif blockY >= 2 * self.chunkSize:
                return [self.chunk_position[0], self.chunk_position[1] + 1, blockX - self.chunkSize,
                        blockY - 2 * self.chunkSize]

        elif 2 * self.chunkSize <= blockX:
            if blockY < self.chunkSize:
                return [self.chunk_position[0] + 1, self.chunk_position[1] - 1, blockX - 2 * self.chunkSize, blockY]

            if self.chunkSize <= blockY < 2 * self.chunkSize:
                return [self.chunk_position[0] + 1, self.chunk_position[1], blockX - 2 * self.chunkSize,
                        blockY - self.chunkSize]

            if blockY >= 2 * self.chunkSize:
                return [self.chunk_position[0] + 1, self.chunk_position[1] + 1, blockX - 2 * self.chunkSize,
                        blockY - 2 * self.chunkSize]

    def placeBlock(self, currentMousePosition):
        [self.blockX, self.blockY] = self.getBlockPositionOnMap(currentMousePosition)
        self.currentMap[self.blockY][self.blockX][0] = 10
        self.tileMap[self.blockY][self.blockX] = self.mapManage.woodenWall
        # self.tileMap[self.blockY][self.blockX] = self.mapManage.woodenWall

        [chunkX, chunkY, self.block_X_inChunk, self.block_Y_inChunk] = self.findAlteredChunk_andBlocks(self.blockX,
                                                                                                       self.blockY)

        alteredBlock = AlteredBlock.AlteredBlock()
        alteredBlock.x = self.block_X_inChunk
        alteredBlock.y = self.block_Y_inChunk
        alteredBlock.num = 10
        alteredBlock.tile = self.mapManage.woodenWall

        i = self.isAltered(chunkX, chunkY)
        if i != -1:
            self.alteredChunks[i].alteredBlocks.append(alteredBlock)
        else:
            alteredChunk = AlteredChunk.AlteredChunk()
            alteredChunk.x = chunkX
            alteredChunk.y = chunkY
            alteredChunk.alteredBlocks.append(alteredBlock)
            self.alteredChunks.append(alteredChunk)

        self.blockJustPlaced = True

    def saveCoords(self):
        self.lastBlockX = self.blockX
        self.lastBlockY = self.blockY

    def getDustCloudPosition(self):
        x = self.lastBlockX - self.realative_position[0] + self.widthTiles // 2
        y = self.lastBlockY - self.realative_position[1] + self.heightTiles // 2
        print("lastBlocks: ", self.lastBlockX, self.lastBlockY)
        print("x and y ", x, y)
        return x, y

    # def checkAndChangeRelativePosition(self):
