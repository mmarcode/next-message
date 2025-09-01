"""Message sender with improved error handling and performance"""
import pandas as pd
import asyncio
import time
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional
from config.settings import settings
from utils import setup_logger, sanitize_for_log, validate_phone_number, validate_message_type
from exceptions import ValidationError, MessageSendError, APIConnectionError
from constants import MAX_IMAGE_SIZE, ALLOWED_IMAGE_EXTENSIONS, RETRY_DELAY, REQUIRED_CSV_COLUMNS
from .client import EvolutionAPIClient

class MessageSender:
  """Improved message sender with better error handling and performance"""

  def __init__(self):
    self.client = EvolutionAPIClient()
    self.logger = setup_logger(
      'message_sender',
      settings.logs_dir / 'message_sender.log',
      settings.log_level
    )

  def load_contacts(self, file_path: str = 'contacts/contacts.csv') -> pd.DataFrame:
    """Load contacts from CSV with proper error handling"""
    try:
      if not Path(file_path).exists():
        raise FileNotFoundError(f"Contacts file not found: {file_path}")

      df = pd.read_csv(file_path)

      if df.empty:
        raise ValidationError("Contacts file is empty")

      required_columns = REQUIRED_CSV_COLUMNS
      missing_columns = [col for col in required_columns if col not in df.columns]
      if missing_columns:
        raise ValidationError(f"Missing required columns: {missing_columns}")

      # Add caption column if not present
      if 'caption' not in df.columns:
        df['caption'] = ''

      # Fill NaN values in caption with empty string
      df['caption'] = df['caption'].fillna('')

      self.logger.info(f"Loaded {len(df)} contacts from {sanitize_for_log(file_path)}")
      return df

    except FileNotFoundError as e:
      self.logger.error(f"File not found: {sanitize_for_log(str(e))}")
      raise
    except pd.errors.EmptyDataError as e:
      self.logger.error(f"Empty CSV file: {sanitize_for_log(str(e))}")
      raise ValidationError("CSV file is empty")
    except pd.errors.ParserError as e:
      self.logger.error(f"CSV parsing error: {sanitize_for_log(str(e))}")
      raise ValidationError(f"Invalid CSV format: {e}")

  async def _send_local_image(self, phone: str, image_path: str, name: str) -> Optional[str]:
    """Send local image file from images/ directory using base64"""
    try:
      # Handle URLs - reject them as we only accept local files
      if image_path.startswith(('http://', 'https://')):
        self.logger.error(f"URLs not supported. Only local files from images/ directory: {sanitize_for_log(image_path)}")
        return None

      # Build full path - handle both 'images/file.png' and 'file.png'
      if image_path.startswith('images/'):
        file_path = Path(image_path)
      else:
        file_path = Path('images') / image_path

      # Check if file exists
      if not file_path.exists():
        self.logger.error(f"Image file not found: {sanitize_for_log(str(file_path))}")
        return None

      # Check file size
      file_size = file_path.stat().st_size
      if file_size > MAX_IMAGE_SIZE:
        self.logger.error(f"Image file too large: {file_size} bytes (max {MAX_IMAGE_SIZE // (1024*1024)}MB)")
        return None

      # Validate file extension
      if file_path.suffix.lower() not in ALLOWED_IMAGE_EXTENSIONS:
        self.logger.error(f"Unsupported image format: {file_path.suffix}. Allowed: {ALLOWED_IMAGE_EXTENSIONS}")
        return None

      # Read and encode image to base64
      with open(file_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

      self.logger.info(f"Image processed: {sanitize_for_log(str(file_path))} ({file_size} bytes)")
      return image_data

    except Exception as e:
      self.logger.error(f"Error processing image {sanitize_for_log(image_path)}: {sanitize_for_log(str(e))}")
      return None

  async def send_single_message(self, contact: Dict[str, Any]) -> bool:
    """Send single message with validation and retry logic"""
    try:
      phone = validate_phone_number(str(contact['phone']))
      message_type = validate_message_type(str(contact['message_type']))
      content = str(contact['content'])
      caption = str(contact.get('caption', ''))
      name = sanitize_for_log(str(contact.get('name', 'Usuario')))

      for attempt in range(settings.retry_attempts):
        try:
          if message_type == 'text':
            success = self.client.send_text_message(phone, content)
          elif message_type == 'image':
            # Get base64 data from local image
            image_data = await self._send_local_image(phone, content, name)
            if image_data:
              # Send image with custom caption or empty string
              success = self.client.send_image_message(phone, image_data, caption)
            else:
              success = False
          else:
            self.logger.warning(f"Invalid message type: {sanitize_for_log(message_type)}")
            return False

          if success:
            self.logger.info(f"Message sent to {name} ({sanitize_for_log(phone)}) - Attempt {attempt + 1}")
            return True
          else:
            self.logger.warning(f"Failed sending to {name} - Attempt {attempt + 1}")

        except (MessageSendError, APIConnectionError) as e:
          self.logger.error(f"Error sending to {name}: {sanitize_for_log(str(e))} - Attempt {attempt + 1}")

        if attempt < settings.retry_attempts - 1:
          await asyncio.sleep(RETRY_DELAY)

        self.logger.error(f"Failed to send to {name} after {settings.retry_attempts} attempts")
        return False

    except ValidationError as e:
      self.logger.error(f"Validation error: {sanitize_for_log(str(e))}")
      return False

  async def send_batch_messages(self, contacts: List[Dict[str, Any]]) -> Dict[str, int]:
    """Send batch messages with improved concurrency control"""
    semaphore = asyncio.Semaphore(settings.max_concurrent_messages)

    async def send_with_delay(contact):
      async with semaphore:
        result = await self.send_single_message(contact)
      # Move delay outside semaphore to improve throughput
      await asyncio.sleep(settings.delay_between_messages)
      return result

    tasks = [send_with_delay(contact) for contact in contacts]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Handle exceptions properly
    success_count = 0
    exception_count = 0

    for result in results:
      if isinstance(result, Exception):
        exception_count += 1
        self.logger.error(f"Exception in batch processing: {sanitize_for_log(str(result))}")
      elif result is True:
        success_count += 1

    total_count = len(contacts)
    failed_count = total_count - success_count

    return {
      'success': success_count,
      'total': total_count,
      'failed': failed_count,
      'exceptions': exception_count
    }

  def send_bulk_messages(self, contacts_file: str = 'contacts/contacts.csv') -> Dict[str, int]:
    """Send bulk messages with comprehensive error handling"""
    try:
      # Load and validate contacts
      contacts_df = self.load_contacts(contacts_file)

      # Check connection
      if not self.client.check_connection_status():
        raise APIConnectionError("WhatsApp not connected. Run setup first.")

      contacts_list = contacts_df.to_dict('records')

      self.logger.info(f"Starting bulk send to {len(contacts_list)} contacts")
      self.logger.info(f"Config: {settings.max_concurrent_messages} concurrent, {settings.delay_between_messages}s delay")

      # Execute async sending
      start_time = time.time()
      results = asyncio.run(self.send_batch_messages(contacts_list))
      end_time = time.time()

      # Calculate metrics
      duration = end_time - start_time
      rate = results['total'] / duration if duration > 0 else 0

      # Log results
      self.logger.info(f"Bulk send results:")
      self.logger.info(f"   Successful: {results['success']}")
      self.logger.info(f"   Failed: {results['failed']}")
      self.logger.info(f"   Total: {results['total']}")
      self.logger.info(f"   Duration: {duration:.2f} seconds")
      self.logger.info(f"   Rate: {rate:.2f} messages/second")

      return results

    except (ValidationError, APIConnectionError, FileNotFoundError) as e:
      self.logger.error(f"Bulk send failed: {sanitize_for_log(str(e))}")
      return {'success': 0, 'total': 0, 'failed': 0, 'exceptions': 1}

