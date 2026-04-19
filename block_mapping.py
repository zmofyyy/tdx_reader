#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
板块映射操作
1. 从 tdxzs_new.csv 筛选 block_encoding 为 Txx 格式的板块
2. 使用 tdxhy_new.csv 映射板块到成分股
3. 建立板块层级关系
4. 确保子板块成分股合并到一级板块
"""

import os
import csv
import re
from collections import defaultdict


def read_tdxzs_file(file_path):
    """
    读取 tdxzs_new.csv 文件

    Args:
        file_path: 文件路径

    Returns:
        list: 板块数据列表
    """
    blocks = []
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                blocks.append(row)
        print(f"成功读取 {len(blocks)} 个板块")
    except Exception as e:
        print(f"读取 tdxzs_new.csv 失败: {str(e)}")
    return blocks


def read_tdxhy_file(file_path):
    """
    读取 tdxhy_new.csv 文件

    Args:
        file_path: 文件路径

    Returns:
        dict: 行业代码到股票列表的映射
    """
    industry_map = defaultdict(list)
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                industry_code = row.get('industry_code')
                stock_code = row.get('stock_code')
                if industry_code and stock_code:
                    industry_map[industry_code].append(stock_code)
        print(f"成功读取 {len(industry_map)} 个行业代码的成分股")
    except Exception as e:
        print(f"读取 tdxhy_new.csv 失败: {str(e)}")
    return industry_map


def filter_t_blocks(blocks):
    """
    筛选出 block_encoding 为 Txx 格式的板块

    Args:
        blocks: 板块数据列表

    Returns:
        list: 筛选后的板块列表
    """
    filtered = []
    pattern = r'^T\d+'
    for block in blocks:
        block_encoding = block.get('block_encoding')
        if block_encoding and re.match(pattern, block_encoding):
            filtered.append(block)
    print(f"筛选出 {len(filtered)} 个 T 格式板块")
    return filtered


def build_block_hierarchy(blocks):
    """
    建立板块层级关系

    Args:
        blocks: 筛选后的板块列表

    Returns:
        dict: 板块层级结构
    """
    hierarchy = {}
    
    # 先按编码长度分组
    blocks_by_length = {5: [], 7: []}
    for block in blocks:
        encoding = block.get('block_encoding')
        if encoding:
            length = len(encoding)
            if length in blocks_by_length:
                blocks_by_length[length].append(block)

    # 处理一级板块 (Txxxx)
    for block in blocks_by_length[5]:
        encoding = block.get('block_encoding')
        if encoding:
            hierarchy[encoding] = {
                'block': block,
                'level': 1,
                'children': [],
                'stocks': []
            }

    # 处理二级板块 (Txxxxxx)
    for block in blocks_by_length[7]:
        encoding = block.get('block_encoding')
        if encoding:
            parent_encoding = encoding[:5]  # 取前5位作为父级编码
            if parent_encoding in hierarchy:
                hierarchy[parent_encoding]['children'].append({
                    'block': block,
                    'level': 2,
                    'stocks': []
                })
            else:
                # 如果父级不存在，创建一个新的一级板块
                hierarchy[encoding] = {
                    'block': block,
                    'level': 1,
                    'children': [],
                    'stocks': []
                }

    print(f"建立了 {len(hierarchy)} 个一级板块的层级结构")
    return hierarchy


def map_stocks_to_blocks(hierarchy, industry_map):
    """
    将成分股映射到板块

    Args:
        hierarchy: 板块层级结构
        industry_map: 行业代码到股票列表的映射
    """
    for encoding, block_info in hierarchy.items():
        # 尝试直接匹配板块编码
        if encoding in industry_map:
            block_info['stocks'] = industry_map[encoding]
            print(f"为一级板块 {encoding} 映射了 {len(block_info['stocks'])} 只成分股")

        # 处理二级板块
        for child in block_info['children']:
            child_encoding = child['block'].get('block_encoding')
            if child_encoding and child_encoding in industry_map:
                child['stocks'] = industry_map[child_encoding]
                print(f"为二级板块 {child_encoding} 映射了 {len(child['stocks'])} 只成分股")


def merge_child_stocks_to_parent(hierarchy):
    """
    将子板块的成分股合并到一级板块

    Args:
        hierarchy: 板块层级结构
    """
    for encoding, block_info in hierarchy.items():
        # 收集所有子板块的成分股
        child_stocks = []
        for child in block_info['children']:
            child_stocks.extend(child['stocks'])

        # 去重并合并到一级板块
        if child_stocks:
            # 合并并去重
            all_stocks = list(set(block_info['stocks'] + child_stocks))
            block_info['stocks'] = all_stocks
            print(f"将子板块成分股合并到一级板块 {encoding}，总成分股数: {len(all_stocks)}")


def validate_block_hierarchy(hierarchy):
    """
    验证板块层级结构的正确性

    Args:
        hierarchy: 板块层级结构
    """
    print("\n验证板块层级结构...")
    
    total_parent_stocks = 0
    total_child_stocks = 0
    total_unique_stocks = 0

    for encoding, block_info in hierarchy.items():
        parent_stocks = len(block_info['stocks'])
        total_parent_stocks += parent_stocks

        # 检查子板块
        child_count = len(block_info['children'])
        if child_count > 0:
            print(f"一级板块 {encoding} 包含 {child_count} 个子板块")
            
            for child in block_info['children']:
                child_encoding = child['block'].get('block_encoding')
                child_stocks = len(child['stocks'])
                total_child_stocks += child_stocks
                print(f"  二级板块 {child_encoding} 有 {child_stocks} 只成分股")

                # 验证子板块成分股是否包含在父板块中
                for stock in child['stocks']:
                    if stock not in block_info['stocks']:
                        print(f"  错误: 子板块 {child_encoding} 的成分股 {stock} 未包含在父板块中")

        # 统计唯一成分股
        total_unique_stocks += len(set(block_info['stocks']))

    print(f"\n验证结果:")
    print(f"一级板块总成分股数: {total_parent_stocks}")
    print(f"二级板块总成分股数: {total_child_stocks}")
    print(f"一级板块唯一成分股数: {total_unique_stocks}")


def save_block_mapping(hierarchy, output_file):
    """
    保存板块映射结果

    Args:
        hierarchy: 板块层级结构
        output_file: 输出文件路径
    """
    try:
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # 写入表头
            writer.writerow(['level', 'block_encoding', 'block_name', 'child_encoding', 'child_name', 'stock_count', 'stocks'])

            # 写入一级板块
            for encoding, block_info in hierarchy.items():
                block = block_info['block']
                stock_count = len(block_info['stocks'])
                stocks = ','.join(block_info['stocks'])
                writer.writerow([
                    block_info['level'],
                    encoding,
                    block.get('block_name', ''),
                    '',
                    '',
                    stock_count,
                    stocks
                ])

                # 写入二级板块
                for child in block_info['children']:
                    child_block = child['block']
                    child_encoding = child_block.get('block_encoding')
                    child_stock_count = len(child['stocks'])
                    child_stocks = ','.join(child['stocks'])
                    writer.writerow([
                        child['level'],
                        encoding,
                        block.get('block_name', ''),
                        child_encoding,
                        child_block.get('block_name', ''),
                        child_stock_count,
                        child_stocks
                    ])

        print(f"成功保存板块映射结果到 {output_file}")
    except Exception as e:
        print(f"保存板块映射结果失败: {str(e)}")


def main():
    """
    主函数
    """
    # 读取文件
    tdxzs_file = "./converter/tdxzs_new.csv"
    tdxhy_file = "./converter/tdxhy_new.csv"
    output_file = "./block_mapping_result.csv"

    # 读取数据
    blocks = read_tdxzs_file(tdxzs_file)
    industry_map = read_tdxhy_file(tdxhy_file)

    if not blocks or not industry_map:
        print("数据读取失败，无法继续")
        return

    # 筛选 T 格式板块
    filtered_blocks = filter_t_blocks(blocks)

    if not filtered_blocks:
        print("没有找到 T 格式板块")
        return

    # 建立板块层级
    hierarchy = build_block_hierarchy(filtered_blocks)

    # 映射成分股
    map_stocks_to_blocks(hierarchy, industry_map)

    # 合并子板块成分股到一级板块
    merge_child_stocks_to_parent(hierarchy)

    # 验证板块层级结构
    validate_block_hierarchy(hierarchy)

    # 保存结果
    save_block_mapping(hierarchy, output_file)

    print("板块映射操作完成！")


if __name__ == "__main__":
    main()
