"""One PNG chunk: length, type, data and its CRC."""

import struct
import zlib


def png_chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
