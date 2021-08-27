from openlocationcode import openlocationcode as olc
from enum import Enum

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
        return self.code_length

    def getCoordinateIncrement(self):
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

def isPadded(code):
    return code.find(PADDING_CHARACTER) != -1
def isTileAddress(code):
    return code.find(SEPARATOR) == -1

def OpenGeoTile(code):
    def __init__(self,
                 code=None,
                 tileSize=None,
                 lat=None,
                 long=None,
                 ):
        if lat and long:
            self.constructTileFromLatLong(lat, long, tileSize)
        elif code and tileSize:
            self.constructTileFromCodeAndSize(code, tileSize)
        elif code:
            if isTileAddress(code):
                self.constructTileFromTileAddress(code)
            else:
                self.constructTileFromCode(code)


    def constructTileFromCode(self, code):
        '''/**
        * Creates a new OpenGeoTile from an existing
        * {@link com.google.openlocationcode.OpenLocationCode}.
        * @param olc OpenLocationCode for the current location. This can be a padded code, in which
        *            case the resulting OpenGeoTile will have a larger TileSize.
        * @throws IllegalArgumentException if olc is not a full code
        */'''
        if not olc.isFull(code):
            raise Exception("Only full OLC supported. Use olc.recoverNearest().")

        self.code = code

        if isPadded(code):
            code_length = code.find(PADDING_CHARACTER)
        else:
            code_length = min(len(code)-1, 10)

        if code_length == TileSize.GLOBAL.getCodeLength():
            self.tileSize = TileSize.GLOBAL

        elif code_length==TileSize.REGION.getCodeLength():
            self.tileSize = TileSize.REGION

        elif code_length==TileSize.DISTRICT.getCodeLength():
            self.tileSize = TileSize.DISTRICT

        elif code_length==TileSize.NEIGHBORHOOD.getCodeLength():
            self.tileSize = TileSize.NEIGHBORHOOD

        elif code_length==TileSize.PINPOINT.getCodeLength():
            self.tileSize = TileSize.PINPOINT

        else:
            raise Exception("Too precise, sort this later")


    def constructTileFromCodeAndSize(self, code, tileSize)
        '''
        Creates a new OpenGeoTile from an existing
        {@link com.google.openlocationcode.OpenLocationCode}.
        @param olc OpenLocationCode for the current location
        @param tileSize tile size to use for this OpenGeoTile
        @throws IllegalArgumentException when trying to pass a short (non-full) OLC, or if OLC has
        too much padding for given tileSize
        '''
        if not olc.isFull(code):
            raise Exception("Only full OLC supported. Use recover().")

        if isPadded(code):
            if code.find(PADDING_CHARACTER) < tileSize.getCodeLength():
                raise Exception("OLC padding larger than allowed by tileSize")

        self.code = code
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
        self.code =  olc.encode(lat, long, tileSize.getCodeLength())
        self.tileSize = tileSize

    def constructTileFromTileAddress(self, tileAddress)
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
            olcBuilder += tileAddress[0:8] + SEPARATOR + tileAddress[8,10]

        if detectedTileSize == None
            raise Exception("Invalid tile address")

        self.tileSize = detectedTileSize
        self.code = olcBuilder


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