from tester import *

from PIL import Image
try:
    from PIL import ImageGrab
    Image.core.grabscreen
except (AttributeError, ImportError), v:
    skip(v)

def test_grab():
    im = ImageGrab.grab()
    assert_image(im, im.mode, im.size)


