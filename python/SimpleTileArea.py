from openlocationcode import openlocationcode as olc
from TileArea import TileArea

class SimpleTileArea(TileArea):
    '''/**
     * Simplest implementation of {@link TileArea} possible. This just collects all tiles that are added
     * to it, but does not clean up its internal collection (for example by merging tiles,
     * by removing smaller tiles when a larger, encompassing one is added) or by managing territory
     * beyond its individual, potentially non-contiguous tiles.
    */'''
    #public class SimpleTileArea extends TileArea {
    def __init__(self, tile_list=[]):
        super().__init__(tile_list)
        self.smallestTileSize = ogt.TileSize.GLOBAL

    def addNonContainedTile(newTile):
        self.tile_list.append(newTile):
        if newTile.getTileSize().getCodeLength() > self.smallestTileSize.getCodeLength():
            self.smallestTileSize = newTile.getTileSize()

    def getSmallestTileSize():
        return self.smallestTileSize


    def contains(tile):
        for memberTile in self.tile_list:
            if memberTile.contains(tile):
                return True
        return False

    def getCoveringTileArrayList():
        return self.tile_list

