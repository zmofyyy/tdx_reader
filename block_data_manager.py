#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
板块数据管理工具

使用 pytdx 从本地文件或服务器获取板块数据
"""

import os
import argparse
from pytdx.reader.block_reader import BlockReader, BlockReader_TYPE_GROUP
from pytdx.hq import TdxHq_API


def get_block_data_from_file(file_path):
    """
    从本地文件读取板块数据
    
    Args:
        file_path (str): 板块数据文件路径
        
    Returns:
        list: 板块数据列表
    """
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
        
        return data
        
    except Exception as e:
        print(f"从文件读取失败: {str(e)}")
        return None


def get_block_data_from_server(ip, port):
    """
    从行情服务器获取板块数据
    
    Args:
        ip (str): 行情服务器 IP 地址
        port (int): 行情服务器端口
        
    Returns:
        dict: 板块数据字典
    """
    try:
        # 初始化 API
        api = TdxHq_API()
        
        # 连接服务器
        with api.connect(ip, port):
            print(f"成功连接到服务器: {ip}:{port}")
            
            # 尝试获取板块数据
            # 注意：不同版本的 pytdx API 可能有所不同
            try:
                # 尝试使用 get_block_info 方法
                print("尝试获取板块信息...")
                # 这里需要知道具体的板块代码，我们尝试获取第一个板块
                block_info = api.get_block_info(0, '1')
                if block_info:
                    print(f"获取到板块信息: {block_info}")
                    return block_info
                else:
                    print("未能获取板块信息")
            except Exception as e:
                print(f"获取板块信息失败: {str(e)}")
                
    except Exception as e:
        print(f"连接服务器失败: {str(e)}")
    
    return None


def display_block_data(data):
    """
    显示板块数据
    
    Args:
        data: 板块数据
    """
    if not data:
        print("没有板块数据可显示")
        return
    
    if isinstance(data, list):
        # 从文件读取的数据格式
        print(f"获取到 {len(data)} 个板块")
        
        # 打印前10个板块
        for i, block in enumerate(data[:10]):
            block_name = block['blockname']
            block_type = block['block_type']
            stock_count = block['stock_count']
            stock_codes = block['code_list'].split(',')
            
            print(f"\n{i+1}. 板块名称: {block_name}")
            print(f"   板块类型: {block_type}")
            print(f"   股票数量: {stock_count}")
            print(f"   股票代码: {', '.join(stock_codes[:5])}..." if len(stock_codes) > 5 else f"   股票代码: {', '.join(stock_codes)}")
        
        if len(data) > 10:
            print(f"\n... 还有 {len(data) - 10} 个板块未显示")
    
    elif isinstance(data, dict):
        # 从服务器获取的数据格式
        print("获取到板块数据:")
        print(data)
    
    else:
        print("未知数据格式")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='板块数据管理工具')
    parser.add_argument('--file', help='板块数据文件路径')
    parser.add_argument('--server', help='行情服务器 IP:端口，如 124.71.187.72:7709')
    
    args = parser.parse_args()
    
    if args.file:
        # 从文件读取
        print(f"从文件读取板块数据: {args.file}")
        print("-" * 100)
        data = get_block_data_from_file(args.file)
        display_block_data(data)
    
    elif args.server:
        # 从服务器获取
        try:
            ip, port = args.server.split(':')
            port = int(port)
            print(f"从服务器获取板块数据: {ip}:{port}")
            print("-" * 100)
            data = get_block_data_from_server(ip, port)
            display_block_data(data)
        except ValueError:
            print("服务器地址格式错误，请使用 IP:端口 格式")
    
    else:
        # 默认行为
        print("请指定数据源:")
        print("  --file: 从本地文件读取板块数据")
        print("  --server: 从行情服务器获取板块数据")
        
        # 尝试默认文件路径
        default_path = "D:\\tdx_new\\T0002\\hq_cache\\block_zs.dat"
        print(f"\n尝试默认路径: {default_path}")
        print("-" * 100)
        data = get_block_data_from_file(default_path)
        display_block_data(data)


if __name__ == "__main__":
    main()
