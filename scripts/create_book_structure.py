#!/usr/bin/env python3
"""
网络101书籍项目目录结构创建脚本

功能：
1. 解析 toc.md 文件
2. 创建带章节号的完整目录结构
3. 创建所有 Markdown 文件并添加章节号前缀
4. 为 introduction 文件添加 .0 后缀
5. 初始化所有文件的模板内容

使用方法：
    python create_book_structure.py

作者：Claude Code
日期：2025-09-21
"""

import os
import re
from pathlib import Path


class BookStructureCreator:
    def __init__(self, toc_file="toc.md", contents_dir="contents"):
        self.base_dir = Path(__file__).parent.parent
        self.toc_file = self.base_dir / toc_file
        self.contents_dir = self.base_dir / contents_dir
        self.created_files = []
        self.created_dirs = []

    def clean_filename(self, name):
        """清理文件名，移除不支持的字符"""
        # 移除或替换文件系统不支持的字符
        name = re.sub(r'[<>:"/\\|?*]', '', name)
        name = name.replace('：', '：')  # 保留中文冒号
        name = name.strip()
        return name

    def parse_toc(self):
        """解析 toc.md 文件，返回结构化的章节信息"""
        if not self.toc_file.exists():
            raise FileNotFoundError(f"找不到 {self.toc_file} 文件")

        with open(self.toc_file, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')
        structure = []
        current_path = []

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            # 计算层级（通过前导空格或制表符）
            level = 0
            original_line = line
            while line.startswith('  ') or line.startswith('\t'):
                level += 1
                line = line[2:] if line.startswith('  ') else line[1:]

            # 移除列表标记
            line = re.sub(r'^[-*+]\s*', '', line).strip()
            if not line:
                continue

            # 调整 current_path 到当前层级
            current_path = current_path[:level]
            current_path.append(line)

            structure.append({
                'level': level,
                'title': line,
                'path': current_path.copy(),
                'full_path': ' → '.join(current_path)
            })

        return structure

    def assign_numbers(self, structure):
        """为结构中的每个项目分配章节号"""
        counters = [0] * 10  # 支持最多10层嵌套

        for item in structure:
            level = item['level']

            # 重置更深层的计数器
            for i in range(level + 1, len(counters)):
                counters[i] = 0

            # 增加当前层级计数器
            counters[level] += 1

            # 生成章节号
            number_parts = [str(counters[i]) for i in range(level + 1) if counters[i] > 0]
            item['number'] = '.'.join(number_parts)

        return structure

    def determine_file_type(self, structure, index):
        """判断当前项目是文件还是目录（是否有子项目）"""
        current_level = structure[index]['level']

        # 检查后续项目是否有更深层级的子项目
        for i in range(index + 1, len(structure)):
            next_level = structure[i]['level']
            if next_level <= current_level:
                break
            if next_level == current_level + 1:
                return 'directory'  # 有直接子项目，是目录

        return 'file'  # 没有子项目，是文件

    def create_file_template(self, title, number, file_type='content'):
        """创建文件模板内容"""
        if file_type == 'introduction':
            return f"""# {number} introduction

## 概述

本节将介绍{title}的相关内容。

## 学习目标

通过本节的学习，您将了解：

- 核心概念和基本原理
- 实际应用场景
- 相关技术要点

## 主要内容

### 内容框架

1. 基础概念介绍
2. 核心技术分析
3. 实践应用指导
4. 常见问题解答

---

*状态：未开始编写*

*项目：网络101书籍*
"""
        else:
            return f"""# {number} {title}

## 内容概要

本节将详细介绍{title}的相关知识。

## 学习目标

- 理解基本概念
- 掌握核心技术
- 能够实际应用

## 主要内容

### 1. 基础知识

### 2. 核心概念

### 3. 实际应用

### 4. 总结

---

*状态：未开始编写*

*项目：网络101书籍*
"""

    def create_structure(self):
        """创建完整的目录结构"""
        print("开始创建网络101书籍项目目录结构...")

        # 解析 toc.md
        print("解析 toc.md 文件...")
        structure = self.parse_toc()
        structure = self.assign_numbers(structure)

        # 清空并重新创建 contents 目录
        if self.contents_dir.exists():
            print(f"删除现有的 {self.contents_dir} 目录...")
            import shutil
            shutil.rmtree(self.contents_dir)

        self.contents_dir.mkdir(parents=True, exist_ok=True)
        print(f"创建 {self.contents_dir} 目录")

        # 创建文件和目录
        for i, item in enumerate(structure):
            file_type = self.determine_file_type(structure, i)
            number = item['number']
            title = item['title']
            level = item['level']

            # 构建相对路径
            path_parts = []
            for j in range(level + 1):
                ancestor = structure[i - (level - j)]
                ancestor_number = ancestor['number']
                ancestor_title = self.clean_filename(ancestor['title'])
                path_parts.append(f"{ancestor_number} {ancestor_title}")

            if file_type == 'directory':
                # 创建目录
                dir_path = self.contents_dir
                for part in path_parts:
                    dir_path = dir_path / part

                dir_path.mkdir(parents=True, exist_ok=True)
                self.created_dirs.append(str(dir_path.relative_to(self.base_dir)))
                print(f"创建目录: {dir_path.relative_to(self.base_dir)}")

                # 创建 introduction 文件
                intro_filename = f"{number}.0 introduction.md"
                intro_path = dir_path / intro_filename
                intro_content = self.create_file_template(title, f"{number}.0", 'introduction')

                with open(intro_path, 'w', encoding='utf-8') as f:
                    f.write(intro_content)

                self.created_files.append(str(intro_path.relative_to(self.base_dir)))
                print(f"创建文件: {intro_path.relative_to(self.base_dir)}")

            else:
                # 创建文件
                file_dir = self.contents_dir
                for part in path_parts[:-1]:  # 除了最后一个（文件名）
                    file_dir = file_dir / part

                file_dir.mkdir(parents=True, exist_ok=True)

                filename = f"{number} {self.clean_filename(title)}.md"
                file_path = file_dir / filename
                file_content = self.create_file_template(title, number, 'content')

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)

                self.created_files.append(str(file_path.relative_to(self.base_dir)))
                print(f"创建文件: {file_path.relative_to(self.base_dir)}")

    def print_summary(self):
        """打印创建摘要"""
        print("\n" + "="*60)
        print("目录结构创建完成！")
        print("="*60)
        print(f"创建目录数量: {len(self.created_dirs)}")
        print(f"创建文件数量: {len(self.created_files)}")
        print(f"总计: {len(self.created_dirs) + len(self.created_files)} 个项目")

        # 统计各类文件
        intro_files = [f for f in self.created_files if 'introduction.md' in f]
        content_files = [f for f in self.created_files if 'introduction.md' not in f]

        print(f"\n文件类型统计:")
        print(f"- Introduction 文件: {len(intro_files)}")
        print(f"- 内容文件: {len(content_files)}")

        print(f"\n所有文件已创建在: {self.contents_dir}")
        print("可以开始进行内容撰写工作！")


def main():
    """主函数"""
    try:
        creator = BookStructureCreator()
        creator.create_structure()
        creator.print_summary()

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()