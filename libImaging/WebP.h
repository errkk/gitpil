/* WebP.h */

#if PY_VERSION_HEX < 0x02040000
/* Newer versions of Python.h imports this. */
#include <stdint.h>
#endif

/* FIXME: Split CONTEXT into encoder and decoder contexts. */

typedef struct {

    /* CONFIGURATION */

    /* Converter output mode (input to the shuffler).  If empty,
       convert conversions are disabled.  Used when decoding. */
    char rawmode[8+1];

    /* Quality (1-100, 0 means default).  Used when encoding. */
    int quality;

    /* INTERNAL */
    uint8_t* output_data; /* pointer to next data chunk */
    size_t output_size; /* bytes left to copy */

    uint8_t* output_buffer; /* pointer to output data buffer*/

} WEBPCONTEXT;
