#!/usr/bin/env python
import fontforge
import os.path
import re
from os import walk

#Definitions
glyphlist = "../reference/glyphlist.txt"
glyphPath = "../glyphs/"
buildPath = "../build/"
fontname = "ZXSpectrum"
fullname = "ZX Spectrum Unicode"
ascent = 700
descent = 100
em = 800
encoding = "UnicodeBmp"

#Functions
def createFont():
  font = fontforge.font()
  font.fontname = fontname
  font.fullname = fullname
  font.ascent = ascent
  font.descent = descent
  font.em = em
  font.encoding = encoding
  font.save(buildPath+fontname+".sfd")
  return font

def createNamedChar(charName, file):
  print("     -> creating "+charName)
  glyph = font.createMappedChar(charName)
  glyph.importOutlines(file)

def createCodedChar(code, file):
  print("     -> creating U"+code)
  glyph = font.createChar(int(code, 16))
  glyph.importOutlines(file)

def createSpace():
  print("     -> creating Space Character")
  glyph = font.createChar(32)
  glyph.width = em

def processGlyphList():
  for line in open(glyphlist):
    li=line.strip()
    if not li.startswith("#"):
      char = line.split(";")
      if char[0][0].isupper():
        path = glyphPath+"upper/"
      else:
        path = glyphPath+"lower/"
      if os.path.isfile(path+char[0]+".svg"):
        createNamedChar(char[0], path+char[0]+".svg")

def processUnnamedGlyphs():
  filelist = []
  path = glyphPath+"unnamed/"
  for (dirpath, dirnames, filenames) in walk(path):
    filelist.extend(filenames)
  for file in filelist:
    code = re.search('U(.+?).svg', file).group(1)
    createCodedChar(code, path+file)

#Main
print "Creating the new font empty"
#font = fontforge.open("blank.sfd")
font = createFont()

print "Process glyphs"
processGlyphList()
processUnnamedGlyphs()
createSpace()

font.save(buildPath+fontname+".sfd")
font.generate(buildPath+fontname+".ttf")
font.generate(buildPath+fontname+".bdf","bdf")