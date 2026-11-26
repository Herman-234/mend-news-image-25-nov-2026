#!/usr/bin/env python3
"""Ship the finished front page.

The grader runs this file. It takes the rendered ``entry.png`` that sits
next to it, drops a copy into the output folder the platform expects, and
checks the copy is exactly the picture we entered: same sha256, same
1024x1024 size taken from the PNG header. Standard library only, so it
runs anywhere with no installs and no network.
"""

import hashlib
import os
import shutil
import struct
import sys

EXPECTED_SHA256 = "756341ebea6e20cf3df45148a745055dfa5f162e1a93b7d37b0757d78b67a9f2"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def pick_output_dir():
    """Where the platform wants the finished image."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        return env_dir
    if os.path.isdir("/output"):
        return "/output"
    return os.path.join(HERE, "output")


def png_dimensions(path):
    """Read width and height out of the PNG IHDR chunk."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    if header[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk first: %s" % path)
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def sha256_of(path):
    """Hex digest of a file, streamed so big files stay cheap."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = pick_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)

    digest = sha256_of(target)
    width, height = png_dimensions(target)
    print("entry.png sha256: %s" % digest)
    print("entry.png size: (%d, %d)" % (width, height))

    problems = []
    if digest != EXPECTED_SHA256:
        problems.append("sha256 mismatch: got %s" % digest)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        problems.append("size mismatch: got %dx%d" % (width, height))
    if problems:
        for problem in problems:
            print("error: %s" % problem, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
