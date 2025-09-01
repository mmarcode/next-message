"""Custom exceptions for Next Message application"""

class NextMessageError(Exception):
  """Base exception for Next Message application"""
  pass

class APIConnectionError(NextMessageError):
  """Raised when API connection fails"""
  pass

class MessageSendError(NextMessageError):
  """Raised when message sending fails"""
  pass

class ConfigurationError(NextMessageError):
  """Raised when configuration is invalid"""
  pass

class ValidationError(NextMessageError):
  """Raised when data validation fails"""
  pass