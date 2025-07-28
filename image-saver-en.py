#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clipboard Image Saver
Supports multiple formats & custom resolution
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import pathlib

from PIL import Image, ImageGrab
import pyperclip

APP_NAME = "Clipboard Image Saver"
CONFIG_FILE = pathlib.Path.home() / ".clipboard_saver.json"
DEFAULT_DIR = pathlib.Path.home() / "Downloads"

FORMATS = {
    "PNG":  ("png",  True),   # Extension, lossless support
    "JPG":  ("jpg",  False),
    "JPEG": ("jpeg", False),
    "BMP":  ("bmp",  True),
    "TIFF": ("tiff", True),
    "WebP": ("webp", True),
    "GIF":  ("gif",  False),
}

# ---------- Utilities ----------
def load_config():
    # Load config file
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"last_dir": str(DEFAULT_DIR)}

def save_config(cfg):
    # Save config file
    try:
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print("Failed to save config:", e)

def get_clipboard_image():
    # Get image from clipboard
    try:
        im = ImageGrab.grabclipboard()
    except Exception:
        im = None
    return im

# ---------- GUI ----------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.resizable(False, False)
        self.configure(padx=20, pady=15)

        self.cfg = load_config()
        self.save_dir  = tk.StringVar(value=self.cfg["last_dir"])
        self.file_name = tk.StringVar()
        self.fmt_name  = tk.StringVar(value="PNG")
        self.resize_mode = tk.StringVar(value="none")   # none | long_edge | wh
        self.long_edge = tk.IntVar(value=1920)
        self.width  = tk.IntVar(value=1920)
        self.height = tk.IntVar(value=1080)

        self.init_ui()
        self.after(100, self.check_clipboard)

    def init_ui(self):
        # Title
        ttk.Label(self, text=APP_NAME, font=("Segoe UI", 14, "bold")).pack()

        # Clipboard status
        self.status_lbl = ttk.Label(self, text="Checking clipboard…", foreground="blue")
        self.status_lbl.pack(pady=5)

        # Save directory
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=5)
        ttk.Label(frm, text="Save to:").pack(side="left")
        ttk.Entry(frm, textvariable=self.save_dir, width=35).pack(side="left", padx=5)
        ttk.Button(frm, text="Browse…", command=self.choose_dir).pack(side="left")

        # File name
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=5)
        ttk.Label(frm, text="File name:").pack(side="left")
        ttk.Entry(frm, textvariable=self.file_name, width=25).pack(side="left", padx=5)
        ttk.Label(frm, text="(Leave blank to use timestamp)").pack(side="left")

        # Format
        frm = ttk.LabelFrame(self, text="Format")
        frm.pack(fill="x", pady=5)
        fmt_combo = ttk.Combobox(frm, textvariable=self.fmt_name,
                                 values=list(FORMATS.keys()), state="readonly", width=10)
        fmt_combo.pack(side="left", padx=5)
        self.fmt_name.trace_add("write", self.on_fmt_change)

        # Resolution
        frm = ttk.LabelFrame(self, text="Resolution")
        frm.pack(fill="x", pady=5)
        self.res_frm = frm
        self.build_resize_ui()

        # Save button
        self.btn_save = ttk.Button(self, text="Save Image", command=self.save_image)
        self.btn_save.pack(pady=10)
        self.btn_save.state(["disabled"])

    def build_resize_ui(self):
        # Clear previous widgets
        for w in self.res_frm.winfo_children():
            w.destroy()

        mode = self.resize_mode.get()
        ttk.Radiobutton(self.res_frm, text="Original", value="none",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(self.res_frm, text="Fixed long edge", value="long_edge",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(self.res_frm, text="Custom size", value="wh",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=2, sticky="w")

        if mode == "long_edge":
            ttk.Label(self.res_frm, text="Long edge(px):").grid(row=1, column=0, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.long_edge, width=6).grid(row=1, column=1, sticky="w")
        elif mode == "wh":
            ttk.Label(self.res_frm, text="Width:").grid(row=1, column=0, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.width, width=6).grid(row=1, column=1, sticky="w")
            ttk.Label(self.res_frm, text="Height:").grid(row=1, column=2, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.height, width=6).grid(row=1, column=3, sticky="w")

    def on_fmt_change(self, *_):
        """Refresh UI when format changes (for extension)"""
        pass

    def choose_dir(self):
        # Choose save directory
        d = filedialog.askdirectory(initialdir=self.save_dir.get())
        if d:
            self.save_dir.set(d)

    def check_clipboard(self):
        # Check if clipboard has image
        im = get_clipboard_image()
        if im is not None:
            self.status_lbl.config(text="✅ Image detected in clipboard", foreground="green")
            self.btn_save.state(["!disabled"])
        else:
            self.status_lbl.config(text="❌ No image in clipboard", foreground="red")
            self.btn_save.state(["disabled"])
        self.after(1000, self.check_clipboard)

    def save_image(self):
        # Save image
        im = get_clipboard_image()
        if im is None:
            messagebox.showerror("Error", "No image in clipboard")
            return

        # Resolution processing
        mode = self.resize_mode.get()
        if mode == "long_edge":
            im.thumbnail((self.long_edge.get(), self.long_edge.get()), Image.LANCZOS)
        elif mode == "wh":
            im = im.resize((self.width.get(), self.height.get()), Image.LANCZOS)

        # Directory & file name
        directory = pathlib.Path(self.save_dir.get())
        directory.mkdir(parents=True, exist_ok=True)

        name = self.file_name.get().strip()
        if not name:
            name = datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = FORMATS[self.fmt_name.get()][0]
        path = directory / f"{name}.{ext}"

        counter = 1
        while path.exists():
            path = directory / f"{name}_{counter}.{ext}"
            counter += 1

        # Save
        try:
            if ext.lower() in ("jpg", "jpeg"):
                im = im.convert("RGB")
            im.save(path)
        except Exception as e:
            messagebox.showerror("Save failed", str(e))
            return

        # Remember directory
        self.cfg["last_dir"] = str(directory)
        save_config(self.cfg)

        messagebox.showinfo("Success", f"Saved:\n{path}")

# ---------- Entry Point ----------
if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    App().mainloop()
    