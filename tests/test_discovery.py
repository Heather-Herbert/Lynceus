import json
from unittest.mock import MagicMock, patch
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
            assert extensions[0]["path"] == "/mock/path"


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


def test_discover_npm_packages():
    """Stub test for npm package discovery."""
    assert isinstance(discover_npm_packages(), list)
