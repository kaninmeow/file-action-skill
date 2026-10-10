#!/usr/bin/env python3
"""
证书文件处理流程脚本
用于处理用户上传的证书文件，包括识别、确认、存储等步骤
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from certificate_manager import CertificateManager
from identify_certificate import CertificateIdentifier


class CertificateProcessor:
    """证书处理器"""

    def __init__(self, storage_dir: str):
        """
        初始化处理器

        Args:
            storage_dir: 存储目录路径
        """
        self.manager = CertificateManager(storage_dir)
        self.identifier = CertificateIdentifier()

    def process_upload(self, file_path: str, text_content: str) -> Dict[str, Any]:
        """
        处理上传的文件

        Args:
            file_path: 文件路径
            text_content: 文件文本内容

        Returns:
            处理结果，包含识别信息和确认提示
        """
        # 识别证书
        identification = self.identifier.identify(text_content)

        # 生成确认提示
        confirmation_prompt = self._generate_confirmation_prompt(identification)

        return {
            'status': 'pending_confirmation',
            'file_path': file_path,
            'identification': identification,
            'confirmation_prompt': confirmation_prompt
        }

    def _generate_confirmation_prompt(self, identification: Dict[str, Any]) -> str:
        """生成确认提示"""
        info = identification['info']

        prompt = f"""我识别到这是一个{identification['type']}，请确认以下信息是否正确：

📋 **识别结果：**
- 证书类型：{info['type']}
- 获奖人：{info['awardee'] or '未识别'}
- 颁发机构：{info['issuer'] or '未识别'}
- 奖项名称：{info['awardName'] or '未识别'}
- 获奖日期：{info['awardDate'] or '未识别'}
- 证书编号：{info['certNumber'] or '未识别'}

**置信度：** {identification['confidence']*100:.1f}%

**建议标签：** {', '.join(identification['suggested_tags'])}

