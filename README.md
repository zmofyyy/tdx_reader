# Industry Sector Data Reader for pytdx

This project provides a comprehensive solution for reading and parsing industry sector data from the `block_zs.dat` file using the pytdx library's `BlockReader` module.

## Features

- **File Validation**: Checks for file existence, read permissions, and data integrity
- **Multiple Output Formats**: Supports both grouped and flat output formats
- **Error Handling**: Gracefully handles various error scenarios
- **Command-Line Interface**: Easy to use from the command line
- **Programmatic API**: Can be imported and used as a module in other Python scripts

## Requirements

- Python 3.6+
- pytdx library
- pandas (optional, for DataFrame output)

## Installation

1. Install the pytdx library:
   ```bash
   pip install pytdx
   ```

2. Clone or download this repository to your local machine.

## Usage

### Command-Line Interface

```bash
# Read and display sectors in grouped format (default)
python block_zs_reader.py "D:\tdx_new\T0002\hq_cache\block_zs.dat"

# Read and display sectors in flat format
python block_zs_reader.py "D:\tdx_new\T0002\hq_cache\block_zs.dat" --format flat
```

### Programmatic API

```python
from block_zs_reader import get_sectors_grouped, get_sectors_flat

# Get sectors in grouped format
file_path = "D:\tdx_new\T0002\hq_cache\block_zs.dat"
sectors = get_sectors_grouped(file_path)

# Access sector information
for sector_name, sector_info in sectors.items():
    print(f"Sector: {sector_name}")
    print(f"Type: {sector_info['type']}")
    print(f"Stock Count: {sector_info['stock_count']}")
    print(f"Stocks: {sector_info['stocks']}")

# Get sectors in flat format
flat_sectors = get_sectors_flat(file_path)
```

## Output Formats

### Grouped Format

The grouped format returns a dictionary where each key is a sector name, and the value is a dictionary containing:
- `type`: The sector type
- `stock_count`: The number of stocks in the sector
- `stocks`: A list of stock codes in the sector

### Flat Format

The flat format returns a list of dictionaries, each containing:
- `blockname`: The sector name
- `block_type`: The sector type
- `code_index`: The index of the stock within the sector
- `code`: The stock code

## Error Handling

The code includes comprehensive error handling for:
- File not found
- Permission denied
- Empty file path
- General file reading errors

## File Format

The `block_zs.dat` file is a binary file used by the TDX (通达信) software to store industry sector information. The format is parsed by the `BlockReader` class from the pytdx library.

## Testing

Run the test script to verify the implementation:

```bash
python test_block_reader.py
```

## License

This project is open-source and available under the MIT License.
