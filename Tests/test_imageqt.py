from tester import *

from PIL import Image
try:
    from PIL import ImageQt
except ImportError, v:
    skip(v)

success()
