#!/usr/bin/env python3
"""Write the entry image to the grader's output directory.

The image is pre-rendered and stored in this repo as entry.png. This
script copies it to <output>/entry.png and verifies the copy
byte-for-byte, so every run produces identical output. Standard library
only, no network, no writes outside the output directory.
"""
import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
CHUNK = 65536
EXPECTED_SIZE = (1024, 1024)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def output_dir():
    """Return the directory the grader wants the entry written to."""
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(os.getcwd(), "output")


def sha256_of(path):
    """Return the hex sha256 digest of the file at `path`."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def png_dimensions(path):
    """Return the (width, height) of a PNG by reading its IHDR chunk.

    Pure stdlib: the PNG signature is 8 bytes, then the IHDR chunk
    holds width and height as big-endian 32-bit integers at offset 16.
    """
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 29 or header[:8] != PNG_SIGNATURE:
        raise SystemExit("entry.png is not a PNG file")
    if header[12:16] != b"IHDR":
        raise SystemExit("entry.png has no IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    return (width, height)


def main():
    """Copy entry.png to the output directory and verify the copy."""
    target_dir = output_dir()
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, "entry.png")
    shutil.copyfile(SOURCE, target)

    source_hash = sha256_of(SOURCE)
    target_hash = sha256_of(target)
    if source_hash != target_hash:
        raise SystemExit("entry.png copy mismatch: hashes differ")

    size = png_dimensions(target)
    if size != EXPECTED_SIZE:
        raise SystemExit(f"unexpected entry.png size: {size}")

    print("entry.png sha256:", target_hash)
    print("entry.png size:", size)


if __name__ == "__main__":
    main()
