#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
使用 pytdx 获取板块指数数据
"""

from pytdx.hq import TdxHq_API
import pandas as pd


def get_block_index_data(ip, port, code, start=0, count=10):
    """
    从行情服务器获取板块指数数据
    
    Args:
        ip (str): 行情服务器 IP 地址
        port (int): 行情服务器端口
        code (str): 板块指数代码
        start (int): 开始位置
        count (int): 获取数量
    """
    print(f"连接到行情服务器: {ip}:{port} 获取板块指数数据")
    print("-" * 100)
    
    try:
        # 初始化 API
        api = TdxHq_API()
        
        # 连接服务器
        with api.connect(ip, port):
            print("✓ 连接成功!")
            
            # 获取板块指数 K 线数据
            print(f"\n获取板块指数 {code} 的 K 线数据:")
            data = None
            # 尝试不同的市场代码
            for market in [0, 1]:
                print(f"尝试市场代码: {market}")
                # 使用 get_index_bars 方法获取指数 K 线数据
                # 参数说明: (category, market, code, start, count)
                #0 5分钟K线 1 15分钟K线 2 30分钟K线 3 1小时K线 4 日K线 5 周K线 6 月K线 7 1分钟 8 1分钟K线 9 日K线 10 季K线 11 年K线
                # market: 0=深圳, 1=上海
                # code: 股票代码
                # start: 起始位置
                # count: 数量
                market=1
                data = api.get_index_bars(9, market, code, start, count)
                
                if data:
                    print(f"✓ 成功获取数据 (市场代码: {market})")
                    break
            
            if data:
                print(f"获取到 {len(data)} 条 K 线数据")
                
                # 转换为 DataFrame 方便查看
                df = pd.DataFrame(data)
                print("\nK 线数据:")
                print(df[['datetime', 'open', 'high', 'low', 'close', 'vol', 'amount']])
                
                # 打印最新数据
                latest = data[0]
                print("\n最新数据:")
                print(f"日期: {latest['datetime']}")
                print(f"开盘价: {latest['open']}")
                print(f"最高价: {latest['high']}")
                print(f"最低价: {latest['low']}")
                print(f"收盘价: {latest['close']}")
                print(f"成交量: {latest['vol']}")
                print(f"成交额: {latest['amount']}")
            else:
                print("✗ 未能获取板块指数数据")
                
    except Exception as e:
        print(f"✗ 连接失败: {str(e)}")
    
    print("-" * 100)


def main():
    """
    主函数
    """
    # 使用指定的 IP 和端口
    ip = "124.71.187.72"
    port = 7709
    
    # 测试 880301 板块指数
    code = "880302"
    get_block_index_data(ip, port, code)


if __name__ == "__main__":
    main()
