from OpenGeoTile import OpenGeoTile, TileSize
from openlocationcode import openlocationcode as olc

'''
    by scoofy on 09.08.21
'''

north_pole_and_svalbard_tile = OpenGeoTile('CF')
peuget_sound = OpenGeoTile('84VV0000+')


def test_TileSize():
    assert TileSize.GLOBAL.getCodeLength() == 2
    assert TileSize.GLOBAL.getCoordinateIncrement() == 20.0

    assert TileSize.REGION.getCodeLength() == 4
    assert TileSize.REGION.getCoordinateIncrement() == 1.0

    assert TileSize.DISTRICT.getCodeLength() == 6
    assert TileSize.DISTRICT.getCoordinateIncrement() == 0.05

    assert TileSize.NEIGHBORHOOD.getCodeLength() == 8
    assert TileSize.NEIGHBORHOOD.getCoordinateIncrement() == 0.0025

    assert TileSize.PINPOINT.getCodeLength() == 10
    assert TileSize.PINPOINT.getCoordinateIncrement() == 0.000125

def test_constructTileFromCode():
    peuget_sound = OpenGeoTile('84VV0000+')
    assert '84VV0000+' == peuget_sound.returnCode()

def test_constructTileFromCodeAndSize():
    seattle_code = '84VVJM00+'
    peuget_sound = OpenGeoTile(seattle_code, TileSize.REGION)
    assert '84VV0000+' == peuget_sound.returnCode()

def test_constructTileFromLatLong():
    seattle_lat, seattle_long = 47.625, -122.325
    peuget_sound = OpenGeoTile(lat=seattle_lat, long=seattle_long, tile_size=TileSize.REGION)
    assert '84VV0000+' == peuget_sound.returnCode()

def test_constructTileFromTileAddress():
    peuget_sound = OpenGeoTile('84VV')
    assert '84VV0000+' == peuget_sound.returnCode()

def test_getWrappedOpenLocationCode():
    peuget_sound = OpenGeoTile('84VV0000+')
    assert '84VV0000+' == peuget_sound.getWrappedOpenLocationCode()

def test_getTileSize():
    seattle_code = '84VVJM00+'
    peuget_sound = OpenGeoTile(seattle_code, TileSize.REGION)
    assert TileSize.REGION == peuget_sound.getTileSize()

def test_getTileAddress():
    peuget_sound = OpenGeoTile('84VV')
    assert '84VV' == peuget_sound.getTileAddress()

def test_getTileAddressPrefix():
    gum_wall = '84VVJM558V'
    pikes_place = '84VVJM55'
    seattle = '84VVJM'
    peuget_sound = '84VV'
    us_west_coast = '84'

    address_list = [
        gum_wall,
        pikes_place,
        seattle,
        peuget_sound,
        us_west_coast,
        ""
    ]

    for index, address in enumerate(address_list):
        if address:
            tile = OpenGeoTile(address)
            assert tile.getTileAddressPrefix() == address_list[index + 1]

def test_OpenLocationCode():
    peuget_sound = OpenGeoTile('84VV0000+')
    assert '84VV0000+' == peuget_sound.getTileOpenLocationCode()

