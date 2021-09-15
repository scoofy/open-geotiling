from openlocationcode import openlocationcode as olc
from TileArea import TileArea
from OpenGeoTile import OpenGeoTile, TileSize
import pytest

CODE_ALPHABET = olc.CODE_ALPHABET_
BASE_20_SET = {x+y for x in CODE_ALPHABET for y in CODE_ALPHABET}
BASE_20_BORDER_SET = {x for x in BASE_20_SET if x[0] in ['2', 'X'] or x[1] in ['2', 'X']}
NORTH_DIGITS = {x for x in BASE_20_BORDER_SET if x[0] == 'X'}
EAST_DIGITS = {x for x in BASE_20_BORDER_SET if x[1] == 'X'}
SOUTH_DIGITS = {x for x in BASE_20_BORDER_SET if x[0] == '2'}
WEST_DIGITS = {x for x in BASE_20_BORDER_SET if x[1] == '2'}

digit_mapping_dict = {str(index): str(digit) for index, digit in enumerate(list(CODE_ALPHABET))}
san_francisco_codes = [
                 "849VRG00+", "849VRH00+", "849VRJ00+",
    "849VQF00+", "849VQG00+", "849VQH00+", "849VQJ00+",
    "849VPF00+", "849VPG00+", "849VPH00+", "849VPJ00+",
]
san_francisco_tile_list = [OpenGeoTile(code) for code in san_francisco_codes]

def test_fail_new_TileArea():
    failing_argument_list = ['not_a_list', [], [1], [0.001], ['hello'], [{'hey': 'there'}]]
    for failing_argument in failing_argument_list:
        with pytest.raises(Exception):
            fail_tile = TileArea(argument)

def test_new_TileArea_from_tile():
    pass_tile = TileArea(OpenGeoTile("849VQF00+"))
    assert isinstance(pass_tile, TileArea)

def test_new_TileArea_from_list():
    san_francisco_TileArea = TileArea(san_francisco_tile_list)
    assert set(
                [tile.getTileAddress() for tile in san_francisco_TileArea.tile_set]
            ) == set(
                [tile.getTileAddress() for tile in san_francisco_tile_list]
            )

def test_getShortestCoveringTileList():
    de_Young_NEIGHBORHOOD_code = "849VQGCJ+"
    de_Young_PINPOINT_plus_codes = []
    for i in range(20):
        i_digit = digit_mapping_dict.get(str(i))
        for j in range(20):
            j_digit = digit_mapping_dict.get(str(j))
            de_Young_PINPOINT_plus_codes.append(OpenGeoTile(de_Young_NEIGHBORHOOD_code + i_digit + j_digit))

    assert len(de_Young_PINPOINT_plus_codes) == 20 * 20
    de_Young_TileArea = TileArea(de_Young_PINPOINT_plus_codes)
    assert len(de_Young_TileArea.tile_set) == 1

    western_coast_usa = OpenGeoTile('84000000+')
    de_Young_TileArea.addTile(western_coast_usa)

    assert len(de_Young_TileArea.tile_set) == 1
    assert '84' in {t.getTileAddress() for t in de_Young_TileArea.tile_set}

def test_TileArea_contains():
    san_francisco_TileArea = TileArea(san_francisco_tile_list)

    central_sf = OpenGeoTile('849VQH00+')
    palace_of_fine_arts = OpenGeoTile('849VRH32+')
    uc_berkeley_statium = OpenGeoTile('849VVPCX+')
    western_coast_usa = OpenGeoTile('84000000+')
    assert san_francisco_TileArea.contains(central_sf)
    assert san_francisco_TileArea.contains(palace_of_fine_arts)
    assert not san_francisco_TileArea.contains(uc_berkeley_statium)
    assert not san_francisco_TileArea.contains(western_coast_usa)

