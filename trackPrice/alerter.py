from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os


class alerter:
    def __init__(self, sender=None, email_address=os.environ.get("ALERTER_EMAIL_ADDRESS"), email_password=os.environ.get("ALERTER_EMAIL_PASSWORD"), smtp_address="smtp.gmail.com", smtp_port=587):
        if sender:
            self.sender = sender
        else:
            # set up the SMTP server
            s = smtplib.SMTP(host=smtp_address, port=smtp_port)
            s.starttls()
            s.login(email_address, email_password)
            self.sender = s

    def build_message(self, text, subject, subtype="plain"):
        msg = MIMEMultipart()
        msg['From'] = "jasaldanah@gmail.com"
        msg['Subject'] = subject
        msg.attach(MIMEText(text, subtype))
        return msg

    def send_email(self, msg, destination="jasaldanah@gmail.com"):
        successful = True
        if isinstance(destination, list):
            for destinatary in destination:
                msg['To'] = destinatary
                success = self.sender.send_message(msg)
                successful = successful and success
        else:
            msg['To'] = destination
            successful = self.sender.send_message(msg)
        return successful

    def alert(self, message_text="This is an alerter test", alert_type="TEST", destination="jasaldanah@gmail.com", times: int = 1):
        if times > 1:
            successful = True
            for i in range(times):
                msg = self.build_message(message_text, alert_type)
                success = self.send_email(msg, destination=destination)
                successful = successful and success
        else:
            msg = self.build_message(message_text, alert_type)
            successful = self.send_email(msg, destination=destination)
        return successful
