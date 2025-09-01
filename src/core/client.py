"""Evolution API Client with improved error handling and security"""
import requests
import time
from typing import Dict, Optional, Union
from config.settings import settings
from utils import setup_logger, sanitize_for_log, validate_phone_number
from exceptions import APIConnectionError, MessageSendError

class EvolutionAPIClient:
  """Improved Evolution API client with better error handling"""

  def __init__(self):
    self.base_url = settings.evolution_api_url
    self.instance_name = settings.instance_name
    self.api_key = settings.api_key
    self.logger = setup_logger(
      'evolution_client',
      settings.logs_dir / 'evolution_api.log',
      settings.log_level
    )

  def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, files: Optional[Dict] = None) -> Dict:
    """Make HTTP request with proper error handling"""
    url = f"{self.base_url}/{endpoint}"
    headers = {'apikey': self.api_key}

    if not files:
      headers['Content-Type'] = 'application/json'

    try:
      if method.upper() == 'POST':
        if files:
          response = requests.post(url, data=data, files=files, 
                                  headers={k: v for k, v in headers.items() if k != 'Content-Type'})
        else:
          response = requests.post(url, json=data, headers=headers)
      elif method.upper() == 'GET':
        response = requests.get(url, headers=headers)
      else:
        raise ValueError(f"Unsupported HTTP method: {method}")

      response.raise_for_status()
      return response.json()

    except requests.exceptions.ConnectionError as e:
      self.logger.error(f"Connection error: {sanitize_for_log(str(e))}")
      raise APIConnectionError(f"Failed to connect to Evolution API: {e}")
    except requests.exceptions.Timeout as e:
      self.logger.error(f"Timeout error: {sanitize_for_log(str(e))}")
      raise APIConnectionError(f"Request timeout: {e}")
    except requests.exceptions.HTTPError as e:
      self.logger.error(f"HTTP error: {sanitize_for_log(str(e))}")
      raise APIConnectionError(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
      self.logger.error(f"Request error: {sanitize_for_log(str(e))}")
      raise APIConnectionError(f"Request failed: {e}")

  def create_instance(self) -> bool:
    """Create WhatsApp instance"""
    self.logger.info(f"Creating instance: {sanitize_for_log(self.instance_name)}")

    data = {
      "instanceName": self.instance_name,
      "qrcode": True
    }

    try:
      result = self._make_request('POST', 'instance/create', data)
      if 'error' not in result:
        self.logger.info("Instance created successfully")
        return True
      elif 'already in use' in str(result).lower():
        self.logger.info("Instance already exists, checking connection status")
        return self.check_connection_status()
      else:
        self.logger.error(f"Error creating instance: {sanitize_for_log(str(result))}")
        return False
    except APIConnectionError:
      return False

  def get_qr_code(self) -> Optional[str]:
    """Get QR code for WhatsApp connection"""
    self.logger.info("Getting QR code...")

    try:
      result = self._make_request('GET', f'instance/connect/{self.instance_name}')
      return self._extract_qr_code(result)
    except APIConnectionError:
      return None

  def _extract_qr_code(self, result: Dict) -> Optional[str]:
    """Extract QR code from API response"""
    if 'qrcode' in result and result['qrcode']:
      if 'base64' in result['qrcode']:
        return result['qrcode']['base64']
      elif 'code' in result['qrcode']:
        return result['qrcode']['code']

    if 'base64' in result:
      return result['base64']
    elif 'code' in result:
      return result['code']

    self.logger.warning("Could not extract QR code from response")
    return None

  def check_connection_status(self) -> bool:
    """Check instance connection status"""
    try:
      result = self._make_request('GET', f'instance/connectionState/{self.instance_name}')

      if 'instance' in result:
        state = result['instance']['state']
        self.logger.info(f"Connection state: {sanitize_for_log(state)}")
        return state == 'open'

      return False
    except APIConnectionError:
      return False

  def _normalize_phone(self, phone: str) -> str:
    """Normalize phone number for API"""
    normalized_phone = validate_phone_number(phone)
    return normalized_phone.replace('+', '').replace('-', '').replace(' ', '')

  def send_text_message(self, phone: str, message: str) -> bool:
    """Send text message with validation"""
    try:
      clean_phone = self._normalize_phone(phone)

      data = {
          "number": clean_phone,
          "textMessage": {
              "text": message
          }
      }

      result = self._make_request('POST', f'message/sendText/{self.instance_name}', data)

      if 'error' not in result and 'key' in result:
        self.logger.info(f"Text message sent to {sanitize_for_log(phone)}")
        return True
      else:
        self.logger.error(f"Error sending text to {sanitize_for_log(phone)}: {sanitize_for_log(str(result))}")
        return False

    except (APIConnectionError, ValueError) as e:
      self.logger.error(f"Failed to send text message: {sanitize_for_log(str(e))}")
      raise MessageSendError(f"Failed to send text message: {e}")

  def send_image_message(self, phone: str, image_url: str, caption: str = "") -> bool:
    """Send image message using URL"""
    try:
      clean_phone = self._normalize_phone(phone)

      data = {
        "number": clean_phone,
        "mediaMessage": {
          "media": image_url,
          "mediatype": "image"
        }
      }

      if caption:
        data["mediaMessage"]["caption"] = caption

      result = self._make_request('POST', f'message/sendMedia/{self.instance_name}', data)

      if 'error' not in result and 'key' in result:
        self.logger.info(f"Image sent to {sanitize_for_log(phone)}")
        return True
      else:
        self.logger.error(f"Error sending image to {sanitize_for_log(phone)}: {sanitize_for_log(str(result))}")
        return False

    except (APIConnectionError, ValueError) as e:
      self.logger.error(f"Failed to send image message: {sanitize_for_log(str(e))}")
      raise MessageSendError(f"Failed to send image message: {e}")

  def wait_for_connection(self, timeout: int = 60) -> bool:
    """Wait for instance connection with exponential backoff"""
    self.logger.info("Waiting for WhatsApp connection...")

    start_time = time.time()
    sleep_time = 1

    while time.time() - start_time < timeout:
      if self.check_connection_status():
        self.logger.info("WhatsApp connected successfully")
        return True

      time.sleep(sleep_time)
      sleep_time = min(sleep_time * 1.5, 5)  # Exponential backoff, max 5 seconds

    self.logger.error("Timeout waiting for WhatsApp connection")
    return False