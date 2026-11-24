#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261123 v3 submission.

Copies the repo's entry.png to the output directory. Standard library only.
The grader runs this without MAKEFUN_OUTPUT_DIR set and expects the image
at /output/entry.png, so the default output dir is /output.
"""
import hashlib
import os
import shutil
import struct
import sys

DEFAULT_OUT = "/output"
IMAGE_NAME = "entry.png"


def script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def verify_png(path):
    """Check PNG magic bytes and that the IHDR says 1024x1024."""
    with open(path, "rb") as fh:
        header = fh.read(33)
    if len(header) < 33 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"{path}: not a PNG file")
    if header[12:16] != b"IHDR":
        raise ValueError(f"{path}: missing IHDR chunk")
    width, height = struct.unpack(">II", header[16:24])
    if (width, height) != (1024, 1024):
        raise ValueError(f"{path}: expected 1024x1024, got {width}x{height}")
    return width, height


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUT
    src = os.path.join(script_dir(), IMAGE_NAME)
    if not os.path.isfile(src):
        print(f"error: {src} not found", file=sys.stderr)
        return 1
    verify_png(src)
    src_digest = sha256_file(src)
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, IMAGE_NAME)
    shutil.copyfile(src, dst)
    verify_png(dst)
    dst_digest = sha256_file(dst)
    if dst_digest != src_digest:
        print("error: copy mismatch (sha256 differs)", file=sys.stderr)
        return 1
    size = os.path.getsize(dst)
    print(f"wrote {dst}: {size} bytes, sha256 {dst_digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
