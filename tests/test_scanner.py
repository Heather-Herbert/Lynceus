from src.scanner import local_av_scan, virustotal_scan

def test_local_av_scan():
    result = local_av_scan("test_file")
    assert "status" in result
    assert result["status"] == "clean"

def test_virustotal_scan():
    result = virustotal_scan("test_file", "fake_key")
    assert "status" in result
    assert result["status"] == "unknown"
