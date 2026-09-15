# Sacred Underworld Savepak Decoder

Most other Sacred Gold/Sacred Underworld save readers only work directly on the exported saves (PAX) intended for sharing.

This Python application should help demystify parts of the .PAK format.

## Running

1. Put Sacred Underworld save at `example.pak` in the file root
2. `./main.py`

TODO: support file arguments

Initially this will just dump some information available in this file

## Known save file details

### Checksum

The save file contains a checksum, so directly editing bytes beyond the first 256 bytes isn't going to work.

The checksum bytes are placed at the last 48 bytes of the first 256 bytes, of which these 48 bytes are:
- 4x 8 bytes contains the main checksum - they have a simple algorithm run over them based on the entire remaining contents of the save file
- the last 16 bytes are seeded randomly, the first of the 8 contains the seed, and the last of the 8 contains `checksum2 ^ seed`

This is expected to be provided as a part of the programming API

> Being able to fix up the checksum for an edited file might come later as part of this project.

