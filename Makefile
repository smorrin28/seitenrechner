.PHONY: run build clean install

# Run the app locally (requires Python with tkinter)
run:
	uv run python seitenrechner.py

# Install build dependencies
install:
	uv sync --group dev

# Build a single-file Windows .exe (must be run on Windows)
build: install
	uv run pyinstaller \
		--onefile \
		--windowed \
		--name Seitenrechner \
		--icon NONE \
		seitenrechner.py
	@echo ""
	@echo "Fertig! Installer liegt unter: dist/Seitenrechner.exe"

# Remove build artifacts
clean:
	rm -rf build dist __pycache__ Seitenrechner.spec
