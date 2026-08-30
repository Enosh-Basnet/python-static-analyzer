from collections import defaultdict


def find_duplicate_code(
    source: str,
    min_block_size: int = 3
) -> list[dict]:
    """Finds exact duplicate code blocks of at least `min_block_size` logical lines within Python source code."""
    if not isinstance(source, str):
        raise TypeError(f"Expected source as str, received {type(source).__name__}")

    if not isinstance(min_block_size, int) or isinstance(min_block_size, bool):
        raise TypeError(f"Expected min_block_size as int, received {type(min_block_size).__name__}")

    if min_block_size < 3:
        raise ValueError(f"min_block_size must be at least 3, got {min_block_size}")

    # Extract non-empty and non-comment logical lines with original source line numbers
    logical_lines: list[tuple[int, str]] = []
    for line_num, raw_line in enumerate(source.splitlines(), start=1):
        cleaned = raw_line.strip()
        if cleaned and not cleaned.startswith("#"):
            logical_lines.append((line_num, cleaned))

    if len(logical_lines) < min_block_size:
        return []

    # Map block tuples to their starting source line numbers using a sliding window
    blocks: dict[tuple[str, ...], list[int]] = defaultdict(list)
    for i in range(len(logical_lines) - min_block_size + 1):
        window = logical_lines[i : i + min_block_size]
        block_content = tuple(line for _, line in window)
        start_line = window[0][0]
        blocks[block_content].append(start_line)

    # Filter for blocks occurring more than once
    results: list[dict] = []
    for block_content, occurrences in blocks.items():
        if len(occurrences) > 1:
            results.append({
                "block": block_content,
                "occurrences": occurrences,
            })

    return results