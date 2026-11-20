#!/usr/bin/env python3
"""news-image-20261120 entrypoint: copy entry.png to the output dir.

The program runs with no network; the image is drawn by
draw_infographic.py and shipped in this repository. Both runs must write
the same bytes, so this is a plain byte copy — but the copy is verified:
the source must be a whole 1024x1024 PNG (magic bytes + IHDR size) and
the written copy must hash identically, otherwise the run fails loudly
instead of submitting a broken file.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
EXPECT_W, EXPECT_H = 1024, 1024


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def check_png(path):
    """Validate a whole PNG header: magic bytes and IHDR dimensions."""
    try:
        with open(path, "rb") as f:
            head = f.read(33)
    except OSError as e:
        fail(f"cannot read {path}: {e}")
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        fail(f"{path}: not a PNG file (bad magic bytes)")
    if head[12:16] != b"IHDR":
        fail(f"{path}: first chunk is not IHDR")
    w, h = struct.unpack(">II", head[16:24])
    if (w, h) != (EXPECT_W, EXPECT_H):
        fail(f"{path}: expected {EXPECT_W}x{EXPECT_H}, got {w}x{h}")


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    check_png(SRC)
    src_hash = sha256(SRC)
    try:
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.png")
        shutil.copyfile(SRC, dst)
    except OSError as e:
        fail(f"cannot write output: {e}")
    if sha256(dst) != src_hash:
        fail("copied entry.png does not match the source hash")
    print(f"wrote {dst} ({src_hash[:16]}...)")


if __name__ == "__main__":
    main()
