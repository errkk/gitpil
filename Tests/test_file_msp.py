from tester import *

from PIL import Image

def test_sanity():

    file = tempfile("temp.msp")

    assert_no_exception(lambda: lena("1").save(file))
    assert_exception(IOError, lambda: lena("L").save(file))

    lena("1").save(file)

    im = Image.open(file)
    im.load()
    assert_equal(im.mode, "1")
    assert_equal(im.size, (128, 128))
    assert_equal(im.format, "MSP")
