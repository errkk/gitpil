from tester import *

from PIL import Image, FontFile, BdfFontFile

filename = "Images/courB08.bdf"

def test_sanity():

    file = open(filename, "rb")
    font = BdfFontFile.BdfFontFile(file)

    assert_true(isinstance(font, FontFile.FontFile))
    assert_equal(len(filter(None, font.glyph)), 190)
