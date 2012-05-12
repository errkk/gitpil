/*
 * The Python Imaging Library.
 *
 * compatibility macros for the Python bindings
 *
 * history:
 * 2011-01-10 fl   Created
 *
 * Copyright (c) 1997-2011 by Secret Labs AB 
 * Copyright (c) 1995-2011 by Fredrik Lundh
 *
 * See the README file for information on usage and redistribution.
 */

#if PY_VERSION_HEX < 0x01060000
#define PyObject_New PyObject_NEW
#define PyObject_Del PyMem_DEL
#endif

#if PY_VERSION_HEX >= 0x01060000
#if PY_VERSION_HEX  < 0x02020000 || defined(Py_USING_UNICODE)
/* defining this enables unicode support (default under 1.6a1 and later) */
#define HAVE_UNICODE
#endif
#endif

#if PY_VERSION_HEX < 0x02030000
#define PyMODINIT_FUNC DL_EXPORT(void)
#define PyLong_AsUnsignedLongMask PyLong_AsUnsignedLong
#endif

#if PY_VERSION_HEX < 0x02050000
#define Py_ssize_t int
#define lenfunc inquiry
#define ssizeargfunc intargfunc
#define ssizessizeargfunc intintargfunc
#define ssizeobjargproc intobjargproc
#define ssizessizeobjargproc intintobjargproc
#endif

#if PY_VERSION_HEX < 0x02060000
#define Py_TYPE(op) (op)->ob_type
#endif

#if PY_VERSION_HEX < 0x03000000
#define PY2
#define ARG(a,b) a
#else
#define ARG(a,b) b
#define PyIntObject PyLongObject
#define PyInt_Check PyLong_Check
#define PyInt_AsLong PyLong_AsLong
#define PyInt_AS_LONG PyLong_AS_LONG
#define PyInt_FromLong PyLong_FromLong
#define PyStringObject PyBytesObject
#define PyString_Check PyBytes_Check
#define PyString_AsString PyBytes_AsString
#define PyString_AS_STRING PyBytes_AS_STRING
#define PyString_GET_SIZE PyBytes_GET_SIZE
#define PyString_FromString PyBytes_FromString
#define PyString_FromStringAndSize PyBytes_FromStringAndSize
#define _PyString_Resize _PyBytes_Resize
#endif