def test_getNeighbors_isNeighbor():
    peuget_sound = OpenGeoTile('84VV0000+')

    victoria_ca = OpenGeoTile('84WR0000+')
    bellingham_wa = OpenGeoTile('84WV0000+')
    mt_baker_wa = OpenGeoTile('84WW0000+')
    snoqualmie_pass = OpenGeoTile('84VW0000+')
    mt_rainier = OpenGeoTile('84RW0000+')
    mt_st_helens = OpenGeoTile('84RV0000+')
    columbia_river = OpenGeoTile('84RR0000+')
    olympic_nat_park = OpenGeoTile('84VR0000+')

    manual_neighbor_list = [
        victoria_ca,
        bellingham_wa,
        mt_baker_wa,
        snoqualmie_pass,
        mt_rainier,
        mt_st_helens,
        columbia_river,
        olympic_nat_park,
    ]

    eight_point_dirctions = ['NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W']
    for index, direction in enumerate(eight_point_dirctions):
        assert manual_neighbor_list[index].code ==  peuget_sound.getNeighbors(
                                                        eight_point_direction=direction
                                                    )[0].code

    function_neighbor_list = peuget_sound.getNeighbors()

    assert set([t.code for t in manual_neighbor_list]) == set([t.code for t in function_neighbor_list])

    for tile in function_neighbor_list:
        assert peuget_sound.isNeighbor(tile)

    # TEST POLAR COORDINATES

    north_pole_and_svalbard_tile = OpenGeoTile('CF')

    west_of_svalbard = OpenGeoTile('CC000000+')
    east_of_svalbard = OpenGeoTile('CG000000+')
    se_of_svalbard = OpenGeoTile('9G000000+')
    south_of_svalbard = OpenGeoTile('9F000000+')
    sw_of_svalbard = OpenGeoTile('9C000000+')

    manual_neighbor_list = [
        west_of_svalbard,
        east_of_svalbard,
        se_of_svalbard,
        south_of_svalbard,
        sw_of_svalbard,
    ]
    function_neighbor_list = north_pole_and_svalbard_tile.getNeighbors()
    assert set([t.code for t in manual_neighbor_list]) == set([t.code for t in function_neighbor_list])
    for tile in function_neighbor_list:
        assert north_pole_and_svalbard_tile.isNeighbor(tile)

#isSameTile -> test_constructionsSameBlock

def test_contains():
    peuget_sound = OpenGeoTile('84VV0000+')
    seattle = OpenGeoTile('84VVJM00+')
    us_west_coast = OpenGeoTile('84000000+')
    uc_berkeley_statium = OpenGeoTile('849VVPCX+')


    assert peuget_sound.contains(seattle)
    assert not peuget_sound.contains(us_west_coast)
    assert not peuget_sound.contains(uc_berkeley_statium)

def test_returnSetOfSubtiles():
    uc_berkeley_address = '849VVPCX'
    BASE_20_SET = {x+y for x in olc.CODE_ALPHABET_ for y in olc.CODE_ALPHABET_}
    berkeley_statium_address_subset = set()
    for base in BASE_20_SET:
        berkeley_statium_address_subset.add(uc_berkeley_address + base)
    assert len(berkeley_statium_address_subset) == 20 * 20

    uc_berkeley_statium = OpenGeoTile('849VVPCX+')
    berkeley_statium_tile_subset = uc_berkeley_statium.returnSetOfSubtiles()
    assert berkeley_statium_address_subset == {tile.getTileAddress() for tile in berkeley_statium_tile_subset}

    seattle_address = '84VVJM'
    seattle_address_subset = set()
    seattle_address_double_subset = set()
    for base in BASE_20_SET:
        seattle_address_subset.add(seattle_address + base)
        for subbase in BASE_20_SET:
            seattle_address_double_subset.add(seattle_address + base + subbase)

    assert len(seattle_address_subset) == 20 * 20

    seattle = OpenGeoTile('84VVJM00+')

    seattle_tile_subset = seattle.returnSetOfSubtiles(desired_tile_size=TileSize.NEIGHBORHOOD)
    assert seattle_address_subset == {tile.getTileAddress() for tile in seattle_tile_subset}

    seattle_tile_double_subset = seattle.returnSetOfSubtiles()
    assert seattle_address_double_subset == {tile.getTileAddress() for tile in seattle_tile_double_subset}

def test_returnSetOfBorderSubtiles():
    uc_berkeley_statium = OpenGeoTile('849VVPCX+')
    berkeley_statium_tile_subset = uc_berkeley_statium.returnSetOfSubtiles()
    berkeley_border_address_verify = {tile.getTileAddress() for tile in berkeley_statium_tile_subset
                                        if (tile.getTileAddress()[-1] in ['2', 'X'])
                                        or (tile.getTileAddress()[-2] in ['2', 'X'])
                                     }
    assert len(berkeley_border_address_verify) == (20 * 4) - 4

    berkeley_border_tile_set = uc_berkeley_statium.returnSetOfBorderSubtiles()
    assert berkeley_border_address_verify == {tile.getTileAddress() for tile in berkeley_border_tile_set}




