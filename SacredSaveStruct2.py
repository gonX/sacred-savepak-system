import struct

import Enums

class SacredSaveStruct2:
    STRIDE = 12

    def __init__(self, buffer):
        if len(buffer) != 0x300: raise Exception("unexpected buffer size") # theoretically as long as its divisible by 12 it should work
        self.buffer = buffer

    @staticmethod
    def getSaveStruct2object(buffer):
        (i, readIndex, value) = struct.unpack("iii", buffer)
        return { "id": i, "idStr": Enums.SacredSaveStruct2Enum(i), "readIndex": readIndex, "value": value }

    def getSaveStruct2objects(self):
        """Gets all non-null objects from string"""
        return [(i, self.buffer[i:i+self.STRIDE]) for i in range(len(self.buffer)) if (i % self.STRIDE == 0 and int.from_bytes(self.buffer[i:i+4]) != 0)]

    def dumpSaveStruct2(self):
        for (idx, bufSlice) in self.getSaveStruct2objects():
            obj = self.getSaveStruct2object(bufSlice)
            print(f"offset {idx:#05x} ({idx:3}): {obj}")

    # the value (offset 12) is seemingly intended to be object size, but not all values can be trusted, seemingly
    # therefore, calculate based off of next objects offset instead
    def calculateRealSize(self, bufferOffset):
        if bufferOffset % self.STRIDE != 0: raise Exception("invalid offset")

        nexObj = None
        curObj = self.getSaveStruct2object(self.buffer[bufferOffset:bufferOffset+self.STRIDE])

        while nexObj is None:
            nexObj = self.getSaveStruct2object(self.buffer[bufferOffset+self.STRIDE:bufferOffset+self.STRIDE*2])
            if nexObj["id"] == 0:
                bufferOffset += self.STRIDE
                if (bufferOffset + self.STRIDE >= len(self.buffer)):
                    return -1
                nexObj = None
                continue
        return nexObj["readIndex"] - curObj["readIndex"]
