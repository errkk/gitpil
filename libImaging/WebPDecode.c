/*
 * The Python Imaging Library.
 * $Id$
 *
 * WebP decoder
 *
 * history:
 * 2011-06-26 fl  created
 *
 * Copyright (c) Fredrik Lundh 2011.
 *
 * See the README file for information on usage and redistribution.
 */

#include "Imaging.h"

#ifdef HAVE_LIBWEBP

#include "WebP.h"
#include "webp/decode.h"

int
ImagingWebPDecode(Imaging im, ImagingCodecState state, UINT8* buf, int bytes)
{
    WEBPCONTEXT* context = (WEBPCONTEXT*) state->context;

    UINT32 image_size;
    UINT8* image_data;
    int y, xsize, ysize;
    UINT8* p;

    /* wait until we have enough data */

    if (bytes < 8)
        return 0;

    image_size = (buf[4] | (buf[5] << 8) | (buf[6] << 16) | (buf[7] << 24));

    if (bytes < 8 + image_size)
        return 0;

    /* decode and unpack everything in one go */
    if (strcmp(context->rawmode, "RGB") == 0)
        image_data = WebPDecodeRGB(buf, bytes, &xsize, &ysize);
    else {
        /* FIXME: add YCbCr support */
        state->errcode = IMAGING_CODEC_CONFIG;
	return -1;
    }

    if (!image_data) {
        state->errcode = IMAGING_CODEC_BROKEN;
	return -1;
    }

    for (y = 0, p = image_data; y < state->ysize; y++, p += state->xsize*3) {
        state->shuffle((UINT8*) im->image[y + state->yoff] +
		       state->xoff * im->pixelsize, p,
		       state->xsize);
    }

    free(image_data);

    return -1; /* done */
}

#endif
