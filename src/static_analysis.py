import subprocess
import json
import os


def run_semgrep_scan(target_path):
    """
    Runs a Semgrep scan on the target path using default security rules.
    Returns a dictionary with scan results.
    """
    if not os.path.exists(target_path):
        return {"status": "error", "message": f"Path not found: {target_path}"}

    try:
        # Run semgrep with the 'p/security-audit' and 'p/secrets' rulesets
        # We use --json to get machine-readable output
        result = subprocess.run(
            [
                "semgrep",
                "scan",
                "--config",
                "p/security-audit",
                "--config",
                "p/secrets",
                "--json",
                "--quiet",
                target_path,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode not in [0, 1]:  # Semgrep returns 1 if findings exist
            return {
                "status": "error",
                "message": f"Semgrep failed with code {result.returncode}",
                "stderr": result.stderr,
            }

        scan_data = json.loads(result.stdout)
        findings = scan_data.get("results", [])

        return {
            "status": "success",
            "findings_count": len(findings),
            "findings": [
                {
                    "check_id": f.get("check_id"),
                    "path": f.get("path"),
                    "line": f.get("start", {}).get("line"),
                    "message": f.get("extra", {}).get("message"),
                    "severity": f.get("extra", {}).get("severity"),
                }
                for f in findings
            ],
        }

    except (subprocess.SubprocessError, json.JSONDecodeError, OSError) as e:
        return {"status": "error", "message": str(e)}
