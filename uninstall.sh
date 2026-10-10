#!/bin/bash

# File Action Skill 卸载脚本

set -e

echo "=========================================="
echo "  File Action Skill 卸载程序"
echo "=========================================="

# 确认卸载
read -p "确定要卸载 File Action Skill 吗？(y/n): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "卸载已取消"
    exit 0
fi

# 检查是否备份数据
read -p "是否备份证书数据？(y/n): " backup_data
if [[ "$backup_data" == "y" || "$backup_data" == "Y" ]]; then
    echo "备份证书数据..."

    # 读取存储目录
    if [[ -f .env ]]; then
        source .env
    fi

    if [[ -n "$STORAGE_DIR" && -d "$STORAGE_DIR" ]]; then
        backup_file="backup_$(date +%Y%m%d_%H%M%S).zip"
        zip -r "$backup_file" "$STORAGE_DIR"
        echo "✓ 数据已备份到: $backup_file"
    else
        echo "⚠ 未找到存储目录，跳过备份"
    fi
fi

# 删除虚拟环境
if [[ -d "venv" ]]; then
    echo "删除虚拟环境..."
    rm -rf venv
    echo "✓ 虚拟环境已删除"
fi

# 删除配置文件
if [[ -f "config/config.json" ]]; then
    read -p "是否删除配置文件？(y/n): " delete_config
    if [[ "$delete_config" == "y" || "$delete_config" == "Y" ]]; then
        rm -f config/config.json
        echo "✓ 配置文件已删除"
    fi
fi

# 删除环境变量文件
if [[ -f ".env" ]]; then
    read -p "是否删除环境变量文件？(y/n): " delete_env
    if [[ "$delete_env" == "y" || "$delete_env" == "Y" ]]; then
        rm -f .env
        echo "✓ 环境变量文件已删除"
    fi
fi

# 删除缓存文件
echo "清理缓存文件..."
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete
echo "✓ 缓存文件已清理"

echo ""
echo "=========================================="
echo "  卸载完成！"
echo "=========================================="
echo ""
echo "注意："
echo "1. 证书数据文件未删除，如需删除请手动操作"
echo "2. 如有备份，请妥善保管备份文件"
echo "=========================================="