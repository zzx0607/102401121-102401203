from pathlib import Path

ROOT = Path(__file__).resolve().parent

class Config:
    DATABASE = str(ROOT / 'instance' / 'lost_found.db')
    UPLOAD_FOLDER = str(ROOT / 'instance' / 'uploads')
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024
    MAX_IMAGE_BYTES = 5 * 1024 * 1024
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
