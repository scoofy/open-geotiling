from openlocationcode import openlocationcode as olc
from OpenGeoTile import OpenGeoTile, TileSize
from operator import methodcaller
from collections.abc import Iterable
import pprint
pp = pprint.pformat

class TileArea():
    '''/**
     * An area defined by one or more {@link OpenGeoTile} tiles
    */'''
    def __init__(self, tile_or_tile_iterable):
        '''/**
         * default constructor
         */'''

        '''/**
         * Construct a TileArea from a list of tiles.
         * @param tiles an ArrayList of tiles that should be added to this object
        */'''
        if not isinstance(tile_or_tile_iterable, (Iterable, OpenGeoTile)):
            raise Exception("New TileArea must contain valid OpenGeoTile tiles")

        if isinstance(tile_or_tile_iterable, OpenGeoTile):
            tile_or_tile_iterable = set([tile_or_tile_iterable])

        self.tile_set = set()
        for newTile in tile_or_tile_iterable:
            self.addTile(newTile, convert_to_shortest_covering_tile_set=False)
        self.tile_set = self.getShortestCoveringTileSet()

    def getShortestCoveringTileSet(self):
        '''/**
         * Get a list of tiles that fully cover this TileArea as currently defined. Note that this is
         * not necessarily the same list that went into this object over time. In case of a contiguous
         * TileArea, it can also include tiles that never have been added.
         * @return an ArrayList of {@link OpenGeoTile} tiles which fully cover the area of this TileArea
        */'''
        # get address set list
        existing_address_list_unsorted = [tile.getTileAddress() for tile in self.tile_set]

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

        shortest_covering_tile_set = set()
        for parent, child_set in address_dict.items():
            for child in child_set:
                full_address = parent + child
                shortest_covering_tile_set.add(OpenGeoTile(code=full_address))
        return shortest_covering_tile_set

    def recursiveShortestCoveringTileDictBuilder(self, tile_address, address_dict):
            parent, child = tile_address[:-2],  tile_address[-2:]
            child_set = address_dict.get(parent, set())
            child_set.add(child)
            if len(child_set) == 20*20: # if full tile
                del address_dict[parent]
                return self.recursiveShortestCoveringTileDictBuilder(parent, address_dict)
            else:
                address_dict[parent] = child_set
                return address_dict

    def contains(self, tile):
        '''/**
         * Check if the area defined by {@link OpenGeoTile} tile is completely inside this object's
         * area.
         * @param tile an OpenGeoTile, the area of which will be checked
         * @return true if the whole area of {@code tile} is inside this object's area, false if not
        */'''
        for existing_tile in self.tile_set:
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
        smallest_tile = sorted(list(self.tile_set), key=lambda x: len(x.getTileAddress()), reverse=True)[0]
        return smallest_tile.getTileSize()

    def addNonContainedTile(self, nonContainedTile, convert_to_shortest_covering_tile_set=True):
        '''/**
         * Package-private method to add a code that has already been checked to NOT be contained yet.
         * @param newTile a full OpenGeoTile, the area of which will be added to this object's area
        */'''
        if not isinstance(nonContainedTile, OpenGeoTile):
            raise Exception("New TileArea must contain valid OpenGeoTile tiles")
        self.tile_set.add(nonContainedTile)
        if convert_to_shortest_covering_tile_set:
            self.tile_set = self.getShortestCoveringTileSet()

    def addTile(self, newTile, convert_to_shortest_covering_tile_set=True):
        '''/**
         * Adds the area defined by the {@link OpenGeoTile} newTile to the area represented by this
         * object. Subsequent calls to {@link #contains(OpenGeoTile)} must return true for the
         * same tile address (e.g. "C9C9") as well as for all longer addresses (e.g. "C9C9XXXX")
         * @param newTile a full OpenGeoTile, the area of which will be added to this object's area
        */'''
        if not isinstance(newTile, OpenGeoTile):
            raise Exception("New TileArea must contain valid OpenGeoTile tiles")
        if not self.contains(newTile):
            self.addNonContainedTile(newTile, convert_to_shortest_covering_tile_set=convert_to_shortest_covering_tile_set)

    def addTileArea(self, newTileArea):
        '''/**
         * Adds the area defined by another TileArea to the area represented by this
         * object.
         * @param newTileArea another TileArea
         */'''
        for newTile in newTileArea.tile_set:
            self.addTile(newTile, convert_to_shortest_covering_tile_set=False)
        self.tile_set = self.getShortestCoveringTileSet()

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

    def getEdgeTileSet(self):
        edge_addresses = set()
        contained_addresses = set()
        external_addresses = set()
        for tile in self.tile_set:
            tile_is_edge = False
            if tile.tile_size.getCodeLength() != TileSize.PINPOINT.getCodeLength():
                border_subtile_set = tile.returnSetOfBorderSubtiles()
            else:
                border_subtile_set = set([tile])
            for subtile in border_subtile_set:
                if not tile_is_edge:
                    neighbors = subtile.getNeighbors()
                    for neighbor in neighbors:
                        if not tile_is_edge:
                            if neighbor.getTileAddress() in contained_addresses:
                                continue
                            elif self.contains(neighbor):
                                contained_addresses.add(neighbor.getTileAddress())
                                continue
                            elif neighbor.getTileAddress() in external_addresses:
                                edge_addresses.add(tile.getTileAddress())
                                tile_is_edge = True
                                break
                            elif not self.contains(neighbor):
                                external_addresses.add(neighbor.getTileAddress())
                                edge_addresses.add(tile.getTileAddress())
                                tile_is_edge = True
                                break
        edge_tile_set = set()
        for tile in self.tile_set:
            if not tile in edge_tile_set:
                for address in edge_addresses:
                    if address.startswith(tile.getTileAddress()):
                        edge_tile_set.add(tile)
                        break
        return edge_tile_set

    def expandTileArea(self, tile_size, num_of_tiles=1):
        for i in range(num_of_tiles):
            new_area = SimpleTileArea()
            print('empty:', new_area.tile_set)
            edge_tile_set = self.getEdgeTileSet()
            print('len edge_tile_set:', len(edge_tile_set))
            for tile in edge_tile_set:
                print('tile:', tile.getTileAddress())
                neighbors = tile.getNeighbors()
                for neighbor in neighbors:
                    if not self.contains(neighbor) and not new_area.contains(neighbor):
                        print('neighbor:', neighbor.getTileAddress())
                        if neighbor.tile_size == tile_size:
                            if not self.contains(neighbor):
                                ''' new_area.contains(neighbor) in add algo '''
                                new_area.addTile(neighbor)
                        else:
                            direction = neighbor.getEightPointDirectionOfNeighbor(tile)
                            print(
                                '\nneighbor:', neighbor.getTileAddress(),
                                '\nto tile:', tile.getTileAddress(),
                                f'\n{direction}'
                            )
                            neighbor_subtiles = neighbor.returnSetOfBorderSubtiles(desired_tile_size=tile_size, eight_point_direction=direction)
                            print('len neighbor subs:', len(neighbor_subtiles))
                            for subtile in neighbor_subtiles:
                                if not self.contains(neighbor):
                                    ''' new_area.contains(neighbor) in add algo '''
                                    new_area.addTile(subtile)
            self.addTileArea(new_area)



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
    def __init__(self, tile_set=set()):
        self.smallestTileSize = TileSize.GLOBAL
        super().__init__(tile_set)


    def addNonContainedTile(self, newTile, convert_to_shortest_covering_tile_set=False):
        self.tile_set.add(newTile)
        if newTile.getTileSize().getCodeLength() > self.smallestTileSize.getCodeLength():
            self.smallestTileSize = newTile.getTileSize()

    def getSmallestTileSize(self):
        return self.smallestTileSize


    def contains(self, tile):
        for memberTile in self.tile_set:
            if memberTile.contains(tile):
                return True
        return False

    def getShortestCoveringTileSet(self):
        return self.tile_set






















