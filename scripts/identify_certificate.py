#!/usr/bin/env python3
"""
证书识别辅助脚本
用于识别证书文件内容并提取关键信息
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, Optional

class CertificateIdentifier:
    """证书识别器"""

    def __init__(self):
        self.certificate_types = {
            '获奖证书': ['获奖', '奖励', '奖项', '奖学金', '一等奖', '二等奖', '三等奖', '优秀', '竞赛'],
            '荣誉证书': ['荣誉', '称号', '表彰', '先进', '模范'],
            '资格证书': ['资格', '认证', '证书', '执照', '许可证'],
            '申报材料': ['申报', '申请', '材料', '项目', '计划'],
            '毕业证书': ['毕业', '学位', '学士', '硕士', '博士'],
            '结业证书': ['结业', '培训', '进修'],
        }

        self.date_patterns = [
            r'(\d{4})年(\d{1,2})月(\d{1,2})日',
            r'(\d{4})年(\d{1,2})月',
            r'(\d{4})\.(\d{1,2})\.(\d{1,2})',
            r'(\d{4})-(\d{1,2})-(\d{1,2})',
            r'(\d{4})/(\d{1,2})/(\d{1,2})',
        ]

    def identify(self, text_content: str) -> Dict[str, Any]:
        """
        识别证书内容

        Args:
            text_content: 证书文本内容

        Returns:
            识别结果
        """
        # 识别证书类型
        cert_type = self._identify_type(text_content)

        # 提取关键信息
        info = self._extract_info(text_content, cert_type)

        # 生成识别结果
        result = {
            'type': cert_type,
            'confidence': self._calculate_confidence(text_content, cert_type),
            'info': info,
            'suggested_tags': self._generate_tags(info),
            'raw_text': text_content[:500] if len(text_content) > 500 else text_content
        }

        return result

    def _identify_type(self, text: str) -> str:
        """识别证书类型"""
        text_lower = text.lower()

        # 计算每种类型的匹配分数
        scores = {}
        for cert_type, keywords in self.certificate_types.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[cert_type] = score

        # 返回得分最高的类型
        if scores:
            return max(scores, key=scores.get)

        return "未知"

    def _extract_info(self, text: str, cert_type: str) -> Dict[str, Any]:
        """提取证书信息"""
        info = {
            'type': cert_type,
            'awardee': self._extract_name(text),
            'issuer': self._extract_issuer(text),
            'awardName': self._extract_award_name(text),
            'awardDate': self._extract_date(text),
            'description': self._extract_description(text),
            'certNumber': self._extract_cert_number(text)
        }

        return info

    def _extract_name(self, text: str) -> Optional[str]:
        """提取姓名"""
        # 匹配常见姓名模式
        patterns = [
            r'([一-龥]{2,4})\s*(?:同学|同志|先生|女士)',
            r'姓名[：:]\s*([一-龥]{2,4})',
            r'([一-龥]{2,4})\s*在',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        # 如果没有明确模式，尝试提取第一个2-4字的中文词
        name_match = re.search(r'([一-龥]{2,4})', text)
        if name_match:
            return name_match.group(1)

        return None

    def _extract_issuer(self, text: str) -> Optional[str]:
        """提取颁发机构"""
        patterns = [
            r'颁发[：:]\s*([一-龥]+)',
            r'([一-龥]+大学)',
            r'([一-龥]+学院)',
            r'([一-龥]+学校)',
            r'([一-龥]+公司)',
            r'([一-龥]+机构)',
            r'([一-龥]+委员会)',
            r'([一-龥]+部门)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return None

    def _extract_award_name(self, text: str) -> Optional[str]:
        """提取奖项名称"""
        patterns = [
            r'([一-龥]+奖)',
            r'([一-龥]+奖学金)',
            r'([一-龥]+竞赛)',
            r'([一-龥]+荣誉)',
            r'([一-龥]+称号)',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return None

    def _extract_date(self, text: str) -> Optional[str]:
        """提取日期"""
        for pattern in self.date_patterns:
            match = re.search(pattern, text)
            if match:
                groups = match.groups()
                if len(groups) == 3:
                    return f"{groups[0]}-{int(groups[1]):02d}-{int(groups[2]):02d}"
                elif len(groups) == 2:
                    return f"{groups[0]}-{int(groups[1]):02d}"

        return None

    def _extract_description(self, text: str) -> str:
        """提取描述"""
        # 取前200个字符作为描述
        if len(text) > 200:
            return text[:200] + '...'
        return text

    def _extract_cert_number(self, text: str) -> Optional[str]:
        """提取证书编号"""
        patterns = [
            r'编号[：:]\s*([A-Z0-9\-]+)',
            r'证书号[：:]\s*([A-Z0-9\-]+)',
            r'No[.：:]\s*([A-Z0-9\-]+)',
            r'([A-Z]{2,3}\d{8,12})',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return None

    def _calculate_confidence(self, text: str, cert_type: str) -> float:
        """计算识别置信度"""
        if cert_type == "未知":
            return 0.0

        keywords = self.certificate_types.get(cert_type, [])
        if not keywords:
            return 0.0

        text_lower = text.lower()
        matched = sum(1 for keyword in keywords if keyword in text_lower)

        return min(matched / len(keywords), 1.0)

    def _generate_tags(self, info: Dict[str, Any]) -> list:
        """生成标签列表"""
        tags = []

        if info['type'] and info['type'] != "未知":
            tags.append(info['type'])

        if info['awardee']:
            tags.append(info['awardee'])

        if info['issuer']:
            tags.append(info['issuer'])

        if info['awardName']:
            tags.append(info['awardName'])

        if info['awardDate']:
            tags.append(info['awardDate'])

        return tags


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("用法: python identify_certificate.py <text_file>")
        sys.exit(1)

    text_file = sys.argv[1]

    # 读取文本文件
    with open(text_file, 'r', encoding='utf-8') as f:
        text_content = f.read()

    # 识别证书
    identifier = CertificateIdentifier()
    result = identifier.identify(text_content)

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()