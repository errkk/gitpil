#
# The Python Imaging Library.
# $Id$
#
# portability layer
#
# history:
# 2011-01-05 fl   Created
#
# Copyright (c) 2011 by Secret Labs AB
# Copyright (c) 2011 by Fredrik Lundh
#
# See the README file for information on usage and redistribution.
#

import sys

if sys.version_info < (3, 0):
    from ImageSupport2 import *
else:
    from ImageSupport3 import *
