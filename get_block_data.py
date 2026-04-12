#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用 pytdx 获取板块数据
"""

import os
from pytdx.reader.block_reader import BlockReader, BlockReader_TYPE_GROUP


def get_block_data_from_file(file_path):
    """
    从本地文件读取板块数据
    
    Args:
        file_path (str): 板块数据文件路径
    """
    print(f"从本地文件读取板块数据: {file_path}")
    print("-" * 100)
    
    try:
        # 验证文件
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        if not os.access(file_path, os.R_OK):
            raise PermissionError(f"没有读取权限: {file_path}")
        
        # 初始化 BlockReader
        reader = BlockReader()
        
        # 读取数据
        data = reader.get_data(file_path, result_type=BlockReader_TYPE_GROUP)
        
        if data:
            print(f"获取到 {len(data)} 个板块")
            
            # 打印板块信息
            for i, block in enumerate(data):
                block_name = block['blockname']
                block_type = block['block_type']
                stock_count = block['stock_count']
                stock_codes = block['code_list'].split(',')
                
                print(f"\n{i+1}. 板块名称: {block_name}")
                print(f"   板块类型: {block_type}")
                print(f"   股票数量: {stock_count}")
                print(f"   股票代码: {', '.join(stock_codes[:5])}..." if len(stock_codes) > 5 else f"   股票代码: {', '.join(stock_codes)}")
        else:
            print("✗ 未能获取板块数据")
            
    except Exception as e:
        print(f"✗ 读取失败: {str(e)}")
    
    print("-" * 100)


def main():
    """
    主函数
    """
    # 板块数据文件路径
    # 这里使用用户之前提到的路径
    file_path = "D:\\tdx_new\\T0002\\hq_cache\\block_zs.dat"
    
    get_block_data_from_file(file_path)


if __name__ == "__main__":
    main()
