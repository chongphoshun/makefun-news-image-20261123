#!/usr/bin/env python3
"""Copy entry.png to the output directory.

Standard library only. Resolves paths from this script's own folder,
never from the current working directory.
Usage: MAKEFUN_OUTPUT_DIR=out python3 main.py
Without MAKEFUN_OUTPUT_DIR the grader default is /output.
"""
import hashlib
import os
import shutil
import struct
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / "entry.png"
    data = SRC.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print(f"error: expected 1024x1024, got {width}x{height}", file=sys.stderr)
        return 1
    shutil.copyfile(SRC, dst)
    check = dst.read_bytes()
    if check != data:
        print("error: copy mismatch", file=sys.stderr)
        return 1
    if dst.stat().st_size == 0:
        print("error: output is empty", file=sys.stderr)
        return 1
    print(f"wrote {dst} ({len(data)} bytes, {width}x{height})")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
