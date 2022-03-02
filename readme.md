# About 

When audio is captured in synthstrom Deluge, whether by resample or from an external source, the device automatically creates a .WAV audio file.

The naming of these files is incremental, and therefore as the device is used it is difficult to know which files are used in which song.

This little script takes care of that task. It parses the XML of all available songs in the "/SONG" folder of the specified path and renames the clips or resamples according to the name of the first song they appear in. All other references in other songs are updated to work correctly.

For its use it is recommended to backup the entire songs and samples before running the scripts. Specifically, changes will be made in the XML of the songs and in:

`/SONGS`
`/SAMPLES/CLIPS`
`/SAMPLES/RESAMPLE`

The operation has been tested with songs from firmware 3.1+ and 4.0beta. However I have only tested with my song library.

**Nota that no changes are made to the KITS**, so keep in mind that **if you have used a clip or resample within a KIT you must rename the XML by hand** if you want to use this tool.

No warranty is given for the use of this tool, try it at your own risk. My recommendation is to make a copy of the SD and test it with the copy, to check that all your songs work correctly.

I hope you find it useful.

# Installation

* Download it: `git clone https://github.com/fidelaznar/deluge_organizer` (or download and save the file from https://raw.githubusercontent.com/fidelaznar/deluge_organizer/master/dorg.py)

* Use it (you need python3 installed): `python dorg.py`

# Usage

~~~~~
usage: dorg.py [-h] [-s] [-i] path

Simple Deluge Helper for Clips Organization

positional arguments:
  path        Path of Deluge Song folder

optional arguments:
  -h, --help  show this help message and exit
  -s          Simulate changes with no HD changes
  -i          Show instrument stats of your songs
~~~~~