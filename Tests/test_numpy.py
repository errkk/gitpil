from tester import *

from PIL import Image

try:
    import site
    import numpy
except ImportError:
    skip()

import sys

def test_numpy_to_image():

    def to_image(dtype, bands=1, bool=0):
        if bands == 1:
            if bool:
                data = [0, 1] * 50
            else:
                data = range(100)
            a = numpy.array(data, dtype=dtype)
            a.shape = 20, 5
            i = Image.fromarray(a)
            if list(i.getdata()) != data:
                print "data mismatch for", dtype
        else:
            data = range(100)
            a = numpy.array([[x]*bands for x in data], dtype=dtype)
            a.shape = 20, 5, bands
            i = Image.fromarray(a)
            if list(i.split()[0].getdata()) != range(100):
                print "data mismatch for", dtype
        return i

    # assert_image(to_image(numpy.bool, bool=1), "1", (5, 20))
    # assert_image(to_image(numpy.bool8, bool=1), "1", (5, 20))

    assert_exception(TypeError, lambda: to_image(numpy.uint))
    assert_image(to_image(numpy.uint8), "L", (5, 20))
    assert_exception(TypeError, lambda: to_image(numpy.uint16))
    assert_exception(TypeError, lambda: to_image(numpy.uint32))
    assert_exception(TypeError, lambda: to_image(numpy.uint64))

    if sys.maxint <= 2**32:
        # PIL doesn't support int64 modes yet
        assert_image(to_image(int), "I", (5, 20))
        assert_image(to_image(numpy.int), "I", (5, 20))

    assert_image(to_image(numpy.int8), "I", (5, 20))
    assert_image(to_image(numpy.int16), "I;16", (5, 20))
    assert_image(to_image(numpy.int32), "I", (5, 20))
    assert_exception(TypeError, lambda: to_image(numpy.int64))

    assert_image(to_image(float), "F", (5, 20))
    assert_image(to_image(numpy.float), "F", (5, 20))
    assert_image(to_image(numpy.float32), "F", (5, 20))
    assert_image(to_image(numpy.float64), "F", (5, 20))

    assert_image(to_image(numpy.uint8, 3), "RGB", (5, 20))
    assert_image(to_image(numpy.uint8, 4), "RGBA", (5, 20))

def test_numpy_from_image():

    def from_image(mode):
        i = Image.new(mode, (5, 20))
        i.putdata(range(100))
        return numpy.asarray(i)

    def assert_array(a, dtype, bands=None):
        # FIXME: verify content as well
        shape = (20, 5)
        if bands:
            shape += (bands,)
        assert_equal(a.dtype, dtype)
        assert_equal(a.shape, shape)

    assert_array(from_image("L"), numpy.uint8)
    assert_array(from_image("I"), numpy.int32)
    assert_array(from_image("F"), numpy.float32)
    assert_array(from_image("RGB"), numpy.uint8, 3)
    assert_array(from_image("RGBA"), numpy.uint8, 4)
    assert_array(from_image("RGBX"), numpy.uint8, 4)
    assert_array(from_image("CMYK"), numpy.uint8, 4)
    assert_array(from_image("YCbCr"), numpy.uint8, 3)


