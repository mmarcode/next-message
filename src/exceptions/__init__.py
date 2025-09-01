"""Custom exceptions for Next Message"""
from .custom_exceptions import (
  NextMessageError,
  APIConnectionError,
  MessageSendError,
  ConfigurationError,
  ValidationError
)

__all__ = [
  'NextMessageError',
  'APIConnectionError', 
  'MessageSendError',
  'ConfigurationError',
  'ValidationError'
]