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

    # Map block content to starting logical indices and source line numbers
    blocks: dict[tuple[str, ...], dict[str, list[int]]] = defaultdict(
        lambda: {"logical_indices": [], "line_numbers": []}
    )

    for i in range(len(logical_lines) - min_block_size + 1):
        window = logical_lines[i : i + min_block_size]
        block_content = tuple(line for _, line in window)
        start_line = window[0][0]
        blocks[block_content]["logical_indices"].append(i)
        blocks[block_content]["line_numbers"].append(start_line)

    # Collect candidate blocks that occur more than once
    candidates = []
    for block_content, data in blocks.items():
        if len(data["line_numbers"]) > 1:
            candidates.append({
                "block": block_content,
                "occurrences": data["line_numbers"],
                "logical_indices": set(data["logical_indices"]),
                "first_idx": data["logical_indices"][0],
            })

    # Sort candidates by their initial logical index to establish evaluation order
    candidates.sort(key=lambda c: c["first_idx"])

    # Filter out shifted windows resulting from consecutive block repetitions
    accepted_candidates = []
    for cand in candidates:
        is_shifted = False
        cand_indices = cand["logical_indices"]

        for prev in accepted_candidates:
            prev_indices = prev["logical_indices"]
            k = cand["first_idx"] - prev["first_idx"]
            if k > 0 and all((idx - k) in prev_indices for idx in cand_indices):
                is_shifted = True
                break

        if not is_shifted:
            accepted_candidates.append(cand)

    return [
        {
            "block": cand["block"],
            "occurrences": cand["occurrences"],
        }
        for cand in accepted_candidates
    ]