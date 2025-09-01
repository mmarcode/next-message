"""Application constants"""

# Image processing
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
MIME_TYPES = {
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', 
  '.png': 'image/png',
  '.gif': 'image/gif'
}

# Retry configuration
RETRY_DELAY = 2  # seconds
DEFAULT_RETRY_ATTEMPTS = 3

# CSV columns
REQUIRED_CSV_COLUMNS = ['name', 'phone', 'message_type', 'content']
OPTIONAL_CSV_COLUMNS = ['caption']

# Message types
MESSAGE_TYPES = {'text', 'image'}