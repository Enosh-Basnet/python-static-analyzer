# AI-Assisted Test-Driven Development of a Python Static Code Analyzer

This project implements a modular Python static code analyzer developed using an AI-assisted Test-Driven Development (AI-TDD) workflow.

The analyzer inspects Python source code without executing it and provides:

- Cyclomatic complexity analysis
- Unused-variable detection
- Naming-convention checks
- Duplicate-code detection
- Code metrics
- Command-line file analysis

## Project Structure

```text
python-static-code-analyzer/
├── src/
│   ├── __init__.py
│   ├── analyzer.py
│   ├── cli.py
│   ├── complexity.py
│   ├── unused_variables.py
│   ├── naming.py
│   ├── duplicate_code.py
│   └── metrics.py
├── tests/
│   ├── test_analyzer.py
│   ├── test_cli.py
│   ├── test_complexity.py
│   ├── test_unused_variables.py
│   ├── test_naming.py
│   ├── test_duplicate.py
│   └── test_metrics.py
└── README.md
```

## Installation

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the testing dependencies:

```bash
python -m pip install pytest pytest-cov
```

## Usage

Analyze a Python file from the project root:

```bash
python -m src.cli example.py
```

You can also provide the full path to any Python file:

```bash
python -m src.cli /path/to/file.py
```

## Running Tests

Run the complete automated test suite:

```bash
python -m pytest -v
```

The final project contains **86 automated tests** covering component, boundary, invalid-input, regression, integration, and CLI behaviour.

## Code Coverage

Run statement and branch coverage:

```bash
python -m pytest --cov=src --cov-branch --cov-report=term-missing
```

The final test suite achieved **84% overall branch-aware code coverage**.

## Development Approach

The project followed an AI-assisted TDD workflow:

1. Requirements were defined before implementation.
2. Automated tests were written first.
3. Tests were executed to establish the Red stage.
4. AI-generated implementations were reviewed against the requirements and tests.
5. Implementations were executed to reach the Green stage.
6. Defects discovered during review were converted into regression tests.
7. Refined implementations were retested to ensure previous behaviour was preserved.
8. The completed components were integrated into a single analyzer and CLI.

AI-generated code was not accepted automatically. Outputs were accepted or modified based on test results, requirement compliance, and technical review.

## Main Components

### Complexity Analysis
Calculates cyclomatic complexity for discovered functions and methods using Python's AST.

### Unused Variable Detection
Reports supported variables that are assigned but not subsequently read within the same supported scope.

### Naming Violation Detection
Checks project-defined naming rules for functions, classes, and ordinary variables.

### Duplicate Code Detection
Detects exact repeated normalized code blocks using a configurable minimum block size.

### Code Metrics
Reports logical lines of code, function count, class count, and import count.

### Integration Layer
Combines all five analysis components into a single structured result.

### Command-Line Interface
Reads a `.py` file, performs analysis, and displays a human-readable report.

## Notes

- The analyzer performs static analysis and does **not execute** the target Python program.
- The project intentionally implements a defined subset of static-analysis behaviour and is not intended to replace production tools such as Pylint, Ruff, Flake8, or SonarQube.
- A graphical user interface is outside the project scope; the application is operated through the command line.
