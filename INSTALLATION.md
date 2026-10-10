# File Action Skill - 安装指南

## 📋 系统要求

- **操作系统**：Windows、macOS、Linux
- **Python**：3.7 或更高版本
- **磁盘空间**：至少 100MB（取决于证书数量）
- **内存**：至少 512MB

## 🚀 安装步骤

### 1. 获取技能

```bash
# 方式一：克隆 Git 仓库
git clone https://github.com/openclaw/clawhub.git
cd clawhub/skills/file-action-skill

# 方式二：下载并解压
wget https://example.com/file-action-skill.zip
unzip file-action-skill.zip
cd file-action-skill
```

### 2. 运行安装脚本

```bash
# Linux / macOS
chmod +x install.sh
./install.sh

# Windows (Git Bash)
chmod +x install.sh
./install.sh

# Windows (PowerShell)
# 手动执行安装步骤
```

### 3. 手动安装（可选）

如果安装脚本无法运行，可以手动安装：

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv

# 激活虚拟环境
# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# 创建目录结构
mkdir -p scripts
mkdir -p config

# 复制配置文件
cp config.example.json config/config.json

# 设置执行权限
chmod +x scripts/*.py
```

### 4. 配置环境变量

```bash
# Linux / macOS
export STORAGE_DIR=/path/to/your/storage/directory

# Windows (PowerShell)
$env:STORAGE_DIR="C:\path\to\your\storage\directory"

# Windows (CMD)
set STORAGE_DIR=C:\path\to\your\storage\directory
```

或者创建 `.env` 文件：

```bash
# .env
STORAGE_DIR=/path/to/your/storage/directory
```

### 5. 验证安装

```bash
# 运行测试
python tests/test_certificate_manager.py

# 查看帮助
python scripts/process_file.py --help
```

## 📁 目录结构

安装完成后，目录结构如下：

```
file-action-skill/
├── SKILL.md                          # 技能定义文件
├── README.md                         # 使用说明
├── INSTALLATION.md                   # 安装指南
├── SKILL_STRUCTURE.md                # 结构说明
├── config.example.json               # 配置示例
├── install.sh                        # 安装脚本
├── uninstall.sh                      # 卸载脚本
├── .gitignore                        # Git 忽略文件
│
├── scripts/                          # 脚本目录
│   ├── certificate_manager.py        # 核心管理器
│   ├── identify_certificate.py       # 证书识别器
│   └── process_file.py               # 文件处理器
│
├── examples/                         # 示例目录
│   ├── sample_files.json             # 示例文件数据
│   ├── sample_tags.json              # 示例标签数据
│   ├── sample_dates.json             # 示例日期数据
│   └── usage_examples.md             # 使用示例
│
├── tests/                            # 测试目录
│   └── test_certificate_manager.py   # 测试脚本
│
├── config/                           # 配置目录
│   └── config.json                   # 配置文件
│
└── venv/                             # 虚拟环境（可选）
```

## ⚙️ 配置说明

### 基本配置

编辑 `config/config.json` 文件：

```json
{
  "storage_dir": "/path/to/your/storage/directory",
  "supported_formats": [".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"],
  "max_file_size": 10485760,
  "ocr_enabled": true,
  "ocr_language": "chi_sim"
}
```

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `storage_dir` | 文件存储目录 | `./storage` |
| `supported_formats` | 支持的文件格式 | `[".jpg", ".jpeg", ".png", ".pdf"]` |
| `max_file_size` | 最大文件大小（字节） | `10485760` (10MB) |
| `ocr_enabled` | 是否启用 OCR | `true` |
| `ocr_language` | OCR 语言 | `chi_sim` |
| `auto_backup` | 自动备份 | `true` |
| `backup_interval_days` | 备份间隔（天） | `7` |
| `backup_path` | 备份路径 | `./backups` |

## 🔧 依赖安装

### Python 依赖

```bash
# 基础依赖（必需）
pip install --upgrade pip

# OCR 依赖（可选）
pip install pytesseract
pip install Pillow

# PDF 处理（可选）
pip install PyPDF2
pip install pdf2image

# Excel 导出（可选）
pip install openpyxl
```

### 系统依赖

#### OCR 依赖

**Windows：**
```bash
# 下载并安装 Tesseract OCR
# https://github.com/UB-Mannheim/tesseract/wiki
```

**macOS：**
```bash
brew install tesseract
brew install tesseract-lang
```

**Linux：**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-chi-sim
```

## 🧪 测试安装

### 运行测试套件

```bash
python tests/test_certificate_manager.py
```

### 测试命令行工具

```bash
# 处理证书
python scripts/process_file.py --storage-dir $STORAGE_DIR upload test.jpg --text "测试内容"

# 搜索证书
python scripts/process_file.py --storage-dir $STORAGE_DIR search "测试"

# 列出标签
python scripts/process_file.py --storage-dir $STORAGE_DIR tags

# 生成报告
python scripts/process_file.py --storage-dir $STORAGE_DIR report
```

## 🔗 集成到 OpenClaw

### 1. 复制技能到 OpenClaw 技能目录

```bash
# 查找 OpenClaw 技能目录
find ~ -name ".openclaw" -type d

# 复制技能
cp -r file-action-skill ~/.openclaw/skills/
```

### 2. 在 OpenClaw 中启用技能

```bash
# 使用 OpenClaw CLI
openclaw skill enable file-action-skill

# 或者在配置文件中启用
vim ~/.openclaw/config.yaml
```

### 3. 测试集成

```
用户：[发送证书图片]

系统：我识别到这是一个获奖证书，请确认以下信息是否正确...
```

## 🛠️ 故障排除

### 常见问题

**Q: 安装脚本无法运行**
```bash
# 确保有执行权限
chmod +x install.sh

# 检查 Python 版本
python3 --version

# 手动安装
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

**Q: 找不到模块**
```bash
# 确保在正确的目录
cd file-action-skill

# 激活虚拟环境
source venv/bin/activate

# 添加到 Python 路径
export PYTHONPATH=$PYTHONPATH:$(pwd)/scripts
```

**Q: OCR 识别不准确**
```bash
# 检查 Tesseract 是否安装
tesseract --version

# 安装语言包
# macOS
brew install tesseract-lang

# Linux
sudo apt-get install tesseract-ocr-chi-sim
```

**Q: 存储目录权限错误**
```bash
# 创建存储目录
mkdir -p /path/to/storage

# 设置权限
chmod 755 /path/to/storage
```

### 日志文件

查看日志文件以获取更多信息：

```bash
# 查看错误日志
tail -f logs/error.log

# 查看调试日志
tail -f logs/debug.log
```

## 📞 获取帮助

如果遇到问题，请：

1. 查看 README.md 文件
2. 查看 SKILL_STRUCTURE.md 文件
3. 运行测试脚本
4. 提交 Issue 到 GitHub 仓库

## 🔄 更新技能

```bash
# 拉取最新版本
git pull origin main

# 重新安装
./install.sh

# 运行测试
python tests/test_certificate_manager.py
```

## 🗑️ 卸载技能

```bash
# 运行卸载脚本
./uninstall.sh

# 或者手动删除
rm -rf file-action-skill
```

## 📝 更新日志

### v1.0.0 (2024-10-10)
- ✨ 初始版本
- 📄 支持基本的证书识别和管理
- 🏷️ 支持标签管理
- 🔍 支持多种搜索方式
- 📊 支持报告生成

---

**安装完成后，即可开始使用 File Action Skill！** 🎉