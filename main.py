#!/usr/bin/env python3
"""Ship the finished news image to the grader's output folder.

The picture itself is already rendered and checked into this repository
as entry.png. All this script does is place a copy of it where the
grader expects it, then prove the copy is intact: same bytes, same
dimensions. Only the Python standard library is used, and nothing is
downloaded or written outside the chosen output folder.
"""

import hashlib
import os
import shutil
import struct

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "entry.png"
IMAGE_PATH = os.path.join(BASE_DIR, IMAGE_NAME)
READ_SIZE = 65536
WANTED_DIMS = (1024, 1024)
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def find_output_folder():
    """Pick where the entry goes: env var first, then /output, else ./output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return chosen
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.getcwd(), "output")


def file_sha256(path):
    """Hash a file in chunks and return its hex digest."""
    hasher = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            piece = stream.read(READ_SIZE)
            if not piece:
                break
            hasher.update(piece)
    return hasher.hexdigest()


def read_png_size(path):
    """Read a PNG's width and height straight from its IHDR chunk.

    A PNG starts with an 8-byte signature, then a 4-byte length, the
    4-byte chunk name "IHDR", and the width/height as two big-endian
    unsigned 32-bit numbers. That puts both numbers at bytes 16..24.
    """
    with open(path, "rb") as stream:
        head = stream.read(33)
    if len(head) < 29 or head[:8] != PNG_MAGIC:
        raise SystemExit("entry.png does not look like a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit("entry.png is missing its IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def run():
    """Copy the image out and check the copy before finishing."""
    folder = find_output_folder()
    os.makedirs(folder, exist_ok=True)
    destination = os.path.join(folder, IMAGE_NAME)
    shutil.copyfile(IMAGE_PATH, destination)

    original_hash = file_sha256(IMAGE_PATH)
    copied_hash = file_sha256(destination)
    if original_hash != copied_hash:
        raise SystemExit("copied entry.png failed its hash check")

    dims = read_png_size(destination)
    if dims != WANTED_DIMS:
        raise SystemExit("entry.png has the wrong size: %s" % (dims,))

    print("entry.png sha256:", copied_hash)
    print("entry.png size:", dims)


if __name__ == "__main__":
    run()
