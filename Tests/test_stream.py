from tester import *

from PIL import ImageSupport

def test_binary_stream():

    stream = StringIO("\x00\x01\x02\x03")

    fp = ImageSupport.BinaryFileWrapper(stream, "filename", 2)
    
    fp.seek(0)
    assert_equal(fp.tell(), 0)
    assert_equal(len(fp.read(4)), 4)
    assert_equal(len(fp.read(4)), 0)
    assert_equal(fp.tell(), 4)

    fp.seek(0)
    assert_equal(len(fp.saferead(4)), 4)
    assert_equal(len(fp.saferead(4)), 0)

    # get reads and unpacks
    fp.seek(0)
    assert_equal(fp.get("b"), 0)
    assert_equal(fp.get("b"), 1)
    fp.seek(0)
    assert_equal(fp.get("bbbb"), (0, 1, 2, 3))
    fp.seek(0)
    assert_exception(ValueError, lambda: fp.get("ii"))

    # read should return an object that supports unpack
    fp.seek(0)
    s = fp.read(4)
    assert_equal(s.unpack("b"), 0)
    assert_equal(s.unpack("bbbb"), (0, 1, 2, 3))

    # see test_bytearray for additional tests
