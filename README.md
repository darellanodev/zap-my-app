# Zap My App

Desktop app for Windows (Python + Tkinter) that runs `.bat` files grouped by categories. Dark theme and keyboard navigation.

## Usage

Double click `launcher.pyw`, or run it with `pythonw` from a terminal:

```powershell
pythonw launcher.pyw
```

Because it is a `.pyw` file, no console window opens.

- `F1`–`F12`: run the buttons in order.
- Up/down arrows and `Tab`: move the focus between active buttons.
- `Enter`: run the focused button.

## Settings

Everything is edited in the `CATEGORIES` list inside `launcher.pyw`. Each category has these fields:

| Field     | Description                                                              |
| --------- | ------------------------------------------------------------------------ |
| `name`    | Name shown in the window (the interface text is in Spanish).             |
| `icon`    | Emoji (for example `"??"`) or a PNG/GIF path relative to the script.     |
| `color`   | Color of the header and the focus (light colors work best on dark mode). |
| `actions` | List of tuples `(text, bat_path, show_console)`.                         |

Each action:

- `text`: label of the button.
- `bat_path`: path to the `.bat` file (relative to the script, or absolute). If it is `None`, the button is an empty placeholder and does nothing.
- `show_console`: `True` opens a console (`cmd /k`, it stays open). `False` runs it hidden (`cmd /c`).

## Documentation

- [AutoHotkey shortcut](docs/autohotkey.md): open, focus or close the launcher with `Ctrl + Alt + L`.
