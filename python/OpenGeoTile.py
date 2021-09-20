from openlocationcode import openlocationcode as olc
from enum import Enum
import math, re

class TileSize(Enum):
    ''' An area of 20° x 20°. The side length of this tile varies with its location on the globe,
        but can be up to approximately 2200km. Tile addresses will be 2 characters long.'''
    GLOBAL = (2, 20.0)

    ''' An area of 1° x 1°. The side length of this tile varies with its location on the globe,
        but can be up to approximately 110km. Tile addresses will be 4 characters long.'''
    REGION = (4, 1.0)

    ''' An area of 0.05° x 0.05°. The side length of this tile varies with its location on the
        globe, but can be up to approximately 5.5km. Tile addresses will be 6 characters long.'''
    DISTRICT = (6, 0.05)

    ''' An area of 0.0025° x 0.0025°. The side length of this tile varies with its location on
        the globe, but can be up to approximately 275m.
        Tile addresses will be 8 characters long.'''
    NEIGHBORHOOD = (8, 0.0025)

    ''' An area of 0.000125° x 0.000125°. The side length of this tile varies with its location
        on the globe, but can be up to approximately 14m.
        Tile addresses will be 10 characters long.'''
    PINPOINT = (10, 0.000125)

    def __init__(self, code_length, coordinate_increment):
        self.code_length = code_length
        self.coordinate_increment = coordinate_increment

    def getCodeLength(self):
        '''get 0th value'''
        return self.code_length

    def getCoordinateIncrement(self):
        '''get 1th value'''
        return self.coordinate_increment

# Copy from OpenLocationCode.java
# A separator used to break the code into two parts to aid memorability.
SEPARATOR = '+'

# Copy from OpenLocationCode.java
# The character used to pad codes.
PADDING_CHARACTER = '0'

PADDING_2 = "00"
PADDING_4 = "0000"
PADDING_6 = "000000"
CODE_ALPHABET = olc.CODE_ALPHABET_



def is_padded(plus_code):
    return plus_code.find(PADDING_CHARACTER) != -1
def is_tile_address(plus_code):
    return plus_code.find(SEPARATOR) == -1
def return_code_of_tile_size(too_precise_plus_code, desired_tile_size):
    code = too_precise_plus_code
    if not is_tile_address(code):
        code = code.replace(SEPARATOR, '')
    if is_padded(code):
        if code.find(PADDING_CHARACTER) < desired_tile_size.getCodeLength():
            raise Exception("OLC padding larger than allowed by desired_tile_size")
    code_address = code[:desired_tile_size.getCodeLength()]
    full_length = TileSize.PINPOINT.getCodeLength()
    code = code_address + ("0" * (full_length - len(code_address)))
    if desired_tile_size == TileSize.PINPOINT:
        code = code[:-2] + SEPARATOR + code[-2:]
    else:
        code = code[:-2] + SEPARATOR
    return code

def return_set_of_subaddresses(set_of_addresses):
    BASE_20_SET = {x+y for x in CODE_ALPHABET for y in CODE_ALPHABET}
    for address in set_of_addresses:
        if len(address) == TileSize.PINPOINT.getCodeLength():
            ''' address already minimum possible size '''
            return None
    return {address+base for address in set_of_addresses for base in BASE_20_SET}

