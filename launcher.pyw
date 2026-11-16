"""Launcher of shortcuts grouped by categories (Windows, Tkinter)."""

import ctypes
import os
import subprocess
import tkinter as tk
from tkinter import messagebox

WINDOW_TITLE = "Lanzador"
BUTTON_WIDTH = 28
ICON_SIZE = 24
MAX_FUNCTION_KEYS = 12
FONT = ("Segoe UI", 11)
HEADER_FONT = ("Segoe UI", 10, "bold")

BG_COLOR = "#1e1e1e"
BUTTON_COLOR = "#2d2d2d"
BUTTON_HOVER_COLOR = "#3c3c3c"
BUTTON_PRESSED_COLOR = "#4a4a4a"
TEXT_COLOR = "#e6e6e6"
EMPTY_TEXT_COLOR = "#777777"

EMPTY_TEXT = "- vacío -"

CATEGORIES = [
    {
        "name": "Vídeo",
        "icon": "??",
        "color": "#ab47bc",
        "actions": [
            (EMPTY_TEXT, None, False),
            (EMPTY_TEXT, None, False),
        ],
    },
    {
        "name": "Programación",
        "icon": "??",
        "color": "#42a5f5",
        "actions": [
            (EMPTY_TEXT, None, False),
            (EMPTY_TEXT, None, False),
        ],
    },
    {
        "name": "Otros",
        "icon": "??",
        "color": "#ffa726",
        "actions": [
            (EMPTY_TEXT, None, False),
        ],
    },
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_EXTENSIONS = (".png", ".gif")


def resolve_path(path):
    if os.path.isabs(path):
        return path
    return os.path.join(BASE_DIR, path)


def load_icon(icon):
    if icon.lower().endswith(IMAGE_EXTENSIONS):
        path = resolve_path(icon)
        if os.path.isfile(path):
            try:
                image = tk.PhotoImage(file=path)
                factor = max(image.width(), image.height()) // ICON_SIZE
                if factor > 1:
                    image = image.subsample(factor, factor)
                return image, ""
            except tk.TclError:
                pass
        return None, ""
    return None, icon


def run_bat(name, bat_path, show_console):
    bat_path = resolve_path(bat_path)

    if not os.path.isfile(bat_path):
        messagebox.showerror(
            "Archivo no encontrado",
            f"No existe el archivo de '{name}':\n{bat_path}",
        )
        return

    try:
        if show_console:
            subprocess.Popen(
                ["cmd", "/k", bat_path],
                cwd=os.path.dirname(bat_path),
                creationflags=subprocess.CREATE_NEW_CONSOLE,
            )
        else:
            subprocess.Popen(
                ["cmd", "/c", bat_path],
                cwd=os.path.dirname(bat_path),
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
    except OSError as error:
        messagebox.showerror(
            "Error al ejecutar",
            f"No se pudo lanzar '{name}':\n{error}",
        )


def use_dark_title_bar(root):
    try:
        root.update()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        value = ctypes.c_int(1)
        # 20 = DWMWA_USE_IMMERSIVE_DARK_MODE (19 en algunas builds de Windows 10)
        for attribute in (20, 19):
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, attribute, ctypes.byref(value), ctypes.sizeof(value)
            )
    except Exception:
        pass


def make_button(parent, label, image, color, command, enabled=True):
    options = {
        "text": label,
        "anchor": "w",
        "padx": 10,
        "pady": 4,
        "font": FONT,
        "width": BUTTON_WIDTH,
        "bg": BUTTON_COLOR,
        "fg": TEXT_COLOR if enabled else EMPTY_TEXT_COLOR,
        "activebackground": BUTTON_PRESSED_COLOR if enabled else BUTTON_COLOR,
        "activeforeground": color if enabled else EMPTY_TEXT_COLOR,
        "relief": "flat",
        "borderwidth": 0,
        "highlightthickness": 2,
        "highlightbackground": BUTTON_COLOR,
        "highlightcolor": color,
        "takefocus": 1 if enabled else 0,
        "cursor": "hand2" if enabled else "arrow",
        "command": command if enabled else (lambda: None),
    }
    if image:
        options.update(image=image, compound="left")

    button = tk.Button(parent, **options)
    if enabled:
        button.bind("<Enter>", lambda event: button.config(bg=BUTTON_HOVER_COLOR))
        button.bind("<Leave>", lambda event: button.config(bg=BUTTON_COLOR))
    return button


def main():
    root = tk.Tk()
    root.title(WINDOW_TITLE)
    root.configure(bg=BG_COLOR)
    root.resizable(False, False)
    use_dark_title_bar(root)

    images = []
    key_number = 0
    buttons = []

    for category in CATEGORIES:
        image, emoji = load_icon(category["icon"])
        images.append(image)

        header = tk.Frame(root, bg=BG_COLOR)
        header.pack(fill="x", padx=12, pady=(12, 2))
        tk.Frame(header, bg=category["color"], width=4).pack(side="left", fill="y")
        tk.Label(
            header,
            text=f"{emoji}  {category['name']}".strip(),
            image=image,
            compound="left",
            font=HEADER_FONT,
            bg=BG_COLOR,
            fg=category["color"],
            anchor="w",
            padx=6,
        ).pack(side="left", fill="x")

        for text, bat_path, show_console in category["actions"]:
            key_number += 1
            has_key = key_number <= MAX_FUNCTION_KEYS

            label = f"{emoji}  {text}" if emoji else text
            if has_key:
                label += f"   (F{key_number})"

            button = make_button(
                root,
                label,
                image,
                category["color"],
                command=lambda t=text, b=bat_path, c=show_console: run_bat(t, b, c),
                enabled=bat_path is not None,
            )
            button.pack(fill="x", padx=(22, 12), pady=2)

            if bat_path is not None:
                buttons.append(button)

            if has_key:
                root.bind(f"<F{key_number}>", lambda event, b=button: b.invoke())

    tk.Frame(root, height=10, bg=BG_COLOR).pack()

    def move_focus(step):
        if not buttons:
            return "break"
        current = root.focus_get()
        if current in buttons:
            index = (buttons.index(current) + step) % len(buttons)
        else:
            index = 0
        buttons[index].focus_set()
        return "break"

    def press_focused(event):
        current = root.focus_get()
        if isinstance(current, tk.Button):
            current.invoke()
        return "break"

    root.bind("<Up>", lambda event: move_focus(-1))
    root.bind("<Down>", lambda event: move_focus(1))
    root.bind("<Return>", press_focused)
    root.bind("<KP_Enter>", press_focused)

    if buttons:
        buttons[0].focus_set()
    root.focus_force()

    root.mainloop()


if __name__ == "__main__":
    main()
