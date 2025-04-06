"""
Command-line interface for quasipkg.
"""

import argparse
import sys

from quasipkg.core import QuasiPackageCreator


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Create dummy/placeholder packages for pacman',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  quasipkg --name cc --version 1.0 --description "Fake cc package" --provides cc
  quasipkg --name cmake --provides cmake --conflicts cmake --install
''')

    parser.add_argument('--name', required=True, help='Package name (required)')
    parser.add_argument('--pkgversion', default='1.0', help='Package version (default: 1.0)')
    parser.add_argument('--release', default='1', help='Package release number (default: 1)')
    parser.add_argument('--description', default='Dummy placeholder package',
                        help='Package description')
    parser.add_argument('--provides', help='Package names this dummy provides (comma-separated)')
    parser.add_argument('--conflicts', help='Package names this dummy conflicts with (comma-separated)')
    parser.add_argument('--arch', default='any', help='Package architecture (default: any)')
    parser.add_argument('--license', default='GPL', help='Package license (default: GPL)')
    parser.add_argument('--url', default='https://example.com', help='Package URL')
    parser.add_argument('--output-dir', help='Directory to create package in (default: ./NAME)')
    parser.add_argument('--install', action='store_true', help='Also install the package after building')
    parser.add_argument('--version', action='version',
                        version=f'%(prog)s {__import__("quasipkg").__version__}',
                        help='Show program version and exit')

    return parser.parse_args()


def main():
    """Main entry point for the command line"""
    try:
        args = parse_arguments()
        creator = QuasiPackageCreator(args)
        output_path = creator.create_pkgbuild()
        success = creator.build_package(output_path)

        if not success:
            sys.exit(1)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
