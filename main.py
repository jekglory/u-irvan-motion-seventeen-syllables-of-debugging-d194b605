"""Seventeen Syllables of Debugging -- entry v1.

The grader runs this program twice with no network; both runs must write
the same bytes to /output/entry.txt. The haiku is a fixed string, so the
output is deterministic by construction: no clock, no randomness, no I/O
other than the single write.

The haiku (authored in this session, never copied from the board):

    One log line at three
    a breakpoint waits in the dark
    it was my typo

Why this one: the centre is concrete -- a log line and a breakpoint, the
bounty brief's own examples, at three in the morning. The turn lands in
the last line: a long night of hunting ends on a confession, it was my
own typo. Every word earns its place; nothing is filler added to reach
the count. It reads aloud like plain speech.

Syllable counts, verified by hand (5-7-5, seventeen in all):
    One(1) log(1) line(1) at(1) three(1) = 5
    a(1) break-point(2) waits(1) in(1) the(1) dark(1) = 7
    it(1) was(1) my(1) ty-po(2) = 5
The program asserts this shape itself before writing, so a miscount
can never reach the judge: it would fail loudly instead.
"""

import os

HAIKU = (
    "One log line at three\n"
    "a breakpoint waits in the dark\n"
    "it was my typo"
)

# The competition's gate: /output/entry.txt must be UTF-8 text of
# 1 to 200 characters, not only white space.
MAX_CHARS = 200

# Syllable count of every word in the haiku, as spoken. The program
# asserts the 5-7-5 shape before it writes anything.
SYLLABLES = {
    "one": 1, "log": 1, "line": 1, "at": 1, "three": 1,
    "a": 1, "breakpoint": 2, "waits": 1, "in": 1, "the": 1, "dark": 1,
    "it": 1, "was": 1, "my": 1, "typo": 2,
}

EXPECTED_COUNTS = (5, 7, 5)


def count_syllables(line):
    total = 0
    for word in line.split():
        total += SYLLABLES[word.lower()]
    return total


def main():
    text = HAIKU.strip()
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            "haiku must be 1-%d chars, got %d" % (MAX_CHARS, len(text))
        )
    if not text.strip():
        raise SystemExit("haiku must not be whitespace-only")
    lines = text.split("\n")
    if len(lines) != 3:
        raise SystemExit("haiku must be exactly 3 lines, got %d" % len(lines))
    counts = tuple(count_syllables(line) for line in lines)
    if counts != EXPECTED_COUNTS:
        raise SystemExit(
            "haiku must be 5-7-5 syllables, got %s" % (counts,)
        )
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.txt")
    # The grader owns /output: create it only if it does not exist,
    # never delete or recreate it.
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    # No trailing newline: the haiku ends on "typo", and the gate counts
    # every character of the file.
    data = text.encode("utf-8")
    with open(output_path, "wb") as f:
        f.write(data)
    # Verify the artifact the judge will read is exactly the haiku.
    with open(output_path, "rb") as f:
        if f.read() != data:
            raise SystemExit("written bytes do not match the haiku")
    print(text)


if __name__ == "__main__":
    main()
