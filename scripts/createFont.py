#!/usr/bin/env python
import fontforge
import os.path

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
  font.save("test.sfd")
  return font

def createNamedChar(charName):
  print("     -> creating "+charName)
  glyph = font.createMappedChar(charName)
  glyph.importOutlines(glyphPath+charName+".svg")

def processGlyphList():
  for line in open(glyphlist):
    li=line.strip()
    if not li.startswith("#"):
      char = line.split(";")
      if os.path.isfile("../glyphs/"+char[0]+".svg"):
        createNamedChar(char[0])


#Main
print "Creating the new font empty"
#font = fontforge.open("blank.sfd")
font = createFont()

print "Process glyphs"
processGlyphList()

font.generate(buildPath+fontname+".ttf")