# Media 图片资源管理项目

## 📖 项目简介

这是一个专业的图片资源管理项目，提供高效的图片压缩、管理和存储解决方案。项目集成了智能压缩算法、并发处理技术和完整的Git版本控制，为开发者和管理员提供强大的图片资源管理工具。

## ✨ 主要功能

### 🖼️ 智能图片压缩
- **多格式支持**: PNG、JPG、JPEG、BMP、GIF、TIFF、WebP等
- **智能压缩判断**: 自动跳过压缩率不达标的文件，避免文件变大
- **可配置压缩参数**: 自定义质量、最大尺寸、压缩率阈值
- **批量处理**: 支持整个目录的批量压缩

### 🚀 并发处理
- **多线程压缩**: 显著提升处理速度
- **可配置工作线程数**: 根据系统性能调整并发数
- **线程安全输出**: 避免日志混乱

### 🛠️ 开发工具
- **Python脚本**: 完整的压缩处理脚本
- **依赖管理**: requirements.txt 文件
- **跨平台支持**: Windows、macOS、Linux

### 📁 版本控制
- **Git集成**: 完整的版本控制支持
- **大文件优化**: 支持大量图片文件的存储
- **远程同步**: GitHub仓库同步

## 🚀 快速开始

### 环境要求
- Python 3.7+
- Git
- 足够的磁盘空间

### 安装步骤

1. **克隆仓库**
```bash
git clone https://github.com/trueLoving/Media.git
cd Media
```

2. **安装依赖**
```bash
cd scripts
pip install -r requirements.txt
```

3. **运行压缩脚本**
```bash
python compress_images.py
```

## 📋 使用方法

### 基本用法

```bash
# 使用默认参数压缩images目录
python scripts/compress_images.py

# 指定输出目录
python scripts/compress_images.py --output images/compressed

# 设置压缩质量
python scripts/compress_images.py --quality 85

# 设置最大尺寸
python scripts/compress_images.py --max-size 1920

# 设置最小压缩率
python scripts/compress_images.py --min-compression 10

# 设置并发线程数
python scripts/compress_images.py --workers 8
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--input` | 输入目录 | `images` |
| `--output` | 输出目录 | `images/compressed` |
| `--quality` | 压缩质量 (1-100) | `85` |
| `--max-size` | 最大尺寸 (像素) | `1920` |
| `--min-compression` | 最小压缩率 (%) | `0` |
| `--workers` | 并发线程数 | `4` |
| `--overwrite` | 覆盖已存在的文件 | `False` |

## 📁 项目结构

```
Media/
├── README.md                 # 项目说明文档
├── images/                   # 图片资源目录
│   └── website/             # 网站图片资源
│       ├── *.png            # PNG格式图片
│       ├── *.jpg            # JPG格式图片
│       ├── *.jpeg           # JPEG格式图片
│       └── *.bmp            # BMP格式图片
└── scripts/                  # 脚本工具目录
    ├── compress_images.py    # 主压缩脚本
    ├── requirements.txt      # Python依赖
    └── README.md            # 脚本使用说明
```

## 🔧 脚本功能详解

### compress_images.py

主要的图片压缩脚本，具有以下特性：

- **智能压缩**: 自动判断是否需要压缩
- **并发处理**: 多线程并行压缩
- **进度显示**: 实时显示压缩进度和统计信息
- **错误处理**: 完善的异常处理机制
- **日志记录**: 详细的压缩日志

### 压缩算法

1. **尺寸调整**: 如果图片超过最大尺寸，按比例缩放
2. **质量压缩**: 使用Pillow库进行高质量压缩
3. **格式保持**: 保持原始图片格式
4. **智能判断**: 跳过压缩率不达标的文件

## 📊 性能特性

### 并发性能
- **4线程**: 处理速度提升约3-4倍
- **8线程**: 适合高性能系统
- **可扩展**: 根据CPU核心数调整

### 压缩效果
- **平均压缩率**: 20-60%
- **质量保持**: 85%质量下视觉差异极小
- **文件大小**: 显著减少存储空间

## 🐛 故障排除

### 常见问题

1. **依赖安装失败**
```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Pillow
```

2. **内存不足**
```bash
# 减少并发线程数
python scripts/compress_images.py --workers 2
```

3. **权限问题**
```bash
# 确保有目录写入权限
chmod 755 images/
```

### 错误代码

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `ModuleNotFoundError` | 缺少依赖 | 安装requirements.txt |
| `PermissionError` | 权限不足 | 检查目录权限 |
| `MemoryError` | 内存不足 | 减少并发数 |

## 🤝 贡献指南

欢迎贡献代码和提出建议！

### 贡献方式
1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起 Pull Request

### 代码规范
- 遵循PEP 8 Python代码规范
- 添加适当的注释和文档
- 确保代码通过测试

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- **项目地址**: https://github.com/trueLoving/Media
- **问题反馈**: 通过GitHub Issues提交
- **功能建议**: 欢迎提出新功能建议

## 🔄 更新日志

### v1.0.0 (2024-12-19)
- ✨ 初始版本发布
- 🖼️ 智能图片压缩功能
- 🚀 并发处理支持
- 📁 完整的项目结构
- 📚 详细的使用文档

---

**⭐ 如果这个项目对您有帮助，请给个Star支持一下！** 