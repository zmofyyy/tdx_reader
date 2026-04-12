#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Industry Sector Data Reader for pytdx

This script uses the pytdx BlockReader module to read and parse industry sector data
from the block_zs.dat file. It provides functions to:
1. Read and parse the binary block_zs.dat file
2. Structure the data in a clear, accessible format
3. Handle errors gracefully
4. Provide both grouped and flat output formats
"""

import os
import argparse
from pytdx.reader.block_reader import BlockReader, BlockReader_TYPE_GROUP, BlockReader_TYPE_FLAT


def validate_file(file_path):
    """
    Validate that the file exists and is readable
    
    Args:
        file_path (str): Path to the file to validate
        
    Raises:
        FileNotFoundError: If the file does not exist
        PermissionError: If the file is not readable
        ValueError: If the file path is empty
    """
    if not file_path:
        raise ValueError("File path cannot be empty")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Permission denied: {file_path}")


def read_block_zs(file_path, result_type=BlockReader_TYPE_GROUP):
    """
    Read and parse the block_zs.dat file
    
    Args:
        file_path (str): Path to the block_zs.dat file
        result_type (int): Result type (BlockReader_TYPE_GROUP or BlockReader_TYPE_FLAT)
        
    Returns:
        list: List of dictionaries containing sector data
    """
    # Validate file
    validate_file(file_path)
    
    try:
        # Initialize BlockReader
        reader = BlockReader()
        
        # Read data
        data = reader.get_data(file_path, result_type=result_type)
        
        return data
        
    except Exception as e:
        raise Exception(f"Error reading file: {str(e)}")


def get_sectors_grouped(file_path):
    """
    Get sectors in grouped format
    
    Args:
        file_path (str): Path to the block_zs.dat file
        
    Returns:
        dict: Dictionary with sector names as keys and sector info as values
    """
    data = read_block_zs(file_path, BlockReader_TYPE_GROUP)
    
    sectors = {}
    for item in data:
        sector_name = item['blockname']
        sectors[sector_name] = {
            'type': item['block_type'],
            'stock_count': item['stock_count'],
            'stocks': item['code_list'].split(',')
        }
    
    return sectors


def get_sectors_flat(file_path):
    """
    Get sectors in flat format
    
    Args:
        file_path (str): Path to the block_zs.dat file
        
    Returns:
        list: List of dictionaries with sector-stock relationships
    """
    return read_block_zs(file_path, BlockReader_TYPE_FLAT)


def print_sectors_grouped(sectors):
    """
    Print sectors in grouped format
    
    Args:
        sectors (dict): Dictionary with sector information
    """
    print("Industry Sectors (Grouped Format):")
    print("-" * 100)
    
    for sector_name, sector_info in sectors.items():
        print(f"Sector: {sector_name}")
        print(f"Type: {sector_info['type']}")
        print(f"Stock Count: {sector_info['stock_count']}")
        
        stocks = sector_info['stocks']
        if len(stocks) > 10:
            print(f"Stocks (first 10): {', '.join(stocks[:10])}...")
        else:
            print(f"Stocks: {', '.join(stocks)}")
        
        print("-" * 100)


def print_sectors_flat(sectors):
    """
    Print sectors in flat format
    
    Args:
        sectors (list): List of sector-stock relationships
    """
    print("Industry Sectors (Flat Format):")
    print("-" * 100)
    print(f"{'Sector':<20} {'Type':<10} {'Index':<10} {'Code':<10}")
    print("-" * 100)
    
    for item in sectors:
        print(f"{item['blockname']:<20} {item['block_type']:<10} {item['code_index']:<10} {item['code']:<10}")
    
    print("-" * 100)


def main():
    """
    Main function with command-line arguments
    """
    parser = argparse.ArgumentParser(description='Read and parse industry sector data from block_zs.dat')
    parser.add_argument('file_path', help='Path to block_zs.dat file')
    parser.add_argument('--format', choices=['grouped', 'flat'], default='grouped',
                        help='Output format (default: grouped)')
    
    args = parser.parse_args()
    
    try:
        if args.format == 'grouped':
            sectors = get_sectors_grouped(args.file_path)
            print_sectors_grouped(sectors)
        else:
            sectors = get_sectors_flat(args.file_path)
            print_sectors_flat(sectors)
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
