#!/usr/bin/env python
#
# dump sections from pak to folder (atm only reads the sections but does not do anything with them)

import os
import zlib

import SacredPak as sp
import SacredSaveStruct2 as sss2

PAKNAME="example.pak"
DEBUG=True

if __name__ == "__main__":
    with sp.SacredPak(PAKNAME) as i:
        if not (i.verify_pak_header()):
            print("not a valid pak?")
            exit(1)
        if not os.path.isdir("dump"):
            os.mkdir("dump")
        for (idx, rawObj) in i.sss2.getSaveStruct2objects():
            objData = i.sss2.getSaveStruct2object(rawObj)
            realSize = i.sss2.calculateRealSize(idx)
            reportedSize = objData['value']
            if DEBUG and realSize == -1:
                print(f"DEBUG: could not get real size for object at offset {idx}, maybe end of buffer follows?")
                realSize = reportedSize
            elif DEBUG and realSize != objData["value"] and not str(objData["idStr"]).endswith("_C"): # don't report for compressed objects, value is decompressed size
                print(f"DEBUG: spoofed size for object at offset {idx}, {objData['idStr']}: actual {realSize} but file said {reportedSize}")
            with open(f"dump/{objData['idStr']}.bin", "wb+") as fp:
                i.openedPak.seek(objData['readIndex'])
                if not str(objData['idStr']).endswith('_C'):
                    fp.write(i.openedPak.read(realSize))
                    print(f"Wrote {realSize} bytes to {fp.name}")
                else: # compressed
                    i.openedPak.seek(i.openedPak.tell()+0x20) # first 32 bytes are something else afaict
                    decompressedBuffer = zlib.decompress(i.openedPak.read(realSize))
                    fp.write(decompressedBuffer)
                    print(f"Wrote {len(decompressedBuffer)} decompressed bytes (compressed {realSize}) to {fp.name}") #TODO: make this use proper name when decompressed
