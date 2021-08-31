import pytest
import OpenGeoTile as ogt

originalBlock = ogt.OpenGeoTile("8CRW2X")

def test_Adjacency():
    '''//neighboring blocks at the same scale are considered adjacent'''
    neighborBlock1 = ogt.OpenGeoTile("8CRW3W")
    neighborBlock2 = ogt.OpenGeoTile("8CRW3X")
    neighborBlock3 = ogt.OpenGeoTile("8CRX32")
    neighborBlock4 = ogt.OpenGeoTile("8CRX22")
    neighborBlock5 = ogt.OpenGeoTile("8CQXX2")
    neighborBlock6 = ogt.OpenGeoTile("8CQWXX")
    neighborBlock7 = ogt.OpenGeoTile("8CQWXW")
    neighborBlock8 = ogt.OpenGeoTile("8CRW2W")
    assert originalBlock.isNeighbor(neighborBlock1)
    assert originalBlock.isNeighbor(neighborBlock2)
    assert originalBlock.isNeighbor(neighborBlock3)
    assert originalBlock.isNeighbor(neighborBlock4)
    assert originalBlock.isNeighbor(neighborBlock5)
    assert originalBlock.isNeighbor(neighborBlock6)
    assert originalBlock.isNeighbor(neighborBlock7)
    assert originalBlock.isNeighbor(neighborBlock8)

def test_AdjacencyWrapping():
    '''//adjacency wraps correctly'''
    pacificLeft = ogt.OpenGeoTile("8V")
    pacificRight = ogt.OpenGeoTile("72")
    assert pacificLeft.isNeighbor(pacificRight)

def test_NonAdjacencyRandomBlock():
    '''//non-neighboring blocks are not considered adjacent'''
    noNeighborBlock = ogt.OpenGeoTile("3FHP99")
    assert not originalBlock.isNeighbor(noNeighborBlock)

def test_AdjacencyDifferentScale():
    '''//neighboring blocks at different scales are considered adjacent,
       //unless one is contained within the other'''
    neighborBlockDifferentSize1 = ogt.OpenGeoTile("8CRW2W8X")
    neighborBlockDifferentSize2 = ogt.OpenGeoTile("8CRX")
    containingBlock = ogt.OpenGeoTile("8CRW")
    assert originalBlock.isNeighbor(neighborBlockDifferentSize1)
    assert originalBlock.isNeighbor(neighborBlockDifferentSize2)
    assert not originalBlock.isNeighbor(containingBlock)

def test_NonAdjacencySelf():
    '''//no block is adjacent to itself, even at the poles'''
    polarBlock = ogt.OpenGeoTile("CC")
    assert not originalBlock.isNeighbor(originalBlock)
    assert not polarBlock.isNeighbor(polarBlock)

