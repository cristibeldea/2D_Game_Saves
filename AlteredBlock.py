import MapManagement
class AlteredBlock:
    def __init__(self):
        self.mapManage = MapManagement.MapManagement(noiseManage=0)
        self.x = 0
        self.y = 0
        self.tile = self.mapManage.grassTile
        self.num = 0

