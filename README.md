Here are the polished markdown versions of both README files:

---

**README.md (English)**

```markdown
# Clipboard Image Saver – Listener Edition

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-Free-green)

A Python application that monitors your clipboard for images and allows you to save them with customizable options.

## ✨ Features

- 📋 One-click clipboard image saving
- 🔍 Auto-save in listener mode
- 🖼️ Multiple formats: PNG, JPG, BMP, TIFF, WebP, GIF
- 📏 Resize options: original/fixed long edge/custom
- 🎚️ Quality control for lossy formats
- 🖥️ System tray operation
- ⌨️ Global hotkey (Ctrl+Shift+S)
- 🌐 Bilingual UI (English/中文)
- 📋 Automatic path copying
- 🗂️ Configurable save directory and filename

## ⚙️ Requirements

- Python 3.6+
- Dependencies:
  ```bash
  pip install pillow pyperclip pystray pynput
  ```

## 🚀 Installation

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python clipimg.py
   ```

## 📖 Usage Guide

1. Copy any image to clipboard
2. Application will auto-detect
3. Configure save options:
   - Save directory
   - Filename (timestamp if blank)
   - Image format
   - Quality (JPG/WebP)
   - Resolution settings
4. Save via:
   - "Save Image" button
   - Ctrl+Shift+S hotkey
5. Enable listener mode for auto-saving

## ⚡ Configuration

Settings stored in `~/.clipboard_saver.json`:

| Setting | Description |
|---------|-------------|
| `last_dir` | Last used directory |
| `lang` | UI language (zh/en) |
| `quality` | Default quality (1-100) |
| `copy_path` | Copy path after save |
| `override` | Allow file overwrite |
| `listen_mode` | Auto-save enabled |

## ⚠️ Known Issues

- ❗ May conflict with clipboard managers
- ❗ Tray requires pystray+PIL
- ❗ Hotkey requires pynput

## 🤝 Contributing

Found an issue? Want to improve?

1. Open an issue with details
2. Suggest possible solutions
3. PRs are welcome!

## 📜 License

Free for use and modification.
```

---

**README.md (中文)**

```markdown
# 剪贴板图片保存器 – 监听版

![Python 版本](https://img.shields.io/badge/python-3.6%2B-blue)
![许可证](https://img.shields.io/badge/license-Free-green)

一个可以监控剪贴板并保存图片的Python应用程序

## ✨ 功能特点

- 📋 一键保存剪贴板图片
- 🔍 监听模式自动保存
- 🖼️ 多种格式: PNG/JPG/BMP/TIFF/WebP/GIF
- 📏 分辨率调整: 原图/固定长边/自定义
- 🎚️ 有损格式质量调节
- 🖥️ 托盘后台运行
- ⌨️ 全局热键 (Ctrl+Shift+S)
- 🌐 双语界面 (中文/English)
- 📋 自动复制文件路径
- 🗂️ 可配置保存路径和文件名

## ⚙️ 系统要求

- Python 3.6+
- 依赖包:
  ```bash
  pip install pillow pyperclip pystray pynput
  ```

## 🚀 安装方法

1. 克隆或下载仓库
2. 安装依赖:
   ```bash
   pip install -r requirements.txt
   ```
3. 运行程序:
   ```bash
   python clipimg.py
   ```

## 📖 使用指南

1. 复制图片到剪贴板
2. 程序自动检测图片
3. 配置保存选项:
   - 保存目录
   - 文件名 (留空使用时间戳)
   - 图片格式
   - 质量 (JPG/WebP)
   - 分辨率设置
4. 保存方式:
   - 点击"保存图片"按钮
   - 使用Ctrl+Shift+S热键
5. 开启监听模式自动保存

## ⚡ 配置信息

设置保存在`~/.clipboard_saver.json`:

| 配置项 | 说明 |
|--------|------|
| `last_dir` | 上次使用的目录 |
| `lang` | 界面语言 (zh/en) |
| `quality` | 默认质量 (1-100) |
| `copy_path` | 保存后复制路径 |
| `override` | 允许覆盖文件 |
| `listen_mode` | 自动保存开关 |

## ⚠️ 已知问题

- ❗ 可能与剪贴板管理器冲突
- ❗ 托盘需要pystray+PIL
- ❗ 热键需要pynput

## 🤝 贡献指南

发现问题或有改进建议？

1. 提交issue描述问题
2. 建议解决方案
3. 欢迎提交PR!

## 📜 许可证

可自由使用和修改
```

Key improvements:
1. Added badges for version and license
2. Organized content with better markdown formatting
3. Added emoji visual indicators
4. Created tables for configuration
5. Improved section headers
6. Added code block formatting
7. Made installation steps clearer
8. Enhanced visual hierarchy

Both files maintain the same content but with much better readability and visual appeal. You can use either or both in your project.