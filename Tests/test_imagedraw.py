from tester import *

# FIXME: this module needs a lot more tests!

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

def test_sanity():

    im = lena("RGB").copy()

    draw = ImageDraw.ImageDraw(im)
    draw = ImageDraw.Draw(im)

    draw.ellipse(range(4))
    draw.line(range(10))
    draw.polygon(range(100))
    draw.rectangle(range(4))

    success()

def test_deprecated():
    
    im = lena().copy()

    draw = ImageDraw.Draw(im)

    assert_exception(AttributeError, lambda: draw.setink(0))
    assert_exception(AttributeError, lambda: draw.setfill(0))

def test_unicode_text():

    # use replace semantics when using unicode strings with bitmap
    # fonts

    im1 = Image.new("L", (512, 512), "white")
    im2 = Image.new("L", (512, 512), "white")

    font = ImageFont.load_default()

    text = u"-\u263a-"

    ImageDraw.Draw(im1).text((40, 40), text, font=font)
    ImageDraw.Draw(im2).text((40, 40), text.encode("iso-8859-1", "replace"), font=font)

    assert_image_equal(im1, im2)
