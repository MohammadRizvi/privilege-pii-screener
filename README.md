# Privilege & PII Screener

A Python tool for Early Case Assessment in legal document review.

## What it does

Scans a folder of plain text legal documents, scores each for privilege keywords and personal data, assigns one of four review designations, and outputs a color-coded HTML dashboard sorted by risk. It replaces slow manual first-pass review while staying transparent about why each document was flagged.

## Review designations

The tool assigns one of four designations using ordered rules. Privilege is tested before PII, so a document carrying both signals receives the more cautious privilege label.

- **Privileged** (red): privilege score of 3 or more
- **Potentially Privileged** (orange): privilege score of 1 or 2
- **Needs Further Review** (yellow): privilege score of 0, PII score of 1 or more
- **Not Privileged** (green): both scores 0

The dashboard's triggers column shows the exact words and signals that caused each flag, so the reviewer can see why a document was tagged rather than trusting a black box.

## How to run

1. Make sure you have Python 3 installed.
2. Clone or download this repository.
3. Place your `.txt` documents in the `docs` folder. A sample set is included.
4. From the project folder, run:

```
python screener.py
```

The console prints a ranked report, and a `report.html` dashboard is written to the project folder. Open `report.html` in any browser to view the color-coded results.

## Project files

- `screener.py` is the main script.
- `docs/` holds the sample test documents covering each tier.
- `report.html` is generated when the script runs.

## Course concepts used

Built for Code in Place 2026 final project. Uses:

- **For Loops:** iterating through files, search terms, results, and characters
- **While Loops and If Statements:** the four-tier if, elif, else block for review designations
- **Print and Input:** building a clean ranked console report
- **Numbers in Python:** score accumulation, comparison operators, and sort weights
- **Functions:** three custom functions with parameters and return values, including a boolean helper for digit-run detection
- **Lists:** master results list, trigger collection, and methods like append, sort, and join
- **Dictionaries:** per-document data bundling and mapping designations to sort order and CSS classes
- **Art of Problem Solving:** ordered logic so privilege is tested before PII, and honest acknowledgement of known limitations

Built entirely on Python's standard library, with `os` as the only import.

## Known limitations

These are intentional and reflect course constraints, where regular expressions and external libraries are out of scope.

- Phone detection keys on runs of seven or more digits with no separators, so a number written as 555-123-4567 will be missed.
- Privilege scoring is keyword based and cannot read context.
- Email detection by `@` count is a rough proxy.
- Only `.txt` files are supported.
- All scores are advisory signals, not legal determinations.
