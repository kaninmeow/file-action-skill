# File Action Skill - 结构说明

## 📁 目录结构

```
file-action-skill/
├── SKILL.md                          # 技能主文件（OpenClaw 技能定义）
├── README.md                         # 详细使用说明
├── SKILL_STRUCTURE.md                # 本文件（结构说明）
├── config.example.json               # 配置文件示例
├── install.sh                        # 安装脚本
├── uninstall.sh                      # 卸载脚本
├── .gitignore                        # Git 忽略文件
│
├── scripts/                          # 脚本目录
│   ├── certificate_manager.py        # 核心管理器
│   ├── identify_certificate.py       # 证书识别器
│   └── process_file.py               # 文件处理器
│
└── examples/                         # 示例目录
    ├── sample_files.json             # 示例文件数据
    ├── sample_tags.json              # 示例标签数据
    ├── sample_dates.json             # 示例日期数据
    └── usage_examples.md             # 使用示例
```

## 📄 文件说明

### 核心文件

#### SKILL.md
- **用途**：OpenClaw 技能定义文件
- **内容**：技能元数据、功能说明、使用方法
- **格式**：Markdown + YAML frontmatter

#### README.md
- **用途**：详细使用文档
- **内容**：安装说明、使用指南、API 文档
- **受众**：最终用户

### 脚本文件

#### scripts/certificate_manager.py
- **用途**：核心管理器类
- **功能**：
  - 文件存储和管理
  - 元数据管理
  - 标签索引
  - 搜索和检索
  - 报告生成
  - 数据备份

#### scripts/identify_certificate.py
- **用途**：证书识别器
- **功能**：
  - 证书类型识别
  - 信息提取（姓名、机构、日期等）
  - 标签生成
  - 置信度计算

#### scripts/process_file.py
- **用途**：文件处理器
- **功能**：
  - 处理上传文件
  - 生成确认提示
  - 保存证书
  - 搜索证书
  - 生成报告

### 配置文件

#### config.example.json
- **用途**：配置文件示例
- **内容**：
  - 存储目录配置
  - 支持的文件格式
  - 证书类型定义
  - 识别规则
  - 日期模式

### 安装脚本

#### install.sh
- **用途**：安装脚本
- **功能**：
  - 检查 Python 版本
  - 创建虚拟环境
  - 安装依赖
  - 创建目录结构
  - 设置环境变量

#### uninstall.sh
- **用途**：卸载脚本
- **功能**：
  - 备份数据
  - 删除虚拟环境
  - 清理配置文件
  - 清理缓存

### 示例文件

#### examples/sample_files.json
- **用途**：示例文件数据
- **内容**：5 个证书文件的完整元数据

#### examples/sample_tags.json
- **用途**：示例标签数据
- **内容**：标签到文件的映射关系

#### examples/sample_dates.json
- **用途**：示例日期数据
- **内容**：年份到文件的映射关系

#### examples/usage_examples.md
- **用途**：使用示例
- **内容**：15 个完整的交互示例

## 🔧 技术架构

### 核心类

```python
CertificateManager          # 证书管理器
├── 文件存储管理
├── 元数据管理
├── 标签索引
├── 搜索和检索
└── 报告生成

CertificateIdentifier       # 证书识别器
├── 类型识别
├── 信息提取
├── 标签生成
└── 置信度计算

CertificateProcessor        # 证书处理器
├── 文件上传处理
├── 确认流程
├── 搜索接口
└── 报告生成
```

### 数据流

```
用户上传文件
    ↓
识别证书内容 (CertificateIdentifier)
    ↓
生成确认提示
    ↓
用户确认/纠正
    ↓
保存证书 (CertificateManager)
    ↓
更新索引和标签
    ↓
返回保存结果
```

### 存储结构

```
$STORAGE_DIR/
├── files/                    # 原始文件
│   └── YYYY/MM/             # 按年月组织
├── metadata/                 # 元数据
│   ├── files.json           # 文件索引
│   ├── tags.json            # 标签索引
│   └── dates.json           # 日期索引
└── config.json              # 配置文件
```

## 🚀 快速开始

### 1. 安装

```bash
# 克隆技能
git clone <repository-url>
cd certificate-manager

# 运行安装脚本
./install.sh
```

### 2. 配置

```bash
# 编辑配置文件
cp config.example.json config/config.json
vim config/config.json

# 设置环境变量
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