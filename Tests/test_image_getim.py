from tester import *

from PIL import Image

def test_sanity():

    im = lena()

    type_repr = repr(type(im.getim()))
    assert_true(type_repr.find("PyCObject") >= 0)

    assert_true(isinstance(im.im.id, (int, long)))

