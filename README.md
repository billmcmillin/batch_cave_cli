## batch_cave_cli

A command-line interface version of batch_cave in Python3.

## Changes
* Syntax: print changed to fucntion version

* Iterables: keys dict had to be transformed with list(dict(...

* Utilites pulled out into a separate module, requiring file names to be passed
explicitly to certain functions.

## MarcEditBreakFile now BreakMarcFile
* MarcEdit has been replaced by PyMarc
