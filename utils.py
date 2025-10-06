import os, re, time, logging
from config import OUTPUT_DIR, LOG_LEVEL, LOG_FORMAT

def setup_logging():
    logging.basicConfig(
        level=LOG_LEVEL,
        format=LOG_FORMAT,
        datefmt="%H:%M:%S"
    )
    

def create_slug(video_id: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_-]', '', video_id)


def save_markdown_file(content: str, slug: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, f"{slug}.md")
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        logging.info(f"Markdown gespeichert: {filepath}")
    except Exception as e:
        logging.error(f"Fehler beim Speichern: {e}")


def sanitize_text(text: str, max_len: int = 15000) -> str:
    if not text:
        return ""
    clean = re.sub(r"[`#<>]", "", text)
    if len(clean) > max_len:
        clean = clean[:max_len] + " ... [gekürzt]"
    return clean.strip()


def retry_call(func, retries=3, delay=2, *args, **kwargs):
    for attempt in range(1, retries+1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.warning(f"Versuch {attempt} fehlgeschlagen: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                logging.error(f"Alle {retries} Versuche gescheitert.")
                raise
