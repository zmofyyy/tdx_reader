#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
读取 tdxhy.cfg 文件并转换为 CSV 格式
"""

import os
import csv


def convert_tdxhy_to_csv(input_file, output_file):
    """
    读取 tdxhy.cfg 文件并转换为 CSV 格式
    
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
        
        # 读取文件内容
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"读取到 {len(lines)} 行数据")
        
        # 处理数据
        data = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 按 | 分隔列
            columns = line.split('|')
            if len(columns) >= 4:
                # 提取前四列，忽略第四列
                market_code = columns[0]
                stock_code = columns[1]
                industry_code = columns[2]
                # 忽略第四列
                
                # 添加到数据列表
                data.append([market_code, stock_code, industry_code])
        
        print(f"处理后得到 {len(data)} 条有效数据")
        
        # 写入 CSV 文件
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # 写入英文表头
            writer.writerow(['market_code', 'stock_code', 'industry_code'])
            # 写入数据，确保股票代码是六位字符串并添加前缀
            for row in data:
                market_code = row[0]
                # 确保股票代码是六位字符串，不足六位前面补零
                stock_code = str(row[1]).strip()
                # 补零到六位
                stock_code = stock_code.zfill(6)
                # 根据市场代码添加前缀
                if market_code == '0':
                    stock_code = f"SZ.{stock_code}"
                elif market_code == '1':
                    stock_code = f"SH.{stock_code}"
                elif market_code == '2':
                    stock_code = f"BJ.{stock_code}"
                row[1] = stock_code
                writer.writerow(row)
        
        print(f"成功转换为 CSV 文件: {output_file}")
        print(f"市场代码说明: 0=深成指, 1=上证, 2=北证")
        
    except Exception as e:
        print(f"转换失败: {str(e)}")
    
    print("-" * 100)


def main():
    """
    主函数
    """
    # 输入文件路径
    input_file = "./tdxhy.cfg"
    # 输出文件路径
    output_file = "./tdxhy_new.csv"
    
    convert_tdxhy_to_csv(input_file, output_file)


if __name__ == "__main__":
    main()
