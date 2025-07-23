import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file.")

# Ensure index directory exists
INDEX_DIR = "index"
INDEX_PATH = os.path.join(INDEX_DIR, "file_index.json")
os.makedirs(INDEX_DIR, exist_ok=True)

# Directories to scan for files
ROOT_DIRS = [
    os.path.expanduser("~/Downloads"),
    os.path.expanduser("~/Desktop")
]
