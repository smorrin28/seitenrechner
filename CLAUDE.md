# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv run python seitenrechner.py   # run the app
uv sync --group dev              # install build deps (pyinstaller)
make build                       # build dist/Seitenrechner.exe (Windows only)
make clean                       # remove build/, dist/, __pycache__, .spec
```

On Windows, `build.bat` is an alternative to `make build`.

## Architecture

The entire application lives in `seitenrechner.py` — no packages, no modules. It has two layers:

- **Logic** (`parse_page_ranges`): parses comma-separated page numbers and ranges (e.g. `2-7, 11, 14`) into a `set[int]`. Raises `ValueError` with German messages on bad input.
- **GUI** (`berechnen`, `kopieren`, and the `__main__` block): a single tkinter window. `berechnen` calls the parser, computes the set complement of colored pages against the total range, and renders the result. `kopieren` copies the result text to the clipboard.

All user-facing strings are in German.