def test_getSmallestTileSize():
    san_francisco_TileArea = TileArea(san_francisco_tile_list)

    assert san_francisco_TileArea.getSmallestTileSize() == TileSize.DISTRICT
    print("849VMGX2+")
    san_francisco_TileArea.addTile(OpenGeoTile("849VMGX2+"))
    assert san_francisco_TileArea.getSmallestTileSize() == TileSize.NEIGHBORHOOD
    print("849VMGW2+X7")
    san_francisco_TileArea.addTile(OpenGeoTile("849VMGW2+X7"))
    assert san_francisco_TileArea.getSmallestTileSize() == TileSize.PINPOINT
    western_coast_usa = OpenGeoTile('84000000+')
    san_francisco_TileArea.addTile(western_coast_usa)
    assert san_francisco_TileArea.getSmallestTileSize() == TileSize.GLOBAL


def test_addTileArea():
    # standard addition
    san_francisco_TileArea = TileArea(san_francisco_tile_list)
    sf_tile_list_num = len(san_francisco_TileArea.tile_set)
    berkeley_codes = [
                     '849VWP00+',
        '849VVM00+', '849VVP00+',
        ]
    berkeley_tile_list = [OpenGeoTile(code) for code in berkeley_codes]
    berkeley_TileArea = TileArea(berkeley_tile_list)
    san_francisco_TileArea.addTileArea(berkeley_TileArea)
    assert len(san_francisco_TileArea.tile_set) == sf_tile_list_num + len(berkeley_codes)

    # subsumptive addition
    western_usa = TileArea([OpenGeoTile('84000000+'), OpenGeoTile('85000000+')])
    san_francisco_TileArea.addTileArea(western_usa)
    assert len(san_francisco_TileArea.tile_set) == len(western_usa.tile_set)


def test_containsPlusCode():
    san_francisco_TileArea = TileArea(san_francisco_tile_list)

    central_sf_code = '849VQH00+'
    palace_of_fine_arts_code = '849VRH32+'
    uc_berkeley_statium_code = '849VVPCX+'
    western_coast_usa_code = '84000000+'
    assert san_francisco_TileArea.containsPlusCode(central_sf_code)
    assert san_francisco_TileArea.containsPlusCode(palace_of_fine_arts_code)
    assert not san_francisco_TileArea.containsPlusCode(uc_berkeley_statium_code)
    assert not san_francisco_TileArea.containsPlusCode(western_coast_usa_code)

def test_containsLatLong():
    san_francisco_TileArea = TileArea(san_francisco_tile_list)

    buena_vista_peak_lat, buena_vista_peak_long  = 37.767761, -122.441560
    eiffel_tower_lat, eiffel_tower_long = 48.858589, 2.293681
    assert san_francisco_TileArea.containsLatLong(buena_vista_peak_lat, buena_vista_peak_long)
    assert not san_francisco_TileArea.containsLatLong(eiffel_tower_lat, eiffel_tower_long)


def test_getEdgeTileSet():
    missing_digits = ['8','9','C','F','G','H','J','M','P','Q','R','V']
    gw_high_school_sf_border_addresses = [
        '849VQGH5',
        '849VQGG5X7', '849VQGG5XW',
        '849VQGG5W7', '849VQGG5WW',
    ]
    for digit in missing_digits:
        gw_high_school_sf_border_addresses.append('849VQGG5W'+digit)
    gw_high_school_sf_NON_border_addresses = ['849VQGG5X' + digit for digit in missing_digits]

    gw_high_addresses = gw_high_school_sf_border_addresses + gw_high_school_sf_NON_border_addresses

    gw_high = TileArea([OpenGeoTile(address) for address in gw_high_addresses])

    gw_edge_tiles = gw_high.getEdgeTileSet()
    assert {tile.getTileAddress() for tile in gw_edge_tiles} == set(gw_high_school_sf_border_addresses)

