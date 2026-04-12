#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
完整测试使用 pytdx 连接到指定 IP 和端口获取行情数据
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
    print("-" * 100)
    
    try:
        # 初始化 API
        api = TdxHq_API()
        
        # 连接服务器
        with api.connect(ip, port):
            print("✓ 连接成功!")
            
            # 测试 1: 获取平安银行数据
            print("\n测试 1: 获取平安银行 (000001) 行情数据:")
            data = api.get_security_quotes([(0, '000001')])
            if data:
                for item in data:
                    print(f"代码: {item['code']}")
                    print(f"最新价: {item['price']}")
                    print(f"开盘价: {item['open']}")
                    print(f"最高价: {item['high']}")
                    print(f"最低价: {item['low']}")
                    print(f"成交量: {item['vol']}")
                    print(f"成交额: {item['amount']}")
                    print(f"时间: {item['servertime']}")
            else:
                print("✗ 未能获取行情数据")
                
            # 测试 2: 获取上证指数数据
            print("\n测试 2: 获取上证指数 (999999) 行情数据:")
            data = api.get_security_quotes([(0, '999999')])
            if data:
                for item in data:
                    print(f"代码: {item['code']}")
                    print(f"最新价: {item['price']}")
                    print(f"开盘价: {item['open']}")
                    print(f"最高价: {item['high']}")
                    print(f"最低价: {item['low']}")
                    print(f"成交量: {item['vol']}")
                    print(f"成交额: {item['amount']}")
                    print(f"时间: {item['servertime']}")
            else:
                print("✗ 未能获取行情数据")
                
            # 测试 3: 获取深证成指数据
            print("\n测试 3: 获取深证成指 (399001) 行情数据:")
            data = api.get_security_quotes([(0, '399001')])
            if data:
                for item in data:
                    print(f"代码: {item['code']}")
                    print(f"最新价: {item['price']}")
                    print(f"开盘价: {item['open']}")
                    print(f"最高价: {item['high']}")
                    print(f"最低价: {item['low']}")
                    print(f"成交量: {item['vol']}")
                    print(f"成交额: {item['amount']}")
                    print(f"时间: {item['servertime']}")
            else:
                print("✗ 未能获取行情数据")
                
            # 测试 4: 获取多只股票数据
            print("\n测试 4: 获取多只股票行情数据:")
            stocks = [(0, '000001'), (0, '000002'), (1, '600000')]
            data = api.get_security_quotes(stocks)
            if data:
                for item in data:
                    print(f"代码: {item['code']}, 最新价: {item['price']}, 涨跌幅: {(item['price']/item['last_close']-1)*100:.2f}%")
            else:
                print("✗ 未能获取行情数据")
                
            # 测试 4: 获取股票列表
            print("\n测试 4: 获取股票列表:")
            stocks = api.get_security_list(0, 0, 10)
            if stocks:
                print(f"获取到 {len(stocks)} 只股票")
                for stock in stocks[:5]:
                    print(f"代码: {stock['code']}, 名称: {stock['name']}")
            else:
                print("✗ 未能获取股票列表")
                
    except Exception as e:
        print(f"✗ 连接失败: {str(e)}")
    
    print("-" * 100)


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
