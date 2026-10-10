#!/usr/bin/env python3
"""
证书文件管理器 - OpenClaw 技能实现
用于管理和整理个人证书、获奖证书、荣誉证书和申报材料
"""

import os
import json
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import re

class CertificateManager:
    """证书文件管理器核心类"""

    def __init__(self, storage_dir: str):
        """
        初始化证书管理器

        Args:
            storage_dir: 存储目录路径
        """
        self.storage_dir = Path(storage_dir)
        self.files_dir = self.storage_dir / "files"
        self.metadata_dir = self.storage_dir / "metadata"

        # 元数据文件路径
        self.files_json = self.metadata_dir / "files.json"
        self.tags_json = self.metadata_dir / "tags.json"
        self.dates_json = self.metadata_dir / "dates.json"

        # 初始化目录和文件
        self._initialize()

    def _initialize(self):
        """初始化目录结构和元数据文件"""
        # 创建目录
        self.files_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)

        # 初始化元数据文件
        for json_file in [self.files_json, self.tags_json, self.dates_json]:
            if not json_file.exists():
                json_file.write_text('{}', encoding='utf-8')

    def _load_json(self, file_path: Path) -> Dict:
        """加载 JSON 文件"""
        try:
            return json.loads(file_path.read_text(encoding='utf-8'))
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_json(self, file_path: Path, data: Dict):
        """保存 JSON 文件"""
        file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')

    def _generate_file_id(self, filename: str) -> str:
        """生成文件唯一 ID"""
        timestamp = datetime.now().isoformat()
        content = f"{filename}_{timestamp}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def _extract_date_from_text(self, text: str) -> Optional[str]:
        """从文本中提取日期"""
        # 匹配各种日期格式
        date_patterns = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})年(\d{1,2})月',
            r'(\d{4})\.(\d{1,2})\.(\d{1,2})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{4})/(\d{1,2})/(\d{1,2})',
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    return f"{groups[0]}-{int(groups[1]):02d}-{int(groups[2]):02d}"
                elif len(groups) == 2:
                    return f"{groups[0]}-{int(groups[1]):02d}"

        return None

    def _identify_certificate_type(self, text: str) -> str:
        """识别证书类型"""
        text_lower = text.lower()

        # 获奖证书关键词
        award_keywords = ['获奖', '奖励', '奖项', '奖学金', '一等奖', '二等奖', '三等奖', '优秀', '竞赛']
        if any(keyword in text_lower for keyword in award_keywords):
            return "获奖证书"

        # 荣誉证书关键词
        honor_keywords = ['荣誉', '称号', '表彰', '先进', '模范']
        if any(keyword in text_lower for keyword in honor_keywords):
            return "荣誉证书"

        # 资格证书关键词
        qualification_keywords = ['资格', '认证', '证书', '执照', '许可证']
        if any(keyword in text_lower for keyword in qualification_keywords):
            return "资格证书"

        # 申报材料关键词
        application_keywords = ['申报', '申请', '材料', '项目', '计划']
        if any(keyword in text_lower for keyword in application_keywords):
            return "申报材料"

        return "其他"

    def _extract_certificate_info(self, text: str, cert_type: str) -> Dict[str, Any]:
        """提取证书信息"""
        info = {
            'type': cert_type,
            'awardee': None,
            'issuer': None,
            'awardName': None,
            'awardDate': None,
            'description': text[:200] if len(text) > 200 else text
        }

        # 提取获奖人（假设是第一个出现的姓名）
        name_pattern = r'([一-龥]{2,4})'
        name_match = re.search(name_pattern, text)
        if name_match:
            info['awardee'] = name_match.group(1)

        # 提取颁发机构
        issuer_patterns = [
            r'颁发[：:]\s*([一-龥]+)',
            r'([一-龥]+大学)',
            r'([一-龥]+学院)',
            r'([一-龥]+公司)',
            r'([一-龥]+机构)',
        ]
        for pattern in issuer_patterns:
            issuer_match = re.search(pattern, text)
            if issuer_match:
                info['issuer'] = issuer_match.group(1)
                break

        # 提取奖项名称
        award_patterns = [
            r'([一-龥]+奖)',
            r'([一-龥]+奖学金)',
            r'([一-龥]+竞赛)',
        ]
        for pattern in award_patterns:
            award_match = re.search(pattern, text)
            if award_match:
                info['awardName'] = award_match.group(1)
                break

        # 提取日期
        if cert_type == "获奖证书":
            info['awardDate'] = self._extract_date_from_text(text)

        return info

    def _generate_tags(self, info: Dict[str, Any]) -> List[str]:
        """生成标签列表"""
        tags = []

        # 添加证书类型标签
        if info['type']:
            tags.append(info['type'])

        # 添加获奖人标签
        if info['awardee']:
            tags.append(info['awardee'])

        # 添加颁发机构标签
        if info['issuer']:
            tags.append(info['issuer'])

        # 添加奖项名称标签
        if info['awardName']:
            tags.append(info['awardName'])

        # 添加日期标签
        if info['awardDate']:
            tags.append(info['awardDate'])

        return tags

    def _store_file(self, file_path: str, filename: str) -> str:
        """存储文件到指定目录"""
        # 按年月组织目录
        now = datetime.now()
        year_dir = self.files_dir / str(now.year)
        month_dir = year_dir / f"{now.month:02d}"
        month_dir.mkdir(parents=True, exist_ok=True)

        # 生成目标路径
        target_path = month_dir / filename

        # 复制文件
        shutil.copy2(file_path, target_path)

        # 返回相对路径
        return str(target_path.relative_to(self.storage_dir))

    def _update_metadata(self, file_id: str, filename: str, file_path: str,
                         info: Dict[str, Any], tags: List[str]):
        """更新元数据"""
        # 更新文件索引
        files_data = self._load_json(self.files_json)
        files_data[file_id] = {
            'filename': filename,
            'path': file_path,
            'type': info['type'],
            'uploadDate': datetime.now().isoformat(),
            'awardDate': info.get('awardDate'),
            'awardee': info.get('awardee'),
            'issuer': info.get('issuer'),
            'awardName': info.get('awardName'),
            'description': info.get('description'),
            'tags': tags
        }
        self._save_json(self.files_json, files_data)

        # 更新标签索引
        tags_data = self._load_json(self.tags_json)
        for tag in tags:
            if tag not in tags_data:
                tags_data[tag] = []
            if file_id not in tags_data[tag]:
                tags_data[tag].append(file_id)
        self._save_json(self.tags_json, tags_data)

        # 更新日期索引
        if info.get('awardDate'):
            dates_data = self._load_json(self.dates_json)
            year = info['awardDate'][:4]
            if year not in dates_data:
                dates_data[year] = []
            if file_id not in dates_data[year]:
                dates_data[year].append(file_id)
            self._save_json(self.dates_json, dates_data)

    def process_certificate(self, file_path: str, text_content: str) -> Dict[str, Any]:
        """
        处理证书文件

        Args:
            file_path: 文件路径
            text_content: 文件文本内容（OCR 识别结果）

        Returns:
            识别结果信息
        """
        filename = Path(file_path).name

        # 识别证书类型
        cert_type = self._identify_certificate_type(text_content)

        # 提取证书信息
        info = self._extract_certificate_info(text_content, cert_type)

        # 生成标签
        tags = self._generate_tags(info)

        # 存储文件
        stored_path = self._store_file(file_path, filename)

        # 生成文件 ID
        file_id = self._generate_file_id(filename)

        # 更新元数据
        self._update_metadata(file_id, filename, stored_path, info, tags)

        return {
            'file_id': file_id,
            'filename': filename,
            'stored_path': stored_path,
            'type': cert_type,
            'info': info,
            'tags': tags
        }

    def update_certificate_info(self, file_id: str, corrected_info: Dict[str, Any]):
        """
        更新证书信息（当用户纠正识别结果时）

        Args:
            file_id: 文件 ID
            corrected_info: 纠正后的信息
        """
        files_data = self._load_json(self.files_json)

        if file_id not in files_data:
            raise ValueError(f"文件 ID {file_id} 不存在")

        file_info = files_data[file_id]

        # 更新信息
        for key, value in corrected_info.items():
            if value is not None:
                file_info[key] = value

        # 重新生成标签
        tags = self._generate_tags(file_info)
        file_info['tags'] = tags

        # 保存更新
        files_data[file_id] = file_info
        self._save_json(self.files_json, files_data)

        # 更新标签索引
        self._rebuild_tag_index()

        # 更新日期索引
        if file_info.get('awardDate'):
            self._rebuild_date_index()

    def _rebuild_tag_index(self):
        """重建标签索引"""
        files_data = self._load_json(self.files_json)
        tags_data = {}

        for file_id, file_info in files_data.items():
            for tag in file_info.get('tags', []):
                if tag not in tags_data:
                    tags_data[tag] = []
                if file_id not in tags_data[tag]:
                    tags_data[tag].append(file_id)

        self._save_json(self.tags_json, tags_data)

    def _rebuild_date_index(self):
        """重建日期索引"""
        files_data = self._load_json(self.files_json)
        dates_data = {}

        for file_id, file_info in files_data.items():
            award_date = file_info.get('awardDate')
            if award_date:
                year = award_date[:4]
                if year not in dates_data:
                    dates_data[year] = []
                if file_id not in dates_data[year]:
                    dates_data[year].append(file_id)

        self._save_json(self.dates_json, dates_data)

    def search_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        按标签搜索文件

        Args:
            tag: 标签名称

        Returns:
            匹配的文件列表
        """
        tags_data = self._load_json(self.tags_json)
        files_data = self._load_json(self.files_json)

        if tag not in tags_data:
            return []

        results = []
        for file_id in tags_data[tag]:
            if file_id in files_data:
                file_info = files_data[file_id]
                file_info['file_id'] = file_id
                results.append(file_info)

        return results

    def search_by_year(self, year: str) -> List[Dict[str, Any]]:
        """
        按年份搜索文件

        Args:
            year: 年份

        Returns:
            匹配的文件列表
        """
        dates_data = self._load_json(self.dates_json)
        files_data = self._load_json(self.files_json)

        if year not in dates_data:
            return []

        results = []
        for file_id in dates_data[year]:
            if file_id in files_data:
                file_info = files_data[file_id]
                file_info['file_id'] = file_id
                results.append(file_info)

        return results

    def search_by_type(self, cert_type: str) -> List[Dict[str, Any]]:
        """
        按证书类型搜索

        Args:
            cert_type: 证书类型

        Returns:
            匹配的文件列表
        """
        files_data = self._load_json(self.files_json)

        results = []
        for file_id, file_info in files_data.items():
            if file_info.get('type') == cert_type:
                file_info['file_id'] = file_id
                results.append(file_info)

        return results

    def search_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """
        按关键词搜索

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的文件列表
        """
        files_data = self._load_json(self.files_json)

        results = []
        for file_id, file_info in files_data.items():
            # 在文件名、描述、标签中搜索
            searchable_text = ' '.join([
                file_info.get('filename', ''),
                file_info.get('description', ''),
                ' '.join(file_info.get('tags', []))
            ])

            if keyword.lower() in searchable_text.lower():
                file_info['file_id'] = file_id
                results.append(file_info)

        return results

    def get_all_tags(self) -> Dict[str, int]:
        """
        获取所有标签及其文件数量

        Returns:
            标签到文件数量的映射
        """
        tags_data = self._load_json(self.tags_json)
        return {tag: len(files) for tag, files in tags_data.items()}

    def get_all_years(self) -> List[str]:
        """
        获取所有有证书的年份

        Returns:
            年份列表
        """
        dates_data = self._load_json(self.dates_json)
        return sorted(dates_data.keys(), reverse=True)

    def get_file_path(self, file_id: str) -> Optional[str]:
        """
        获取文件的完整路径

        Args:
            file_id: 文件 ID

        Returns:
            文件完整路径，如果不存在返回 None
        """
        files_data = self._load_json(self.files_json)

        if file_id not in files_data:
            return None

        file_info = files_data[file_id]
        return str(self.storage_dir / file_info['path'])

    def delete_file(self, file_id: str) -> bool:
        """
        删除文件

        Args:
            file_id: 文件 ID

        Returns:
            是否删除成功
        """
        files_data = self._load_json(self.files_json)

        if file_id not in files_data:
            return False

        file_info = files_data[file_id]
        file_path = self.storage_dir / file_info['path']

        # 删除物理文件
        if file_path.exists():
            file_path.unlink()

        # 删除元数据
        del files_data[file_id]
        self._save_json(self.files_json, files_data)

        # 重建索引
        self._rebuild_tag_index()
        self._rebuild_date_index()

        return True

    def export_report(self, year: Optional[str] = None,
                      cert_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        导出证书报告

        Args:
            year: 年份筛选（可选）
            cert_type: 证书类型筛选（可选）

        Returns:
            报告数据
        """
        files_data = self._load_json(self.files_json)

        results = []
        for file_id, file_info in files_data.items():
            # 应用筛选条件
            if year and file_info.get('awardDate', '').startswith(year):
                continue
            if cert_type and file_info.get('type') != cert_type:
                continue

            file_info['file_id'] = file_id
            results.append(file_info)

        # 按日期排序
        results.sort(key=lambda x: x.get('awardDate', ''), reverse=True)

        return results

    def backup_data(self, backup_path: str) -> str:
        """
        备份所有数据

        Args:
            backup_path: 备份文件路径

        Returns:
            备份文件路径
        """
        backup_file = Path(backup_path)
        backup_file.parent.mkdir(parents=True, exist_ok=True)

        # 创建备份
        shutil.make_archive(
            str(backup_file.with_suffix('')),
            'zip',
            self.storage_dir
        )

        return str(backup_file.with_suffix('.zip'))


