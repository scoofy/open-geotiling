from openlocationcode import openlocationcode as olc
from OpenGeoTile import OpenGeoTile, TileSize
from operator import methodcaller
import pprint
pp = pprint.pformat

class TileArea():
    '''/**
     * An area defined by one or more {@link OpenGeoTile} tiles
    */'''
    def __init__(self, tile_list):
        '''/**
         * default constructor
         */'''

        '''/**
         * Construct a TileArea from a list of tiles.
         * @param tiles an ArrayList of tiles that should be added to this object
        */'''
        if not isinstance(tile_list, (list, OpenGeoTile)):
            raise Exception("New TileArea must contain valid OpenGeoTile tiles")

        self.tile_list = []
        if isinstance(tile_list, OpenGeoTile):
            tile_list = [tile_list]
        for newTile in tile_list:
            self.addTile(newTile, convert_to_shortest_covering_tile_list=False)
        self.tile_list = self.getShortestCoveringTileList()

    def getShortestCoveringTileList(self):
        '''/**
         * Get a list of tiles that fully cover this TileArea as currently defined. Note that this is
         * not necessarily the same list that went into this object over time. In case of a contiguous
         * TileArea, it can also include tiles that never have been added.
         * @return an ArrayList of {@link OpenGeoTile} tiles which fully cover the area of this TileArea
        */'''
        # get address set list
        existing_address_list_unsorted = list(set([tile.getTileAddress() for tile in self.tile_list]))

        # filter out tiles subsumed in bigger tiles
        existing_address_list_without_subsumption = []
        existing_address_list_shortest_to_longest = sorted(existing_address_list_unsorted, key=len)
        for unfiltered_address in existing_address_list_shortest_to_longest:
            tile_is_subtile = False
            for filtered_address in existing_address_list_without_subsumption:
                if not tile_is_subtile:
                    if len(filtered_address) < len(unfiltered_address):
                        if unfiltered_address.startswith(filtered_address):
                            tile_is_subtile = True
            if not tile_is_subtile:
                existing_address_list_without_subsumption.append(unfiltered_address)


        # sort from biggest tiles to smallest
        existing_address_list_longest_to_shortest = sorted(existing_address_list_without_subsumption, key=len, reverse=True)
        '''
        create dict like this:
        take the last two digits, and split off their parent,
        if the parent list ends up equaling 20x20 length it's full, add parent letters
        to dict in the same method,
        go from smallest to biggest, and it should work.
        Then, after you make them, just unite all the parents with all the children
        dict = {
            parent: child_list,

            "3333": ["22", "33"... etc],
            "22": ["22", "33"... etc],

        }'''
        address_dict = {}
        for address in existing_address_list_longest_to_shortest:
            #print("address:", address)
            address_dict = self.recursiveShortestCoveringTileDictBuilder(address, address_dict)
        #print("address_dict:", pp(address_dict))

        shortest_covering_tile_list = []
        for parent, child_list in address_dict.items():
            for child in child_list:
                full_address = parent + child
                shortest_covering_tile_list.append(OpenGeoTile(code=full_address))
        return shortest_covering_tile_list

    def recursiveShortestCoveringTileDictBuilder(self, tile_address, address_dict):
            parent, child = tile_address[:-2],  tile_address[-2:]
            child_list = address_dict.get(parent, [])
            child_list.append(child)
            if len(child_list) == 20*20: # if full tile
                del address_dict[parent]
                return self.recursiveShortestCoveringTileDictBuilder(parent, address_dict)
            else:
                address_dict[parent] = child_list
                return address_dict

    def contains(self, tile):
        '''/**
         * Check if the area defined by {@link OpenGeoTile} tile is completely inside this object's
         * area.
         * @param tile an OpenGeoTile, the area of which will be checked
         * @return true if the whole area of {@code tile} is inside this object's area, false if not
        */'''
        for existing_tile in self.getShortestCoveringTileList():
            if existing_tile.contains(tile):
                return True
        return False
        # public abstract boolean contains(OpenGeoTile tile);

    def getSmallestTileSize(self):
        '''/**
         * Gets the {@link org.bocops.opengeotiling.OpenGeoTile.TileSize} of the smallest
         * {@link OpenGeoTile} used to define the area of this object.
         * @return the smallest tile size (=longest address) used by one of the tiles of this area
        */'''
        # sorting by getTileAddress, reversed, so the longest address is first, which is the smallest tile
        smallest_tile = sorted(self.tile_list, key=lambda x: len(x.getTileAddress()), reverse=True)[0]
        return smallest_tile.getTileSize()

    def addNonContainedTile(self, nonContainedTile, convert_to_shortest_covering_tile_list=True):
        '''/**
         * Package-private method to add a code that has already been checked to NOT be contained yet.
         * @param newTile a full OpenGeoTile, the area of which will be added to this object's area
        */'''
        if not isinstance(nonContainedTile, OpenGeoTile):
            raise Exception("New TileArea must contain valid OpenGeoTile tiles")
        self.tile_list.append(nonContainedTile)
        if convert_to_shortest_covering_tile_list:
            self.tile_list = self.getShortestCoveringTileList()

    def addTile(self, newTile, convert_to_shortest_covering_tile_list=True):
        '''/**
         * Adds the area defined by the {@link OpenGeoTile} newTile to the area represented by this
         * object. Subsequent calls to {@link #contains(OpenGeoTile)} must return true for the
         * same tile address (e.g. "C9C9") as well as for all longer addresses (e.g. "C9C9XXXX")
         * @param newTile a full OpenGeoTile, the area of which will be added to this object's area
        */'''
        if not isinstance(newTile, OpenGeoTile):
            raise Exception("New TileArea must contain valid OpenGeoTile tiles")
        if not self.contains(newTile):
            self.addNonContainedTile(newTile, convert_to_shortest_covering_tile_list=convert_to_shortest_covering_tile_list)

    def addTileArea(self, newTileArea):
        '''/**
         * Adds the area defined by another TileArea to the area represented by this
         * object.
         * @param newTileArea another TileArea
         */'''
        for newTile in newTileArea.getShortestCoveringTileList():
            self.addTile(newTile, convert_to_shortest_covering_tile_list=False)
        self.tile_list = self.getShortestCoveringTileList()

    def containsPlusCode(self, plus_code):
        '''/**
         * Check if the area defined by {@link OpenGeoTile} code is completely inside this object's
         * area.
         * @param code a full {@link OpenLocationCode}, the area of which will be checked
         * @return true if the whole area of {@code code} is inside this object's area, false if not
        */'''
        return self.contains(OpenGeoTile(plus_code))

    def containsLatLong(self, lat, long):
        '''/**
         * Check if a location is inside this object's area.
         * @param latitude latitude value of the location to be checked
         * @param longitude longitude value of the location to be checked
         * @return true if inside, false if not
        */'''
        return self.contains(OpenGeoTile(lat=lat, long=long, tile_size=self.getSmallestTileSize()))

