#!/usr/bin/env python3
"""One emoji, one dream vacation, for make.fun.

The program's only job is to write the entry to
``/output/entry.txt``: exactly one emoji, nothing else — a
penguin, standing in for a dream trip to Antarctica, the last
faraway place, where the locals waddle up to say hello.

A penguin is the whole postcard at a glance: snow, ice and the
animal you crossed the world to see, in a single character that
reads instantly at any size, in any culture. The entry is stored
as two fragments and joined at runtime. ``EMOJI_BASE`` carries
the penguin itself; ``EMOJI_TAIL`` carries nothing after it —
the entry is one emoji and one emoji only, so the tail is the
empty string, and ``assemble`` still joins the two parts the
same way a longer entry would. ``validate`` enforces the entry
gate; ``run`` writes the validated entry. Standard library only,
no network, no input.
"""

from pathlib import Path

# The entry, in two fragments. Keep the joined entry byte-identical:
# U+1F427 PENGUIN, 1 character, 4 bytes UTF-8, no trailing newline.
EMOJI_BASE = "🐧"
EMOJI_TAIL = ""

ENTRY_PATH = Path("/output/entry.txt")
MIN_CHARS = 1
MAX_CHARS = 8


def assemble(base: str, tail: str) -> str:
    """Join the entry's fragments into the single entry text."""
    return base + tail


def validate(entry: str) -> str:
    """Enforce the entry gate on a candidate entry, returning it unchanged.

    A valid entry is between MIN_CHARS and MAX_CHARS characters,
    contains no line breaks or control characters, is not blank,
    and encodes as UTF-8. Anything else raises ValueError (or
    UnicodeEncodeError) and nothing is written.
    """
    length = len(entry)
    if length < MIN_CHARS or length > MAX_CHARS:
        raise ValueError(
            f"entry must be {MIN_CHARS}-{MAX_CHARS} characters, got {length}"
        )
    if any(ch in entry for ch in ("\n", "\r")):
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in entry):
        raise ValueError("entry must not contain control characters")
    if entry.strip() == "":
        raise ValueError("entry must not be blank")
    entry.encode("utf-8")
    return entry


def run() -> None:
    """Build, validate and write the entry."""
    entry = validate(assemble(EMOJI_BASE, EMOJI_TAIL))
    ENTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENTRY_PATH.write_text(entry, encoding="utf-8")


if __name__ == "__main__":
    run()
