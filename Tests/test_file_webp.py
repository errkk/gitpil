from tester import *

from PIL import Image
from PIL import WebPImagePlugin

codecs = dir(Image.core)

if "webp_decoder" not in codecs or "webp_encoder" not in codecs:
    skip("webp support not available")

def roundtrip(im, **options):
    out = StringIO()
    im.save(out, "WEBP", **options)
    bytes = out.tell()
    out.seek(0)
    im = Image.open(out)
    im.bytes = bytes # for testing only
    return im

def test_sanity():
    # basic identify/read sanity check

    # internal version number
    # assert_match(Image.core.webp_version, "\d+\.\d+\.\d+(\.\d+)?$")

    im = Image.open("Images/lena.webp")
    assert_equal(im.mode, "RGB")
    assert_equal(im.size, (128, 128))
    assert_equal(im.format, "WEBP")

    im.load()

def test_save():
    # save and read back
    im1 = lena()
    im2 = roundtrip(im1)
    assert_equal(im1.mode, im2.mode)
    assert_equal(im1.size, im2.size)

def test_draft():
    # test draft mode
    im = Image.open("Images/lena.webp")
    px = im.getpixel((0, 0))
    im = Image.open("Images/lena.webp")
    im.draft("YCbCr", (256, 256))
    assert_equal(im.mode, "RGB")  # ignored
    assert_equal(im.size, (128, 128))
    im.load()
    assert_equal(im.mode, "RGB")
    assert_equal(im.size, (128, 128))

#     assert_equal(im.mode, "YCbCr")
#     assert_equal(im.size, (128, 128))
#     im.load()
#     assert_equal(im.mode, "YCbCr")
#     assert_equal(im.size, (128, 128))
#     # make sure the codec doesn't read as RGB
#     assert_false(px == im.getpixel((0, 0)))

def test_quality():
    # test saving with different qualities
    im80 = roundtrip(lena(), quality=80)
    im60 = roundtrip(lena(), quality=60)
    im20 = roundtrip(lena(), quality=20)
    assert_true(im20.bytes < im60.bytes < im80.bytes)
