# AGENTS.md

Guide for agents working on this repository.

## Project

Windows desktop launcher written in Python 3 + Tkinter (`launcher.pyw`; the `.pyw` extension lets you run it with a double click and no console). It runs `.bat` files grouped in categories defined in the `CATEGORIES` constant.

## Code rules

- Do not add comments unless they are really needed (for example, magic numbers of the Windows API).
- Keep the existing style: small functions, English names, interface text in Spanish.
- Do not add external dependencies; use only the standard library.
- Keep the dark theme and the keyboard navigation working.

## Editing categories

`CATEGORIES` is a list of dictionaries:

```python
{
    "name": "Vídeo",
    "icon": "??",          # emoji or relative path to a PNG/GIF
    "color": "#ab47bc",    # header and focus color
    "actions": [
        ("Button text", "path/to/script.bat", True),
        (EMPTY_TEXT, None, False),  # empty button / placeholder
    ],
}
```

- `bat_path=None` disables the button (placeholder).
- Relative paths are resolved from the `launcher.pyw` folder.
- Actions get `F1`–`F12` in order; after the 12th they have no key.

## Check

```powershell
python -m py_compile launcher.pyw
```

## Documentation

- `README.md`: usage and settings for the end user.
- [docs/autohotkey.md](docs/autohotkey.md): `Ctrl + Alt + L` shortcut to open/close the launcher.
