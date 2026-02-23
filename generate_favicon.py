#!/usr/bin/env python3
"""Generate a 32x32 PNG favicon: blue background, white book icon. No deps (stdlib only). Saves as favicon.png."""

import zlib
import struct

SIZE = 32
BLUE = (0, 122, 255)
WHITE = (255, 255, 255)


def png_pack(png_tag, data):
    chunk_head = png_tag + data
    return (
        struct.pack("!I", len(data))
        + chunk_head
        + struct.pack("!I", 0xFFFFFFFF & zlib.crc32(chunk_head))
    )


def write_png(buf, width, height):
    width_byte_4 = width * 4
    raw_data = b"".join(
        b"\x00" + buf[span : span + width_byte_4]
        for span in range((height - 1) * width * 4, -1, -width_byte_4)
    )
    return b"".join([
        b"\x89PNG\r\n\x1a\n",
        png_pack(b"IHDR", struct.pack("!2I5B", width, height, 8, 6, 0, 0, 0)),
        png_pack(b"IDAT", zlib.compress(raw_data, 9)),
        png_pack(b"IEND", b""),
    ])


def main():
    # RGBA buffer: 32*32*4 bytes
    buf = bytearray(SIZE * SIZE * 4)
    for y in range(SIZE):
        for x in range(SIZE):
            i = (y * SIZE + x) * 4
            r, g, b = BLUE
            buf[i : i + 3] = (r, g, b)
            buf[i + 3] = 255

    # Draw simple white open-book (two rectangles + spine)
    margin = 4
    center = SIZE // 2
    for y in range(margin + 2, SIZE - margin - 2):
        for x in range(margin, center):
            i = (y * SIZE + x) * 4
            buf[i : i + 3] = WHITE
        for x in range(center + 1, SIZE - margin):
            i = (y * SIZE + x) * 4
            buf[i : i + 3] = WHITE
    for y in range(margin + 4, SIZE - margin - 4):
        for dx in (0, 1):
            x = center + dx
            if 0 <= x < SIZE:
                i = (y * SIZE + x) * 4
                buf[i : i + 3] = WHITE

    png_data = write_png(bytes(buf), SIZE, SIZE)
    with open("favicon.png", "wb") as f:
        f.write(png_data)
    print("Saved favicon.png (32x32)")


if __name__ == "__main__":
    main()
