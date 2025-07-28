import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data paths
TEMP_DIR = os.path.join(BASE_DIR, "temp_data")
UPLOAD_DIR = os.path.join(TEMP_DIR, "uploads")
PARSED_DIR = os.path.join(TEMP_DIR, "parsed")

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PARSED_DIR, exist_ok=True)

# File settings
ALLOWED_EXTENSIONS = ['.txt', '.csv']

# Display settings
APP_TITLE = "📊 WhatsApp Chat Analyzer"
APP_DESCRIPTION = (
    "Upload your WhatsApp chat and get analytics, sentiment insights, and download options."
)
