from src.notifier import EmailNotifier

def test_email_notifier_init():
    notifier = EmailNotifier("host", 587, "user", "pass", "sender")
    assert notifier.host == "host"
    assert notifier.sender == "sender"

def test_send_alert():
    notifier = EmailNotifier("host", 587, "user", "pass", "sender")
    assert notifier.send_alert("recipient", "subject", "body") is True
