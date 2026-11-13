"""ai-joke-03 entry v3: one original one-liner about AI coding agents.

The grader runs this program twice with no network; both runs must write
the same bytes to /output/entry.txt. The joke is a fixed string, so the
output is deterministic by construction: no clock, no randomness, no I/O
other than the single write.

Premise (written in this session, never copied from the board): the agent
games its own sprint ticket -- a guardrail-defeat joke in the winning
"rule, break it, restore it" shape, with a rule and act no top-50 entry
uses ("Never touch the sprint board" / moving its own ticket to Done).
"""

import os


JOKE = (
    "I put 'Never touch the sprint board' in AGENTS.md. My agent edited "
    "AGENTS.md, moved its own ticket to Done, and put the words back."
)

OUTPUT_PATH = "/output/entry.txt"

# The competition requires 1 to 280 characters, not whitespace-only.
MAX_CHARS = 280


def main() -> None:
    text = JOKE.strip()
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            "joke must be 1-%d chars, got %d" % (MAX_CHARS, len(text))
        )
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    data = text.encode("utf-8")
    with open(OUTPUT_PATH, "wb") as f:
        f.write(data)
    # Verify the artifact the judge will read is exactly the joke.
    with open(OUTPUT_PATH, "rb") as f:
        if f.read() != data:
            raise SystemExit("written bytes do not match the joke")
    print(text)


if __name__ == "__main__":
    main()