class OpenGeoTile():
    '''
    /**
     * A wrapper around an {@code OpenLocationCode} object, focusing on the area identified by a prefix
     * of the given OpenLocationCode.
     *
     * Using this wrapper class allows to determine whether two locations are in the same or adjacent
     * "tiles", to determine all neighboring tiles of a given one, to calculate a distance in tiles etc.
     *
     * Open Location Code is a technology developed by Google and licensed under the Apache License 2.0.
     * For more information, see https://github.com/google/open-location-code
     *
     * @author Andreas Bartels
     * @version 0.1.0
     */

        Ported by scoofy on 08.31.21
    '''
    def __init__(self,
                 code=None,
                 tile_size=None,
                 lat=None,
                 long=None,
                 ):
        if not (code or (code and tile_size) or (lat and long)):
            raise Exception("Invalid OpenGeoTile constructor arguments")
        if lat and long:
            self.constructTileFromLatLong(lat, long, tile_size)
        elif code and tile_size:
            self.constructTileFromCodeAndSize(code, tile_size)
        elif code:
            if is_tile_address(code):
                self.constructTileFromTileAddress(code)
            else:
                self.constructTileFromCode(code)
        self.tile_address = self.code.replace(SEPARATOR, "")[0: self.tile_size.getCodeLength()]


    def constructTileFromCode(self, plus_code):
        '''/**
        * Creates a new OpenGeoTile from an existing
        * {@link com.google.openlocationcode.OpenLocationCode}.
        * @param olc OpenLocationCode for the current location. This can be a padded code, in which
        *            case the resulting OpenGeoTile will have a larger TileSize.
        * @throws IllegalArgumentException if olc is not a full code
        */'''
        if not olc.isFull(plus_code):
            raise Exception("Only full OLC supported. Use olc.recoverNearest().")

        self.code = plus_code.upper()

        if is_padded(plus_code):
            code_length = plus_code.find(PADDING_CHARACTER)
        else:
            code_length = min(len(plus_code)-1, 10)

        if code_length   == TileSize.GLOBAL.getCodeLength():
            self.tile_size = TileSize.GLOBAL

        elif code_length == TileSize.REGION.getCodeLength():
            self.tile_size = TileSize.REGION

        elif code_length == TileSize.DISTRICT.getCodeLength():
            self.tile_size = TileSize.DISTRICT

        elif code_length == TileSize.NEIGHBORHOOD.getCodeLength():
            self.tile_size = TileSize.NEIGHBORHOOD

        elif code_length == TileSize.PINPOINT.getCodeLength():
            self.tile_size = TileSize.PINPOINT

        else:
            raise Exception("Too precise, sort this later")


    def constructTileFromCodeAndSize(self, plus_code, tile_size):
        '''
        Creates a new OpenGeoTile from an existing
        {@link com.google.openlocationcode.OpenLocationCode}.
        @param olc OpenLocationCode for the current location
        @param tile_size tile size to use for this OpenGeoTile
        @throws IllegalArgumentException when trying to pass a short (non-full) OLC, or if OLC has
        too much padding for given tile_size
        '''
        if not olc.isFull(plus_code):
            raise Exception("Only full OLC supported. Use recover().")
        modified_plus_code = return_code_of_tile_size(plus_code, tile_size)


        self.code = modified_plus_code.upper()
        self.tile_size = tile_size

    def constructTileFromLatLong(self, lat: float, long: float, tile_size=None):
        '''/**
        * Creates a new OpenGeoTile from lat/long coordinates.
        * @param latitude latitude of the location
        * @param longitude longitude of the location
        * @param tile_size tile size to use for this OpenGeoTile
        * @throws IllegalArgumentException passed through from
        *         {@link OpenLocationCode#OpenLocationCode(double, double, int)}
        */'''
        if not tile_size:
            tile_size = TileSize.PINPOINT
        self.code = olc.encode(lat, long, tile_size.getCodeLength()).upper()
        self.tile_size = tile_size

    def constructTileFromTileAddress(self, tileAddress):
        '''/**
         * Creates a new OpenGeoTile from a tile address.
         * @param tileAddress a tile address is a [2/4/6/8/10]-character string that corresponds to a
         *                     valid {@link com.google.openlocationcode.OpenLocationCode} after removing
         *                     '+' and an additional number of trailing characters; tile size is
         *                     determined by the length of this address
         * @throws IllegalArgumentException passed through from
         *         {@link OpenLocationCode#OpenLocationCode(String)} or thrown if tileAddress is of
         *         invalid length
        */'''
        detectedTileSize = None
        olcBuilder = ""

        if len(tileAddress) == TileSize.GLOBAL.getCodeLength():
            detectedTileSize = TileSize.GLOBAL
            olcBuilder += tileAddress + PADDING_6 + SEPARATOR

        if len(tileAddress) == TileSize.REGION.getCodeLength():
            detectedTileSize = TileSize.REGION
            olcBuilder += tileAddress + PADDING_4 + SEPARATOR

        if len(tileAddress) == TileSize.DISTRICT.getCodeLength():
            detectedTileSize = TileSize.DISTRICT
            olcBuilder += tileAddress + PADDING_2 + SEPARATOR

        if len(tileAddress) == TileSize.NEIGHBORHOOD.getCodeLength():
            detectedTileSize = TileSize.NEIGHBORHOOD
            olcBuilder += tileAddress + SEPARATOR

        if len(tileAddress) == TileSize.PINPOINT.getCodeLength():
            detectedTileSize = TileSize.PINPOINT
            olcBuilder += tileAddress[0:8] + SEPARATOR + tileAddress[8:10]

        if detectedTileSize == None:
            print(tileAddress)
            raise Exception("Invalid tile address")

        self.tile_size = detectedTileSize
        self.code = olcBuilder.upper()

    def getWrappedOpenLocationCode(self):
        # this code is effectively redundant as python has no wrapping
        '''/**
        * The exact {@link com.google.openlocationcode.OpenLocationCode} wrapped by this OpenGeoTile.
        * For the plus code of the whole tile, see {@link #getTileOpenLocationCode()}.
        * @return the exact plus code wrapped by this OpenGeoTile
        */'''
        return self.code

    def returnCode(self):
        return self.code

    def getTileSize(self):
        '''/**
        * Get the {@link TileSize} of this OpenGeoTile.
        * @return the {@link TileSize} of this OpenGeoTile
        */'''
        return self.tile_size

    def getTileAddress(self):
        '''/**
        * A tile address is a string of length 2, 4, 6, 8, or 10, which corresponds to a valid
        * {@link com.google.openlocationcode.OpenLocationCode} after padding with an appropriate
        * number of '0' and '+' characters. Example: Address "CVXW" corresponds to OLC "CVXW0000+"
        * @return the tile address of this OpenGeoTile;
         */'''
        return self.tile_address

    def getTileAddressPrefix(self):
        '''/**
        * The prefix of a tile address is the address of the next biggest tile at this location.
        * @return this tile's address with the final two characters removed. In case of a GLOBAL tile,
        * returns the empty string.
        */'''
        if self.tile_size == TileSize.GLOBAL:
            return ""
        else:
            return self.getTileAddress()[0: self.tile_size.getCodeLength()-2]
    def getParentTileAddress(self):
        return self.getTileAddressPrefix()

    def getTileOpenLocationCode(self):
        # this code is redundant
        '''/**
        * The full {@link com.google.openlocationcode.OpenLocationCode} for this tile. Other than
        * {@link #getWrappedOpenLocationCode()}, this will return a full plus code for the whole tile.
        * @return a plus code for the whole tile, probably padded with '0' characters
        */'''
        return self.getWrappedOpenLocationCode()

    def getNeighbors(self, eight_point_direction=None):
        '''/**
        * Get an array of the typically 8  neighboring tiles of the same size.
        * @return an array of the typically 8 neighboring tiles of the same size;
        * may return less than 8 neighbors for tiles near the poles.
        */'''

        # deltas = [20.0, 1.0, 0.05, 0.0025, 0.000125]
        delta = self.getTileSize().getCoordinateIncrement()

        code_area = olc.decode(self.code)
        latitude = code_area.latitudeCenter
        longitude = code_area.longitudeCenter

        '''directions_list included to keep ordered data'''
        directions_list = ["NW", "N", "NE", "E", "SE", "S", "SW", "W"]
        direction_dict = {
            "NW": [+1, -1], "N": [+1, 0],   "NE": [+1, +1],
             "W": [ 0, -1],                  "E": [ 0, +1],
            "SW": [-1, -1], "S": [-1, 0],   "SE": [-1, +1],
        }

        #lat_diff =  [+1, +1, +1,  0, -1, -1, -1,  0]
        #long_diff = [-1,  0, +1, +1, +1,  0, -1, -1]

        if not type(eight_point_direction) in [type(None), list, str]:
            raise Exception("eight_point_direction must be of type list or str")
        if eight_point_direction is None:
            directions = directions_list
        elif isinstance(eight_point_direction, str):
            directions = []
            if eight_point_direction.upper() in directions_list:
                directions.append(eight_point_direction.upper())
        else:
            ''' this list construction keeps directions in the order above '''
            uppercase_input_directions = [d.upper() for d in eight_point_direction]
            directions = [direction for direction in directions_list if direction in uppercase_input_directions]

        neighbors = set()
        for direction in directions:
            lat_diff, long_diff = direction_dict.get(direction)
            ''' //OLC constructor clips and normalizes,
                //so we don't have to deal with invalid lat/long values directly'''
            neighborLatitude  = latitude  + (delta * lat_diff)
            neighborLongitude = longitude + (delta * long_diff)

            new_OpenGeoTile = OpenGeoTile(lat=neighborLatitude, long=neighborLongitude, tile_size=self.getTileSize())
            if not self.isSameTile(new_OpenGeoTile):
                '''//don't add tiles that are the same as this one due to clipping near the poles'''
                neighbors.add(new_OpenGeoTile)

        return neighbors

    def isSameTile(self, potentialSameTile):
        '''/**
        * Check if a tile describes the same area as this one.
        * @param potentialSameTile the OpenGeoTile to check
        * @return true if tile sizes and addresses are the same; false if not
        */'''
        if potentialSameTile.getTileSize() != self.getTileSize():
            return False
        return potentialSameTile.getTileAddress() == self.getTileAddress()

    def isNeighbor(self, potentialNeighbor):
        '''/**
        * Check if a tile is neighboring this one.
        * @param potentialNeighbor the OpenGeoTile to check
        * @return true if this and potentialNeighbor are adjacent (8-neighborhood);
        *         false if not
        */'''
        if potentialNeighbor.getTileSize() == self.getTileSize():
            '''//avoid iterating over neighbors for same tile'''
            if self.isSameTile(potentialNeighbor):
                return False

            neighbors = self.getNeighbors()
            for neighbor in neighbors:
                if potentialNeighbor.isSameTile(neighbor):
                    return True
            return False
        else:
            '''//tiles of different size are adjacent if at least one neighbor of the smaller tile,
            //but not the smaller tile itself, is contained within the bigger tile'''
            if potentialNeighbor.getTileSize().getCodeLength() > self.tile_size.getCodeLength():
                smallerTile = potentialNeighbor
                biggerTile = self
            else:
                smallerTile = self
                biggerTile = potentialNeighbor

            if biggerTile.contains(smallerTile):
                return False

            neighbors = smallerTile.getNeighbors()
            for neighbor in neighbors:
                if biggerTile.contains(neighbor):
                    return True
            return False

    def contains(self, potentialMember):
        '''/**
        * Check if this tile contains another one.
        * @param potentialMember the OpenGeoTile to check
        * @return true if the area potentialMember falls within the area of this tile, including cases
        * where both are the same; false if not
        */'''
        # //if A contains B, then B's address has A's address as a prefix
        return potentialMember.getTileAddress().startswith(self.getTileAddress())

    def getManhattanTileDistanceTo(self, otherTile):
        '''/**
        * Calculates the Manhattan (city block) distance between this and another tile of the same size.
        * @param otherTile another tile of the same size as this one
        * @return an integer value corresponding to the number of tiles of the given size that need to
        * be traversed getting from one to the other tile
        * @throws IllegalArgumentException thrown if otherTile has different {@link TileSize}
        */'''
        if otherTile.getTileSize() != self.getTileSize():
            raise Exception("Tile sizes don't match")

        return self.getLatitudinalTileDistance(otherTile, True) + self.getLongitudinalTileDistance(otherTile, True)

    def getChebyshevTileDistanceTo(self, otherTile):
        '''/**
        * Calculates the Chebyshev (chessboard) distance between this and another tile of the same size.
        * @param otherTile another tile of the same size as this one
        * @return an integer value corresponding to the number of tiles of the given size that need to
        * be traversed getting from one to the other tile
        * @throws IllegalArgumentException thrown if otherTile has different {@link TileSize}
        */'''
        if otherTile.getTileSize() != self.getTileSize():
            raise Exception("Tile sizes don't match")

        return max(self.getLatitudinalTileDistance(otherTile, True),
                   self.getLongitudinalTileDistance(otherTile, True))

    def getDirection(self, otherTile):
        '''/**
        * Returns the approximate direction of the other tile relative to this. The return value can
        * have a large margin of error, especially for big or far away tiles, so this should only be
        * interpreted as a very rough approximation and used as such.
        * @param otherTile another tile of the same size as this one
        * @return an angle in radians, 0 being an eastward direction, +/- PI being westward direction
        * @throws IllegalArgumentException thrown if otherTile has different {@link TileSize}
        */'''
        if otherTile.getTileSize() != self.getTileSize():
            raise Exception("Tile sizes don't match")

        xDiff = int(self.getLongitudinalTileDistance(otherTile, False))
        yDiff = int(self.getLatitudinalTileDistance(otherTile, False))
        return math.atan2(yDiff, xDiff)

    def getEightPointDirectionOfNeighbor(self, neighborTile):
        ''' returns neighbor's direction, to assist in expanding tile areas '''
        if not self.isNeighbor(neighborTile):
            raise Exception("neighborTile must be neighbor")
        if neighborTile.getTileSize() != self.getTileSize():
            raise Exception("Tile sizes don't match")
        self_tile_x = self.getTileAddress()[-2]
        self_tile_y = self.getTileAddress()[-1]
        other_tile_x = neighborTile.getTileAddress()[-2]
        other_tile_y = neighborTile.getTileAddress()[-1]

        direction = ""
        north_south = None

        if self_tile_x != other_tile_x:
            ''' one tile is above the other '''
            if CODE_ALPHABET.find(self_tile_x) in [0, len(CODE_ALPHABET)-1] and CODE_ALPHABET.find(other_tile_x) in [0, len(CODE_ALPHABET)-1]:
                ''' ajacent parent tiles '''
                if CODE_ALPHABET.find(other_tile_x) == 0:
                    ''' other tile is above -> neighborTile is north '''
                    direction = direction + 'N'
                else:
                    direction = direction + 'S'
            else:
                if CODE_ALPHABET.find(self_tile_x) < CODE_ALPHABET.find(other_tile_x):
                    ''' other tile is above -> neighborTile is north '''
                    direction = direction + 'N'
                else:
                    ''' other tile is below -> neighborTile is south '''
                    direction = direction + 'S'
        if self_tile_y != other_tile_y:
            ''' one tile is above the other '''
            if CODE_ALPHABET.find(self_tile_y) in [0, len(CODE_ALPHABET)-1] and CODE_ALPHABET.find(other_tile_y) in [0, len(CODE_ALPHABET)-1]:
                ''' ajacent parent tiles '''
                if CODE_ALPHABET.find(other_tile_y) == 0:
                    ''' other tile is right -> neighborTile is east '''
                    direction = direction + 'E'
                else:
                    ''' other tile is left -> neighborTile is west '''
                    direction = direction + 'W'
            else:
                if CODE_ALPHABET.find(self_tile_y) < CODE_ALPHABET.find(other_tile_y):
                    ''' other tile is right -> neighborTile is east '''
                    direction = direction + 'E'
                else:
                    ''' other tile is left -> neighborTile is west '''
                    direction = direction + 'W'
        return direction


    def getCharacterIndex(self, c):
        '''//following definitions copied from OpenLocationCode.java'''
        index = "23456789CFGHJMPQRVWX".find(c.upper())
        if index == -1:
            raise Exception("Character does not exist in alphabet")
        return index

    def characterDistance(self, c1, c2):
        return self.getCharacterIndex(c1) - self.getCharacterIndex(c2)

    def getLatitudinalTileDistance(self, otherTile, absolute_value_bool):
        if otherTile.getTileSize() != self.getTileSize():
            raise Exception("Tile sizes don't match")

        numIterations = self.tile_size.getCodeLength()/2 #1..5
        tileDistance = 0
        for i in range(int(numIterations)):
            tileDistance *= 20
            c1 = self.getTileAddress()[i*2]
            c2 = otherTile.getTileAddress()[i*2]
            tileDistance += self.characterDistance(c1,c2)

        if absolute_value_bool:
            return abs(tileDistance)
        return tileDistance


    def getLongitudinalTileDistance(self, otherTile, absolute_value_bool):
        if otherTile.getTileSize() != self.getTileSize():
            raise Exception("Tile sizes don't match")

        numIterations = self.tile_size.getCodeLength()/2 #; //1..5
        tileDistance = 0
        for i in range(int(numIterations)):
            tileDistance *= 20
            c1 = self.getTileAddress()[i*2 + 1]
            c2 = otherTile.getTileAddress()[i*2 + 1]
            if i == 0:
                '''//for the first longitudinal value, we need to take care of wrapping - basically,
                   //if it's shorter to go the other way around, do so'''
                firstDiff = self.characterDistance(c1, c2)
                NUM_CHARACTERS_USED = 18 #; //360°/20° = 18
                if abs(firstDiff) > NUM_CHARACTERS_USED/2:
                    if firstDiff > 0:
                        firstDiff -= NUM_CHARACTERS_USED
                    else:
                        firstDiff += NUM_CHARACTERS_USED
                tileDistance += firstDiff
            else:
                tileDistance += self.characterDistance(c1, c2)

        if absolute_value_bool:
            return abs(tileDistance)
        return tileDistance

    def returnSetOfSubtiles(self, desired_tile_size=TileSize.PINPOINT):
        if self.tile_size.getCodeLength() == desired_tile_size.getCodeLength():
            ''' tile is desired size '''
            return self
        elif self.tile_size.getCodeLength() > desired_tile_size.getCodeLength():
            'desired_tile_size is too big'
            raise Exception("OLC padding larger than allowed by desired_tile_size")
        iterations_needed = desired_tile_size.getCodeLength()/2 - self.tile_size.getCodeLength()/2
        address_set = set([self.getTileAddress()])
        for i in range(int(iterations_needed)):
            address_set = return_set_of_subaddresses(address_set)
        tile_set = {OpenGeoTile(address) for address in address_set}
        return tile_set

    def returnSetOfBorderSubtiles(self, desired_tile_size=TileSize.PINPOINT, eight_point_direction=None):
        BASE_20_SET = {x+y for x in CODE_ALPHABET for y in CODE_ALPHABET}
        BASE_20_BORDER_SET = {x for x in BASE_20_SET if x[0] in ['2', 'X'] or x[1] in ['2', 'X']}
        NORTH_DIGITS = {x for x in BASE_20_BORDER_SET if x[0] == 'X'}
        EAST_DIGITS = {x for x in BASE_20_BORDER_SET if x[1] == 'X'}
        SOUTH_DIGITS = {x for x in BASE_20_BORDER_SET if x[0] == '2'}
        WEST_DIGITS = {x for x in BASE_20_BORDER_SET if x[1] == '2'}
        memoized_digit_dict = {
            "N1": NORTH_DIGITS,
            "E1": EAST_DIGITS,
            "S1": SOUTH_DIGITS,
            "W1": WEST_DIGITS,
        }


        address = self.getTileAddress()

        if len(address) == TileSize.PINPOINT.getCodeLength():
            ''' address already minimum possible size '''
            return None
        elif self.tile_size.getCodeLength() > desired_tile_size.getCodeLength():
            'desired_tile_size is too big'
            raise Exception("OLC padding larger than allowed by desired_tile_size")

        iterations_needed = int(desired_tile_size.getCodeLength()/2 - self.tile_size.getCodeLength()/2)

        north_set = set()
        east_set = set()
        south_set = set()
        west_set = set()

        if isinstance(eight_point_direction, str):
            eight_point_direction = eight_point_direction.upper()

        set_of_border_subaddresses = set()
        if eight_point_direction is None:
            ''' all borders '''
            ''' traveling salesman problem '''
            ''' let's do it once, and try to reduce by swaping digits '''
            all_border_set = memoized_digit_dict.get(f"A{iterations_needed}")
            if not all_border_set:
                north_base_set = memoized_digit_dict.get(f"N{iterations_needed}")
                if not north_base_set:
                    self.memoizeDigitDict("N", iterations_needed)


                north_set = memoized_digit_dict.get(f"N{iterations_needed}")
                east_set = memoized_digit_dict.get(f"E{iterations_needed}", set())
                south_set = memoized_digit_dict.get(f"S{iterations_needed}", set())
                west_set = memoized_digit_dict.get(f"W{iterations_needed}", set())
                east_exists = east_set != set()
                south_exists = south_set != set()
                west_exists = west_set != set()
                for base in north_set:
                    east_base = ""
                    south_base = ""
                    west_base = ""
                    base_tuple_list = re.findall('..', base)
                    ''' north will be   Xd
                        east            dX
                        south           2d
                        west            d2'''
                    for n_tuple in base_tuple_list:
                        relevant_digit = n_tuple[1]
                        if not east_exists:
                            east_base += relevant_digit + "X"
                        if not south_exists:
                            south_base += "2" + relevant_digit
                        if not west_exists:
                            west_base += relevant_digit + "2"
                    if not east_exists:
                        east_set.add(east_base)
                    if not south_exists:
                        south_set.add(south_base)
                    if not west_exists:
                        west_set.add(west_base)
                memoized_digit_dict[f"E{iterations_needed}"] = east_set
                memoized_digit_dict[f"S{iterations_needed}"] = south_set
                memoized_digit_dict[f"W{iterations_needed}"] = west_set
                all_border_set = north_set | east_set | south_set | west_set
                memoized_digit_dict[f"A{iterations_needed}"] = all_border_set
            return {OpenGeoTile(address+base) for base in all_border_set}

        elif len(eight_point_direction) == 1:
            ''' North, South, East, or West '''
            base_set = memoized_digit_dict.get(f"{eight_point_direction}{iterations_needed}")
            if not base_set:
                self.memoizeDigitDict(eight_point_direction, iterations_needed)

            base_set = memoized_digit_dict.get(f'{eight_point_direction}{iterations_needed}')
            return {OpenGeoTile(address + base) for base in base_set}
        elif len(eight_point_direction) == 2:
            ''' NW, NE, SW, SE... should return only one tile'''
            ordinal_digit_dict = {
                'NW': 'X2',
                'NE': 'XX',
                'SE': '2X',
                'SW': '22'
            }
            base = ''
            for i in range(iterations_needed):
                base += ordinal_digit_dict.get(eight_point_direction)
            return {OpenGeoTile(address + base)}


    def memoizeDigitDict(self, eight_point_direction, iterations_needed):
        BASE_20_SET = {x+y for x in CODE_ALPHABET for y in CODE_ALPHABET}
        BASE_20_BORDER_SET = {x for x in BASE_20_SET if x[0] in ['2', 'X'] or x[1] in ['2', 'X']}
        NORTH_DIGITS = {x for x in BASE_20_BORDER_SET if x[0] == 'X'}
        EAST_DIGITS = {x for x in BASE_20_BORDER_SET if x[1] == 'X'}
        SOUTH_DIGITS = {x for x in BASE_20_BORDER_SET if x[0] == '2'}
        WEST_DIGITS = {x for x in BASE_20_BORDER_SET if x[1] == '2'}
        memoized_digit_dict = {
            "N1": NORTH_DIGITS,
            "E1": EAST_DIGITS,
            "S1": SOUTH_DIGITS,
            "W1": WEST_DIGITS,
        }


        base_set = memoized_digit_dict.get(f"{eight_point_direction}{iterations_needed}")
        if not base_set:
            quickest_i = 0
            for i in reversed(range(iterations_needed)):
                if memoized_digit_dict.get(f"{eight_point_direction}{i + 1}"):
                    quickest_i = i
                    break
            for i in range(quickest_i, iterations_needed):
                existing_bases = memoized_digit_dict.get(f"{eight_point_direction}{i + 1}")
                next_set = {existing_base + base for existing_base in existing_bases for base in memoized_digit_dict.get(f"{eight_point_direction}1")}
                memoized_digit_dict[f"{eight_point_direction}{i + 2}"] = next_set



















