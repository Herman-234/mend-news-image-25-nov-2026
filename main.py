#!/usr/bin/env python3
"""Write the entry image to /output/entry.png.

No network. Deterministic: copies the pre-rendered image held in this
repository, so two runs produce byte-identical output.
"""
import hashlib
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

os.makedirs("/output", exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = "/output/entry.png"
shutil.copyfile(src, dst)

# Verify the copy is byte-identical to the repository image.
def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

assert _sha256(src) == _sha256(dst), "entry.png copy mismatch"
print("entry.png sha256:", _sha256(dst))
