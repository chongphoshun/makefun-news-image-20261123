#!/usr/bin/env python3
"""Copy entry.png to the output directory (make.fun harness entrypoint).

Standard library only. Resolves paths from this script's own folder,
never from the current working directory. The output directory comes
from MAKEFUN_OUTPUT_DIR and defaults to /output when unset.
"""
import hashlib
import os
import shutil
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DEFAULT_OUT = "/output"


def png_size(path):
    """Return (width, height) from a PNG header, or raise ValueError."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file: %s" % path)
    if head[12:16] != b"IHDR":
        raise ValueError("missing IHDR chunk: %s" % path)
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or DEFAULT_OUT
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dest)
    width, height = png_size(dest)
    if (width, height) != (1024, 1024):
        raise ValueError("entry.png must be 1024x1024, got %dx%d"
                         % (width, height))
    with open(dest, "rb") as fh:
        data = fh.read()
    with open(SRC, "rb") as fh:
        src_data = fh.read()
    if data != src_data:
        raise ValueError("copied entry.png differs from source")
    digest = hashlib.sha256(data).hexdigest()
    print("wrote %s (%d bytes, sha256 %s)" % (dest, len(data), digest))
    return 0


if __name__ == "__main__":
    sys.exit(main())
