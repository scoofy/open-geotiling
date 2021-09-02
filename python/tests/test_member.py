import OpenGeoTile as ogt

'''/**
 * Created by andreas on 08.07.17.
 */
    ported by scoofy on 08.31.21
'''
def testMembership():
    bigBlock   = ogt.OpenGeoTile("8CFF")
    smallBlock = ogt.OpenGeoTile("8CFFXX")
    tinyBlock  = ogt.OpenGeoTile("8CFFXXHH")

    assert bigBlock.contains(smallBlock)
    assert bigBlock.contains(tinyBlock)
    assert smallBlock.contains(tinyBlock)

    assert bigBlock.contains(bigBlock)

    assert not smallBlock.contains(bigBlock)



def testNonMembership():
    smallBlock = ogt.OpenGeoTile("8CFFXX")
    tinyBlock  = ogt.OpenGeoTile("8CXXHHFF")

    assert not smallBlock.contains(tinyBlock)

