#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clipboard Image Saver – 监听版 / Clipboard Image Saver – Listener Edition
路径：D:\Tao\ClipboardSaver\clipimg.py / Path: D:\Tao\ClipboardSaver\clipimg.py
依赖：pillow pyperclip pystray pynput pyinstaller / Dependencies: pillow pyperclip pystray pynput pyinstaller
图标：icon.ico（窗口图标） / Icon: icon.ico (window icon)
托盘：tray_icon.png（托盘图标） / Tray: tray_icon.png (tray icon)
打包：build.ps1 / Packaging: build.ps1
"""
import os
import sys
import json
import pathlib
import threading
import queue
import time
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from PIL import Image, ImageGrab
except ImportError as e:
    print("Pillow is required: pip install pillow / Pillow 是必需的：pip install pillow")
    sys.exit(1)
import pyperclip

# ----------------------------------------------------------
# 语言资源 / Language resources
LANG = {
    "zh": {
        "app": "剪贴板图片保存器",
        "check": "正在检查剪贴板...",
        "ok": "✅ 已检测到剪贴板图片",
        "none": "❌ 剪贴板无图片",
        "save_btn": "保存图片",
        "save_to": "保存到：",
        "browse": "浏览...",
        "file_name": "文件名：",
        "blank_ts": "（留空用时间戳）",
        "format": "格式",
        "quality": "质量：",
        "resolution": "分辨率",
        "original": "原图",
        "long": "长边固定",
        "custom": "自定义宽高",
        "long_px": "长边像素：",
        "width": "宽：",
        "height": "高：",
        "override": "允许覆盖",
        "copy_path": "保存后复制路径到剪贴板",
        "listen_mode": "监听剪贴板",
        "saved": "已保存：\n{}",
        "auto_saved": "自动保存：{}",
        "err_no_img": "剪贴板无图片",
        "err_save": "保存失败：{}",
        "success": "成功",
        "error": "错误",
        "tray_open": "显示窗口",
        "tray_hide": "隐藏窗口",
        "tray_exit": "退出",
        "tray_listen_on": "启用监听",
        "tray_listen_off": "暂停监听",
        "log": "日志",
        "format_options": ["PNG", "JPG", "JPEG", "BMP", "TIFF", "WebP", "GIF"],
        "log_hotkey": "全局热键 Ctrl+Shift+S 已注册",
        "log_listen_on": "监听模式已开启",
        "log_listen_off": "监听模式已关闭",
        "log_tray_required": "托盘功能需安装 pystray 和 pillow",
        "log_hotkey_required": "全局热键需安装 pynput"
    },
    "en": {
        "app": "Clipboard Image Saver",
        "check": "Checking clipboard...",
        "ok": "✅ Image detected in clipboard",
        "none": "✅ No image in clipboard",
        "save_btn": "Save Image",
        "save_to": "Save to:",
        "browse": "Browse...",
        "file_name": "File name:",
        "blank_ts": "(Leave blank for timestamp)",
        "format": "Format",
        "quality": "Quality:",
        "resolution": "Resolution",
        "original": "Original",
        "long": "Fixed long edge",
        "custom": "Custom size",
        "long_px": "Long edge(px):",
        "width": "Width:",
        "height": "Height:",
        "override": "Allow overwrite",
        "copy_path": "Copy path to clipboard after save",
        "listen_mode": "Listen to clipboard",
        "saved": "Saved:\n{}",
        "auto_saved": "Auto saved: {}",
        "err_no_img": "No image in clipboard",
        "err_save": "Save failed: {}",
        "success": "Success",
        "error": "Error",
        "tray_open": "Show Window",
        "tray_hide": "Hide Window",
        "tray_exit": "Exit",
        "tray_listen_on": "Enable Listen",
        "tray_listen_off": "Disable Listen",
        "log": "Log",
        "format_options": ["PNG", "JPG", "JPEG", "BMP", "TIFF", "WebP", "GIF"],
        "log_hotkey": "Global hotkey Ctrl+Shift+S registered",
        "log_listen_on": "Listen mode enabled",
        "log_listen_off": "Listen mode disabled",
        "log_tray_required": "Tray requires pystray and pillow",
        "log_hotkey_required": "Global hotkey requires pynput"
    }
}

# ----------------------------------------------------------
# 配置 / Configuration
CONFIG_FILE = pathlib.Path.home() / ".clipboard_saver.json"
DEFAULT_DIR = pathlib.Path.home() / "Downloads"
FORMATS = {"PNG": ("png", True), "JPG": ("jpg", False), "JPEG": ("jpeg", False),
           "BMP": ("bmp", True), "TIFF": ("tiff", True), "WebP": ("webp", False),
           "GIF": ("gif", False)}

# ----------------------------------------------------------
# 工具函数 / Utility functions
def resource_path(rel: str) -> pathlib.Path:
    if hasattr(sys, '_MEIPASS'):
        return pathlib.Path(sys._MEIPASS) / rel
    return pathlib.Path(__file__).parent / rel

def load_config():
    dft = {"last_dir": str(DEFAULT_DIR), "lang": "zh", "quality": 95,
           "copy_path": True, "override": False, "listen_mode": False}
    if CONFIG_FILE.exists():
        try:
            dft.update(json.loads(CONFIG_FILE.read_text(encoding="utf8")))
        except Exception:
            pass
    return dft

def save_config(cfg):
    try:
        CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2),
                               encoding="utf8")
    except Exception as e:
        print("save_config:", e)

def get_clipboard_image():
    try:
        return ImageGrab.grabclipboard()
    except Exception:
        return None

# ----------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.L = LANG[self.cfg["lang"]]
        self.title(self.L["app"])
        self.resizable(False, False)
        self.configure(padx=20, pady=15)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # 变量 / Variables
        self.save_dir = tk.StringVar(value=self.cfg["last_dir"])
        self.file_name = tk.StringVar()
        self.fmt_name = tk.StringVar(value="PNG")
        self.resize_mode = tk.StringVar(value="none")
        self.long_edge = tk.IntVar(value=1920)
        self.width = tk.IntVar(value=1920)
        self.height = tk.IntVar(value=1080)
        self.quality = tk.IntVar(value=self.cfg["quality"])
        self.copy_path = tk.BooleanVar(value=self.cfg["copy_path"])
        self.override = tk.BooleanVar(value=self.cfg["override"])
        self.listen_mode = tk.BooleanVar(value=self.cfg["listen_mode"])

        self._last_digest = None
        self.log_queue = queue.Queue()

        self.init_ui()
        self.init_tray()
        self.init_hotkey()
        self.after(200, self.process_log)
        self.schedule_clipboard()

    # ---------------- UI ----------------
    def init_ui(self):
        # 语言按钮 / Language buttons
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=2)
        ttk.Button(frm, text="中文", width=4,
                   command=lambda: self.switch_lang("zh")).pack(side="right")
        ttk.Button(frm, text="EN", width=3,
                   command=lambda: self.switch_lang("en")).pack(side="right", padx=2)

        self.title_lbl = ttk.Label(self, text=self.L["app"], font=("Segoe UI", 14, "bold"))
        self.title_lbl.pack()
        self.status_lbl = ttk.Label(self, text=self.L["check"], foreground="blue")
        self.status_lbl.pack(pady=5)

        # 目录 / Directory
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=5)
        ttk.Label(frm, text=self.L["save_to"]).pack(side="left")
        ttk.Entry(frm, textvariable=self.save_dir, width=35).pack(side="left", padx=5)
        ttk.Button(frm, text=self.L["browse"], command=self.choose_dir).pack(side="left")

        # 文件名 / File name
        frm = ttk.Frame(self)
        frm.pack(fill="x", pady=5)
        ttk.Label(frm, text=self.L["file_name"]).pack(side="left")
        ttk.Entry(frm, textvariable=self.file_name, width=25).pack(side="left", padx=5)
        self.blank_lbl = ttk.Label(frm, text=self.L["blank_ts"])
        self.blank_lbl.pack(side="left")

        # 格式 / Format
        self.fmt_frm = ttk.LabelFrame(self, text=self.L["format"])
        self.fmt_frm.pack(fill="x", pady=5)
        fmt_combo = ttk.Combobox(self.fmt_frm, textvariable=self.fmt_name,
                                 values=self.L["format_options"], state="readonly", width=8)
        fmt_combo.pack(side="left", padx=5)
        fmt_combo.bind("<<ComboboxSelected>>", self.on_fmt_change)
        self.quality_lbl = ttk.Label(self.fmt_frm, text=self.L["quality"])
        self.quality_lbl.pack(side="left", padx=(15, 5))
        self.quality_scl = ttk.Scale(self.fmt_frm, from_=1, to=100, variable=self.quality,
                                     orient="horizontal", length=120)
        self.quality_scl.pack(side="left")
        self.quality_val = ttk.Label(self.fmt_frm, text=str(self.quality.get()))
        self.quality_val.pack(side="left", padx=5)
        self.quality_scl.bind("<Motion>",
                              lambda e: self.quality_val.config(text=str(int(self.quality.get()))))
        self.on_fmt_change()

        # 分辨率 / Resolution
        self.res_frm = ttk.LabelFrame(self, text=self.L["resolution"])
        self.res_frm.pack(fill="x", pady=5)
        self.build_resize_ui()

        # 选项 / Options
        self.opt_frm = ttk.Frame(self)
        self.opt_frm.pack(fill="x", pady=5)
        self.override_btn = ttk.Checkbutton(self.opt_frm, text=self.L["override"], variable=self.override)
        self.override_btn.pack(side="left")
        self.copy_path_btn = ttk.Checkbutton(self.opt_frm, text=self.L["copy_path"], variable=self.copy_path)
        self.copy_path_btn.pack(side="left", padx=10)
        self.listen_btn = ttk.Checkbutton(self.opt_frm, text=self.L["listen_mode"], variable=self.listen_mode,
                        command=self.on_listen_toggle)
        self.listen_btn.pack(side="left", padx=10)

        # 保存 / Save
        self.btn_save = ttk.Button(self, text=self.L["save_btn"], command=self.save_image)
        self.btn_save.pack(pady=10)
        self.btn_save.state(["disabled"])

        # 日志 / Log
        self.log_frm = ttk.LabelFrame(self, text=self.L["log"])
        self.log_frm.pack(fill="both", expand=True, pady=5)
        self.log_text = tk.Text(self.log_frm, height=5, width=50, state="disabled")
        self.log_text.pack(padx=5, pady=5)

    # ---------------- 分辨率 UI / Resolution UI ----------------
    def build_resize_ui(self):
        for w in self.res_frm.winfo_children():
            w.destroy()
        L = self.L
        ttk.Radiobutton(self.res_frm, text=L["original"], value="none",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(self.res_frm, text=L["long"], value="long_edge",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(self.res_frm, text=L["custom"], value="wh",
                        variable=self.resize_mode,
                        command=self.build_resize_ui).grid(row=0, column=2, sticky="w")
        mode = self.resize_mode.get()
        if mode == "long_edge":
            ttk.Label(self.res_frm, text=L["long_px"]).grid(row=1, column=0, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.long_edge, width=6).grid(row=1, column=1, sticky="w")
        elif mode == "wh":
            ttk.Label(self.res_frm, text=L["width"]).grid(row=1, column=0, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.width, width=6).grid(row=1, column=1, sticky="w")
            ttk.Label(self.res_frm, text=L["height"]).grid(row=1, column=2, sticky="e")
            ttk.Spinbox(self.res_frm, from_=1, to=9999,
                        textvariable=self.height, width=6).grid(row=1, column=3, sticky="w")

    def on_fmt_change(self, *args):
        lossy = not FORMATS[self.fmt_name.get()][1]
        st = "normal" if lossy else "disabled"
        self.quality_lbl.config(state=st)
        self.quality_scl.config(state=st)
        self.quality_val.config(state=st)

    def choose_dir(self):
        d = filedialog.askdirectory(initialdir=self.save_dir.get())
        if d:
            self.save_dir.set(d)

    # ---------------- 日志 / Log ----------------
    def log(self, msg_key, *args):
        message = self.L[msg_key].format(*args) if args else self.L[msg_key]
        self.log_queue.put(message)

    def process_log(self):
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.config(state="normal")
                self.log_text.insert("end", f"{datetime.now():%H:%M:%S}  {msg}\n")
                self.log_text.see("end")
                self.log_text.config(state="disabled")
        except queue.Empty:
            pass
        self.after(200, self.process_log)

    # ---------------- 语言 / 托盘 / Language / Tray ----------------
    def switch_lang(self, lang):
        self.cfg["lang"] = lang
        save_config(self.cfg)
        self.L = LANG[lang]
        self.refresh_text()
    
    def refresh_text(self):
        L = self.L
        self.title(L["app"])
        self.title_lbl.config(text=L["app"])
        self.status_lbl.config(text=L["check"])
        self.blank_lbl.config(text=L["blank_ts"])
        self.quality_lbl.config(text=L["quality"])
        self.btn_save.config(text=L["save_btn"])
        
        # Update frame titles
        self.fmt_frm.config(text=L["format"])
        self.res_frm.config(text=L["resolution"])
        self.log_frm.config(text=L["log"])
        
        # Update option buttons
        self.override_btn.config(text=L["override"])
        self.copy_path_btn.config(text=L["copy_path"])
        self.listen_btn.config(text=L["listen_mode"])
        
        # Rebuild resolution UI
        self.build_resize_ui()
        
        # Update tray menu
        self.update_tray_menu()

    def init_tray(self):
        try:
            import pystray
            from PIL import Image as PILImage
        except ImportError:
            self.log("log_tray_required")
            return

        tray_img_path = resource_path("icon.ico")
        try:
            img = PILImage.open(tray_img_path).convert("RGBA")
        except Exception:
            img = PILImage.new("RGBA", (64, 64), (0, 0, 0, 0))

        self.tray_icon = pystray.Icon(
            self.L["app"], img, self.L["app"], self.build_tray_menu())
        threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def build_tray_menu(self):
        import pystray
        return pystray.Menu(
            pystray.MenuItem(self.L["tray_open"], self.show_window, default=True),
            pystray.MenuItem(self.L["tray_hide"], self.hide_window),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                lambda txt: self.L["tray_listen_off"] if self.listen_mode.get()
                else self.L["tray_listen_on"], self.toggle_listen_tray),
            pystray.MenuItem(self.L["tray_exit"], self.quit_app)
        )

    def update_tray_menu(self):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.menu = self.build_tray_menu()

    def show_window(self, *args):
        self.after(0, lambda: (self.deiconify(), self.lift()))

    def hide_window(self, *args):
        self.after(0, self.withdraw())

    def on_close(self):
        self.hide_window()

    def quit_app(self, *args):
        if hasattr(self, 'tray_icon'):
            self.tray_icon.stop()
        self.destroy()

    def toggle_listen_tray(self):
        self.listen_mode.set(not self.listen_mode.get())
        self.on_listen_toggle()

    # ---------------- 热键 / Hotkey ----------------
    def init_hotkey(self):
        try:
            from pynput import keyboard
        except ImportError:
            self.log("log_hotkey_required")
            return
        def hotkey():
            if not self.btn_save.instate(["disabled"]):
                self.save_image()
        listener = keyboard.GlobalHotKeys({'<ctrl>+<shift>+s': hotkey})
        listener.start()
        self.log("log_hotkey")
    

    # ---------------- 监听 / Listen ----------------
    def on_listen_toggle(self):
        save_config({**self.cfg, "listen_mode": self.listen_mode.get()})
        self.update_tray_menu()
        self.log("log_listen_on" if self.listen_mode.get() else "log_listen_off")

    def schedule_clipboard(self):
        self.check_clipboard()
        self.after(500 if self.listen_mode.get() else 1000, self.schedule_clipboard)

    def check_clipboard(self):
        im = get_clipboard_image()
        if im is None:
            self.status_lbl.config(text=self.L["none"], foreground="red")
            self.btn_save.state(["disabled"])
            self._last_digest = None
            return
        digest = im.tobytes()[:1024]
        if self.listen_mode.get() and digest != self._last_digest:
            self._last_digest = digest
            threading.Thread(target=self.auto_save_image, args=(im,), daemon=True).start()
        else:
            self._last_digest = None
        self.status_lbl.config(text=self.L["ok"], foreground="green")
        self.btn_save.state(["!disabled"])

    # ---------------- 保存 / Save ----------------
    def make_path(self):
        d = pathlib.Path(self.save_dir.get())
        d.mkdir(parents=True, exist_ok=True)
        name = self.file_name.get().strip() or datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = FORMATS[self.fmt_name.get()][0]
        path = d / f"{name}.{ext}"
        if not self.override.get():
            counter = 1
            while path.exists():
                path = d / f"{name}_{int(time.time()*1000)}.{ext}"
                counter += 1
        return path

    def save_image(self):
        im = get_clipboard_image()
        if im is None:
            messagebox.showerror(self.L["error"], self.L["err_no_img"])
            return
        self._save(im, self.make_path(), show_msg=True)

    def auto_save_image(self, im):
        self._save(im, self.make_path(), show_msg=False)

    def _save(self, im, path, show_msg=False):
        try:
            mode = self.resize_mode.get()
            if mode == "long_edge":
                im.thumbnail((self.long_edge.get(), self.long_edge.get()), Image.LANCZOS)
            elif mode == "wh":
                im = im.resize((self.width.get(), self.height.get()), Image.LANCZOS)
            ext = path.suffix.lower()[1:]
            kw = {}
            if ext in ("jpg", "jpeg"):
                im = im.convert("RGB")
                kw["quality"] = self.quality.get()
            elif ext == "webp":
                kw["quality"] = self.quality.get()
            im.save(path, **kw)
        except Exception as e:
            self.log("err_save", str(e))
            if show_msg:
                messagebox.showerror(self.L["error"], self.L["err_save"].format(e))
            return
        
        save_config({**self.cfg,
                    "last_dir": str(path.parent),
                    "quality": self.quality.get(),
                    "copy_path": self.copy_path.get(),
                    "override": self.override.get()})
        
        msg_key = "saved" if show_msg else "auto_saved"
        self.log(msg_key, str(path))
        
        if self.copy_path.get():
            pyperclip.copy(str(path))


# ----------------------------------------------------------
if __name__ == "__main__":
    if sys.platform == "win32":
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    App().mainloop()