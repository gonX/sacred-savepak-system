from struct import *

def repackIntTo4Bytes(i): # TODO: name sucks
    """input: 0x12345678
       output: 0x78787878
       """
    v = i & 0xff
    return unpack('I', pack('BBBB', v, v, v, v))[0]

def intListToHexStrings(ilist):
    return [("%#x" % i) for i in ilist]
