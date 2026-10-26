#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Okkar-Saga contributors
"""Check a UTF-8 XYZ text file without changing it.

Each data row must contain exactly three finite floating-point numbers.
Blank lines and comments beginning with # are allowed, including inline comments.
This checks text structure only, not coordinate systems or measurement accuracy.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
import sys


class InvalidXYZ(ValueError):
    """A malformed data row, carrying its original file line number."""

    def __init__(self, line: int, reason: str):
        self.line = line
        super().__init__(reason)


class InvalidEncoding(ValueError):
    """A file line that cannot be decoded as UTF-8."""

    def __init__(self, line: int):
        self.line = line
        super().__init__("invalid UTF-8 encoding")


def count_points(path: Path) -> int:
    """Validate every row, returning the number of points on success."""
    count = 0
    last_line = 0
    with path.open("rb") as stream:
        for last_line, raw in enumerate(stream, 1):
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError as exc:
                raise InvalidEncoding(last_line) from exc
            fields = text.split("#", 1)[0].split()
            if not fields:
                continue
            if len(fields) != 3:
                raise InvalidXYZ(last_line, "expected exactly 3 coordinates")
            try:
                coordinates = [float(field) for field in fields]
            except ValueError as exc:
                raise InvalidXYZ(last_line, "coordinate is not a number") from exc
            if not all(math.isfinite(value) for value in coordinates):
                raise InvalidXYZ(last_line, "coordinates must be finite")
            count += 1
    if count == 0:
        raise InvalidXYZ(max(1, last_line), "no data rows; at least one point is required")
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="UTF-8 XYZ text file to check")
    args = parser.parse_args(argv)
    # repr escapes control characters in unusual filenames; parent paths stay private.
    name = repr(args.file.name)
    try:
        count = count_points(args.file)
    except InvalidXYZ as exc:
        print(f"{name}:{exc.line}: {exc}", file=sys.stderr)
        return 1
    except InvalidEncoding as exc:
        print(f"{name}:{exc.line}: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"{name}: cannot read file ({type(exc).__name__})", file=sys.stderr)
        return 2
    print(f"{name}: OK — {count} point{'s' if count != 1 else ''}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
