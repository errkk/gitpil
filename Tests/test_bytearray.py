from tester import *

from PIL import ImageSupport

def data(s):
    # portably convert string to raw bytes object
    return s.encode("iso-8859-1")

def test_array():

    array = ImageSupport.ByteArray(data("\x00\x01\x02\x03"))

    assert_true(array)
    assert_equal(len(array), 4)
    assert_equal(len(array+array), 8)

    # assert_exception(IndexError, lambda: array[-1]) ???
    assert_equal(array[0], 0x00)
    assert_equal(array[3], 0x03)
    assert_exception(IndexError, lambda: array[4])

    assert_equal(array[1:3].tostring(), "\x01\x02")

    assert_equal(array.find("\x03"), 3)
    assert_equal(array.find("\x04"), -1)

    assert_true(array.startswith("\x00"))
    assert_false(array.startswith("\x01"))

    assert_equal(array[:1].tostring(), "\x00")
    assert_equal(array[3:].tostring(), "\x03")

    assert_equal(array.unpack("b"), 0)
    assert_equal(array.unpack("b", 3), 3)
    assert_equal(array.unpack("bbbb"), (0, 1, 2, 3))
    assert_exception(ValueError, lambda: array.unpack("ii"))

