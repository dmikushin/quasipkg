"""
Tests for the public Python API.
"""

import tempfile
from pathlib import Path
from unittest import TestCase, mock

from quasipkg import create_package


class TestPublicAPI(TestCase):
    """Test the public Python API functions"""

    @mock.patch('subprocess.run')
    def test_create_package(self, mock_run):
        """Test the create_package function"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock package file to simulate successful build
            pkg_path = Path(tmpdir) / "test-api-pkg-2.0-1-x86_64.pkg.tar.zst"
            pkg_path.touch()

            # Use the public API to create a package
            output_path, success = create_package(
                name="test-api-pkg",
                version="2.0",
                description="API test package",
                arch="x86_64",
                output_dir=tmpdir
            )

            # Check that the function returned success
            self.assertTrue(success)

            # Check that the PKGBUILD file was created
            pkgbuild_path = Path(tmpdir) / "PKGBUILD"
            self.assertTrue(pkgbuild_path.exists())

            # Check the content of the PKGBUILD file
            with open(pkgbuild_path, 'r') as f:
                content = f.read()

                # Check that key elements are in the file
                self.assertIn("pkgname=test-api-pkg", content)
                self.assertIn("pkgver=2.0", content)
                self.assertIn('pkgdesc="API test package"', content)
                self.assertIn("arch=('x86_64')", content)

            # Check that subprocess.run was called to build the package
            mock_run.assert_called()

    @mock.patch('subprocess.run')
    def test_create_package_with_provides(self, mock_run):
        """Test the create_package function with provides option"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a mock package file to simulate successful build
            pkg_path = Path(tmpdir) / "dummy-pkg-1.0-1-any.pkg.tar.zst"
            pkg_path.touch()

            # Use the public API to create a package with provides
            output_path, success = create_package(
                name="dummy-pkg",
                provides="real-pkg,another-pkg",
                output_dir=tmpdir
            )

            # Check that the PKGBUILD file was created with correct provides
            pkgbuild_path = Path(tmpdir) / "PKGBUILD"
            with open(pkgbuild_path, 'r') as f:
                content = f.read()
                self.assertIn("provides=('real-pkg' 'another-pkg')", content)
