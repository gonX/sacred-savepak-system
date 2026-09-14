#!/usr/bin/env python

PAKNAME="example.pak"

import SacredPak as sp

if __name__ == "__main__":
    with sp.SacredPak(PAKNAME) as i:
        if not (i.verify_pak_header()):
            print("not a valid pak?")
            exit(1)
        i.print_pak()
