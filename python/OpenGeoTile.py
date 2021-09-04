from openlocationcode import openlocationcode as olc
from enum import Enum
import math

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

def isPadded(plus_code):
    return plus_code.find(PADDING_CHARACTER) != -1
def isTileAddress(plus_code):
    return plus_code.find(SEPARATOR) == -1

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
                 tileSize=None,
                 lat=None,
                 long=None,
                 ):
        if not (code or (code and tileSize) or (lat and long)):
            raise Exception("Invalid OpenGeoTile constructor arguments")
        if lat and long:
            self.constructTileFromLatLong(lat, long, tileSize)
        elif code and tileSize:
            self.constructTileFromCodeAndSize(code, tileSize)
        elif code:
            if isTileAddress(code):
                self.constructTileFromTileAddress(code)
            else:
                self.constructTileFromCode(code)


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

        if isPadded(plus_code):
            code_length = plus_code.find(PADDING_CHARACTER)
        else:
            code_length = min(len(plus_code)-1, 10)

        if code_length   == TileSize.GLOBAL.getCodeLength():
            self.tileSize = TileSize.GLOBAL

        elif code_length == TileSize.REGION.getCodeLength():
            self.tileSize = TileSize.REGION

        elif code_length == TileSize.DISTRICT.getCodeLength():
            self.tileSize = TileSize.DISTRICT

        elif code_length == TileSize.NEIGHBORHOOD.getCodeLength():
            self.tileSize = TileSize.NEIGHBORHOOD

        elif code_length == TileSize.PINPOINT.getCodeLength():
            self.tileSize = TileSize.PINPOINT

        else:
            raise Exception("Too precise, sort this later")


    def constructTileFromCodeAndSize(self, plus_code, tileSize):
        '''
        Creates a new OpenGeoTile from an existing
        {@link com.google.openlocationcode.OpenLocationCode}.
        @param olc OpenLocationCode for the current location
        @param tileSize tile size to use for this OpenGeoTile
        @throws IllegalArgumentException when trying to pass a short (non-full) OLC, or if OLC has
        too much padding for given tileSize
        '''
        if not olc.isFull(plus_code):
            raise Exception("Only full OLC supported. Use recover().")

        if isPadded(plus_code):
            if plus_code.find(PADDING_CHARACTER) < tileSize.getCodeLength():
                raise Exception("OLC padding larger than allowed by tileSize")

        self.code = plus_code.upper()
        self.tileSize = tileSize

    def constructTileFromLatLong(self, lat: float, long: float, tileSize=None):
        '''/**
        * Creates a new OpenGeoTile from lat/long coordinates.
        * @param latitude latitude of the location
        * @param longitude longitude of the location
        * @param tileSize tile size to use for this OpenGeoTile
        * @throws IllegalArgumentException passed through from
        *         {@link OpenLocationCode#OpenLocationCode(double, double, int)}
        */'''
        if not tileSize:
            tileSize = TileSize.PINPOINT
        self.code = olc.encode(lat, long, tileSize.getCodeLength()).upper()
        self.tileSize = tileSize

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
            raise Exception("Invalid tile address")

        self.tileSize = detectedTileSize
        self.code = olcBuilder.upper()


    def getWrappedOpenLocationCode(self):
        # this code is effectively redundant as python has no wrapping
        '''/**
        * The exact {@link com.google.openlocationcode.OpenLocationCode} wrapped by this OpenGeoTile.
        * For the plus code of the whole tile, see {@link #getTileOpenLocationCode()}.
        * @return the exact plus code wrapped by this OpenGeoTile
        */'''
        return self.code

    def getTileSize(self):
        '''/**
        * Get the {@link TileSize} of this OpenGeoTile.
        * @return the {@link TileSize} of this OpenGeoTile
        */'''
        return self.tileSize

    def getTileAddress(self):
        '''/**
        * A tile address is a string of length 2, 4, 6, 8, or 10, which corresponds to a valid
        * {@link com.google.openlocationcode.OpenLocationCode} after padding with an appropriate
        * number of '0' and '+' characters. Example: Address "CVXW" corresponds to OLC "CVXW0000+"
        * @return the tile address of this OpenGeoTile;
         */'''
        intermediate = self.code.replace(SEPARATOR, "")
        return intermediate[0: self.tileSize.getCodeLength()]

    def getTileAddressPrefix(self):
        '''/**
        * The prefix of a tile address is the address of the next biggest tile at this location.
        * @return this tile's address with the final two characters removed. In case of a GLOBAL tile,
        * returns the empty string.
        */'''
        if self.tileSize == TileSize.GLOBAL:
            return ""
        else:
            return self.getTileAddress()[0: self.tileSize.getCodeLength()-2]

    def getTileOpenLocationCode(self):
        # this code is redundant
        '''/**
        * The full {@link com.google.openlocationcode.OpenLocationCode} for this tile. Other than
        * {@link #getWrappedOpenLocationCode()}, this will return a full plus code for the whole tile.
        * @return a plus code for the whole tile, probably padded with '0' characters
        */'''
        intermediate = OpenGeoTile(self.getTileAddress())
        return intermediate.getWrappedOpenLocationCode()
    def getNeighbors(self):
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

        lat_diff = [+1,+1,+1, 0,-1,-1,-1, 0]
        long_diff = [-1, 0,+1,+1,+1, 0,-1,-1]

        neighbors = []

        for i in range(8):
            ''' //OLC constructor clips and normalizes,
                //so we don't have to deal with invalid lat/long values directly'''
            neighborLatitude  = latitude  + (delta * lat_diff[i])
            neighborLongitude = longitude + (delta * long_diff[i])

            new_OpenGeoTile = OpenGeoTile(lat=neighborLatitude, long=neighborLongitude, tileSize=self.getTileSize())
            if not self.isSameTile(new_OpenGeoTile):
                '''//don't add tiles that are the same as this one due to clipping near the poles'''
                neighbors.append(new_OpenGeoTile)

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
            if potentialNeighbor.getTileSize().getCodeLength() > self.tileSize.getCodeLength():
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

        numIterations = self.tileSize.getCodeLength()/2 #1..5
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

        numIterations = self.tileSize.getCodeLength()/2 #; //1..5
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

