import pygame
import Tile
from Settings import *
class Player:
    def __init__(self, tileSize):

        self.health = 100
        self.elevation = 1

        self.playerImage = pygame.image.load("Tiles/player.png")
        self.playerImage = pygame.transform.scale(self.playerImage, (tileSize, tileSize))
        self.playerTile = Tile.Tile("player", self.playerImage, False, tileSize)

        self.frontRightWalkingImage = pygame.image.load("Tiles/walkingFrontRightFoot.png")
        self.frontRightWalkingImage = pygame.transform.scale(self.frontRightWalkingImage, (tileSize, tileSize))

        self.frontLeftWalkingImage = pygame.image.load("Tiles/walkingFrontLeftFoot.png")
        self.frontLeftWalkingImage = pygame.transform.scale(self.frontLeftWalkingImage, (tileSize, tileSize))

        # self.leftStanding = pygame.image.load("Tiles/standingLeft (1).png")
        # self.leftStanding = pygame.transform.scale(self.leftStanding, (tileSize, tileSize))

        self.leftWalking1 = pygame.image.load("Tiles/Variant1_left1.png")
        self.leftWalking1 = pygame.transform.scale(self.leftWalking1, (tileSize, tileSize))

        self.leftWalking2 = pygame.image.load("Tiles/Variant1_left2.png")
        self.leftWalking2 = pygame.transform.scale(self.leftWalking2, (tileSize, tileSize))

        self.leftWalking3 = pygame.image.load("Tiles/Variant1_left3.png")
        self.leftWalking3 = pygame.transform.scale(self.leftWalking3, (tileSize, tileSize))

        self.backWalkingRightFoot = pygame.image.load("Tiles/walkingBackRightFoot.png")
        self.backWalkingRightFoot = pygame.transform.scale(self.backWalkingRightFoot, (tileSize, tileSize))

        self.backWalkingLeftFoot = pygame.image.load("Tiles/walkingBackLeftFoot.png")
        self.backWalkingLeftFoot = pygame.transform.scale(self.backWalkingLeftFoot, (tileSize, tileSize))

        self.rightWalking1 = pygame.image.load("Tiles/Variant1_right1.png")
        self.rightWalking1 = pygame.transform.scale(self.rightWalking1,(tileSize, tileSize))

        self.rightWalking2 = pygame.image.load("Tiles/Variant1_right2.png")
        self.rightWalking2 = pygame.transform.scale(self.rightWalking2, (tileSize, tileSize))

        self.rightWalking3 = pygame.image.load("Tiles/Variant1_right3.png")
        self.rightWalking3 = pygame.transform.scale(self.rightWalking3, (tileSize, tileSize))


        #self.tileList.append(playerTile)

    def changePlayerImage(self, description):
        if description == "frontRightFoot":
            self.playerTile.image = self.frontRightWalkingImage

        elif description == "standing":
            self.playerTile.image = self.playerImage

        elif description == "frontLeftFoot":
            self.playerTile.image = self.frontLeftWalkingImage

        elif description == "left1":
            self.playerTile.image = self.leftWalking1

        elif description == "left2":
            self.playerTile.image = self.leftWalking2

        elif description == "left3":
            self.playerTile.image = self.leftWalking3

        elif description == "backRightFoot":
            self.playerTile.image = self.backWalkingRightFoot

        elif description == "backLeftFoot":
            self.playerTile.image = self.backWalkingLeftFoot

        elif description == "right1":
            self.playerTile.image = self.rightWalking1

        elif description == "right2":
            self.playerTile.image = self.rightWalking2

        elif description == "right3":
            self.playerTile.image = self.rightWalking3





