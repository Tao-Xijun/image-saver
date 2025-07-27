# Clipboard Image Saver

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-brightgreen.svg)

A lightweight clipboard image saving tool supporting multiple export formats and custom resolution adjustment.

## Features

- 📋 **Clipboard Monitoring**: Automatically detects image content in the clipboard
- 🖼️ **Multiple Format Support**: PNG, JPG, BMP, TIFF, WebP, GIF, and more
- 📏 **Resolution Adjustment**:
  - Keep original size
  - Scale by fixed long edge
  - Custom width and height
- 📂 **Smart Naming**: Automatically generates timestamped filenames to avoid duplicates
- ⚙️ **Config Memory**: Remembers the last used directory

## Usage

### Install Dependencies
```bash
pip install pillow pyperclip
```

### Run the Program
```bash
python image-saver.py
```

### How to Use
1. Copy any image to the clipboard (screenshot/file copy)
2. The program will automatically detect the image (status bar turns green)
3. Set options:
   - Choose save directory (default is Downloads folder)
   - Enter filename (leave blank to use timestamp)
   - Select image format
   - Set resolution (optional)
4. Click the "Save Image" button

## Advanced Features

### Configuration File
User settings are saved in `~/.clipboard_saver.json` and can be edited manually:
```json
{
  "last_dir": "/path/to/your/last/directory"
}
```

### Resolution Modes
- **Original**: Keep original size
- **Fixed Long Edge**: Scale proportionally so the longest edge matches the set value
- **Custom Size**: Force resize to specified width and height

## FAQ

❓ **Why can't the clipboard image be detected?**
- Make sure you copied bitmap data (screenshot tools usually work)
- Some apps may use special formats

❓ **What if saving fails?**
- Check if the target directory is writable
- Try changing the image format

## Contribution Guide

We welcome all kinds of contributions! If you encounter any issues or have suggestions:
1. Check if a similar issue already exists
2. Open a new issue describing your problem or suggestion
3. For code contributions, please fork and submit a Pull Request

## Development Notes

### Compatibility
- Supports Windows/macOS/Linux
- Requires Python 3.6+

### Extension Suggestions
You can add more image formats