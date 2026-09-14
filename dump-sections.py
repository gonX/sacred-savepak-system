#!/usr/bin/env python
#
# dump sections from pak to folder (atm only reads the sections but does not do anything with them)

import SacredPak as sp
import SacredSaveStruct2 as sss2

PAKNAME="example.pak"
DEBUG=True

if __name__ == "__main__":
    with sp.SacredPak(PAKNAME) as i:
        if not (i.verify_pak_header()):
            print("not a valid pak?")
            exit(1)
        for (idx, rawObj) in i.sss2.getSaveStruct2objects():
            objData = i.sss2.getSaveStruct2object(rawObj)
            realSize = i.sss2.calculateRealSize(idx)
            reportedSize = objData['value']
            if DEBUG and realSize == -1:
                print(f"DEBUG: could not get real size for object at offset {idx}, maybe end of buffer follows?")
                realSize = reportedSize
            elif DEBUG and realSize != objData["value"]:
                print(f"DEBUG: spoofed size for object at offset {idx}, {objData['idStr']}: actual {realSize} but file said {reportedSize}")
