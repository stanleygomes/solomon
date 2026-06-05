from dataclasses import dataclass


@dataclass(frozen=True)
class MailMessage:
  """
  Data Transfer Object representing an email message to be sent.
  """

  sender: str
  to: str
  subject: str
  body: str
