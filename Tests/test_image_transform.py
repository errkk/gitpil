from tester import *

from PIL import Image

AFFINE = Image.AFFINE
EXTENT = Image.EXTENT
PERSPECTIVE = Image.PERSPECTIVE
QUAD = Image.QUAD
MESH = Image.MESH

seq = tuple(range(10))

def test_sanity():

    im = lena()

    assert_no_exception(lambda: im.transform((100, 100), AFFINE, seq[:6]))
    assert_no_exception(lambda: im.transform((100, 100), EXTENT, seq[:4]))
    assert_no_exception(lambda: im.transform((100, 100), PERSPECTIVE, seq[:8]))
    assert_no_exception(lambda: im.transform((100, 100), QUAD, seq[:8]))
    assert_no_exception(lambda: im.transform((100, 100), MESH, [(seq[:4], seq[:8])]))

    # see test_imagetransform for transform object tests
