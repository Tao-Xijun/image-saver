


# 剪贴板图片保存器

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Issues Welcome](https://img.shields.io/badge/Issues-Welcome-brightgreen.svg)

一款轻量级的剪贴板图片保存工具，支持多格式导出和自定义分辨率调整。

## 功能特性

- 📋 **剪贴板监控**：自动检测剪贴板中的图片内容
- 🖼️ **多格式支持**：PNG、JPG、BMP、TIFF、WebP、GIF等常见格式
- 📏 **分辨率调整**：
  - 保持原图
  - 固定长边缩放
  - 自定义宽高
- 📂 **智能命名**：自动生成时间戳文件名，避免重复
- ⚙️ **配置记忆**：保存最后一次使用的目录设置

## 使用说明

### 安装依赖
```bash
pip install pillow pyperclip
```

### 运行程序
```bash
python image-saver.py
```

### 操作指南
1. 复制任意图片到剪贴板（截图/文件复制）
2. 程序会自动检测到图片（状态栏变绿）
3. 设置选项：
   - 选择保存目录（默认下载文件夹）
   - 输入文件名（留空使用时间戳）
   - 选择图片格式
   - 设置分辨率（可选）
4. 点击"保存图片"按钮

## 高级功能

### 配置文件
用户设置保存在 `~/.clipboard_saver.json` 中，可手动编辑：
```json
{
  "last_dir": "/path/to/your/last/directory"
}
```

### 分辨率模式说明
- **原图**：保持原始尺寸
- **长边固定**：按比例缩放，最长边为设定值
- **自定义宽高**：强制调整为指定尺寸

## 常见问题

❓ **为什么检测不到剪贴板图片？**
- 确保复制的是位图数据（截图工具通常可以）
- 某些应用可能使用特殊格式复制

❓ **保存失败怎么办？**
- 检查目标目录是否有写入权限
- 尝试更换图片格式

## 贡献指南

我们欢迎各种形式的贡献！如果您遇到任何问题或有改进建议：
1. 请先检查现有Issues是否已有类似问题
2. 新建Issue描述您的问题或建议
3. 如需提交代码，请fork后通过Pull Request提交

## 开发说明

### 兼容性
- 支持 Windows/macOS/Linux
- 需要 Python 3.6+

### 扩展建议
可通过修改 `FORMATS` 字典添加更多图片格式支持

