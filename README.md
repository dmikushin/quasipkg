# quasipkg

A utility to create dummy/placeholder packages for pacman.

## Description

`quasipkg` allows you to create empty packages that satisfy dependencies without installing the actual software. This is particularly useful in situations where:

- You need to satisfy a dependency but don't want the actual package
- You're developing in a containerized or isolated environment
- You're creating a minimal build environment and want to avoid large dependencies

## Installation

```bash
pip install quasipkg
```

Or install from source using Poetry:

```bash
git clone https://github.com/dmikushin/quasipkg.git
cd quasipkg
poetry install
```

## Usage

### Command-line Interface

```bash
# Create a basic dummy package
quasipkg --name cc --version 1.0 --description "Fake cc package" --provides cc

# Create and install a dummy package
quasipkg --name cmake --provides cmake --conflicts cmake --install

# Get help
quasipkg --help
```

### Command-line options

```
  --name NAME           Package name (required)
  --version VERSION     Package version (default: 1.0)
  --release RELEASE     Package release number (default: 1)
  --description DESC    Package description
  --provides PROVIDES   Package names this dummy provides (comma-separated)
  --conflicts CONFLICTS Package names this dummy conflicts with (comma-separated)
  --arch ARCH           Package architecture (default: any)
  --license LICENSE     Package license (default: GPL)
  --url URL             Package URL
  --output-dir DIR      Directory to create package in (default: ./NAME)
  --install             Also install the package after building
```

### Python API

You can also use `quasipkg` programmatically in your Python scripts:

```python
import quasipkg

# Create a basic dummy package
output_path, success = quasipkg.create_package(
    name="cc",
    version="1.0",
    description="Fake cc package",
    provides="cc"
)

# Create package with more options
output_path, success = quasipkg.create_package(
    name="cmake",
    version="3.20.0",
    description="Dummy cmake package",
    provides="cmake",
    conflicts="cmake",
    arch="x86_64",
    license="MIT",
    url="https://github.com/dmikushin/archrepo-docker",
    output_dir="/tmp/packages",
    install=True
)

if success:
    print(f"Package successfully created at {output_path}")
else:
    print("Failed to create package")
```

## Requirements

- Python 3.6+
- `makepkg` and `pacman` (typically available on Arch Linux and derivatives)

## Testing

This package includes a test suite to verify its functionality. You can run the tests using pytest:

```bash
# If you've installed with pip
pip install pytest
pytest

# If you're using Poetry
poetry install
poetry run pytest

# Run with verbosity for more details
poetry run pytest -v

# Run specific test file
poetry run pytest tests/test_quasipkg.py
```

The tests verify basic functionality including:
- Proper formatting of package arrays
- Creation of PKGBUILD files with correct content
- Package building process (mocked)
- Python API functionality

If you're contributing to this project, please ensure all tests pass before submitting pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
