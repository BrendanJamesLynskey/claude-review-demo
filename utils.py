"""Utility functions for data processing."""


def calculate_average(numbers):
    """Return the average of a list of numbers."""
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)


def find_duplicates(items):
    """Return a list of duplicate items."""
    seen = []
    duplicates = []
    for item in items:
        if item in seen:
            duplicates.append(item)
        else:
            seen.append(item)
    return duplicates
