#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目录结构自动创建脚本
根据toc.md文件创建完整的网络101书籍目录结构
"""

import os
import re
from pathlib import Path


class StructureCreator:
    def __init__(self, toc_file_path, base_dir):
        """
        初始化结构创建器

        Args:
            toc_file_path: toc.md文件路径
            base_dir: 目标基础目录
        """
        self.toc_file_path = toc_file_path
        self.base_dir = Path(base_dir)
        self.structure = []
        self.created_files = []
        self.created_dirs = []

    def parse_toc(self):
        """解析toc.md文件，构建目录结构"""
        print("正在解析toc.md文件...")

        with open(self.toc_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        current_chapter = None
        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 解析章节 (## 第X章)
            chapter_match = re.match(r'^##\s+第(\d+)章\s+(.+)', line)
            if chapter_match:
                chapter_num = chapter_match.group(1)
                chapter_title = chapter_match.group(2).strip('：').strip(':')
                current_chapter = {
                    'type': 'chapter',
                    'number': chapter_num,
                    'title': chapter_title,
                    'sections': []
                }
                self.structure.append(current_chapter)
                continue

            # 解析节 (### X.X)
            section_match = re.match(r'^###\s+(\d+\.\d+)\s+(.+)', line)
            if section_match and current_chapter:
                section_num = section_match.group(1)
                section_title = section_match.group(2).strip('？').strip('?').strip('。')
                current_section = {
                    'type': 'section',
                    'number': section_num,
                    'title': section_title,
                    'subsections': []
                }
                current_chapter['sections'].append(current_section)
                continue

            # 解析子节 (- X.X.X)
            subsection_match = re.match(r'^-\s+(\d+\.\d+\.\d+)\s+(.+)', line)
            if subsection_match and current_section:
                subsection_num = subsection_match.group(1)
                subsection_title = subsection_match.group(2).strip('？').strip('?').strip('。')
                subsection = {
                    'type': 'subsection',
                    'number': subsection_num,
                    'title': subsection_title
                }
                current_section['subsections'].append(subsection)
                continue

    def sanitize_filename(self, name):
        """清理文件名，移除不安全字符"""
        # 移除或替换特殊字符
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = name.replace('？', '')
        name = name.replace('?', '')
        name = name.replace('。', '')
        name = name.replace('：', '')
        name = name.replace(':', '')
        name = name.strip()
        return name

    def create_markdown_file(self, file_path, title):
        """创建Markdown文件并写入初始内容"""
        content = f"""# {title}

未开始编写

---

*本文档为《网络101》系列的一部分*
"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.created_files.append(str(file_path))
        print(f"创建文件: {file_path}")

    def create_introduction_file(self, dir_path, number, title):
        """创建introduction.md文件"""
        intro_filename = f"{number}.0 introduction.md"
        intro_path = dir_path / intro_filename

        content = f"""# {title} - 概述

未开始编写

本章节将涵盖以下主要内容：

[待补充具体内容概要]

---

*本文档为《网络101》系列的一部分*
"""
        with open(intro_path, 'w', encoding='utf-8') as f:
            f.write(content)
        self.created_files.append(str(intro_path))
        print(f"创建引言文件: {intro_path}")

    def create_directory_structure(self):
        """创建完整的目录结构"""
        print("正在创建目录结构...")

        # 清理现有contents目录（除了toc.md和.DS_Store）
        if self.base_dir.exists():
            for item in self.base_dir.iterdir():
                if item.name not in ['toc.md', '.DS_Store']:
                    if item.is_file():
                        item.unlink()
                        print(f"删除旧文件: {item}")
                    elif item.is_dir():
                        import shutil
                        shutil.rmtree(item)
                        print(f"删除旧目录: {item}")

        # 创建基础目录
        self.base_dir.mkdir(parents=True, exist_ok=True)

        for chapter in self.structure:
            chapter_num = chapter['number']
            chapter_title = self.sanitize_filename(chapter['title'])
            chapter_dir_name = f"{chapter_num} {chapter_title}"
            chapter_dir = self.base_dir / chapter_dir_name

            # 创建章节目录
            chapter_dir.mkdir(exist_ok=True)
            self.created_dirs.append(str(chapter_dir))
            print(f"创建章节目录: {chapter_dir}")

            # 创建章节的introduction.md
            self.create_introduction_file(chapter_dir, chapter_num, chapter['title'])

            for section in chapter['sections']:
                section_num = section['number']
                section_title = self.sanitize_filename(section['title'])

                # 判断是否有子节
                if section['subsections']:
                    # 有子节，创建节目录
                    section_dir_name = f"{section_num} {section_title}"
                    section_dir = chapter_dir / section_dir_name
                    section_dir.mkdir(exist_ok=True)
                    self.created_dirs.append(str(section_dir))
                    print(f"创建节目录: {section_dir}")

                    # 创建节的introduction.md
                    self.create_introduction_file(section_dir, section_num, section['title'])

                    # 创建子节文件
                    for subsection in section['subsections']:
                        subsection_num = subsection['number']
                        subsection_title = self.sanitize_filename(subsection['title'])
                        subsection_filename = f"{subsection_num} {subsection_title}.md"
                        subsection_path = section_dir / subsection_filename
                        self.create_markdown_file(subsection_path, subsection['title'])
                else:
                    # 没有子节，直接创建节文件
                    section_filename = f"{section_num} {section_title}.md"
                    section_path = chapter_dir / section_filename
                    self.create_markdown_file(section_path, section['title'])

    def generate_report(self):
        """生成创建报告"""
        print("\n" + "="*60)
        print("目录结构创建完成报告")
        print("="*60)
        print(f"总共创建了 {len(self.created_dirs)} 个目录")
        print(f"总共创建了 {len(self.created_files)} 个文件")

        print(f"\n创建的目录列表:")
        for dir_path in sorted(self.created_dirs):
            print(f"  📁 {dir_path}")

        print(f"\n创建的文件列表:")
        for file_path in sorted(self.created_files):
            if 'introduction.md' in file_path:
                print(f"  📋 {file_path} (引言)")
            else:
                print(f"  📄 {file_path}")

        print(f"\n所有文件都已标记为'未开始编写'状态")
        print("目录结构严格按照toc.md的层次关系创建")
        print("="*60)

    def run(self):
        """执行完整的创建流程"""
        print("开始执行网络101书籍目录结构创建...")
        print(f"源文件: {self.toc_file_path}")
        print(f"目标目录: {self.base_dir}")
        print()

        try:
            self.parse_toc()
            self.create_directory_structure()
            self.generate_report()
            return True
        except Exception as e:
            print(f"创建过程中发生错误: {e}")
            return False


def main():
    """主函数"""
    # 设置路径
    toc_file = "/Users/bytedance/codes/network101/contents/toc.md"
    base_dir = "/Users/bytedance/codes/network101/contents"

    # 检查toc.md文件是否存在
    if not os.path.exists(toc_file):
        print(f"错误: toc.md文件不存在于 {toc_file}")
        return False

    # 创建结构创建器并执行
    creator = StructureCreator(toc_file, base_dir)
    return creator.run()


if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ 目录结构创建成功!")
    else:
        print("\n❌ 目录结构创建失败!")