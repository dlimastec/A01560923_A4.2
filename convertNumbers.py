"""
Convert numbers from a text file to binary and hexadecimal.

Reads one item per line, keeps original order, reports invalid entries,
prints results to console, and writes the same results to ConvertionResults.txt.

Usage:
    python convertNumbers.py fileWithData.txt
"""

import sys
import time

RESULT_FILE = "ConvertionResults.txt"
HEX_DIGITS = "0123456789ABCDEF"


def read_items(filename):
    """Read lines and return."""
    items = []
    errors = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                text = line.strip()

                if text == "":
                    errors.append(f"Line {line_number}: empty line (skipped)")
                    items.append((text, None))
                    continue

                try:
                    items.append((text, int(text)))
                except ValueError:
                    errors.append(
                        f"Line {line_number}: invalid number '{text}' (skipped)"
                    )
                    items.append((text, None))

    except FileNotFoundError:
        print(f"ERROR: File not found: {filename}")
        sys.exit(1)

    return items, errors


def to_binary(value):
    """Convert integer to binary."""
    if value >= 0:
        if value == 0:
            return "0"

        bits = []
        n = value
        while n > 0:
            bits.append(str(n % 2))
            n //= 2
        bits.reverse()
        return "".join(bits)

    # 10-bit two's complement for negatives
    width = 10
    unsigned = (1 << width) + value
    bits = []
    for i in range(width - 1, -1, -1):
        bit = (unsigned >> i) & 1
        bits.append(str(bit))
    return "".join(bits)


def to_hex(value):
    """Convert integer to hex. Negatives use 40-bit two's complement."""
    if value >= 0:
        if value == 0:
            return "0"

        digits = []
        n = value
        while n > 0:
            digits.append(HEX_DIGITS[n % 16])
            n //= 16
        digits.reverse()
        return "".join(digits)

    # 40-bit two's complement for negatives (10 hex digits)
    width_bits = 40
    unsigned = (1 << width_bits) + value

    digits = []
    for shift in range(width_bits - 4, -1, -4):
        nibble = (unsigned >> shift) & 0xF
        digits.append(HEX_DIGITS[nibble])
    return "".join(digits)


def save_results(text):
    """Save the results text into the output file."""
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(text)


def build_results_text(filename, items, errors, elapsed_time):
    """Build the output report as text."""
    lines = [
        "Convert Numbers - Results",
        "-------------------------",
        f"Input file: {filename}",
        f"Valid numbers: {sum(1 for _, v in items if v is not None)}",
        f"Invalid lines: {len(errors)}",
        "",
        "Number | Binary | Hex",
        "---------------------",
    ]

    for raw_text, value in items:
        if value is None:
            lines.append(f"{raw_text} | #VALUE! | #VALUE!")
        else:
            binary_str = to_binary(value)
            hex_str = to_hex(value)
            lines.append(f"{value} | {binary_str} | {hex_str}")

    lines.append("")
    lines.append(f"Elapsed time (s): {elapsed_time}")

    return "\n".join(lines) + "\n"


def main():
    """Main entry point: read file, convert numbers, and print results."""
    start_time = time.time()

    if len(sys.argv) != 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    filename = sys.argv[1]
    items, errors = read_items(filename)

    for error in errors:
        print(f"ERROR: {error}")

    if all(value is None for _, value in items):
        print("ERROR: No valid numbers found in the input file.")
        sys.exit(1)

    elapsed_time = time.time() - start_time

    results = build_results_text(filename, items, errors, elapsed_time)

    print(results)
    save_results(results)


if __name__ == "__main__":
    main()
