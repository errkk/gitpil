#
# The Python Imaging Library.
# $Id$
#
# portability layer for Python 3.X
#
# history:
# 2011-01-05 fl   Created
#
# Copyright (c) 2011 by Secret Labs AB
# Copyright (c) 2011 by Fredrik Lundh
#
# See the README file for information on usage and redistribution.
#

import collections, numbers, struct

def isStringType(t):
    return isinstance(t, str)

def isNumberType(t):
    return isinstance(t, numbers.Number)

def isTupleType(t):
    return isinstance(t, tuple)

def isCallable(t):
    return isinstance(t, collections.Callable)

def str2bytes(s):
    # convert str w. bytes to bytes object
    return s.encode("iso-8859-1")

def bytes2str(b):
    # convert bytes object to str w. bytes
    return b.decode("iso-8859-1")

##
# Simple byte array type.

class ByteArray(object):
    # FIXME: can we inherit from binary type?

    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __add__(self, other):
        return ByteArray(self.data + other.data)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return ByteArray(self.data[i])
        return self.data[i]

    def find(self, p):
        return self.data.find(str2bytes(p))

    def startswith(self, s):
        return self.data[:len(s)] == str2bytes(s)

    def tostring(self):
        return bytes2str(self.data)

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
        return self.read(struct.calcsize(fmt)).unpack(fmt)

    def read(self, size):
        return ByteArray(self.fp.read(size))

    def saferead(self, size):
        return ByteArray(_safe_read(self.fp, size, self.safesize))

##
# File wrapper for old-style text stream readers.  This treats the
# file header as a stream of ISO-8859-1 text strings, with one
# character per byte.
#
# @param fp File handle.  Must implement a <b>read</b> method.
# @param filename Name of file, if known.

class TextFileWrapper(object):

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

    def read(self, size):
        return bytes2str(self.fp.read(size))

    def saferead(self, size):
        return bytes2str(_safe_read(self.fp, size, self.safesize))

    def readline(self, size=None):
        # always use safe mode
        if size is None:
            size = self.safesize
        return bytes2str(_safe_readline(self.fp, size, self.safesize))

    def safereadline(self, size):
        return bytes2str(_safe_readline(self.fp, size, self.safesize))

##
# (Internal) Reads large blocks in a safe way.  Unlike fp.read(n),
# this function doesn't trust the user.  If the requested size is
# larger than safesize, the file is read block by block.
#
# @param fp File handle.  Must implement a <b>read</b> method.
# @param size Number of bytes to read.
# @param safesize Max safe block size.
# @return A buffer containing up to <i>size</i> bytes of data.

def _safe_read(fp, size, safesize):
    if size <= 0:
        return b""
    if size <= safesize:
        return fp.read(size)
    data = []
    while size > 0:
        block = fp.read(min(size, safesize))
        if not block:
            break
        data.append(block)
        size = size - len(block)
    return b"".join(data)

##
# (Internal) Safe (and slow) readline implementation.
# <p>
# Note: Codecs that mix line and binary access should be rewritten to
# use an extra buffering layer.
#
# @param fp File handle.  Must implement a <b>read</b> method.
# @param size Max number of bytes to read.
# @param safesize Max safe block size (not used in current version).
# @return A buffer containing up to <i>size</i> bytes of data,
#   including the newline, if found.

def _safe_readline(fp, size, safesize):
    s = b""
    while True:
        c = fp.read(1)
        if not c:
            break
        s = s + c
        if c == b"\n" or len(s) >= size:
            break
    return s
