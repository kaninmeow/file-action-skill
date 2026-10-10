#!/bin/bash

# File Action Skill 安装脚本

set -e

echo "=========================================="
echo "  File Action Skill 安装程序"
echo "=========================================="

# 检查 Python 版本
echo "检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
if [[ -z "$python_version" ]]; then
    echo "错误: 未找到 Python 3"
    exit 1
fi
echo "✓ Python 版本: $python_version"

# 检查依赖
echo "检查依赖..."
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3"
    exit 1
fi

# 创建虚拟环境（可选）
read -p "是否创建虚拟环境？(y/n): " create_venv
if [[ "$create_venv" == "y" || "$create_venv" == "Y" ]]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✓ 虚拟环境已创建并激活"
fi

# 安装依赖
echo "安装 Python 依赖..."
pip install --upgrade pip

# 创建必要的目录
echo "创建目录结构..."
mkdir -p scripts
mkdir -p config

# 复制配置文件
if [[ ! -f config/config.json ]]; then
    echo "创建配置文件..."
    cp config.example.json config/config.json
    echo "✓ 配置文件已创建"
    echo "请编辑 config/config.json 文件，设置存储目录路径"
else
    echo "✓ 配置文件已存在"
fi

# 设置环境变量
echo "设置环境变量..."
read -p "请输入存储目录路径: " storage_dir
if [[ -n "$storage_dir" ]]; then
    # 创建 .env 文件
    cat > .env << EOF
STORAGE_DIR=$storage_dir
EOF
    echo "✓ 环境变量已保存到 .env 文件"

    # 创建存储目录
    mkdir -p "$storage_dir"
    echo "✓ 存储目录已创建"
fi

# 设置脚本执行权限
echo "设置脚本权限..."
chmod +x scripts/*.py
chmod +x install.sh

echo ""
echo "=========================================="
echo "  安装完成！"
echo "=========================================="
echo ""
echo "使用方法："
echo "1. 激活虚拟环境（如果创建了）:"
echo "   source venv/bin/activate"
echo ""
echo "2. 设置环境变量:"
echo "   export STORAGE_DIR=$storage_dir"
echo ""
echo "3. 开始使用:"
echo "   python scripts/process_file.py --help"
echo ""
echo "更多信息请查看 README.md 文件"
echo "=========================================="