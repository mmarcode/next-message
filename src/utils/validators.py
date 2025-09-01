"""Input validation utilities"""
import re
from exceptions import ValidationError

def validate_phone_number(phone: str) -> str:
  """Validate and normalize phone number"""
  if not phone:
    raise ValidationError("Phone number cannot be empty")

  # Remove all non-digit characters except +
  normalized = re.sub(r'[^\d+]', '', phone)

  # Add + if missing and number looks like international format
  if not normalized.startswith('+') and len(normalized) >= 10:
    # If it starts with common country codes, add +
    if normalized.startswith(('52', '1', '34', '44', '49', '33', '39', '81', '86')):
      normalized = '+' + normalized
    else:
      raise ValidationError(f"Invalid phone number format: {phone}. Must include country code with +")

  # Check if it starts with + and has at least 10 digits
  if not re.match(r'^\+\d{10,15}$', normalized):
    raise ValidationError(f"Invalid phone number format: {phone}. Use format: +525512345678")

  return normalized

def validate_message_type(message_type: str) -> str:
  """Validate message type"""
  from constants import MESSAGE_TYPES
  if message_type.lower() not in MESSAGE_TYPES:
    raise ValidationError(f"Invalid message type: {message_type}. Must be one of: {MESSAGE_TYPES}")

  return message_type.lower()

