#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
根据 tdxzs_new.csv 中的板块代码获取板块日线数据
"""

import os
import csv
import pandas as pd
from pytdx.hq import TdxHq_API


def ensure_data_directory():
    """
    确保 data 目录存在
    """
    if not os.path.exists('data'):
        os.makedirs('data')
        print("创建 data 目录成功")
    else:
        print("data 目录已存在")


def read_block_codes(csv_file):
    """
    从 CSV 文件中读取板块代码
    
    Args:
        csv_file (str): CSV 文件路径
        
    Returns:
        list: 板块代码列表
    """
    block_codes = []
    try:
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                block_code = row.get('block_code')
                if block_code:
                    block_codes.append(block_code)
        print(f"成功读取 {len(block_codes)} 个板块代码")
    except Exception as e:
        print(f"读取板块代码失败: {str(e)}")
    return block_codes


def get_existing_data(file_path):
    """
    获取已存在的板块数据
    
    Args:
        file_path (str): 文件路径
        
    Returns:
        pd.DataFrame: 已存在的数据
    """
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
            print(f"读取已存在的数据，共 {len(df)} 条")
            return df
        except Exception as e:
            print(f"读取已存在数据失败: {str(e)}")
            return pd.DataFrame()
    else:
        print("文件不存在，将获取初始数据")
        return pd.DataFrame()


def get_block_daily_data(api, code, start, count):
    """
    获取板块日线数据
    
    Args:
        api: TdxHq_API 实例
        code (str): 板块代码
        start (int): 开始位置
        count (int): 获取数量
        
    Returns:
        list: 板块日线数据
    """
    try:
        # 使用 get_index_bars 获取板块日线数据
        # 参数: (category, market, code, start, count)
        # category: 4=日K线（根据用户提供的参数定义）
        # market: 1=上海（板块指数通常在上海市场）
        data = api.get_index_bars(4, 1, code, start, count)
        return data
    except Exception as e:
        print(f"获取板块 {code} 数据失败: {str(e)}")
        return []


def save_block_data(data, file_path):
    """
    保存板块数据到 CSV 文件
    
    Args:
        data (list): 板块数据
        file_path (str): 文件路径
    """
    if not data:
        print("没有数据可保存")
        return
    
    try:
        # 转换为 DataFrame
        df = pd.DataFrame(data)
        
        # 保存到 CSV 文件
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"成功保存 {len(df)} 条数据到 {file_path}")
    except Exception as e:
        print(f"保存数据失败: {str(e)}")


def main():
    """
    主函数
    """
    # 确保 data 目录存在
    ensure_data_directory()
    
    # 读取板块代码
    csv_file = "./tdxzs_new.csv"
    block_codes = read_block_codes(csv_file)
    
    if not block_codes:
        print("没有板块代码可处理")
        return
    
    # 初始化 API
    api = TdxHq_API()
    
    try:
        # 连接服务器
        with api.connect("124.71.187.72", 7709):
            print("连接服务器成功")
            
            # 处理每个板块
            for block_code in block_codes:
                print(f"\n处理板块: {block_code}")
                
                # 构建文件路径
                file_path = f"data/{block_code}.csv"
                
                # 获取已存在的数据
                existing_df = get_existing_data(file_path)
                
                if existing_df.empty:
                    # 初始获取 800 条数据
                    print("初始获取 800 条数据")
                    data = get_block_daily_data(api, block_code, 0, 800)
                else:
                    # 增量获取数据
                    existing_count = len(existing_df)
                    print(f"增量获取数据，已有 {existing_count} 条")
                    data = get_block_daily_data(api, block_code, existing_count, 200)  # 每次增量获取 200 条
                    
                    # 如果有新数据，追加到已存在的数据中
                    if data:
                        new_df = pd.DataFrame(data)
                        existing_df = pd.concat([existing_df, new_df], ignore_index=True)
                        data = existing_df.to_dict('records')
                
                # 保存数据
                save_block_data(data, file_path)
                
    except Exception as e:
        print(f"连接服务器失败: {str(e)}")
    
    print("\n所有板块数据处理完成")


if __name__ == "__main__":
    main()
