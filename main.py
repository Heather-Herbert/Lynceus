import os
from dotenv import load_dotenv
from src.discovery import discover_vscode_extensions, discover_npm_packages
from src.scanner import local_av_scan, virustotal_scan
from src.static_analysis import run_semgrep_scan


def main():
    """Main entry point for Lynceus."""
    load_dotenv()
    print("Lynceus - The Eyes of the Argonauts")

    # Discovery phase
    extensions = discover_vscode_extensions()
    packages = discover_npm_packages()

    # Scan phase
    for item in extensions + packages:
        path = item.get("path")
        if not path or not os.path.exists(path):
            continue

        print(f"Analyzing: {item.get('name')} ({item.get('type')})")

        # 1. Static Analysis (Semgrep)
        _sa_result = run_semgrep_scan(path)

        # 2. Local AV Scan
        result = local_av_scan(path)

        # 3. Escalation to VirusTotal
        if result["status"] == "suspicious":
            _vt_result = virustotal_scan(path, os.getenv("VT_API_KEY"))
            # Notify if confirmed

    print("Scan complete.")


if __name__ == "__main__":
    main()
