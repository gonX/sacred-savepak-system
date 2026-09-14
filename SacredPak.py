import struct
import datetime as dt

import SacredSaveStruct2

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
        self.sss2 = SacredSaveStruct2.SacredSaveStruct2(self.openedPak.read(0x300))
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

    def verify_pak_header(self):
        return self.header == 'AMS' # sacred underworld 2.28 emits this

    def print_pak(self):
        print("pak print start:")

        success = True

        success |= self.verify_pak_header()
        print(f"header %s ({self.header})" % ("OK" if success else "fail"))

        print(f"save date: {self.date}")

        print(f"saveStruct2:")
        self.sss2.dumpSaveStruct2();
