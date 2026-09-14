import struct
import datetime as dt
from enum import Enum

class SacredPakSaveStruct2Enum(Enum):
    NULL = 0
    ENGINE = 128
    TRIGGERS = 129
    VIEWS = 130
    DESCRIPTOR = 131
    CALENDAR = 139
    INVENTORY = 141
    ITEMS_U = 142 # uncompressed, probably never seen in a finished file
    QUEST_U = 145 # uncompressed
    WEATHER = 146
    PICTURE = 147
    BLOOD = 148
    GENERIC = 149
    PARTICLES = 150 # uncompressed
    MOUSE = 152
    REGIONS = 153
    TEAM = 154
    STATS = 155
    UNK_0x9c = 156 # always 40 value
    UNK_0x9d = 157 # always 0x400 value (all 0 bytes?)
    ITEMS_C = 160 # compressed
    QUEST_C = 161 # compressed
    PARTICLES_C = 162 # compressed
    ENDING_likely = 195 # always 0 value, and always at end?

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN

    def __repr__(self):
        return f'{self.name}'

class SacredPak:
    # TODO: barrier functions that require __enter__() to have run so that we dont get weird uninitialized errors
    HEADER_SLICE = 3

    DATE_OFFSET = 0x5c
    DATE_FORMAT_STRUCT = "iiiiiiii" # y/m/d/wd/h/m/s/ms
    DATE_END = DATE_OFFSET + struct.calcsize(DATE_FORMAT_STRUCT)

    def __init__(self, pakName):
        self.pakName = pakName

    def __enter__(self):
        self.openedPak = open(self.pakName, "rb")
        self.firstHeaderBytes = self.openedPak.read(0x100)
        self.secondHeaderBytes = self.openedPak.read(0x300)
        self._initFromHeaders();
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.openedPak.close()

    def _initFromHeaders(self):
        self.header = self.firstHeaderBytes[:self.HEADER_SLICE].decode()
        self._fixDate()

    def _fixDate(self):
        (year, month, day, _, hour, minute, second, ms) = \
                struct.unpack(self.DATE_FORMAT_STRUCT, self.firstHeaderBytes[self.DATE_OFFSET:self.DATE_END])
        self.date = dt.datetime(year + 1900, month, day, hour, minute, second, ms * 1000)

    @staticmethod
    def getSaveStruct2object(buffer):
        (i, readIndex, value) = struct.unpack("iii", buffer)
        return { "id": i, "idStr": SacredPakSaveStruct2Enum(i), "readIndex": readIndex, "value": value }

    def getSaveStruct2objects(self):
        return [(i, self.secondHeaderBytes[i:i+12]) for i in range(len(self.secondHeaderBytes)) if i % 12 == 0]

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
            print(f"empty objects: {emptyObjects} (total {int(len(self.secondHeaderBytes)/12)})")

    # the values are intended to be sizes but not all values can be trusted, calculate based off offsets
    def calculateRealSize(self, bufferIdx):
        if bufferIdx % 12 != 0: raise Exception("invalid index") 
        offset = bufferIdx * 12
        curObj = self.getSaveStruct2object(self.secondHeaderBytes[offset:offset+12])
        nexObj = self.getSaveStruct2object(self.secondHeaderBytes[offset+12:offset+24]) # FIXME: will miss if next object is empty
        return nexobj.readIndex - curobj.readIndex

    def dumpSaveStruct2SectionsToFile(self):
        pass


    def verify_pak_header(self):
        return self.header == 'AMS' # sacred underworld 2.28 emits this

    def print_pak(self):
        print("pak print start:")

        success = True

        success |= self.verify_pak_header()
        print(f"header %s ({self.header})" % ("OK" if success else "fail"))

        print(f"save date: {self.date}")

        print(f"saveStruct2:")
        self.dumpSaveStruct2();

