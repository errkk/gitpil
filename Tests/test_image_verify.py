from tester import *

from PIL import Image
from StringIO import StringIO


def test_verify():

    data = tostring(lena(), "PNG")

    assert_no_exception(lambda: fromstring(data).load())
    assert_no_exception(lambda: fromstring(data).verify())

    data = data[:-100] + "x" + data[-100:]
    assert_exception(Image.VerificationError, lambda: fromstring(data).verify())

    # backwards compatibility
    assert_exception(SyntaxError, lambda: fromstring(data).verify())
