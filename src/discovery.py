import json
from pathlib import Path


def discover_vscode_extensions():
    """
    Locates and parses installed VS Code extensions.
    Currently supports default Linux path (~/.vscode/extensions).
    """
    extensions_dir = Path.home() / ".vscode" / "extensions"
    if not extensions_dir.exists():
        return []

    discovered = []
    for entry in extensions_dir.iterdir():
        if entry.is_dir():
            pkg_json_path = entry / "package.json"
            if pkg_json_path.exists():
                try:
                    with open(pkg_json_path, encoding="utf-8") as f:
                        data = json.load(f)
                        discovered.append(
                            {
                                "name": data.get("name"),
                                "version": data.get("version"),
                                "publisher": data.get("publisher"),
                                "path": str(entry),
                            }
                        )
                except (json.JSONDecodeError, OSError):
                    continue
    return discovered


def discover_npm_packages(path="."):
    """Parses package.json or package-lock.json for dependencies."""
    # TODO: Implement parsing logic
    return []
