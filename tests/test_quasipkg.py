"""
Basic tests for quasipkg functionality.
"""

import os
import tempfile
from pathlib import Path
from unittest import TestCase, mock

from quasipkg.core import QuasiPackageCreator


class MockArgs:
    """Mock arguments for testing"""
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', 'test-pkg')
        self.pkgversion = kwargs.get('pkgversion', '1.0')
        self.release = kwargs.get('release', '1')
        self.description = kwargs.get('description', 'Test package')
        self.provides = kwargs.get('provides', None)
        self.conflicts = kwargs.get('conflicts', None)
        self.arch = kwargs.get('arch', 'any')
        self.license = kwargs.get('license', 'GPL')
        self.url = kwargs.get('url', 'https://example.com')
        self.output_dir = kwargs.get('output_dir', None)
        self.install = kwargs.get('install', False)


class TestQuasiPackageCreator(TestCase):
    """Test the QuasiPackageCreator class"""

    def test_format_array(self):
        """Test the _format_array method"""
        creator = QuasiPackageCreator(MockArgs())

        # Test with empty string
        self.assertEqual(creator._format_array(""), "")

        # Test with single item
        self.assertEqual(creator._format_array("item1"), "'item1'")

        # Test with multiple items
        self.assertEqual(
            creator._format_array("item1,item2,item3"),
            "'item1' 'item2' 'item3'"
        )

        # Test with whitespace
        self.assertEqual(
            creator._format_array(" item1 , item2 "),
            "'item1' 'item2'"
        )

    def test_create_pkgbuild(self):
        """Test creating a PKGBUILD file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Set up mock arguments with the temp dir as output
            args = MockArgs(
                name="test-pkg",
                pkgversion="2.0",
                description="Test dummy package",
                provides="test-pkg,another-pkg",
                output_dir=tmpdir
            )

            creator = QuasiPackageCreator(args)
            output_path = creator.create_pkgbuild()

            # Check that the PKGBUILD file was created
            pkgbuild_path = Path(tmpdir) / "PKGBUILD"
            self.assertTrue(pkgbuild_path.exists())

            # Check the content of the PKGBUILD file
            with open(pkgbuild_path, 'r') as f:
                content = f.read()

                # Check that key elements are in the file
                self.assertIn("pkgname=test-pkg", content)
                self.assertIn("pkgver=2.0", content)
                self.assertIn('pkgdesc="Test dummy package"', content)
                self.assertIn("provides=('test-pkg' 'another-pkg')", content)

    @mock.patch('subprocess.run')
    def test_build_package(self, mock_run):
        """Test building a package with mocked subprocess calls"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock package file to simulate successful build
            pkg_path = Path(tmpdir) / "test-pkg-1.0-1-any.pkg.tar.zst"
            pkg_path.touch()

            # Set up mock arguments
            args = MockArgs(output_dir=tmpdir)
            creator = QuasiPackageCreator(args)

            # Test build without install
            success = creator.build_package(Path(tmpdir))
            self.assertTrue(success)

            # Test build with install
            args.install = True
            creator = QuasiPackageCreator(args)
            success = creator.build_package(Path(tmpdir))
            self.assertTrue(success)

            # Check that subprocess.run was called correctly
            mock_run.assert_called()
