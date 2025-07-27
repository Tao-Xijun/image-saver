#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
剪贴板图片保存器
支持多格式 & 自定义分辨率
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
import pathlib

from PIL import Image, ImageGrab
import pyperclip

APP_NAME = "剪贴板图片保存器"
CONFIG_FILE = pathlib.Path.home() / ".clipboard_saver.json"
DEFAULT_DIR = pathlib.Path.home() / "Downloads"

FORMATS = {
    "PNG":  ("png",  True),   # 后缀, 是否支持无损
    "JPG":  ("jpg",  False),
    "JPEG": ("jpeg", False),
    "BMP":  ("bmp",  True),
    "TIFF": ("tiff", True),
    "WebP": ("webp", True),
    "GIF":  ("gif",  False),
}

# ---------- 工具 ----------
def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"last_dir": str(DEFAULT_DIR)}

def save_config(cfg):
    try:
        CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception as e:
        print("保存配置失败:", e)

def get_clipboard_image():
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
        # 标题
        ttk.Label(self, text=APP_NAME, font=("Segoe UI", 14, "bold")).pack()

        # 剪贴板状态
        self.status_lbl = ttk.Label(self, text="正在检查剪贴板…", foreground="blue")
        self.status_lbl.pack(pady=5)

        # 保存路径
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=5)
        ttk.Label(frm, text="保存到：").pack(side="left")
        ttk.Entry(frm, textvariable=self.save_dir, width=35).pack(side="left", padx=5)
        ttk.Button(frm, text="浏览…", command=self.choose_dir).pack(side="left")

        # 文件名
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=5)
        ttk.Label(frm, text="文件名：").pack(side="left")
        ttk.Entry(frm, textvariable=self.file_name, width=25).pack(side="left", padx=5)
        ttk.Label(frm, text="（留空用时间戳）").pack(side="left")

        # 格式
        frm = ttk.LabelFrame(self, text="格式")
        frm.pack(fill="x", pady=5)
        fmt_combo = ttk.Combobox(frm, textvariable=self.fmt_name,
                                 values=list(FORMATS.keys()), state="readonly", width=10)
        fmt_combo.pack(side="left", padx=5)
        self.fmt_name.trace_add("write", self.on_fmt_change)

        # 分辨率
        frm = ttk.LabelFrame(self, text="分辨率")
        frm.pack(fill="x", pady=5)
        self.res_frm = frm
        self.build_resize_ui()

        # 保存按钮
        self.btn_save = ttk.Button(self, text="保存图片", command=self.save_image)
        self.btn_save.pack(pady=10)
        self.btn_save.state(["disabled"])

    def build_resize_ui(self):
        # 先清空
        for w in self.res_frm.winfo_children():
            w.destroy()

        mode = self.resize_mode.get()
        ttk.Radiobutton(self.res_frm, text="原图", value="none",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(self.res_frm, text="长边固定", value="long_edge",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(self.res_frm, text="自定义宽高", value="wh",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=2, sticky="w")

        if mode == "long_edge":
            ttk.Label(self.res_frm, text="长边像素：").grid(row=1, column=0, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.long_edge, width=6).grid(row=1, column=1, sticky="w")
        elif mode == "wh":
            ttk.Label(self.res_frm, text="宽：").grid(row=1, column=0, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.width, width=6).grid(row=1, column=1, sticky="w")
            ttk.Label(self.res_frm, text="高：").grid(row=1, column=2, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.height, width=6).grid(row=1, column=3, sticky="w")

    def on_fmt_change(self, *_):
        """格式改变时刷新 UI（可扩展）"""
        pass

    def choose_dir(self):
        d = filedialog.askdirectory(initialdir=self.save_dir.get())
        if d:
            self.save_dir.set(d)

    def check_clipboard(self):
        im = get_clipboard_image()
        if im is not None:
            self.status_lbl.config(text="✅ 已检测到剪贴板图片", foreground="green")
            self.btn_save.state(["!disabled"])
        else:
            self.status_lbl.config(text="❌ 剪贴板无图片", foreground="red")
            self.btn_save.state(["disabled"])
        self.after(1000, self.check_clipboard)

    def save_image(self):
        im = get_clipboard_image()
        if im is None:
            messagebox.showerror("错误", "剪贴板无图片")
            return

        # 分辨率处理
        mode = self.resize_mode.get()
        if mode == "long_edge":
            im.thumbnail((self.long_edge.get(), self.long_edge.get()), Image.LANCZOS)
        elif mode == "wh":
            im = im.resize((self.width.get(), self.height.get()), Image.LANCZOS)

        # 目录 / 文件名
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

        # 保存
        try:
            if ext.lower() in ("jpg", "jpeg"):
                im = im.convert("RGB")
            im.save(path)
        except Exception as e:
            messagebox.showerror("保存失败", str(e))
            return

        # 记住目录
        self.cfg["last_dir"] = str(directory)
        save_config(self.cfg)

        messagebox.showinfo("成功", f"已保存：\n{path}")

# ---------- 启动 ----------
if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    App().mainloop()