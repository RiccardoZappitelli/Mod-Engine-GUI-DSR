# Mod Engine GUI (DSR)

Small GUI tool to edit Dark Souls Remastered Mod Engine configuration (`modengine.toml`) with a clean interface.

## Features
- Toggle mod engine options (debug, loader, etc.)
- Add / remove mods dynamically
- Enable/disable mods with checkboxes
- Browse folder picker for mod paths
- Path validation (invalid paths highlighted in red)
- Save config back to TOML

## Requirements
- Python 3.10+
- CustomTkinter
- tomli_w
- Nuitka (for building)

Install dependencies:
```bash
pip install customtkinter tomli_w
```

## Run (dev)
```bash
python gui.py
```

## Build (Nuitka)

### Single-file build:
```bash
nuitka main.py
  --onefile
  --remove-output
  --follow-imports
  --windows-console=disabled
  --enable-plugin=tk-inter
```

## Notes
- Paths can be relative or absolute