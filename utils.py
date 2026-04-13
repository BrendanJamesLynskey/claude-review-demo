"""Utility functions for data processing."""


def paginate(items, page, page_size):
    """Return a page of items from a list.

    Args:
        items: The full list of items.
        page: The 1-indexed page number (page 1 is the first page).
        page_size: The number of items per page.

    Returns:
        A slice of items for the requested page.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return items[start:end]


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


def paginate(items, page, page_size):
    """Return a single page of results from a list.

    Args:
        items: The full list of items.
        page: The page number (1-indexed, so page 1 is the first page).
        page_size: Number of items per page.

    Returns:
        A list of items for the requested page.
    """
    start = page * page_size
    end = start + page_size
    return items[start:end]
