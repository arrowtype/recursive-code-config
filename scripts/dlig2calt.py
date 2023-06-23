"""
    A script to change dlig features to calt features, 
    to make code ligatures on by default in Rec Code for Code.
"""

from fontTools import ttLib
from fontTools.feaLib import builder
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from argparse import ArgumentParser
import pathops
import subprocess
import os

def simpleDlig2calt(fontPath, inplace=False):
    """
        A simple way to change a "dlig" feature to "calt."

        Assumes the fontPath hasn’t already been converted to a TTX file,
        as that would confuse the variables below.
    """

    # convert font’s GSUB table to a TTX file
    subprocess.run(["ttx", "-t", "GSUB", fontPath]) 

    # make the path for a ttx
    ttxPath = fontPath.replace(".ttf",".ttx")

    # Read in the TTX file
    with open(ttxPath, 'r', encoding='utf-8') as file:
        ttxData = file.read()

    # Replace the target string to update the dlig feature tags to calt feature tags
    ttxData = ttxData.replace('"dlig"', '"calt"')

    # Write the TTX file out again
    with open(ttxPath, 'w', encoding='utf-8') as file:
        file.write(ttxData)

    # merge TTX back into font:
    # ttx -m fontname.ttf fontname.ttx

    # save font
    if inplace:
        subprocess.run(["ttx", "-f", "-m", fontPath, ttxPath])
        print("\nCode ligatures are now under the calt feature and on by default.\n")
    else:
        newFontPath = fontPath.replace('.ttf','.calt_ligs.ttf')
        subprocess.run(["ttx", "-o", newFontPath, "-m", fontPath, ttxPath])
        print("Saved font with feature 'dlig' changed to 'calt' at ", newFontPath)

    # clean up the temporary TTX file
    os.remove(ttxPath)


def makeCodeLigsMonospace(fontPath, inplace=False):
    """
        Takes code ligatures with different widths, and makes them all exactly one monospace character wide.

        The extra width goes over the left bound, and the space is made up for by a newly-created "LIG" glyph.
    """

    font = ttLib.TTFont(fontPath)

    # set unit width / tabular width ... assumes the "=" symbol will have a tabular width for any code font
    # 600 for most monospace fonts w/ UPM=1000
    unitWidth = font['hmtx']['equal'][0]

    # create the "LIG" glyph to fill in gaps for code ligatures made into single-unit-wide glyphs
    font['glyf'].__setitem__('LIG', font['glyf']['space'])
    font['hmtx'].__setitem__('LIG', font['hmtx']['space'])

    # set /LIG glyph width to /equal width, not /space, to allow proportional fonts
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
        fontPath = fontPath.replace('.ttf','.calt_ligs.ttf')
        font.save(fontPath)
        print("Saved font with feature 'dlig' changed to 'calt' at ", fontPath)


def main():
    description = "Change dlig features to calt features."
    parser = ArgumentParser(description=description)
    parser.add_argument('font', nargs=1)
    parser.add_argument('--inplace', action='store_true')
    parser.add_argument('--mono', '-m', action='store_true')
    args = parser.parse_args()

    if args.mono:
        makeCodeLigsMonospace(args.font[0], args.inplace)
    else:
        simpleDlig2calt(args.font[0], args.inplace)


if __name__ == '__main__':
    main()
