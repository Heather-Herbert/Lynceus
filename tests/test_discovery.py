from src.discovery import discover_vscode_extensions, discover_npm_packages

def test_discover_vscode_extensions():
    assert isinstance(discover_vscode_extensions(), list)

def test_discover_npm_packages():
    assert isinstance(discover_npm_packages(), list)
