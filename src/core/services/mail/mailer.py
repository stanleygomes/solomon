import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from loguru import logger
from core.services.mail.config import MailConfig
from core.services.mail.message import MailMessage
from core.exceptions.PreconditionFailedError import PreconditionFailedError
from core.exceptions.ExternalServiceError import ExternalServiceError


class Mailer:
  """
  Manages sending emails.
  """

  def __init__(self, config: MailConfig):
    self.config = config

  def validateConfig(self) -> None:
    if not self.config.host or not self.config.username or not self.config.password:
      raise PreconditionFailedError("Mailer: Missing SMTP configuration")

  def _create_message(self, msg: MailMessage) -> MIMEMultipart:
    """
    Creates a structured MIME message from the MailMessage DTO.
    """

    message = MIMEMultipart()
    message["From"] = msg.sender
    message["To"] = msg.to
    message["Subject"] = msg.subject
    message.attach(MIMEText(msg.body, "html", "utf-8"))

    return message

  def _authenticate_and_send(
    self, server: smtplib.SMTP, message: MIMEMultipart
  ) -> None:
    """
    Authenticates with the SMTP server and sends the email message.
    """
    server.login(self.config.username, self.config.password)
    server.send_message(message)

  def _send_ssl(self, message: MIMEMultipart, context: ssl.SSLContext) -> None:
    """
    Sends the email using a direct SSL/TLS connection (port 465).
    """
    with smtplib.SMTP_SSL(
      self.config.host, self.config.port, context=context
    ) as server:
      self._authenticate_and_send(server, message)

  def _send_starttls(self, message: MIMEMultipart, context: ssl.SSLContext) -> None:
    """
    Sends the email using a STARTTLS connection (port 587).
    """
    with smtplib.SMTP(self.config.host, self.config.port) as server:
      if os.getenv("SMTP_USE_TLS", "true").lower() != "false":
        server.starttls(context=context)
      self._authenticate_and_send(server, message)

  def send(self, msg: MailMessage) -> None:
    self.validateConfig()

    message = self._create_message(msg)
    context = ssl.create_default_context()

    try:
      if self.config.port == 465:
        self._send_ssl(message, context)
      else:
        self._send_starttls(message, context)
      logger.debug(
        "📧 Email sent successfully to {} (Subject: {})", msg.to, msg.subject
      )
    except Exception as e:
      logger.error(
        "❌ Failed to send email to {}. Host: {}:{}, Error: {}",
        msg.to,
        self.config.host,
        self.config.port,
        e,
      )
      raise ExternalServiceError(f"Failed to send email to {msg.to}") from e
