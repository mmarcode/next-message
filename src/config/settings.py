"""Centralized configuration management"""
import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings:
  """Application settings with validation and defaults"""

  def __init__(self):
    self._validate_required_env()

  @property
  def evolution_api_url(self) -> str:
    return os.getenv('EVOLUTION_API_URL', 'http://localhost:8080')

  @property
  def instance_name(self) -> str:
    return os.getenv('INSTANCE_NAME', 'whatsapp_new')

  @property
  def api_key(self) -> str:
    key = os.getenv('API_KEY')
    if not key:
      raise ValueError("API_KEY environment variable is required")
    return key

  @property
  def delay_between_messages(self) -> int:
    try:
      return int(os.getenv('DELAY_BETWEEN_MESSAGES', '2'))
    except ValueError:
      return 2

  @property
  def max_concurrent_messages(self) -> int:
    try:
      return int(os.getenv('MAX_CONCURRENT_MESSAGES', '5'))
    except ValueError:
      return 5

  @property
  def retry_attempts(self) -> int:
    try:
      return int(os.getenv('RETRY_ATTEMPTS', '3'))
    except ValueError:
      return 3

  @property
  def log_level(self) -> int:
    level = os.getenv('LOG_LEVEL', 'INFO').upper()
    return getattr(logging, level, logging.INFO)

  @property
  def logs_dir(self) -> Path:
    return Path('logs')

  def _validate_required_env(self) -> None:
    """Validate required environment variables"""
    required_vars = ['API_KEY']
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
      raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

# Global settings instance
settings = Settings()