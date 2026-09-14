# Sacred Underworld Savepak Decoder

Most other Sacred Gold/Sacred Underworld save readers only work directly on the exported saves (PAX) intended for sharing.

This Python application should help demystify parts of the .PAK format.

## Running

1. Put Sacred Underworld save at `example.pak` in the file root
2. `./main.py`

TODO: support file arguments

Initially this will just dump some information available in this file

## Known save file details

The save file contains a checksum, so directly editing bytes isn't going to work.

Being able to fix up the checksum for an edited file might come later as part of this project.

