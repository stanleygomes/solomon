from pathlib import Path
from loguru import logger
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from core.utils.disk import DiskUtils


class KeyManager:
  """
  Manages loading and automatic generation of RS256 asymmetric keys.
  """

  def __init__(self, keys_dir: Path | None = None) -> None:
    if keys_dir is None:
      # Default to storage/keys relative to project root
      keys_dir = DiskUtils.resolve_path(
        __file__, "..", "..", "..", "..", "storage", "keys"
      )

    self.keys_dir = keys_dir
    self.private_key_path = self.keys_dir / "private_key.pem"
    self.public_key_path = self.keys_dir / "public_key.pem"

    DiskUtils.ensure_directory(self.keys_dir)
    self._ensure_keys_exist()

  def _ensure_keys_exist(self) -> None:
    """
    Generates a new RSA 2048 key pair if they do not already exist on disk.
    """
    if not DiskUtils.exists(self.private_key_path) or not DiskUtils.exists(
      self.public_key_path
    ):
      logger.info("🔑 Keys not found. Generating new RSA 2048 key pair...")

      private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
      )

      # Serialize private key
      private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
      )

      # Serialize public key
      public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
      )

      # Write to files
      DiskUtils.write_bytes(self.private_key_path, private_pem)
      DiskUtils.write_bytes(self.public_key_path, public_pem)
      logger.info("✅ RSA 2048 key pair generated successfully at {}", self.keys_dir)

  def get_private_key(self) -> str:
    """
    Returns the private key PEM string.
    """
    return DiskUtils.read_text(self.private_key_path)

  def get_public_key(self) -> str:
    """
    Returns the public key PEM string.
    """
    return DiskUtils.read_text(self.public_key_path)
