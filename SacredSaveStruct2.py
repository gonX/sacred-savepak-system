import struct

import Enums

class SacredSaveStruct2:
    def __init__(self, buffer):
        if len(buffer) != 0x300: raise Exception("unexpected buffer size")
        self.buffer = buffer

    @staticmethod
    def getSaveStruct2object(buffer):
        (i, readIndex, value) = struct.unpack("iii", buffer)
        return { "id": i, "idStr": Enums.SacredSaveStruct2Enum(i), "readIndex": readIndex, "value": value }

    def getSaveStruct2objects(self):
        return [(i, self.buffer[i:i+12]) for i in range(len(self.buffer)) if i % 12 == 0]

    def dumpSaveStruct2(self):
        emptyObjects = 0
        last_read_index = None
        last_size = None # TODO

        for (idx, bufSlice) in self.getSaveStruct2objects():
            obj = self.getSaveStruct2object(bufSlice)
            if (obj["id"] != 0):
                print(f"offset {idx:#05x} ({idx:3}): {obj}")
            else:
                emptyObjects += 1
        if emptyObjects != 0:
            print(f"empty objects: {emptyObjects} (total {int(len(self.buffer)/12)})")

    # the values are intended to be sizes but not all values can be trusted, calculate based off offsets
    def calculateRealSize(self, bufferIdx):
        if bufferIdx % 12 != 0: raise Exception("invalid index") 
        offset = bufferIdx * 12
        curObj = self.getSaveStruct2object(self.buffer[offset:offset+12])
        nexObj = self.getSaveStruct2object(self.buffer[offset+12:offset+24]) # FIXME: will miss if next object is empty
        return nexobj.readIndex - curobj.readIndex

    def dumpSaveStruct2SectionsToFile(self):
        pass
