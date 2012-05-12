from tester import *

from PIL import Image

def test_sanity():

    data = lena().tostring()
    assert_true(isinstance(data, str))
