from openlocationcode import openlocationcode as olc
from SimpleTileArea import SimpleTileArea
from OpenGeoTile import OpenGeoTile, TileSize
import pytest

digits = [2,3,4,5,6,7,8,9,'C','F','G','H','J','M','P','Q','R','V','W','X']
digit_mapping_dict = {str(index): str(digit) for index, digit in enumerate(digits)}
san_francisco_codes = [
                 "849VRG00+", "849VRH00+", "849VRJ00+",
    "849VQF00+", "849VQG00+", "849VQH00+", "849VQJ00+",
    "849VPF00+", "849VPG00+", "849VPH00+", "849VPJ00+",
]
san_francisco_tile_list = [OpenGeoTile(code) for code in san_francisco_codes]

def test_fail_new_SimpleTileArea():
    failing_argument_list = ['not_a_list', [], [1], [0.001], ['hello'], [{'hey': 'there'}]]
    for failing_argument in failing_argument_list:
        with pytest.raises(Exception):
            fail_tile = SimpleTileArea(argument)

def test_new_SimpleTileArea_from_tile():
    pass_tile = SimpleTileArea(OpenGeoTile("849VQF00+"))
    assert isinstance(pass_tile, SimpleTileArea)

def test_new_SimpleTileArea_from_list():
    san_francisco_SimpleTileArea = SimpleTileArea(san_francisco_tile_list)
    assert set(
                [tile.getTileAddress() for tile in san_francisco_SimpleTileArea.tile_list]
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
    de_Young_SimpleTileArea = SimpleTileArea(de_Young_PINPOINT_plus_codes)
    assert len(de_Young_SimpleTileArea.tile_list) == 20 * 20

    western_coast_usa = OpenGeoTile('84000000+')
    de_Young_SimpleTileArea.addTile(western_coast_usa)

    assert len(de_Young_SimpleTileArea.tile_list) == (20 * 20) + 1 and de_Young_SimpleTileArea.tile_list[-1].getTileAddress() == '84'

def test_SimpleTileArea_contains():
    san_francisco_SimpleTileArea = SimpleTileArea(san_francisco_tile_list)

    central_sf = OpenGeoTile('849VQH00+')
    palace_of_fine_arts = OpenGeoTile('849VRH32+')
    uc_berkeley_statium = OpenGeoTile('849VVPCX+')
    western_coast_usa = OpenGeoTile('84000000+')
    assert san_francisco_SimpleTileArea.contains(central_sf)
    assert san_francisco_SimpleTileArea.contains(palace_of_fine_arts)
    assert not san_francisco_SimpleTileArea.contains(uc_berkeley_statium)
    assert not san_francisco_SimpleTileArea.contains(western_coast_usa)

def test_getSmallestTileSize():
    san_francisco_SimpleTileArea = SimpleTileArea(san_francisco_tile_list)

    print( san_francisco_SimpleTileArea.tile_list[0].code, "san_francisco_SimpleTileArea.tile_list[0].code")
    assert san_francisco_SimpleTileArea.getSmallestTileSize() == TileSize.DISTRICT
    print("849VMGX2+")
    san_francisco_SimpleTileArea.addTile(OpenGeoTile("849VMGX2+"))
    assert san_francisco_SimpleTileArea.getSmallestTileSize() == TileSize.NEIGHBORHOOD
    print("849VMGW2+X7")
    san_francisco_SimpleTileArea.addTile(OpenGeoTile("849VMGW2+X7"))
    assert san_francisco_SimpleTileArea.getSmallestTileSize() == TileSize.PINPOINT
    western_coast_usa = OpenGeoTile('84000000+')
    san_francisco_SimpleTileArea.addTile(western_coast_usa)
    assert san_francisco_SimpleTileArea.getSmallestTileSize() == TileSize.PINPOINT

def test_addTileArea():
    # standard addition
    san_francisco_SimpleTileArea = SimpleTileArea(san_francisco_tile_list)
    sf_tile_list_num = len(san_francisco_SimpleTileArea.tile_list)
    berkeley_codes = [
                     '849VWP00+',
        '849VVM00+', '849VVP00+',
        ]
    berkeley_tile_list = [OpenGeoTile(code) for code in berkeley_codes]
    berkeley_SimpleTileArea = SimpleTileArea(berkeley_tile_list)
    san_francisco_SimpleTileArea.addTileArea(berkeley_SimpleTileArea)
    assert len(san_francisco_SimpleTileArea.tile_list) == sf_tile_list_num + len(berkeley_codes)

    # subsumptive addition
    western_usa = SimpleTileArea([OpenGeoTile('84000000+'), OpenGeoTile('85000000+')])
    san_francisco_SimpleTileArea.addTileArea(western_usa)
    assert len(san_francisco_SimpleTileArea.tile_list) == sf_tile_list_num + len(berkeley_codes) + len(western_usa.tile_list)


def test_containsPlusCode():
    san_francisco_SimpleTileArea = SimpleTileArea(san_francisco_tile_list)

    central_sf_code = '849VQH00+'
    palace_of_fine_arts_code = '849VRH32+'
    uc_berkeley_statium_code = '849VVPCX+'
    western_coast_usa_code = '84000000+'
    assert san_francisco_SimpleTileArea.containsPlusCode(central_sf_code)
    assert san_francisco_SimpleTileArea.containsPlusCode(palace_of_fine_arts_code)
    assert not san_francisco_SimpleTileArea.containsPlusCode(uc_berkeley_statium_code)
    assert not san_francisco_SimpleTileArea.containsPlusCode(western_coast_usa_code)

def test_containsLatLong():
    san_francisco_SimpleTileArea = SimpleTileArea(san_francisco_tile_list)

    buena_vista_peak_lat, buena_vista_peak_long  = 37.767761, -122.441560
    eiffel_tower_lat, eiffel_tower_long = 48.858589, 2.293681
    assert san_francisco_SimpleTileArea.containsLatLong(buena_vista_peak_lat, buena_vista_peak_long)
    assert not san_francisco_SimpleTileArea.containsLatLong(eiffel_tower_lat, eiffel_tower_long)








