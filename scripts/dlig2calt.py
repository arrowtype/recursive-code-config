"""
    A script to change dlig features to calt features, 
    to make code ligatures on by default in Rec Mono for Code.
"""

from fontTools import ttLib
from fontTools.feaLib import builder
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from argparse import ArgumentParser
import pathops


# codeLigs = {} # probably not needed

def dlig2calt(fontPath, inplace=False):

    font = ttLib.TTFont(fontPath)

    # set unit width / tabular width ... assumes the "=" symbol will have a tabular width for any code font
    # 600 for most monospace fonts w/ UPM=1000
    unitWidth = font['hmtx']['equal'][0]

    # make "LIG" glyph
    font['glyf'].__setitem__('LIG', font['glyf']['space'])

    font['hmtx'].__setitem__('LIG', font['hmtx']['space'])

    # set /LIG glyph width to /equal width, not /space, to allow proportional fonts

    # print(font['glyf']._getPhantomPoints('LIG', font['hmtx'].metrics))

    # newPhantomPoints = [(0,0), (600,0), (0, 0), (0, 0)]

    font['glyf']._setCoordinates('LIG', [(0,0), (600,0), (0, 0), (0, 0)], font['hmtx'].metrics)


    # update code ligature widths to be single units with left overhang
    for glyphName in font.getGlyphNames():
        if font['hmtx'][glyphName][0] > unitWidth:

            # only apply this to code ligatures... leave other glyphs as-is, in case they are intentionally proportional (i.e. MONO != 1)
            if ".code" in glyphName:

                # set width to equal sign (e.g. 600), then offset left side to be negative
                oldWidth = font['hmtx'][glyphName][0]
                oldLSB = font['hmtx'][glyphName][1]
                widthDiff = oldWidth - unitWidth
                newLSB = oldLSB - widthDiff
                font['hmtx'].__setitem__(glyphName, (unitWidth, newLSB))

                # Adjust coordinates in glyf table
                coords = font['glyf']._getCoordinatesAndControls(glyphName, font['hmtx'].metrics)[0]
                phantoms = font['glyf']._getPhantomPoints(glyphName, font['hmtx'].metrics)

                # take off last four items of coords to allow adjusted phantoms to be handled separately, then combined
                coords = coords[:len(coords)-4]

                adjustedCoords = [(x-widthDiff, y) for x, y in coords]
                adjustedPhantoms = [(0,0), (600,0), phantoms[-2], phantoms[-1]]

                newCoords = adjustedCoords+adjustedPhantoms
                font['glyf']._setCoordinates(glyphName, newCoords, font['hmtx'].metrics)


    # add new feature code, using calt rather than dlig
    builder.addOpenTypeFeatures(font,"font-data/features/calt-generated--code_fonts_only.fea")


    # save font
    if inplace:
        font.save(fontPath)
        print("\nCode ligatures are now on by default.\n")
    else:
        newPath = fontPath.replace('.ttf','.calt_ligs.ttf')
        font.save(newPath)
        print("Saved font with feature 'dlig' changed to 'calt' at ", newPath)


def main():
  description = "Change dlig features to calt features."
  parser = ArgumentParser(description=description)
  parser.add_argument('font', nargs=1)
  parser.add_argument('--inplace', action='store_true')
  args = parser.parse_args()

  dlig2calt(args.font[0], args.inplace)


if __name__ == '__main__':
    main()
