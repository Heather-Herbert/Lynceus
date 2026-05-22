import json
from unittest.mock import MagicMock, patch
from pathlib import Path
from src.discovery import discover_vscode_extensions, discover_npm_packages


def test_discover_vscode_extensions_success():
    """Tests successful discovery of VS Code extensions."""
    with patch("src.discovery.Path") as mock_path_class:
        mock_home = MagicMock()
        mock_path_class.home.return_value = mock_home

        mock_extensions_dir = MagicMock()
        mock_home.__truediv__.return_value = mock_extensions_dir
        mock_extensions_dir.__truediv__.return_value = mock_extensions_dir
        mock_extensions_dir.exists.return_value = True

        mock_extension = MagicMock()
        mock_extension.is_dir.return_value = True
        mock_extension.__str__.return_value = "/mock/path"

        mock_pkg_json = MagicMock()
        mock_extension.__truediv__.return_value = mock_pkg_json
        mock_pkg_json.exists.return_value = True

        mock_extensions_dir.iterdir.return_value = [mock_extension]

        with (
            patch("builtins.open", MagicMock()),
            patch(
                "json.load",
                return_value={"name": "test", "version": "1.0", "publisher": "me"},
            ),
        ):
            extensions = discover_vscode_extensions()
            assert len(extensions) == 1
            assert extensions[0]["name"] == "test"
            assert extensions[0]["type"] == "vscode-extension"


def test_discover_vscode_extensions_no_dir():
    """Tests behavior when the extensions directory does not exist."""
    with patch("src.discovery.Path") as mock_path_class:
        mock_home = MagicMock()
        mock_path_class.home.return_value = mock_home
        mock_dir = MagicMock()
        mock_home.__truediv__.return_value = mock_dir
        mock_dir.__truediv__.return_value = mock_dir
        mock_dir.exists.return_value = False

        extensions = discover_vscode_extensions()
        assert not extensions


def test_discover_vscode_extensions_error_handling():
    """Tests error handling during extension discovery."""
    with patch("src.discovery.Path") as mock_path_class:
        mock_home = MagicMock()
        mock_path_class.home.return_value = mock_home
        mock_extensions_dir = MagicMock()
        mock_home.__truediv__.return_value = mock_extensions_dir
        mock_extensions_dir.__truediv__.return_value = mock_extensions_dir
        mock_extensions_dir.exists.return_value = True

        mock_extension = MagicMock()
        mock_extension.is_dir.return_value = True
        mock_pkg_json = MagicMock()
        mock_extension.__truediv__.return_value = mock_pkg_json
        mock_pkg_json.exists.return_value = True

        mock_extensions_dir.iterdir.return_value = [mock_extension]

        # Test JSON error
        with (
            patch("builtins.open", MagicMock()),
            patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)),
        ):
            extensions = discover_vscode_extensions()
            assert not extensions

        # Test OS error
        with patch("builtins.open", side_effect=OSError()):
            extensions = discover_vscode_extensions()
            assert not extensions


def test_discover_npm_packages_lockfile():
    """Tests NPM discovery using package-lock.json."""
    mock_root = MagicMock(spec=Path)
    mock_lock = MagicMock(spec=Path)
    mock_pkg = MagicMock(spec=Path)

    mock_root.__truediv__.side_effect = lambda p: (
        mock_lock if p == "package-lock.json" else mock_pkg
    )
    mock_lock.exists.return_value = True

    lock_data = {
        "packages": {
            "": {"name": "root-pkg"},
            "node_modules/lodash": {"version": "4.17.21"},
            "node_modules/request": {"name": "req-pkg", "version": "2.88.2"},
        }
    }

    with (
        patch("src.discovery.Path", return_value=mock_root),
        patch("builtins.open", MagicMock()),
        patch("json.load", return_value=lock_data),
    ):
        packages = discover_npm_packages()
        assert len(packages) == 2
        names = [p["name"] for p in packages]
        assert "lodash" in names
        assert "req-pkg" in names
        assert all(p["type"] == "npm-package" for p in packages)


def test_discover_npm_packages_pkg_only():
    """Tests NPM discovery using package.json only."""
    mock_root = MagicMock(spec=Path)
    mock_lock = MagicMock(spec=Path)
    mock_pkg = MagicMock(spec=Path)

    # Use a mock for the root that returns different mocks for different paths
    def truediv_side_effect(name):
        if name == "package-lock.json":
            return mock_lock
        if name == "package.json":
            return mock_pkg
        return MagicMock(spec=Path)

    mock_root.__truediv__.side_effect = truediv_side_effect
    mock_lock.exists.return_value = False
    mock_pkg.exists.return_value = True

    pkg_data = {
        "dependencies": {"express": "^4.17.1"},
        "devDependencies": {"jest": "^26.6.3"},
    }

    with (
        patch("src.discovery.Path", return_value=mock_root),
        patch("builtins.open", MagicMock()),
        patch("json.load", return_value=pkg_data),
    ):
        packages = discover_npm_packages()
        assert len(packages) == 2
        names = [p["name"] for p in packages]
        assert "express" in names
        assert "jest" in names


def test_discover_npm_packages_none():
    """Tests behavior when no NPM files exist."""
    mock_root = MagicMock(spec=Path)
    mock_root.__truediv__.return_value.exists.return_value = False

    with patch("src.discovery.Path", return_value=mock_root):
        packages = discover_npm_packages()
        assert not packages


def test_discover_npm_packages_error_handling():
    """Tests error handling for NPM discovery."""
    mock_root = MagicMock(spec=Path)
    mock_lock = MagicMock(spec=Path)
    mock_root.__truediv__.return_value = mock_lock
    mock_lock.exists.return_value = True

    # JSON error in lock file
    with (
        patch("src.discovery.Path", return_value=mock_root),
        patch("builtins.open", MagicMock()),
        patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)),
    ):
        assert not discover_npm_packages()

    # JSON error in package.json
    mock_lock.exists.return_value = False
    mock_pkg = MagicMock(spec=Path)
    mock_pkg.exists.return_value = True
    mock_root.__truediv__.side_effect = lambda p: (
        mock_pkg if p == "package.json" else mock_lock
    )

    with (
        patch("src.discovery.Path", return_value=mock_root),
        patch("builtins.open", MagicMock()),
        patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)),
    ):
        assert not discover_npm_packages()
