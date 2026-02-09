"""
Count distinct words and their frequency from a text file.

Reads a file provided as a command-line argument, counts distinct words,
prints results to console, and writes the same output to WordCountResults.txt.

Usage:
    python wordCount.py fileWithData.txt
"""

import os
import sys
import time


RESULT_FILE = "WordCountResults.txt"


def normalize_token(token):
    """Normalize a token: keep only alphanumeric chars and lowercase them."""
    cleaned = []
    for ch in token:
        if ch.isalnum():
            cleaned.append(ch.lower())

    return "".join(cleaned)


def read_words(filename):
    """Read the file and return (words, errors). Words include '(blank)'."""
    words = []
    errors = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                raw_line = line.rstrip("\n")

                # If the line is empty, report it but keep going
                if raw_line.strip() == "":
                    errors.append(f"Line {line_number}: empty line (skipped)")
                    continue

                # Split by a single space so multiple spaces can generate blanks
                parts = raw_line.split(" ")

                for part in parts:
                    normalized = normalize_token(part)
                    if normalized == "":
                        words.append("(blank)")
                    else:
                        words.append(normalized)

    except FileNotFoundError:
        print(f"ERROR: File not found: {filename}")
        sys.exit(1)

    return words, errors


def count_frequencies(words):
    """Count occurrences for each distinct word using a basic dictionary."""
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


def build_report(filename, freq, total, elapsed):
    """Build output text with word counts."""

    file_tag = os.path.splitext(os.path.basename(filename))[0]

    lines = [f"Row Labels\tCount of {file_tag}"]

    for word, count in freq.items():
        lines.append(f"{word}\t{count}")

    lines.append(f"Grand Total\t{total}")
    lines.append(f"Elapsed time (s): {elapsed}")

    return "\n".join(lines) + "\n"


def save_results(text):
    """Write results to the output file."""
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    """Entry point."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python wordCount.py fileWithData.txt")
        sys.exit(1)

    filename = sys.argv[1]

    words, errors = read_words(filename)

    for err in errors:
        print(f"ERROR: {err}")

    if len(words) == 0:
        print("ERROR: No words found in the input file.")
        sys.exit(1)

    freq = count_frequencies(words)
    elapsed = time.time() - start_time

    report = build_report(filename, freq, len(words), elapsed)

    print(report)
    save_results(report)


if __name__ == "__main__":
    main()
