import sys
from pathlib import Path

from src.analyzer import analyze_source


def _print_report(results: dict) -> None:
    """Formats and prints the human-readable static code analysis report."""
    print("Python Static Code Analysis")
    print("=" * 27)

    print("\nComplexity")
    print("-" * 10)
    complexity = results.get("complexity", {})
    if complexity:
        for name, score in complexity.items():
            print(f"  {name}: {score}")
    else:
        print("  No functions or methods found.")

    print("\nUnused Variables")
    print("-" * 16)
    unused = results.get("unused_variables", {})
    if unused:
        for scope, vars_list in unused.items():
            print(f"  {scope}: {', '.join(vars_list)}")
    else:
        print("  No unused variables found.")

    print("\nNaming Violations")
    print("-" * 17)
    naming = results.get("naming_violations", {})
    if naming:
        for category, items in naming.items():
            print(f"  {category}: {', '.join(items)}")
    else:
        print("  No naming violations found.")

    print("\nDuplicate Code")
    print("-" * 14)
    duplicates = results.get("duplicate_code", [])
    if duplicates:
        for item in duplicates:
            print(f"  Lines {item['occurrences']}: {item['block']}")
    else:
        print("  No duplicate code blocks found.")

    print("\nCode Metrics")
    print("-" * 12)
    metrics = results.get("metrics", {})
    if metrics:
        for key, val in metrics.items():
            print(f"  {key}: {val}")
    else:
        print("  No metrics available.")


def main(argv=None) -> int:
    """Command-line entry point for running the static code analyzer on a file."""
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Error: No target file supplied. Please provide a path to a .py file.", file=sys.stderr)
        return 1

    target_path = Path(argv[0])

    if not target_path.exists():
        print(f"Error: File not found: '{target_path}'", file=sys.stderr)
        return 1

    if target_path.is_dir():
        print(f"Error: Path '{target_path}' is a directory, not a file.", file=sys.stderr)
        return 1

    if target_path.suffix != ".py":
        print(f"Error: Expected a .py source file, got '{target_path.name}'", file=sys.stderr)
        return 1

    try:
        source_code = target_path.read_text(encoding="utf-8")
        analysis_results = analyze_source(source_code)
    except SyntaxError as err:
        print(f"Error: Invalid Python syntax in '{target_path}': {err}", file=sys.stderr)
        return 1
    except Exception as err:
        print(f"Error: Failed to analyze source file: {err}", file=sys.stderr)
        return 1

    _print_report(analysis_results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())