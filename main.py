import argparse
import logging
from youtube_api import get_video_id, validate_video_id, get_transcript_with_manual_fallback
from utils import setup_logging, create_slug, save_markdown_file, retry_call
from llm_client import generate_markdown_notes
from prompt_template import create_llm_prompt
from config import EXTRACT_QUOTES  

def main():
    setup_logging()
    parser = argparse.ArgumentParser(
        description="AI-Agent: YouTube-Video in strukturierte Markdown-Notizen umwandeln."
    )
    parser.add_argument("url", help="Die URL des YouTube-Videos.")
    args = parser.parse_args()

    logging.info(f"Starte Verarbeitung für URL: {args.url}")

    # YouTube-Video-ID validieren
    video_id = validate_video_id(get_video_id(args.url))
    if not video_id:
        logging.error("Abbruch: ungültige Video-ID.")
        return

    # Transkript abrufen (mit Retry-Mechanismus)
    transcript = retry_call(get_transcript_with_manual_fallback, retries=3, delay=3, video_id=video_id)
    if not transcript or not transcript.get("transcript"):
        logging.error("Abbruch: Kein Transkript abrufbar.")
        return

    # Prompt vorbereiten
    prompt = create_llm_prompt(transcript, args.url, extract_quotes=EXTRACT_QUOTES)

    # Markdown generieren (mit Retry)
    markdown = retry_call(generate_markdown_notes, retries=2, delay=5, prompt=prompt)
    if not markdown:
        logging.error("Abbruch: Modell hat keine Inhalte geliefert.")
        return

    # Datei speichern
    slug = create_slug(video_id)
    save_markdown_file(markdown, slug)
    logging.info("Workflow abgeschlossen!")

if __name__ == "__main__":
    main()
