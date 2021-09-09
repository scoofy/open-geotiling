import OpenGeoTile as ogt

'''/**
 * Created by andreas on 08.07.17.
 */

   Ported by scoofy on 08.31.21
'''

def test_constructionsSameBlock():
        pluscode = "CCXWXWXW+XW"
        tile_size = ogt.TileSize.DISTRICT

        block2 = ogt.OpenGeoTile(pluscode, tile_size)
        block4 = ogt.OpenGeoTile(block2.getTileAddress())


        assert block2.isSameTile(block4)

