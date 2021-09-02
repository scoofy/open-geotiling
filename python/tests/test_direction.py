import OpenGeoTile as ogt
import math

'''/**
 * Created by andreas on 08.07.17.
 */

     Ported by scoofy on 08.31.21
'''
def test_Directions():
    tile1 = ogt.OpenGeoTile("9F53")
    tile2 = ogt.OpenGeoTile("8FX3") #//diff: 4 vertical
    tile3 = ogt.OpenGeoTile("9F5G") #//diff: -9 horizontal
    tile4 = ogt.OpenGeoTile("8FX7") #//diff: -4 hor., 4 vert.

    delta = 0.0001

    math.isclose( math.pi/2, tile1.getDirection(tile2), abs_tol=delta)
    math.isclose( -math.pi/2, tile2.getDirection(tile1), abs_tol=delta)

    math.isclose( math.pi, tile1.getDirection(tile3), abs_tol=delta)
    math.isclose( 0, tile3.getDirection(tile1), abs_tol=delta)

    math.isclose( 0.75*math.pi, tile1.getDirection(tile4), abs_tol=delta)
    math.isclose( -0.25*math.pi, tile4.getDirection(tile1), abs_tol=delta)
