class EmailNotifier:
    def __init__(self, host, port, user, password, sender):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.sender = sender

    def send_alert(self, recipient, subject, body):
        """Sends an email alert via SMTP."""
        # TODO: Implement SMTP sending logic
        print(f"Alert: {subject} to {recipient}")
        return True
