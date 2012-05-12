from tester import *

from PIL import Image
try:
    from PIL import ImageGL
except ImportError, v:
    skip(v)

success()
