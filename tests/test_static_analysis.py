import json
from unittest.mock import patch, MagicMock
from src.static_analysis import run_semgrep_scan


def test_run_semgrep_scan_success():
    """Tests successful semgrep scan with findings."""
    mock_output = {
        "results": [
            {
                "check_id": "rules.security.dangerous-sink",
                "path": "test.js",
                "start": {"line": 10},
                "extra": {"message": "Dangerous sink found", "severity": "ERROR"},
            }
        ]
    }

    with (
        patch("os.path.exists", return_value=True),
        patch("subprocess.run") as mock_run,
    ):
        mock_run.return_value = MagicMock(
            returncode=0, stdout=json.dumps(mock_output), stderr=""
        )

        result = run_semgrep_scan("some/path")
        assert result["status"] == "success"
        assert result["findings_count"] == 1
        assert result["findings"][0]["check_id"] == "rules.security.dangerous-sink"


def test_run_semgrep_scan_no_path():
    """Tests behavior when target path does not exist."""
    with patch("os.path.exists", return_value=False):
        result = run_semgrep_scan("non/existent/path")
        assert result["status"] == "error"
        assert "Path not found" in result["message"]


def test_run_semgrep_scan_failure():
    """Tests behavior when semgrep command fails."""
    with (
        patch("os.path.exists", return_value=True),
        patch("subprocess.run") as mock_run,
    ):
        mock_run.return_value = MagicMock(
            returncode=2, stdout="", stderr="Binary not found"
        )

        result = run_semgrep_scan("some/path")
        assert result["status"] == "error"
        assert "Semgrep failed" in result["message"]


def test_run_semgrep_scan_exception():
    """Tests error handling during subprocess execution."""
    with (
        patch("os.path.exists", return_value=True),
        patch("subprocess.run", side_effect=OSError("OS error")),
    ):
        result = run_semgrep_scan("some/path")
        assert result["status"] == "error"
        assert "OS error" in result["message"]


def test_run_semgrep_scan_json_error():
    """Tests error handling for malformed JSON output."""
    with (
        patch("os.path.exists", return_value=True),
        patch("subprocess.run") as mock_run,
    ):
        mock_run.return_value = MagicMock(
            returncode=0, stdout="invalid json", stderr=""
        )

        result = run_semgrep_scan("some/path")
        assert result["status"] == "error"
