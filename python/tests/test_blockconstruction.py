import OpenGeoTile as ogt

'''/**
 * Created by andreas on 08.07.17.
 */

   Ported by scoofy on 08.31.21
'''

def test_constructionsSameBlock():
        pluscode = "CCXWXWXW+XW"
        tileSize = ogt.TileSize.DISTRICT

        block2 = ogt.OpenGeoTile(pluscode, tileSize)
        block4 = ogt.OpenGeoTile(block2.getTileAddress())


        assert block2.isSameTile(block4)

