import OpenGeoTile as ogt

def test_DistancesSimpleRegion():
    tile1 = ogt.OpenGeoTile("9F53")
    tile2 = ogt.OpenGeoTile("8FXG") #//diff: 9 horizontal, 4 vertical

    assert tile1.getManhattanTileDistanceTo(tile2)==tile2.getManhattanTileDistanceTo(tile1)
    assert (9+4) == tile1.getManhattanTileDistanceTo(tile2)
    assert 9 == tile1.getChebyshevTileDistanceTo(tile2)

def test_DistancesSimpleDistrict():
    tile1 = ogt.OpenGeoTile("9F53XX")
    tile2 = ogt.OpenGeoTile("8FXGXX") #//diff: 9*20 horizontal, 4*20 vertical

    assert tile1.getManhattanTileDistanceTo(tile2)==tile2.getManhattanTileDistanceTo(tile1)
    assert (9+4)*20 == tile1.getManhattanTileDistanceTo(tile2)
    assert (9*20) == tile1.getChebyshevTileDistanceTo(tile2)

def test_DistancesSimpleNeighborhood():
    tile1 = ogt.OpenGeoTile("9F53XXXX")
    tile2 = ogt.OpenGeoTile("8FXGXXXX") #//diff: 9*20*20 horizontal, 4*20*20 vertical

    assert tile1.getManhattanTileDistanceTo(tile2)==tile2.getManhattanTileDistanceTo(tile1)
    assert (9+4)*20*20 == tile1.getManhattanTileDistanceTo(tile2)
    assert (9*20*20) == tile1.getChebyshevTileDistanceTo(tile2)

def test_DistancesSimplePinpoint():
    tile1 = ogt.OpenGeoTile("9F53XXXXXX")
    tile2 = ogt.OpenGeoTile("8FXGXXXXXX") #//diff: 9*20*20*20 horizontal, 4*20*20*20 vertical

    assert tile1.getManhattanTileDistanceTo(tile2)==tile2.getManhattanTileDistanceTo(tile1)
    assert (9+4)*20*20*20 == tile1.getManhattanTileDistanceTo(tile2)
    assert (9*20*20*20) == tile1.getChebyshevTileDistanceTo(tile2)


def test_DistancesHalfCircle():
    tile1 = ogt.OpenGeoTile("9C22")
    tile2 = ogt.OpenGeoTile("8VX3") #//diff: 9*20+1 horizontal, 1 vertical

    assert tile1.getManhattanTileDistanceTo(tile2)==tile2.getManhattanTileDistanceTo(tile1)
    assert 9*20+1+1 == tile1.getManhattanTileDistanceTo(tile2)
    assert 9*20+1 == tile1.getChebyshevTileDistanceTo(tile2)


def test_DistancesWrapEastWest():
    tile1 = ogt.OpenGeoTile("9622")
    tile2 = ogt.OpenGeoTile("8VX3") #//diff: 5*20-1 horizontal, 1 vertical

    assert tile1.getManhattanTileDistanceTo(tile2)==tile2.getManhattanTileDistanceTo(tile1)
    assert 5*20-1+1 == tile1.getManhattanTileDistanceTo(tile2)
    assert 5*20-1 == tile1.getChebyshevTileDistanceTo(tile2)


def test_DistancesWrapWestEast():
    tile1 = ogt.OpenGeoTile("9H22")
    tile2 = ogt.OpenGeoTile("82X3") #//diff: 7*20+1 horizontal, 1 vertical

    assert tile1.getManhattanTileDistanceTo(tile2)==tile2.getManhattanTileDistanceTo(tile1)
    assert 7*20+1+1 == tile1.getManhattanTileDistanceTo(tile2)
    assert 7*20+1 == tile1.getChebyshevTileDistanceTo(tile2)