def main():
    """主函数 - 命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description='证书文件管理器')
    parser.add_argument('--storage-dir', required=True, help='存储目录路径')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 处理证书命令
    process_parser = subparsers.add_parser('process', help='处理证书文件')
    process_parser.add_argument('file', help='证书文件路径')
    process_parser.add_argument('--text', required=True, help='证书文本内容')

    # 搜索命令
    search_parser = subparsers.add_parser('search', help='搜索证书')
    search_parser.add_argument('--tag', help='按标签搜索')
    search_parser.add_argument('--year', help='按年份搜索')
    search_parser.add_argument('--type', dest='cert_type', help='按类型搜索')
    search_parser.add_argument('--keyword', help='按关键词搜索')

    # 列出标签命令
    subparsers.add_parser('list-tags', help='列出所有标签')

    # 列出年份命令
    subparsers.add_parser('list-years', help='列出所有年份')

    # 导出报告命令
    export_parser = subparsers.add_parser('export', help='导出报告')
    export_parser.add_argument('--year', help='年份筛选')
    export_parser.add_argument('--type', dest='cert_type', help='类型筛选')

    # 备份命令
    backup_parser = subparsers.add_parser('backup', help='备份数据')
    backup_parser.add_argument('path', help='备份文件路径')

    args = parser.parse_args()

    # 初始化管理器
    manager = CertificateManager(args.storage_dir)

    if args.command == 'process':
        result = manager.process_certificate(args.file, args.text)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'search':
        if args.tag:
            results = manager.search_by_tag(args.tag)
        elif args.year:
            results = manager.search_by_year(args.year)
        elif args.cert_type:
            results = manager.search_by_type(args.cert_type)
        elif args.keyword:
            results = manager.search_by_keyword(args.keyword)
        else:
            print("请指定搜索条件")
            return

        print(json.dumps(results, ensure_ascii=False, indent=2))

    elif args.command == 'list-tags':
        tags = manager.get_all_tags()
        print(json.dumps(tags, ensure_ascii=False, indent=2))

    elif args.command == 'list-years':
        years = manager.get_all_years()
        print(json.dumps(years, ensure_ascii=False, indent=2))

    elif args.command == 'export':
        report = manager.export_report(args.year, args.cert_type)
        print(json.dumps(report, ensure_ascii=False, indent=2))

    elif args.command == 'backup':
        backup_file = manager.backup_data(args.path)
        print(f"备份已保存到: {backup_file}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()