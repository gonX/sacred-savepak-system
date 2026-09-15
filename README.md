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

One would think that the checksum is actually useful - but in our case it's
not. You can seemingly edit the file without issues - at least I was able to
change the difficulty field of my game and artificially inflate it to whatever
I wanted.

The checksum bytes are placed at the last 48 bytes of the first 256 bytes, of which these 48 bytes are:
- 4x 8 bytes contains the main checksum - they have a simple algorithm run over them based on the entire remaining contents of the save file
- the last 16 bytes are seeded randomly, the first of the 8 contains the seed, and the last of the 8 contains `checksum2 ^ seed`

Unless there is evidence that the checksum is relevant, this project will not further attempt to recover the original checksum.
