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
                                "type": "vscode-extension",
                            }
                        )
                except (json.JSONDecodeError, OSError):
                    continue
    return discovered


def discover_npm_packages(root_path="."):
    """
    Parses package-lock.json or package.json to identify dependencies.
    Scans the entire tree if package-lock.json is present.
    """
    root = Path(root_path)
    lock_file = root / "package-lock.json"
    pkg_file = root / "package.json"

    discovered = []

    if lock_file.exists():
        try:
            with open(lock_file, encoding="utf-8") as f:
                data = json.load(f)
                # v2/v3 lock files have 'packages' key with the full tree
                packages = data.get("packages", {})
                for pkg_path, pkg_info in packages.items():
                    if not pkg_path:  # Skip the root package itself
                        continue
                    name = pkg_info.get("name")
                    # In 'packages', the key often contains the name if it's
                    # a top-level node_modules entry
                    if not name:
                        name = pkg_path.split("node_modules/")[-1]

                    discovered.append(
                        {
                            "name": name,
                            "version": pkg_info.get("version"),
                            "path": str(root / pkg_path),
                            "type": "npm-package",
                        }
                    )
        except (json.JSONDecodeError, OSError):
            pass

    elif pkg_file.exists():
        # Fallback to just top-level if no lock file
        try:
            with open(pkg_file, encoding="utf-8") as f:
                data = json.load(f)
                deps = data.get("dependencies", {})
                dev_deps = data.get("devDependencies", {})
                for name, version in {**deps, **dev_deps}.items():
                    discovered.append(
                        {
                            "name": name,
                            "version": version,
                            "path": str(root / "node_modules" / name),
                            "type": "npm-package",
                        }
                    )
        except (json.JSONDecodeError, OSError):
            pass

    return discovered
