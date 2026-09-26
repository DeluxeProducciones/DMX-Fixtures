"""One two-colour tile as PNG bytes, with nothing but the standard library."""

import struct
import zlib

from png_chunk import png_chunk

SIZE = 500
# The diagonal the old Photoshop artboards drew: x + y = 499 in pixel
# coordinates, measured on the exported tiles (half coverage at x = 498 - y).
DIAGONAL = 499


def tile_png(first: tuple[int, int, int], second: tuple[int, int, int]) -> bytes:
    """`first` fills the top-left half, `second` the bottom-right, anti-aliased."""
    rows = bytearray()
    for y in range(SIZE):
        rows.append(0)
        for x in range(SIZE):
            room = DIAGONAL - (x + y)
            if room <= 0:
                cover = 0.0
            elif room >= 2:
                cover = 1.0
            elif room <= 1:
                cover = room * room / 2
            else:
                cover = 1 - (2 - room) * (2 - room) / 2
            rows += bytes(round(a * cover + b * (1 - cover)) for a, b in zip(first, second, strict=True))
            rows.append(255)

    header = struct.pack(">IIBBBBB", SIZE, SIZE, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", header)
        + png_chunk(b"IDAT", zlib.compress(bytes(rows), 9))
        + png_chunk(b"IEND", b"")
    )
