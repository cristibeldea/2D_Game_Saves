import pygame
from Settings import *
import Tile

class MapManagement:
    def __init__(self, noiseManage):
        self.noiseManage = noiseManage

        self.tileSize = defaultTileSize
        self.focus = defaultFocus
        self.widthTiles = screenWidth // self.tileSize
        self.heightTiles = screenHeight // self.tileSize
        self.chunkSize = self.widthTiles
        self.step = defaultStep

        self.tileList = []

        grassImage = pygame.image.load("Tiles/grass.png")
        grassImage = pygame.transform.scale(grassImage, (self.tileSize, self.tileSize))
        self.grassTile = Tile.Tile("grass", grassImage, False, self.tileSize)
        self.tileList.append(self.grassTile)

        woodenWallImage = pygame.image.load("Tiles/woodenWall.png")
        woodenWallImage = pygame.transform.scale(woodenWallImage, (self.tileSize, self.tileSize))
        self.woodenWall = Tile.Tile("woodenWall", woodenWallImage, True, self.tileSize)
        self.tileList.append(self.woodenWall)

        sandImage = pygame.image.load("Tiles/sand.png")
        sandImage = pygame.transform.scale(sandImage, (self.tileSize, self.tileSize))
        self.sandTile = Tile.Tile("sand", sandImage, False, self.tileSize)
        self.tileList.append(self.sandTile)

        selectionImage1 = pygame.image.load("Tiles/selectionV1.png")
        self.selectionV1 = pygame.transform.scale(selectionImage1, (self.tileSize, self.tileSize))

        selectionImage2 = pygame.image.load("Tiles/selectionV2.png")
        self.selectionV2 = pygame.transform.scale(selectionImage2, (self.tileSize, self.tileSize))

        transitionImage = pygame.image.load("Tiles/transition.png")
        transitionImage = pygame.transform.scale(transitionImage, (self.tileSize, self.tileSize))
        self.transitionTile = Tile.Tile("trans", transitionImage, False, self.tileSize)
        self.tileList.append(self.transitionTile)

        sharpStonesImage = pygame.image.load("Tiles/sharpStones.png")
        sharpStonesImage = pygame.transform.scale(sharpStonesImage, (self.tileSize, self.tileSize))
        self.sharpStones = Tile.Tile("goldenStones", sharpStonesImage, False, self.tileSize)
        self.tileList.append(self.sharpStones)

        stoneTileImage = pygame.image.load("Tiles/roundedStones.png")
        stoneTileImage = pygame.transform.scale(stoneTileImage, (self.tileSize, self.tileSize))
        self.stoneTile = Tile.Tile("rounbStones", stoneTileImage, False, self.tileSize)
        self.tileList.append(self.stoneTile)



        # keyImage = pygame.image.load("Tiles/key.png")
        # keyImage = pygame.transform.scale(keyImage, (self.tileSize, self.tileSize))
        # self.keyTile = Tile.Tile("key", keyImage,False, self.tileSize)
        # self.tileList.append(self.keyTile)
        #
        # doorImage = pygame.image.load("Tiles/door.png")
        # doorImage = pygame.transform.scale(doorImage, (self.tileSize, self.tileSize))
        # self.doorTile = Tile.Tile("door", doorImage,True, self.tileSize)
        # self.tileList.append(self.doorTile)

    # def testPrint(self):
    #     print("MAP:\n")
    #     print(self.levelMap)



