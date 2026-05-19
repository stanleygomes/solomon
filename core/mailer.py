import smtplib
import ssl
import os
from dataclasses import dataclass
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from dotenv import load_dotenv

@dataclass
class MailConfig:
    host: str
    port: int
    username: str
    password: str

@dataclass
class MailMessage:
    sender: str
    to: str
    subject: str
    body: str

class Mailer:
    def __init__(self, config: MailConfig):
        self.config = config

    @staticmethod
    def from_env() -> 'Mailer':
        load_dotenv()
        host = os.getenv("SMTP_HOST", "")
        port_str = os.getenv("SMTP_PORT", "587")
        user = os.getenv("SMTP_USER", "")
        password = os.getenv("SMTP_PASSWORD", "")
        
        return Mailer(MailConfig(
            host=host,
            port=int(port_str),
            username=user,
            password=password
        ))

    def send(self, msg: MailMessage) -> None:
        if not self.config.host or not self.config.username or not self.config.password:
            raise ValueError("Mailer: Missing SMTP configuration")

        # Create MIME message
        message = MIMEMultipart()
        message["From"] = msg.sender
        message["To"] = msg.to
        message["Subject"] = msg.subject
        message.attach(MIMEText(msg.body, "html", "utf-8"))

        context = ssl.create_default_context()

        if self.config.port == 465:
            # SSL/TLS Direct Connection
            with smtplib.SMTP_SSL(self.config.host, self.config.port, context=context) as server:
                server.login(self.config.username, self.config.password)
                server.send_message(message)
        else:
            # STARTTLS Standard Connection (Port 587)
            with smtplib.SMTP(self.config.host, self.config.port) as server:
                if os.getenv("SMTP_USE_TLS", "true").lower() != "false":
                    server.starttls(context=context)
                server.login(self.config.username, self.config.password)
                server.send_message(message)
