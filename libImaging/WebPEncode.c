/*
 * The Python Imaging Library.
 * $Id$
 *
 * encoder for WebP data
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
#include "webp/encode.h"

int
ImagingWebPEncode(Imaging im, ImagingCodecState state, UINT8* buf, int bytes)
{
    WEBPCONTEXT* context = (WEBPCONTEXT*) state->context;

    UINT8* buffer;
    UINT8* ptr;
    int y, stride;
    float quality = 75.0F;

    if (!state->state) {
	/* copy image contents to packed buffer and compress it */

	stride = state->xsize * 3;
	buffer = malloc(im->ysize * stride);
	if (!buffer) {
	    state->errcode = IMAGING_CODEC_MEMORY;
	    return -1;
	}

	for (ptr = buffer, y = 0; y < state->ysize; ptr += stride, y++) {
	    state->shuffle(ptr, (UINT8*) im->image[y + state->yoff] +
			   state->xoff * im->pixelsize, state->xsize);
	}

	if (context->quality > 0)
	    quality = (float) context->quality;

	context->output_size = WebPEncodeRGB(buffer,
					     state->xsize, state->ysize,
					     stride, quality,
					     &context->output_data);

	free(buffer);

	if (!context->output_size) {
	    state->errcode = IMAGING_CODEC_BROKEN;
	    return -1;
	}

	state->state++;

	/* keep a pointer to the full buffer */
	context->output_buffer = context->output_data;

    }

    if (context->output_size < bytes) {
	/* copy remaining part to output buffer */
        memcpy(buf, context->output_data, context->output_size);
	state->errcode = IMAGING_CODEC_END;
	free(context->output_buffer);
	return context->output_size;
    } else {
	/* not enough space; fill the buffer and try again next time */
	memcpy(buf, context->output_data, bytes);
	context->output_data += bytes;
	context->output_size -= bytes;
	return bytes;
    }
}

#endif
