#
# The Python Imaging Library.
# $Id$
#
# XV Thumbnail file handler by Charles E. "Gene" Cash
# (gcash@magicnet.net)
#
# see xvcolor.c and xvbrowse.c in the sources to John Bradley's XV,
# available from ftp://ftp.cis.upenn.edu/pub/xv/
#
# history:
# 98-08-15 cec  created (b/w only)
# 98-12-09 cec  added color palette
# 98-12-28 fl   added to PIL (with only a few very minor modifications)
#
# To do:
# FIXME: make save work (this requires quantization support)
#

__version__ = "0.1"

import Image
import ImageFile
import ImagePalette

##
# Image plugin for XV thumbnail images.

class XVThumbImageFile(ImageFile.ImageFile):

    format = "XVThumb"
    format_description = "XV thumbnail image"

    def _open(self):

        # check magic
        s = self.fp.read(6)
        if s != "P7 332":
            raise SyntaxError("not an XV thumbnail file")

        # Skip to beginning of next line
        self.fp.safereadline(512)

        # skip info comments
        while True:
            s = self.fp.safereadline(65536)
            if not s:
                raise SyntaxError("Unexpected EOF reading XV thumbnail file")
            if s[0] != '#':
                break

        # parse header line (already read)
        s = s.split()

        self.mode = "P"
        self.size = int(s[0]), int(s[1])

        self.palette = ImagePalette.raw_rgb332()

        self.tile = [
            ("raw", (0, 0)+self.size,
             self.fp.tell(), (self.mode, 0, 1)
             )]

# --------------------------------------------------------------------

Image.register_open("XVThumb", XVThumbImageFile)
