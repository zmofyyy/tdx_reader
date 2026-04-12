#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试使用 pytdx 连接到指定 IP 和端口获取行情数据
"""

from pytdx.hq import TdxHq_API


def test_hq_connection(ip, port):
    """
    测试连接到指定的行情服务器并获取行情数据
    
    Args:
        ip (str): 行情服务器 IP 地址
        port (int): 行情服务器端口
    """
    print(f"测试连接到行情服务器: {ip}:{port}")
    print("-" * 80)
    
    try:
        # 初始化 API
        api = TdxHq_API()
        
        # 连接服务器
        with api.connect(ip, port):
            print("✓ 连接成功!")
            
            # 获取上证指数数据
            print("\n获取上证指数 (000001) 行情数据:")
            data = api.get_security_quotes([(0, '000001')])
            if data:
                print(f"原始数据: {data}")
                # 尝试不同的字段名
                for item in data:
                    print(f"\n数据类型: {type(item)}")
                    if isinstance(item, dict):
                        print(f"可用字段: {list(item.keys())}")
                        # 尝试访问可能的字段
                        if 'code' in item:
                            print(f"代码: {item['code']}")
                        if 'name' in item:
                            print(f"名称: {item['name']}")
                        elif 'stockname' in item:
                            print(f"名称: {item['stockname']}")
                        if 'price' in item:
                            print(f"最新价: {item['price']}")
                        elif 'last_close' in item:
                            print(f"最新价: {item['last_close']}")
            else:
                print("✗ 未能获取行情数据")
                
            # 获取深证成指数据
            print("\n获取深证成指 (399001) 行情数据:")
            data = api.get_security_quotes([(1, '399001')])
            if data:
                print(f"原始数据: {data}")
                # 尝试不同的字段名
                for item in data:
                    print(f"\n数据类型: {type(item)}")
                    if isinstance(item, dict):
                        print(f"可用字段: {list(item.keys())}")
                        # 尝试访问可能的字段
                        if 'code' in item:
                            print(f"代码: {item['code']}")
                        if 'name' in item:
                            print(f"名称: {item['name']}")
                        elif 'stockname' in item:
                            print(f"名称: {item['stockname']}")
                        if 'price' in item:
                            print(f"最新价: {item['price']}")
                        elif 'last_close' in item:
                            print(f"最新价: {item['last_close']}")
            else:
                print("✗ 未能获取行情数据")
                
    except Exception as e:
        print(f"✗ 连接失败: {str(e)}")
    
    print("-" * 80)


def main():
    """
    主函数
    """
    # 测试指定的 IP 和端口
    ip = "124.71.187.72"
    port = 7709
    
    test_hq_connection(ip, port)


if __name__ == "__main__":
    main()
