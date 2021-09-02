import OpenGeoTile as ogt

'''/**
 * Created by andreas on 09.07.17.
 */
     ported by scoofy on 08.31.21
'''

def test_OpenLocationCode():
    tile = ogt.OpenGeoTile("C9")

    assert "C9000000+" == tile.getTileOpenLocationCode()


