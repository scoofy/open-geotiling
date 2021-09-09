import OpenGeoTile as ogt


'''/**
 * Created by andreas on 08.07.17.
 */
     ported by scoofy on 08.31.21
'''



def test_GlobalSize():
    pluscode = "CCXWXWXW+XW"

    tile_size = ogt.TileSize.GLOBAL
    codeLength = ogt.TileSize.GLOBAL.getCodeLength()

    block1 = ogt.OpenGeoTile(pluscode, tile_size)

    assert codeLength == 2
    assert block1.getTileAddress() == pluscode[0:codeLength]



def test_RegionSize():
    pluscode = "CCXWXWXW+XW"

    tile_size = ogt.TileSize.REGION
    codeLength = ogt.TileSize.REGION.getCodeLength()

    block1 = ogt.OpenGeoTile(pluscode, tile_size)

    assert codeLength == 4
    assert block1.getTileAddress() == pluscode[0:codeLength]



def test_DistrictSize():
    pluscode = "CCXWXWXW+XW"

    tile_size = ogt.TileSize.DISTRICT
    codeLength = ogt.TileSize.DISTRICT.getCodeLength()

    block1 = ogt.OpenGeoTile(pluscode, tile_size)

    assert codeLength == 6
    assert block1.getTileAddress() == pluscode[0:codeLength]



def test_NeighborhoodSize():
    pluscode = "CCXWXWXW+XW"

    tile_size = ogt.TileSize.NEIGHBORHOOD
    codeLength = ogt.TileSize.NEIGHBORHOOD.getCodeLength()

    block1 = ogt.OpenGeoTile(pluscode, tile_size)

    assert codeLength == 8
    assert block1.getTileAddress() == pluscode[0:codeLength]



def test_PinpointSize():
    pluscode = "CCXWXWXW+XW"

    tile_size = ogt.TileSize.PINPOINT
    codeLength = ogt.TileSize.PINPOINT.getCodeLength()

    block1 = ogt.OpenGeoTile(pluscode, tile_size)

    assert codeLength == 10
    assert block1.getTileAddress() == pluscode.replace("+","")

