import os
from dotenv import load_dotenv

load_dotenv()

def str_to_bool(v):
    if isinstance(v, bool):
        return v
    return str(v or "").strip().lower() in {"true", "1", "yes", "y"}

def parse_langs(v):
    if not v:
        return ["de"]
    # Unterstütze sowohl LANGUAGE als auch LANGUAGES
    if isinstance(v, list):
        return [x.strip().lower() for x in v if x]
    return [x.strip().lower() for x in v.split(",") if x.strip()]

# lese preferenz (unterstützt alte/verschiedene keys)
lang_raw = os.getenv("LANGUAGES") or os.getenv("LANGUAGE") or "de"
LANGUAGES = parse_langs(lang_raw)

AI_PROVIDER = os.getenv("AI_PROVIDER", "groq").lower()
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")
MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

INCLUDE_TIMESTAMPS = str_to_bool(os.getenv("INCLUDE_TIMESTAMPS", "true"))
EXTRACT_QUOTES = str_to_bool(os.getenv("EXTRACT_QUOTES", "true"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FORMAT = os.getenv("LOG_FORMAT", "[%(levelname)s] %(message)s")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
