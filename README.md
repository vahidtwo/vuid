
# VUID  Package

[![Release](https://img.shields.io/github/v/release/vahidtwo/vuid)](https://img.shields.io/github/v/release/vahidtwo/vuid)
[![Build status](https://img.shields.io/github/actions/workflow/status/vahidtwo/vuid/main.yml?branch=master)](https://github.com/vahidtwo/vuid/actions/workflows/main.yml?query=branch%3Amaster)
[![Commit activity](https://img.shields.io/github/commit-activity/m/vahidtwo/vuid)](https://img.shields.io/github/commit-activity/m/vahidtwo/vuid)
[![License](https://img.shields.io/github/license/vahidtwo/vuid)](https://img.shields.io/github/license/vahidtwo/vuid)

The **VUID ** is a Python package designed to generate vahid unique identifiers (VUIDs) based on a custom epoch time
and a base-62 encoding scheme. The package provides a simple and efficient way to create unique IDs that can be used in
various applications, such as database keys, distributed systems, or any scenario where uniqueness is critical.

## Features

- **Custom Epoch Time**: The package uses a custom epoch time (`START_EPOC_TIME`) to ensure uniqueness and avoid
  collisions with other timestamp-based ID systems.
- **Base-62 Encoding**: Utilizes a base-62 encoding scheme (0-9, A-Z, a-z) to generate compact and human-readable IDs.
- **High Performance**: Capable of generating over 800,000 unique IDs per second, making it suitable for high-throughput
  systems.
- **Timestamp Extraction**: Allows extraction of the creation timestamp from a generated VUID.
- **Randomness**: Adds a 4-character random suffix to each ID to further ensure uniqueness.

## Installation

To install the package, use pip:

```bash
pip install vuid-generator
```

## Usage

### Generating a VUID

To generate a unique VUID, simply create an instance of the `VUID` class with a timestamp:

```python
from datetime import datetime
from vuid import VUID

# Generate a VUID using the current time
timestamp = datetime.now().timestamp()
vuid = VUID(timestamp)

print(vuid)  # Example output: "1A2b3C4d5"
```

### Extracting the Creation Time

You can extract the creation time of a VUID using the `created_time` property:

```python
creation_time = vuid.created_time
print(creation_time)  # Example output: "2025-01-04 12:04:08"
```

### Creating a VUID from an Existing Code

If you already have a VUID code, you can create a `VUID` object from it:

```python
existing_code = "1A2b3C4d5"
vuid = VUID.from_code(existing_code)

print(vuid)  # Output: "1A2b3C4d5"
```

### Comparing VUIDs

The `VUID` class supports comparison operations, allowing you to compare two VUIDs:

```python
vuid1 = VUID(datetime.now().timestamp())
vuid2 = VUID(datetime.now().timestamp())

print(vuid1 == vuid2)  # False
print(vuid1 < vuid2)  # True or False, depending on the timestamps
```

## API Reference

### `VUID(timestamp: float)`

- **Parameters**:
	- `timestamp`: A timestamp (in seconds) used to generate the VUID.
- **Returns**: A `VUID` object.

### `VUID.from_code(code: str)`

- **Parameters**:
	- `code`: An existing VUID code.
- **Returns**: A `VUID` object.

### Properties

- `code`: Returns the VUID as a string.
- `created_time`: Returns the creation time of the VUID as a `datetime` object.

### Methods

- `__str__()`: Returns the VUID as a string.
- `__repr__()`: Returns a formal representation of the VUID.
- `__eq__(other)`: Compares two VUIDs for equality.
- `__hash__()`: Returns the hash of the VUID.
- `__lt__(other)`, `__le__(other)`, `__gt__(other)`, `__ge__(other)`, `__ne__(other)`: Comparison methods for VUIDs.

## Performance

- The package is optimized for high performance, capable of generating over 800,000 unique IDs per second.
- Tested to generate 11,592,876 unique codes in 14.04 seconds.

## Limitations

- The current implementation supports IDs with a maximum length of 9 characters. If the timestamp exceeds the 5-character
  limit (after base-62 encoding), a warning will be logged.
- The package is designed to work until **January 15, 2054**, after which the timestamp encoding will overflow.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on
the [GitHub repository](https://github.com/your-repo/vuid-generator).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
