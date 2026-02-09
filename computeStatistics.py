"""
Compute basic descriptive statistics from a text file.

Reads one value per line, skips invalid entries, prints results to console,
and writes the same results to StatisticsResults.txt.
"""

import sys
import time


# File to save results
RESULT_FILE = "StatisticsResults.txt"


def read_numbers(filename):
    """Read numeric values from a file and return (numbers, errors)."""
    # Read the file line by line and try to convert each line to a number
    numbers = []
    errors = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                text = line.strip()

                # If the line is empty, report it but continue
                if text == "":
                    errors.append(f"Line {line_number}: empty line (skipped)")
                    continue

                try:
                    numbers.append(float(text))
                except ValueError:
                    # If it cannot be converted to a number, log the error
                    errors.append(
                        f"Line {line_number}: invalid number '{text}' (skipped)"
                    )

    except FileNotFoundError:
        print(f"ERROR: File not found: {filename}")
        sys.exit(1)

    return numbers, errors


def mean(values):
    """Return the arithmetic mean of the values."""
    # Calculate the average by summing all values
    total = 0
    for value in values:
        total += value
    return total / len(values)


def median(values):
    """Return the median value from a list of numbers."""
    # Sort values to find the middle
    sorted_values = sorted(values)
    n = len(sorted_values)
    middle = n // 2

    # If odd number of values, return the center
    if n % 2 == 1:
        return sorted_values[middle]

    # If even, average the two center values
    return (sorted_values[middle - 1] + sorted_values[middle]) / 2


def mode(values):
    """Return the mode of the values, or None if there is no unique mode."""
    frequency = {}
    for value in values:
        frequency[value] = frequency.get(value, 0) + 1

    max_count = max(frequency.values())

    # If all values appear once, no mode
    if max_count == 1:
        return None

    # If there is a tie, pick the largest value
    best = None
    for val, count in frequency.items():
        if count == max_count:
            if best is None or val > best:
                best = val

    return best



def variance(values, avg):
    """Return the sample variance of the values."""
    # Sample variance (divide by n - 1) to match the provided expected results
    total = 0
    for value in values:
        diff = value - avg
        total += diff * diff

    n = len(values)
    if n < 2:
        return 0.0

    return total / (n - 1)



def standard_deviation(var):
    """Return the standard deviation given a variance."""
    # Standard deviation is the square root of variance
    return var ** 0.5


def save_results(text):
    """Save the results text into the output file."""
    # Write the results to a file
    with open(RESULT_FILE, "w", encoding="utf-8") as file:
        file.write(text)


def main():
    """Main entry point: read file, compute statistics, and print results."""
    start_time = time.time()

    # Expect exactly one argument: the data file
    if len(sys.argv) != 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        sys.exit(1)

    filename = sys.argv[1]

    numbers, errors = read_numbers(filename)

    # Show any errors found while reading the file
    for error in errors:
        print(f"ERROR: {error}")

    # If no valid numbers were found, stop the program
    if len(numbers) == 0:
        print("ERROR: No valid numbers found in the input file.")
        sys.exit(1)

    avg = mean(numbers)
    med = median(numbers)
    mod = mode(numbers)
    var = variance(numbers, avg)
    var_population = var * (len(numbers) - 1) / len(numbers)
    std = standard_deviation(var_population)

    elapsed_time = time.time() - start_time

    mode_text = "#N/A" if mod is None else str(mod)

    results = (
        "Compute Statistics - Results\n"
        "----------------------------\n"
        f"Input file: {filename}\n"
        f"Valid numbers: {len(numbers)}\n"
        f"Invalid lines: {len(errors)}\n\n"
        "Descriptive Statistics (population):\n"
        f"Mean: {avg}\n"
        f"Median: {med}\n"
        f"Mode: {mode_text}\n"
        f"Variance: {var}\n"
        f"Standard deviation: {std}\n\n"
        f"Elapsed time (s): {elapsed_time}\n"
    )

    print(results)
    save_results(results)


if __name__ == "__main__":
    main()
