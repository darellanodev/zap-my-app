# Open the launcher with AutoHotkey

`Ctrl + Alt + L` shortcut to open, focus or close the launcher. It needs [AutoHotkey v2.0](https://www.autohotkey.com/).

## Behavior

- If the launcher is in the foreground, it closes it.
- If it is open but in the background, it brings it to the front.
- If it is not open, it starts it.

## Script

Save this content in a `.ahk` file (for example `launcher.ahk`) and double click it. To start it with Windows, copy a shortcut to the script into `shell:startup`.

```autohotkey
#Requires AutoHotkey v2.0
#SingleInstance Force

pythonw  := "C:\Users\Daniel\AppData\Local\Programs\Python\Python314\pythonw.exe"
script   := "D:\xampp\htdocs\projects\tools\launcher\launcher.pyw"
workDir  := "D:\xampp\htdocs\projects\tools\launcher\"
winTitle := "Lanzador ahk_class TkTopLevel"

^!l:: {
    if WinActive(winTitle) {
        WinClose(winTitle)
    } else if WinExist(winTitle) {
        WinActivate(winTitle)
    } else {
        Run('"' pythonw '" "' script '"', workDir)
    }
}
```

## Settings

- `pythonw`: path to `pythonw.exe` of your Python installation.
- `script`: absolute path to `launcher.pyw`.
- `workDir`: folder where the launcher runs (relative `.bat` paths are resolved from `launcher.pyw`, not from this folder).
- `winTitle`: must match the window title (`WINDOW_TITLE` in `launcher.pyw`); `ahk_class TkTopLevel` avoids conflicts with other windows with the same name.
