#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the block_zs_reader module
"""

import sys
import os
from block_zs_reader import validate_file, get_sectors_grouped, get_sectors_flat


def test_validate_file():
    """
    Test the validate_file function
    """
    print("Testing validate_file function...")
    
    # Test with non-existent file
    try:
        validate_file("non_existent_file.dat")
        print("FAIL: Should have raised FileNotFoundError")
    except FileNotFoundError as e:
        print(f"PASS: FileNotFoundError raised as expected: {e}")
    
    # Test with empty path
    try:
        validate_file("")
        print("FAIL: Should have raised ValueError")
    except ValueError as e:
        print(f"PASS: ValueError raised as expected: {e}")
    
    # Test with this script file (should pass)
    try:
        validate_file(__file__)
        print("PASS: Valid file passed validation")
    except Exception as e:
        print(f"FAIL: Unexpected error: {e}")
    
    print("\n")


def test_imports():
    """
    Test that all imports work correctly
    """
    print("Testing imports...")
    
    try:
        from pytdx.reader.block_reader import BlockReader
        print("PASS: BlockReader imported successfully")
    except Exception as e:
        print(f"FAIL: Error importing BlockReader: {e}")
    
    print("\n")


def main():
    """
    Run all tests
    """
    print("Running tests for block_zs_reader module...")
    print("-" * 80)
    
    test_imports()
    test_validate_file()
    
    print("All tests completed!")


if __name__ == "__main__":
    main()
