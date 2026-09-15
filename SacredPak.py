import struct
import datetime as dt

from SacredSaveStruct2 import SacredSaveStruct2 as sss2
import Helper

class SacredPak:
    # TODO: barrier functions that require __enter__() to have run so that we dont get weird uninitialized errors
    FIRST_SECTION_BYTES = 0x100

    HEADER_SLICE = 3

    DATE_OFFSET = 0x5c
    DATE_FORMAT_STRUCT = "iiiiiiii" # y/m/d/wd/h/m/s/ms
    DATE_END = DATE_OFFSET + struct.calcsize(DATE_FORMAT_STRUCT)

    CHECKSUM_MAGIC = 0x95
    CHECKSUM_C1_STARTVALUE_MAGIC = 0xABCD1234
    CHECKSUM_C2_STARTVALUE_MAGIC = 0x1234ABCD

    def __init__(self, pakName):
        self.pakName = pakName

    def __enter__(self):
        self.openedPak = open(self.pakName, "rb")
        self.firstHeaderBytes = self.openedPak.read(self.FIRST_SECTION_BYTES)
        self.sss2 = sss2(self.openedPak.read(sss2.EXPECTED_SIZE))
        self.openedPak.seek(0, 2) # SEEK_END
        self.openedPakSize = self.openedPak.tell()
        self.openedPak.seek(0)
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

    def calculate_true_checksum(self):
        magic = self.CHECKSUM_MAGIC
        c1 = self.CHECKSUM_C1_STARTVALUE_MAGIC
        c2 = 0
        c3 = self.CHECKSUM_C2_STARTVALUE_MAGIC
        i = self.FIRST_SECTION_BYTES
        while (i <= self.openedPakSize): # TODO: might be off-by-one
            # FIXME: not quite working as intended - first iteration is correct
            # but tracing this with gdb gives odd results where some iterations
            # do not change the state in gdb (where they do here)
            print(f"iter: {i}: {c1:#x} {c2:#x} {c3:#x}")
            input()
            loop_magic = (magic + i) & 0xFF
            c1 = (c1 ^ Helper.repackIntTo4Bytes(loop_magic)) & 0xFFFFFFFF
            c2 = (c2 ^ loop_magic) & 0xFFFFFFFF
            c3 = (c3 + loop_magic) & 0xFFFFFFFF
            i += 1
        c4 = c2 ^ c3
        return [c1, c2, c3, c4]

    def getChecksum(self):
        return list(struct.unpack('IIIIII', self.firstHeaderBytes[0xe8:0x100]))

    def verify_pak_header(self):
        return self.header == 'AMS' # sacred underworld 2.28 emits this

    def verify_checksum(self):
        """checksum format:
                # main checksum
                checksum0 = foo;
                checksum1 = bar;
                checksum2 = baz;
                checksum3 = bar ^ baz;
                # rng-seeded checksum:
                checksum4 = 1 + 0x270e * (rand() * (float)0x30000000)
                checksum5 = checksum4 ^ checksum1
        """
        checksums = self.getChecksum()

        if not checksums[5] == (checksums[4] ^ checksums[1]):
            print("rng checksum mismatch") # TODO: remove print statement closer to release (or use debug logging)
            return False

        print(Helper.intListToHexStrings(checksums))
        #print(Helper.intListToHexStrings(self.calculate_true_checksum()))
        print("base checksum check unimplemented")
        return False # TODO: verify main checksum
        return True

    def print_pak(self):
        success = True

        verify_pak_header_result = self.verify_pak_header()
        success &= verify_pak_header_result
        print(f"header %s ({self.header})" % ("OK" if verify_pak_header_result else "fail"))

        print(f"save date: {self.date}")

        self.sss2.dumpSaveStruct2();

        checksum_result = self.verify_checksum()
        print(f"checksum %s" % ("OK" if checksum_result else "fail"))
        success &= checksum_result
