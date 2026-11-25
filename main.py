#!/usr/bin/env python3
"""Write the entry image to /output/entry.png.

The image is pre-rendered by build_image.py and stored in this repo as
entry.png. This script copies it to /output/entry.png and verifies the
copy byte-for-byte, so every run produces identical output. No network.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
TARGET = "/output/entry.png"
CHUNK = 65536
EXPECTED_SIZE = (1024, 1024)


def sha256_of(path):
    """Return the hex sha256 digest of the file at `path`."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(CHUNK), b""):
            digest.update(block)
    return digest.hexdigest()


def main():
    """Copy entry.png to /output and verify hash and dimensions."""
    from PIL import Image

    os.makedirs(os.path.dirname(TARGET), exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)

    source_hash = sha256_of(SOURCE)
    target_hash = sha256_of(TARGET)
    if source_hash != target_hash:
        raise SystemExit("entry.png copy mismatch: hashes differ")

    with Image.open(TARGET) as img:
        if img.size != EXPECTED_SIZE:
            raise SystemExit(f"unexpected entry.png size: {img.size}")

    print("entry.png sha256:", target_hash)
    print("entry.png size:", EXPECTED_SIZE)


if __name__ == "__main__":
    main()
