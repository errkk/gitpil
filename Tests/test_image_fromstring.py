from tester import *

from PIL import Image

def test_sanity():

    im1 = lena()
    im2 = Image.fromstring(im1.mode, im1.size, im1.tostring())

    assert_image_equal(im1, im2)