def test_expandTileArea():
    'test expand by one same sized unit'
    berkeley_codes = [
                                            '849VWP00+',
                                '849VVM00+','849VVP00+',
        ]
    berkeley_tile_list = [OpenGeoTile(code) for code in berkeley_codes]
    berkeley_TileArea = TileArea(berkeley_tile_list)

    surrounding_codes = [
                                '849VXM00+','849VXP00+','849VXQ00+',
                    '849VWJ00+','849VWM00+',            '849VWQ00+',
                    '849VVJ00+',                        '849VVQ00+',
                    '849VRJ00+','849VRM00+','849VRP00+','849VRQ00+',
        ]
    surrounding_tiles = [OpenGeoTile(code) for code in surrounding_codes]
    manual_TileArea = TileArea(berkeley_tile_list + surrounding_tiles)

    berkeley_TileArea.expandTileArea(TileSize.DISTRICT)

    assert  {t.getTileAddress() for t in berkeley_TileArea.tile_set} == {
             t.getTileAddress() for t in manual_TileArea.tile_set  }

    ''' test expand by 2 same size units '''
    berkeley_TileArea = TileArea(berkeley_tile_list)

    surrounding_x2_codes = [
                    '84CV2J00+','84CV2M00+','84CV2P00+','84CV2Q00+','84CV2R00+',
        '849VXH00+','849VXJ00+',                                    '849VXR00+',
        '849VWH00+',                                                '849VWR00+',
        '849VVH00+',                                                '849VVR00+',
        '849VRH00+',                                                '849VRR00+',
        '849VQH00+','849VQJ00+','849VQM00+','849VQP00+','849VQQ00+','849VQR00+',
        ]
    surrounding_x2_tiles = [OpenGeoTile(code) for code in surrounding_x2_codes]
    manual_x2_TileArea = TileArea(berkeley_tile_list + surrounding_tiles + surrounding_x2_tiles)

    berkeley_TileArea.expandTileArea(TileSize.DISTRICT, num_of_tiles=2)

    assert  {t.getTileAddress() for t in berkeley_TileArea.tile_set} == {
             t.getTileAddress() for t in manual_x2_TileArea.tile_set  }


    ''' test expand by default units (1, pinpoint) '''
    berkeley_TileArea = TileArea(berkeley_tile_list)
    len_berk_start = len(berkeley_TileArea.tile_set)
    print('len_berk_start:', len_berk_start)


    top_left_code =     ['849VXM2X+2X']
    top_codes =         [code+suffix for code in
                                        [f'849VXP2{digit}+' for digit in CODE_ALPHABET]
                                    for suffix in SOUTH_DIGITS]
    top_right_code=     ['849VXQ22+22']

    right_codes =       [code+suffix for code in
                                        [f'849VWQ{digit}2+' for digit in CODE_ALPHABET]
                                    +   [f'849VVQ{digit}2+' for digit in CODE_ALPHABET]
                                     for suffix in WEST_DIGITS]

    bottom_right_code=  ['849VRQX2+X2']
    bottom_codes =      [code+suffix for code in
                                        [f'849VRMX{digit}+' for digit in CODE_ALPHABET]
                                    +   [f'849VRPX{digit}+' for digit in CODE_ALPHABET]
                                    for suffix in NORTH_DIGITS]
    bottom_left_code=   ['849VRJXX+XX']
    left_codes =        [code+suffix for code in
                                        [f'849VVJ{digit}X+' for digit in CODE_ALPHABET]
                                    for suffix in EAST_DIGITS]
    cutout_left_code=   ['849VWJ2X+2X']
    cutout_bottom_codes=[code+suffix for code in
                                        [f'849VWM2{digit}+' for digit in CODE_ALPHABET]
                                    for suffix in SOUTH_DIGITS]
    cutout_right_codes=[code+suffix for code in
                                        [f'849VWM{digit}X+' for digit in CODE_ALPHABET]
                                    for suffix in EAST_DIGITS]
    border_codes  = set(top_left_code    + top_codes           + top_right_code +
                     cutout_left_code + cutout_bottom_codes + cutout_right_codes +
                     left_codes                             + right_codes +
                     bottom_left_code + bottom_codes        + bottom_right_code)
    border_tiles = [OpenGeoTile(code) for code in border_codes]
    border_TileArea = TileArea(berkeley_tile_list + border_tiles)

    berkeley_TileArea.expandTileArea(TileSize.PINPOINT) #num_of_tiles=1, tile_size=TileSize.PINPOINT

    assert  {t.getTileAddress() for t in berkeley_TileArea.tile_set} == {
             t.getTileAddress() for t in border_TileArea.tile_set  }



