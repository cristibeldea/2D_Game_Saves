class ElevationManagement:
    def __init__(self, noiseManage, posManage):
        self.seaLevel = 0
        self.playerStartLevel = 1
        self.posManage = posManage
        self.noiseManage = noiseManage

    def generateElevationMap(self):
        elevationMap = []

