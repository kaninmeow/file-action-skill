# File Action Skill - 项目总结

## 📋 项目概述

**File Action Skill** 是一个用于 OpenClaw 的技能，帮助大学生和个人管理各类证书、获奖证书、荣誉证书和申报材料。

### 核心功能

- 📄 **智能识别**：自动识别证书类型和内容
- 🏷️ **标签管理**：为文件添加自定义标签
- 📅 **日期提取**：自动识别获奖日期
- 🔍 **快速检索**：通过标签、日期或关键词快速查找文件
- 💾 **安全存储**：所有文件和标签数据持久化存储
- 📊 **报告生成**：生成证书清单和统计报告

## 📁 文件结构

```
file-action-skill/
├── SKILL.md                          # 技能定义文件
├── README.md                         # 详细使用说明
├── INSTALLATION.md                   # 安装指南
├── SKILL_STRUCTURE.md                # 结构说明
├── PROJECT_SUMMARY.md                # 本文件（项目总结）
├── config.example.json               # 配置文件示例
├── install.sh                        # 安装脚本
├── uninstall.sh                      # 卸载脚本
├── .gitignore                        # Git 忽略文件
│
├── scripts/                          # 核心脚本
│   ├── certificate_manager.py        # 证书管理器
│   ├── identify_certificate.py       # 证书识别器
│   └── process_file.py               # 文件处理器
│
├── examples/                         # 示例文件
│   ├── sample_files.json             # 示例文件数据
│   ├── sample_tags.json              # 示例标签数据
│   ├── sample_dates.json             # 示例日期数据
│   └── usage_examples.md             # 使用示例
│
└── tests/                            # 测试脚本
    └── test_certificate_manager.py   # 测试用例
```

## 🔧 核心脚本

### 1. certificate_manager.py
**证书管理器核心类**

功能：
- 文件存储和管理
- 元数据管理（files.json, tags.json, dates.json）
- 标签索引
- 搜索和检索
- 报告生成
- 数据备份

### 2. identify_certificate.py
**证书识别器**

功能：
- 证书类型识别（获奖证书、荣誉证书、资格证书等）
- 信息提取（姓名、机构、日期等）
- 标签生成
- 置信度计算

### 3. process_file.py
**文件处理器**

功能：
- 处理上传文件
- 生成确认提示
- 保存证书
- 搜索证书
- 生成报告

## 📊 数据格式

### 文件元数据 (files.json)

```json
{
  "file_id": {
    "filename": "证书文件名.jpg",
    "path": "files/2024/05/证书文件名.jpg",
    "type": "获奖证书",
    "uploadDate": "2024-10-10T10:30:00Z",
    "awardDate": "2024-05-15",
    "awardee": "张三",
    "issuer": "XX大学",
    "awardName": "优秀学生奖学金",
    "certNumber": "XXU20240515001",
    "description": "证书描述",
    "tags": ["获奖证书", "张三", "XX大学", "2024-05-15", "优秀学生奖学金"]
  }
}
```

### 标签索引 (tags.json)

```json
{
  "标签名": ["file_id_1", "file_id_2", ...]
}
```

### 日期索引 (dates.json)

```json
{
  "2024": ["file_id_1", "file_id_2", ...],
  "2023": ["file_id_3", ...]
}
```

## 🏷️ 标签系统

### 标签类型

1. **证书类型**：获奖证书、荣誉证书、资格证书、申报材料、毕业证书、结业证书
2. **颁发机构**：大学、学院、公司、机构、委员会等
3. **年份**：2024、2023 等
4. **人物**：获奖人姓名
5. **奖项**：奖项名称
6. **其他**：自定义标签

### 标签操作

- **自动标签**：系统自动生成的标签
- **手动标签**：用户手动添加的标签
- **智能标签**：系统学习用户习惯生成的标签

## 🔍 搜索功能

### 搜索类型

1. **按标签搜索**：精确匹配标签
2. **按年份搜索**：按获奖年份搜索
3. **按类型搜索**：按证书类型搜索
4. **按关键词搜索**：模糊匹配文件名、描述、标签
5. **按机构搜索**：按颁发机构搜索

### 搜索示例

```bash
# 按标签搜索
search("获奖证书", type="tag")

# 按年份搜索
search("2024", type="year")

# 按关键词搜索
search("奖学金", type="keyword")

# 按类型搜索
search("荣誉证书", type="type")
```

## 📈 报告功能

### 报告类型

1. **证书清单**：列出所有证书
2. **统计报告**：按类型、年份、机构统计
3. **导出报告**：导出为 Excel、PDF 格式

### 报告内容

- 证书总数
- 按类型分布
- 按年份分布
- 按机构分布
- 详细证书列表

## 🚀 快速开始

### 1. 安装

```bash
cd file-action-skill
./install.sh
```

### 2. 配置

```bash
export STORAGE_DIR=/path/to/storage
```

### 3. 使用

```bash
# 处理证书
python scripts/process_file.py --storage-dir $STORAGE_DIR upload certificate.jpg --text "证书内容..."

# 搜索证书
python scripts/process_file.py --storage-dir $STORAGE_DIR search "获奖证书" --type tag

# 生成报告
python scripts/process_file.py --storage-dir $STORAGE_DIR report --year 2024
```

## 📖 使用示例

### 上传证书
```
用户：[发送证书图片]
系统：识别结果：获奖证书、张三、XX大学、2024-05-15
用户：正确
系统：已保存！
```

### 查询证书
```
用户：找一下我的获奖证书
系统：找到 2 个获奖证书...
```

### 生成报告
```
用户：导出2024年所有证书的清单
系统：报告已生成...
```

## 🔒 安全性

### 数据安全

1. **本地存储**：所有数据存储在本地
2. **文件权限**：设置合适的文件权限
3. **备份加密**：支持加密备份
4. **隐私保护**：不上传到云端

### 访问控制

1. **文件权限**：设置文件读写权限
2. **目录权限**：设置目录访问权限
3. **备份保护**：加密备份文件

## 🛠️ 扩展性

### 自定义证书类型

```json
{
  "certificate_types": {
    "自定义类型": ["关键词1", "关键词2", ...]
  }
}
```

### 自定义识别规则

```json
{
  "date_patterns": ["自定义日期模式"],
  "name_patterns": ["自定义姓名模式"],
  "issuer_patterns": ["自定义机构模式"]
}
```

### 插件系统

支持插件扩展功能：
- OCR 插件
- 报告生成插件
- 云存储插件
- 备份插件

## 📝 更新日志

### v1.0.0 (2024-10-10)
- ✨ 初始版本
- 📄 支持基本的证书识别和管理
- 🏷️ 支持标签管理
- 🔍 支持多种搜索方式
- 📊 支持报告生成

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**Made with ❤️ for students and professionals**