请回复"正确"确认保存，或告诉我需要修改的内容。"""

        return prompt

    def confirm_and_save(self, file_path: str, identification: Dict[str, Any],
                         user_corrections: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        确认并保存证书

        Args:
            file_path: 文件路径
            identification: 识别结果
            user_corrections: 用户纠正的信息

        Returns:
            保存结果
        """
        # 应用用户纠正
        if user_corrections:
            for key, value in user_corrections.items():
                if value is not None:
                    identification['info'][key] = value

        # 重新生成标签
        identification['suggested_tags'] = self.identifier._generate_tags(identification['info'])

        # 处理并保存证书
        result = self.manager.process_certificate(file_path, identification['raw_text'])

        # 使用识别结果更新元数据
        self.manager.update_certificate_info(result['file_id'], identification['info'])

        return {
            'status': 'saved',
            'file_id': result['file_id'],
            'filename': result['filename'],
            'stored_path': result['stored_path'],
            'type': identification['info']['type'],
            'tags': identification['suggested_tags'],
            'info': identification['info']
        }

    def search_certificates(self, query: str, search_type: str = 'auto') -> Dict[str, Any]:
        """
        搜索证书

        Args:
            query: 搜索查询
            search_type: 搜索类型 (auto, tag, year, type, keyword)

        Returns:
            搜索结果
        """
        results = []

        if search_type == 'auto':
            # 自动识别搜索类型
            if query.isdigit() and len(query) == 4:
                # 可能是年份
                results = self.manager.search_by_year(query)
                search_type = 'year'
            elif query in self.identifier.certificate_types:
                # 可能是证书类型
                results = self.manager.search_by_type(query)
                search_type = 'type'
            else:
                # 默认使用关键词搜索
                results = self.manager.search_by_keyword(query)
                search_type = 'keyword'

        elif search_type == 'tag':
            results = self.manager.search_by_tag(query)

        elif search_type == 'year':
            results = self.manager.search_by_year(query)

        elif search_type == 'type':
            results = self.manager.search_by_type(query)

        elif search_type == 'keyword':
            results = self.manager.search_by_keyword(query)

        # 生成搜索结果摘要
        summary = self._generate_search_summary(results, query, search_type)

        return {
            'query': query,
            'search_type': search_type,
            'count': len(results),
            'results': results,
            'summary': summary
        }

    def _generate_search_summary(self, results: list, query: str, search_type: str) -> str:
        """生成搜索结果摘要"""
        if not results:
            return f"未找到与"{query}"相关的证书。"

        summary = f"找到 {len(results)} 个相关证书：\n\n"

        for i, result in enumerate(results[:10], 1):  # 最多显示10个
            filename = result.get('filename', '未知')
            cert_type = result.get('type', '未知')
            award_date = result.get('awardDate', '未知日期')

            summary += f"{i}. {filename}\n"
            summary += f"   类型：{cert_type}\n"
            summary += f"   日期：{award_date}\n"

            if result.get('awardName'):
                summary += f"   奖项：{result['awardName']}\n"

            summary += "\n"

        if len(results) > 10:
            summary += f"... 还有 {len(results) - 10} 个结果\n"

        return summary

    def get_file_for_download(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        获取文件下载信息

        Args:
            file_id: 文件 ID

        Returns:
            文件下载信息
        """
        file_path = self.manager.get_file_path(file_id)

        if not file_path or not Path(file_path).exists():
            return None

        files_data = self.manager._load_json(self.manager.files_json)
        file_info = files_data.get(file_id, {})

        return {
            'file_id': file_id,
            'filename': file_info.get('filename'),
            'path': file_path,
            'type': file_info.get('type'),
            'size': os.path.getsize(file_path)
        }

    def list_all_tags(self) -> Dict[str, Any]:
        """列出所有标签"""
        tags = self.manager.get_all_tags()

        # 按类型分组
        tag_groups = {
            '证书类型': {},
            '颁发机构': {},
            '年份': {},
            '其他': {}
        }

        for tag, count in tags.items():
            if tag in self.identifier.certificate_types:
                tag_groups['证书类型'][tag] = count
            elif any(keyword in tag for keyword in ['大学', '学院', '公司', '机构', '委员会']):
                tag_groups['颁发机构'][tag] = count
            elif tag.isdigit() and len(tag) == 4:
                tag_groups['年份'][tag] = count
            else:
                tag_groups['其他'][tag] = count

        return {
            'total_tags': len(tags),
            'groups': tag_groups,
            'all_tags': tags
        }

    def generate_report(self, year: Optional[str] = None,
                       cert_type: Optional[str] = None) -> Dict[str, Any]:
        """
        生成证书报告

        Args:
            year: 年份筛选
            cert_type: 类型筛选

        Returns:
            报告数据
        """
        report_data = self.manager.export_report(year, cert_type)

        # 统计信息
        stats = {
            'total': len(report_data),
            'by_type': {},
            'by_year': {},
            'by_issuer': {}
        }

        for item in report_data:
            # 按类型统计
            cert_type = item.get('type', '未知')
            stats['by_type'][cert_type] = stats['by_type'].get(cert_type, 0) + 1

            # 按年份统计
            award_date = item.get('awardDate', '')
            if award_date:
                year = award_date[:4]
                stats['by_year'][year] = stats['by_year'].get(year, 0) + 1

            # 按颁发机构统计
            issuer = item.get('issuer', '未知')
            stats['by_issuer'][issuer] = stats['by_issuer'].get(issuer, 0) + 1

        return {
            'report_date': '2024-10-10',
            'filters': {
                'year': year,
                'type': cert_type
            },
            'statistics': stats,
            'items': report_data
        }


def main():
    """主函数 - 命令行接口"""
    import argparse

    parser = argparse.ArgumentParser(description='证书文件处理器')
    parser.add_argument('--storage-dir', required=True, help='存储目录路径')

    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 处理上传命令
    upload_parser = subparsers.add_parser('upload', help='处理上传的证书')
    upload_parser.add_argument('file', help='证书文件路径')
    upload_parser.add_argument('--text', required=True, help='证书文本内容')

    # 确认保存命令
    confirm_parser = subparsers.add_parser('confirm', help='确认并保存证书')
    confirm_parser.add_argument('file', help='证书文件路径')
    confirm_parser.add_argument('--identification', required=True, help='识别结果 JSON')
    confirm_parser.add_argument('--corrections', help='用户纠正信息 JSON')

    # 搜索命令
    search_parser = subparsers.add_parser('search', help='搜索证书')
    search_parser.add_argument('query', help='搜索查询')
    search_parser.add_argument('--type', dest='search_type', default='auto',
                              choices=['auto', 'tag', 'year', 'type', 'keyword'],
                              help='搜索类型')

    # 获取文件命令
    get_parser = subparsers.add_parser('get', help='获取证书文件')
    get_parser.add_argument('file_id', help='文件 ID')

    # 列出标签命令
    subparsers.add_parser('tags', help='列出所有标签')

    # 生成报告命令
    report_parser = subparsers.add_parser('report', help='生成证书报告')
    report_parser.add_argument('--year', help='年份筛选')
    report_parser.add_argument('--type', dest='cert_type', help='类型筛选')

    args = parser.parse_args()

    # 初始化处理器
    processor = CertificateProcessor(args.storage_dir)

    if args.command == 'upload':
        result = processor.process_upload(args.file, args.text)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'confirm':
        identification = json.loads(args.identification)
        corrections = json.loads(args.corrections) if args.corrections else None

        result = processor.confirm_and_save(args.file, identification, corrections)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'search':
        result = processor.search_certificates(args.query, args.search_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'get':
        result = processor.get_file_for_download(args.file_id)
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("文件不存在")

    elif args.command == 'tags':
        result = processor.list_all_tags()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == 'report':
        result = processor.generate_report(args.year, args.cert_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == '__main__':
    main()