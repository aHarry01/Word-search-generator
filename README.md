# Word Search Generator

Program that generates word searches from a file of input words, and formats a pdf output. Currently the wordsearch size is locked at 17x17 letters. Wordsearch generation should work with any size grid, but the output formatting needs to be adjusted so that it will automatically fit on the page.

## Dependencies: 
* [Python 3.xx](https://www.python.org/downloads/)
* [ReportLab](https://www.reportlab.com/dev/opensource/rl-toolkit/)
* [Pillow (7.2)](https://pillow.readthedocs.io/en/stable/)

## Usage:
After installing dependencies, run wordsearch.py. It will ask for some parameters, but the word input filename is the only necessary paremeter. Word input must be a list of words separated by newlines. The words can have spaces in them. If a word couldn't fit in the word search, it will print out a message saying it couldn't insert that word, but will still make a pdf with the other words. Default PDF output filename is output.pdf. Default PDF title is no title. Default background image is plain white.

## License
Licensed under MIT license.
