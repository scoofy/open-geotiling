from openlocationcode import openlocationcode as olc
from TileArea import TileArea
from OpenGeoTile import OpenGeoTile, TileSize

class SimpleTileArea(TileArea):
    '''/**
     * Simplest implementation of {@link TileArea} possible. This just collects all tiles that are added
     * to it, but does not clean up its internal collection (for example by merging tiles,
     * by removing smaller tiles when a larger, encompassing one is added) or by managing territory
     * beyond its individual, potentially non-contiguous tiles.
    */'''
    ''' because the tile areas don't merge, this will be inherently ineffecient
        larger tiles will contain smaller tiles, but they will be redundant
    '''
    def __init__(self, tile_list=[]):
        self.smallestTileSize = TileSize.GLOBAL
        super().__init__(tile_list)


    def addNonContainedTile(self, newTile, convert_to_shortest_covering_tile_list=False):
        self.tile_list.append(newTile)
        if newTile.getTileSize().getCodeLength() > self.smallestTileSize.getCodeLength():
            self.smallestTileSize = newTile.getTileSize()

    def getSmallestTileSize(self):
        return self.smallestTileSize


    def contains(self, tile):
        for memberTile in self.tile_list:
            if memberTile.contains(tile):
                return True
        return False

    def getShortestCoveringTileList(self):
        return self.tile_list

