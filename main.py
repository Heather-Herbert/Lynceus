import os
from dotenv import load_dotenv
from src.discovery import discover_vscode_extensions, discover_npm_packages
from src.scanner import local_av_scan, virustotal_scan
from src.notifier import EmailNotifier

def main():
    load_dotenv()
    print("Lynceus - The Eyes of the Argonauts")
    
    # Discovery phase
    extensions = discover_vscode_extensions()
    packages = discover_npm_packages()
    
    # Scan phase
    # (Example loop)
    for item in extensions + packages:
        result = local_av_scan(item)
        if result["status"] == "suspicious":
            vt_result = virustotal_scan(item, os.getenv("VT_API_KEY"))
            # Notify if confirmed
            pass

    print("Scan complete.")

if __name__ == "__main__":
    main()
