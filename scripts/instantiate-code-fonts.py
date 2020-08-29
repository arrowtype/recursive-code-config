"""
    A script to generate Recursive fonts for code with Regular, Italic, Bold, & Bold Italic,
    as configured in config.yaml. See Readme for usage instructions.

    Run from the directory above, e.g.

    python3 scripts/instantiate-code-fonts.py
"""

import os
import pathlib
from fontTools import ttLib
from fontTools.varLib import instancer
from opentype_feature_freezer import cli as pyftfeatfreeze
import subprocess
import shutil
from dlig2calt import dlig2calt
import yaml
import sys
import logging

# prevents over-active warning logs
logging.getLogger("opentype_feature_freezer").setLevel(logging.ERROR)

# if you provide a custom config path, this picks it up
try:
    configPath = sys.argv[1]
except IndexError:
    configPath = './config.yaml'

# read yaml config
with open(configPath) as file:
    fontOptions = yaml.load(file, Loader=yaml.FullLoader)

# GET / SET NAME HELPER FUNCTIONS

def getFontNameID(font, ID, platformID=3, platEncID=1):
    name = str(font["name"].getName(ID, platformID, platEncID))
    return name


def setFontNameID(font, ID, newName):

    print(f"\n\t• name {ID}:")
    macIDs = {"platformID": 3, "platEncID": 1, "langID": 0x409}
    winIDs = {"platformID": 1, "platEncID": 0, "langID": 0x0}

    oldMacName = font["name"].getName(ID, *macIDs.values())
    oldWinName = font["name"].getName(ID, *winIDs.values())

    if oldMacName != newName:
        print(f"\t\t Mac name was '{oldMacName}'")
        font["name"].setName(newName, ID, *macIDs.values())
        print(f"\t\t Mac name now '{newName}'")

    if oldWinName != newName:
        print(f"\t\t Win name was '{oldWinName}'")
        font["name"].setName(newName, ID, *winIDs.values())
        print(f"\t\t Win name now '{newName}'")


# ----------------------------------------------
# MAIN FUNCTION

oldName = "Recursive"

fontPath = "./font-data/Recursive_VF_1.062.ttf"

def splitFont(
        outputDirectory=f"RecMono{fontOptions['Family Name']}",
        newName="Rec Mono",
):

    # access font as TTFont object
    varfont = ttLib.TTFont(fontPath)

    fontFileName = os.path.basename(fontPath)


    outputSubDir = f"fonts/{outputDirectory}"

    for instance in fontOptions["Fonts"]:

        print("\n--------------------------------------------------------------------------------------\n" + instance)

        instanceFont = instancer.instantiateVariableFont(
            varfont,
            {
                "wght": fontOptions["Fonts"][instance]["wght"],
                "CASL": fontOptions["Fonts"][instance]["CASL"],
                "MONO": fontOptions["Fonts"][instance]["MONO"],
                "slnt": fontOptions["Fonts"][instance]["slnt"],
                "CRSV": fontOptions["Fonts"][instance]["CRSV"],
            },
        )

        # UPDATE NAME ID 6, postscript name
        currentPsName = getFontNameID(instanceFont, 6)
        newPsName = (currentPsName\
            .replace("Sans", "")\
            .replace(oldName,newName.replace(" ", "") + fontOptions['Family Name'].replace(" ",""))\
            .replace("LinearLight", instance.replace(" ", "")))
        setFontNameID(instanceFont, 6, newPsName)

        # UPDATE NAME ID 4, full font name
        currentFullName = getFontNameID(instanceFont, 4)
        newFullName = (currentFullName\
            .replace("Sans", "")\
            .replace(oldName, newName + " " + fontOptions['Family Name'])\
            .replace(" Linear Light", instance))\
            .replace(" Regular", "")
        setFontNameID(instanceFont, 4, newFullName)

        # UPDATE NAME ID 3, unique font ID
        currentUniqueName = getFontNameID(instanceFont, 3)
        newUniqueName = (currentUniqueName.replace(currentPsName, newPsName))
        setFontNameID(instanceFont, 3, newUniqueName)

        # ADD name 2, style linking name
        newStyleLinkingName = instance
        setFontNameID(instanceFont, 2, newStyleLinkingName)
        setFontNameID(instanceFont, 17, newStyleLinkingName)

        # UPDATE NAME ID 1, Font Family name
        currentFamName = getFontNameID(instanceFont, 1)
        newFamName = (newFullName.replace(f" {instance}", ""))
        setFontNameID(instanceFont, 1, newFamName)
        setFontNameID(instanceFont, 16, newFamName)

        newFileName = fontFileName\
            .replace(oldName, (newName + fontOptions['Family Name']).replace(" ", ""))\
            .replace("_VF_", "-" + instance.replace(" ", "") + "-")

        # make dir for new fonts
        pathlib.Path(outputSubDir).mkdir(parents=True, exist_ok=True)

        # -------------------------------------------------------
        # OpenType Table fixes

        # drop STAT table to allow RIBBI style naming & linking on Windows
        del instanceFont["STAT"]

        # In the post table, isFixedPitched flag must be set in the code fonts
        instanceFont['post'].isFixedPitch = 1

        # In the OS/2 table Panose bProportion must be set to 9
        instanceFont["OS/2"].panose.bProportion = 9

        # Also in the OS/2 table, xAvgCharWidth should be set to 600 rather than 612 (612 is an average of glyphs in the "Mono" files which include wide ligatures).
        instanceFont["OS/2"].xAvgCharWidth = 600

        if instance == "Italic":
            instanceFont['OS/2'].fsSelection = 0b1
            instanceFont["head"].macStyle = 0b10
            # In the OS/2 table Panose bProportion must be set to 11 for "oblique boxed" (this is partially a guess)
            instanceFont["OS/2"].panose.bLetterForm = 11

        if instance == "Bold":
            instanceFont['OS/2'].fsSelection = 0b100000
            instanceFont["head"].macStyle = 0b1

        if instance == "Bold Italic":
            instanceFont['OS/2'].fsSelection = 0b100001
            instanceFont["head"].macStyle = 0b11

        # -------------------------------------------------------
        # save instance font

        outputPath = f"{outputSubDir}/{newFileName}"

        # save font
        instanceFont.save(outputPath)

        # -------------------------------------------------------
        # Code font special stuff in post processing

        # freeze in rvrn features with pyftfeatfreeze: serifless 'f', unambiguous 'l', '6', '9'
        pyftfeatfreeze.main([f"--features=rvrn,{','.join(fontOptions['Features'])}", outputPath, outputPath])

        if fontOptions['Code Ligatures']:
            # swap dlig2calt to make code ligatures work in old code editor apps
            dlig2calt(outputPath, inplace=True)

splitFont()
