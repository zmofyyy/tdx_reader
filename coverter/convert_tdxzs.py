#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
读取 tdxzs.cfg 文件并转换为 CSV 格式
"""

import os
import csv


def convert_tdxzs_to_csv(input_file, output_file):
    """
    读取 tdxzs.cfg 文件并转换为 CSV 格式
    
    Args:
        input_file (str): 输入文件路径
        output_file (str): 输出文件路径
    """
    print(f"读取文件: {input_file}")
    print("-" * 100)
    
    try:
        # 检查文件是否存在
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"文件不存在: {input_file}")
        
        # 检查文件是否可读
        if not os.access(input_file, os.R_OK):
            raise PermissionError(f"没有读取权限: {input_file}")
        
        # 读取文件内容，尝试使用多种编码
        encodings = ['gbk', 'gb2312', 'utf-8', 'latin-1']
        lines = []
        
        for encoding in encodings:
            try:
                with open(input_file, 'r', encoding=encoding) as f:
                    lines = f.readlines()
                print(f"成功使用 {encoding} 编码读取文件")
                break
            except UnicodeDecodeError:
                continue
        
        if not lines:
            raise Exception("无法读取文件，所有编码尝试都失败")
        
        print(f"读取到 {len(lines)} 行数据")
        
        # 处理数据
        data = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 按 | 分隔列
            columns = line.split('|')
            if len(columns) >= 6:
                # 提取前六列
                block_name = columns[0]  # 板块名称
                block_code = columns[1]  # 板块代码
                block_type = columns[2]  # 板块种类
                market_type = columns[3]  # 市场种类
                block_level = columns[4]  # 板块等级
                block_encoding = columns[5]  # 板块编码
                
                # 添加到数据列表
                data.append([block_name, block_code, block_type, market_type, block_level, block_encoding])
        
        print(f"处理后得到 {len(data)} 条有效数据")
        
        # 写入 CSV 文件，使用 utf-8-sig 编码（包含 BOM）
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # 写入英文表头
            writer.writerow(['block_name', 'block_code', 'block_type', 'market_type', 'block_level', 'block_encoding'])
            # 写入数据，确保板块代码作为字符串
            for row in data:
                # 确保板块代码是字符串
                row[1] = str(row[1])
                # 确保板块名称是字符串，处理可能的编码问题
                row[0] = str(row[0])
                writer.writerow(row)
        
        print(f"成功转换为 CSV 文件: {output_file}")
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
    
    print("-" * 100)


def main():
    """
    主函数
    """
    # 输入文件路径
    input_file = "./tdxzs.cfg"
    # 输出文件路径
    output_file = "./tdxzs_new.csv"
    
    convert_tdxzs_to_csv(input_file, output_file)


if __name__ == "__main__":
    main()
