import time
import jwt
from pathlib import Path
from loguru import logger
from core.database.setup import DatabaseSetup
from core.database.repositories.user import UserRepository
from core.database.repositories.magic_code import MagicCodeRepository
from core.database.repositories.blacklisted_token import BlacklistedTokenRepository
from core.services.auth.key_manager import KeyManager
from core.services.auth.jwt_manager import JwtManager
from core.services.mail.mailer import Mailer
from core.services.mail.message import MailMessage
from core.services.auth.dto import TokenPair
from core.utils.date import DateManager
from core.utils.security import SecurityManager
from core.utils.string import StringManager
from core.utils.disk import DiskManager
from core.utils.markdown import Markdown
from core.constants.themes import PREDEFINED_THEMES
from core.services.render.renderer import TemplateRenderer
from core.exceptions.PreconditionFailedError import PreconditionFailedError
from core.exceptions.UnauthorizedError import UnauthorizedError
from core.exceptions.AuthenticationError import AuthenticationError


class AuthService:
  """
  Service orchestrating Magic Code authentication and secure JWT issuing/validation using SQLite.
  """

  def __init__(
    self,
    db_manager: DatabaseSetup,
    mailer: Mailer,
    key_manager: KeyManager | None = None,
    keys_dir: Path | None = None,
    refresh_token_expiration: int = 604800,
    magic_code_expiration: int = 300,
    jwt_manager: JwtManager | None = None,
    jwt_algorithm: str = "RS256",
  ) -> None:
    self.db_manager = db_manager
    self.mailer = mailer
    self.key_manager = key_manager or KeyManager(keys_dir=keys_dir)
    self.refresh_token_expiration = refresh_token_expiration
    self.magic_code_expiration = magic_code_expiration
    self.jwt_manager = jwt_manager or JwtManager(jwt_algorithm)

    self.user_repo = UserRepository(self.db_manager)
    self.magic_code_repo = MagicCodeRepository(self.db_manager)
    self.blacklist_repo = BlacklistedTokenRepository(self.db_manager)

  def request_magic_code(self, email: str) -> None:
    """
    Generates a 6-digit magic code, stores it in the database, and emails it.
    """
    email = StringManager.clean_email(email)
    if not email:
      raise PreconditionFailedError("Email not provided")

    # Ensure user exists
    user = self.user_repo.find_by_email(email)
    if not user:
      raise AuthenticationError("User not found")

    code = SecurityManager.generate_numeric_code(6)
    expires_in_seconds = self.magic_code_expiration

    # Save magic code to database
    expires_at = DateManager.now_plus_seconds(expires_in_seconds)
    self.magic_code_repo.create(email, code, expires_at)

    # Render HTML email using Markdown template and theme
    template_path = DiskManager.resolve_path(__file__, "templates", "magic_code.md")
    template_content = DiskManager.read_text(template_path)
    expires_in_minutes = expires_in_seconds // 60

    rendered_markdown = TemplateRenderer.render_text(
      template_content, {"code": code, "expires_in_minutes": expires_in_minutes}
    )
    html_content = Markdown.to_html(rendered_markdown)

    today = DateManager.today_str()
    render_context = {
      "title": "Your Solomon Access Code",
      "date": today,
      "content": html_content,
      "use_case": "auth",
    }
    theme = PREDEFINED_THEMES["noemi"]
    html_body = TemplateRenderer.render_html(theme, render_context)

    # Send magic code email
    mail_message = MailMessage(
      sender=self.mailer.config.email_from,
      to=email,
      subject="Your Solomon Access Code",
      body=html_body,
    )
    self.mailer.send(mail_message)

  def verify_magic_code(self, email: str, code: str) -> None:
    """
    Verifies a magic code from the database and handles rate limiting.
    """
    email = StringManager.clean_email(email)
    code = code.strip()

    record = self.magic_code_repo.find_latest(email)
    if not record or DateManager.is_expired(record.expires_at):
      raise AuthenticationError("Expired or invalid code")

    if record.attempts >= 5:
      self.magic_code_repo.delete_by_email(email)
      raise AuthenticationError("Maximum attempts exceeded for this code")

    if record.code == code:
      self.magic_code_repo.delete_by_email(email)
    else:
      self.magic_code_repo.increment_attempts(str(record.id))
      raise AuthenticationError("Incorrect verification code")

  def issue_tokens(self, email: str, client_type: str = "user") -> TokenPair:
    """
    Issues a new Access Token and Refresh Token for a verified user.
    """
    user = self.user_repo.find_by_email(email)
    if not user:
      raise AuthenticationError("User not found")

    user_id = str(user.id)
    private_key = self.key_manager.get_private_key()
    now_ts = int(time.time())

    # Access Token (15 mins duration)
    access_payload = {
      "sub": user_id,
      "email": email,
      "type": client_type,
      "exp": now_ts + 900,
      "scopes": ["access"],
    }
    access_token = self.jwt_manager.encode(access_payload, private_key)

    # Refresh Token
    refresh_payload = {
      "sub": user_id,
      "email": email,
      "type": client_type,
      "exp": now_ts + self.refresh_token_expiration,
      "scopes": ["refresh"],
    }
    refresh_token = self.jwt_manager.encode(refresh_payload, private_key)

    return TokenPair(access_token=access_token, refresh_token=refresh_token)

  def validate_access_token(self, token: str) -> dict:
    """
    Decodes and validates a JWT access token, checking the SQLite blacklist.
    """
    public_key = self.key_manager.get_public_key()

    # Blacklist check
    if self.blacklist_repo.is_blacklisted(token):
      raise UnauthorizedError("Invalid or revoked token")

    try:
      payload = self.jwt_manager.decode(token, public_key)
      if "access" not in payload.get("scopes", []):
        raise UnauthorizedError("Invalid token scope")
      return payload
    except jwt.ExpiredSignatureError as e:
      raise UnauthorizedError("Expired token") from e
    except jwt.InvalidTokenError as e:
      raise UnauthorizedError("Invalid token") from e

  def blacklist_token(self, token: str) -> None:
    """
    Blacklists a token (Access or Refresh) to revoke active sessions.
    """
    public_key = self.key_manager.get_public_key()
    try:
      # Decode without verification to read expiration if invalid, or verify
      payload = self.jwt_manager.decode(token, public_key)
      exp = payload.get("exp")
      if not exp:
        return

      expires_in = int(exp - time.time())
      if expires_in > 0:
        expires_at_iso = DateManager.now_plus_seconds(expires_in)
        self.blacklist_repo.blacklist(token, expires_at_iso)
    except Exception as e:
      logger.warning("Failed to parse and blacklist token: {}", e)

  def refresh_tokens(self, refresh_token: str) -> TokenPair:
    """
    Validates a refresh token and generates a new token pair, blacklisting the old refresh token.
    """
    public_key = self.key_manager.get_public_key()

    # Blacklist check
    if self.blacklist_repo.is_blacklisted(refresh_token):
      raise UnauthorizedError("Revoked refresh token")

    try:
      payload = self.jwt_manager.decode(refresh_token, public_key)
      if "refresh" not in payload.get("scopes", []):
        raise UnauthorizedError("Invalid token scope")

      email = payload.get("email")
      client_type = payload.get("type", "user")

      # Revoke current refresh token
      self.blacklist_token(refresh_token)

      # Generate new pair
      return self.issue_tokens(email, client_type)
    except jwt.ExpiredSignatureError as e:
      raise UnauthorizedError("Expired refresh token") from e
    except jwt.InvalidTokenError as e:
      raise UnauthorizedError("Invalid refresh token") from e
