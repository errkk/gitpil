#
# The Python Imaging Library.
# $Id$
#
# portability layer for Python 2.X
#
# history:
# 2011-01-05 fl   Created
#
# Copyright (c) 2011 by Secret Labs AB
# Copyright (c) 2011 by Fredrik Lundh
#
# See the README file for information on usage and redistribution.
#

import struct

try:
    basestring
except NameError:
    def isStringType(t):
        return isinstance(t, str) or isinstance(t, unicode)
else:
    def isStringType(t):
        return isinstance(t, basestring)


from operator import isNumberType

##
# (Internal) Checks if an object is a tuple.

def isTupleType(t):
    return isinstance(t, tuple)

##
# (Internal) Checks if an object is callable.

def isCallable(f):
    return callable(f)

##
# Simple byte array type.

class ByteArray(object):

    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        return ByteArray(self.data + other.data)

    def __getitem__(self, i):
        return ord(self.data[i])

    def find(self, p):
        return self.data.find(p)

    def __getslice__(self, i, j):
        return ByteArray(self.data[i:j])

    def startswith(self, s):
        return self.data[:len(s)] == s

    def tostring(self):
        return self.data

    def unpack(self, fmt, i=0):
        try:
            n = struct.calcsize(fmt)
            v = struct.unpack(fmt, self.data[i:i+n])
        except struct.error, v:
            raise ValueError(v)
        if len(v) == 1:
            v = v[0] # singleton
        return v

##
# File wrapper for new-style binary readers.  This treats the
# file header as a stream of byte arrays.
#
# @param fp File handle.  Must implement a <b>read</b> method.
# @param filename Name of file, if known.

class BinaryFileWrapper(object):

    def __init__(self, fp, filename, safesize):
        def copy(attribute):
            value = getattr(fp, attribute, None)
            if value is not None:
                setattr(self, attribute, value)
        copy('seek')
        copy('tell')
        copy('fileno')
        self.fp = fp
        self.name = filename
        self.safesize = safesize

    def get(self, fmt):
        # FIXME: rename?
        # FIXME: move unpack functionality into wrapper?
        return self.read(struct.calcsize(fmt)).unpack(fmt)

    def read(self, size):
        return ByteArray(self.fp.read(size))

    def saferead(self, size):
        return ByteArray(_safe_read(self.fp, size, self.safesize))

##
# File wrapper for old-style text stream readers.  This treats the
# file header as a stream of (ISO-8859-1) text strings.
#
# @param fp File handle.  Must implement a <b>read</b> method.
# @param filename Name of file, if known.

class TextFileWrapper(object):

    def __init__(self, fp, filename, safesize):
        def copy(attribute):
            value = getattr(fp, attribute, None)
            if value is not None:
                setattr(self, attribute, value)
        copy('read')
        copy('seek')
        copy('tell')
        copy('fileno')
        self.fp = fp
        self.name = filename
        self.safesize = safesize

    def readline(self, size=None):
        # always use safe mode
        if size is None:
            size = self.safesize
        return _safe_readline(self.fp, size, self.safesize)

    def saferead(self, size):
        return _safe_read(self.fp, size, self.safesize)

    def safereadline(self, size):
        return _safe_readline(self.fp, size, self.safesize)

##
# (Internal) Reads large blocks in a safe way.  Unlike fp.read(n),
# this function doesn't trust the user.  If the requested size is
# larger than safesize, the file is read block by block.
#
# @param fp File handle.  Must implement a <b>read</b> method.
# @param size Number of bytes to read.
# @param safesize Max safe block size.
# @return A string containing up to <i>size</i> bytes of data.

def _safe_read(fp, size, safesize):
    if size <= 0:
        return ""
    if size <= safesize:
        return fp.read(size)
    data = []
    while size > 0:
        block = fp.read(min(size, safesize))
        if not block:
            break
        data.append(block)
        size = size - len(block)
    return "".join(data)

##
# (Internal) Safe (and slow) readline implementation.
# <p>
# Note: Codecs that mix line and binary access should be rewritten to
# use an extra buffering layer.
#
# @param fp File handle.  Must implement a <b>read</b> method.
# @param size Max number of bytes to read.
# @param safesize Max safe block size (not used in current version).
# @return A string containing up to <i>size</i> bytes of data,
#   including the newline, if found.

def _safe_readline(fp, size, safesize):
    s = ""
    while True:
        c = fp.read(1)
        if not c:
            break
        s = s + c
        if c == "\n" or len(s) >= size:
            break
    return s
