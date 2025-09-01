"""Logging utilities with security improvements"""
import logging
import re
from pathlib import Path
from typing import Any

def sanitize_for_log(value: Any) -> str:
  """Sanitize input for safe logging to prevent log injection"""
  if value is None:
    return "None"

  # Convert to string and remove potentially dangerous characters
  sanitized = str(value)
  # Remove newlines, carriage returns, and other control characters
  sanitized = re.sub(r'[\r\n\t\x00-\x1f\x7f-\x9f]', '', sanitized)
  # Limit length to prevent log flooding
  if len(sanitized) > 200:
    sanitized = sanitized[:200] + "..."

  return sanitized

def setup_logger(name: str, log_file: Path, level: int = logging.INFO) -> logging.Logger:
  """Setup logger with file and console handlers"""
  # Ensure log directory exists
  log_file.parent.mkdir(parents=True, exist_ok=True)

  logger = logging.getLogger(name)
  logger.setLevel(level)

  # Clear existing handlers
  logger.handlers.clear()

  # File handler
  file_handler = logging.FileHandler(log_file)
  file_handler.setLevel(level)

  # Console handler
  console_handler = logging.StreamHandler()
  console_handler.setLevel(level)

  # Formatter
  formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
  )
  file_handler.setFormatter(formatter)
  console_handler.setFormatter(formatter)

  logger.addHandler(file_handler)
  logger.addHandler(console_handler)

  return logger