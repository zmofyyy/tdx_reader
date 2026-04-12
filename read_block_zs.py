#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to read and parse industry sector data from block_zs.dat file using pytdx BlockReader
"""

import os
from pytdx.reader.block_reader import BlockReader, BlockReader_TYPE_GROUP, BlockReader_TYPE_FLAT


def read_industry_sectors(file_path):
    """
    Read and parse industry sector data from the specified file
    
    Args:
        file_path (str): Path to the block_zs.dat file
        
    Returns:
        dict: A dictionary containing industry sector information
    """
    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    # Check if file is readable
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Permission denied: {file_path}")
    
    try:
        # Initialize BlockReader
        reader = BlockReader()
        
        # Read data in grouped format
        data = reader.get_data(file_path, result_type=BlockReader_TYPE_GROUP)
        
        # Structure the output
        sectors = {}
        for item in data:
            sector_name = item['blockname']
            sector_type = item['block_type']
            stock_count = item['stock_count']
            stock_codes = item['code_list'].split(',')
            
            sectors[sector_name] = {
                'type': sector_type,
                'stock_count': stock_count,
                'stocks': stock_codes
            }
        
        return sectors
        
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")


def main():
    """
    Main function to demonstrate reading industry sector data
    """
    file_path = "D:\\tdx_new\\T0002\\hq_cache\\block_zs.dat"
    
    try:
        sectors = read_industry_sectors(file_path)
        
        print("Industry Sectors Data:")
        print("-" * 80)
        
        for sector_name, sector_info in sectors.items():
            print(f"Sector: {sector_name}")
            print(f"Type: {sector_info['type']}")
            print(f"Stock Count: {sector_info['stock_count']}")
            print(f"Stocks: {', '.join(sector_info['stocks'][:5])}..." if len(sector_info['stocks']) > 5 else f"Stocks: {', '.join(sector_info['stocks'])}")
            print("-" * 80)
            
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
