import logging, re
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from config import LANGUAGES, INCLUDE_TIMESTAMPS, EXTRACT_QUOTES
from utils import sanitize_text
from urllib.parse import urlparse, parse_qs

logger = logging.getLogger(__name__)


def get_video_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if "youtu.be" in host:
        return parsed.path.lstrip("/")
    if "youtube.com" in host:
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]
        if parsed.path.startswith(("/embed/", "/shorts/")):
            return parsed.path.split("/")[2]
    return None


def validate_video_id(video_id: str) -> str | None:
    if not video_id or not re.match(r'^[a-zA-Z0-9_-]{6,}$', video_id):
        logging.error("Ungültige Video-ID erkannt.")
        return None
    return video_id


def _try_fetch(ytt_api, video_id: str, languages=LANGUAGES):
    """
    Hilfsfunktion zum Abrufen des Transkripts.
    Gibt bei Erfolg eine Liste von Segmenten zurück, sonst None.
    """
    try:
        return ytt_api.fetch(video_id, languages=languages)
    except TranscriptsDisabled:
        logger.warning(f"Untertitel sind für Video {video_id} deaktiviert.")
        return None
    except NoTranscriptFound:
        logger.debug(f"Kein Transkript für {video_id} mit Sprachen {languages}.")
        return None
    except Exception as e:
        logger.error(f"Fehler beim Abrufen des Transkripts ({video_id}, {languages}): {e}")
        return None


def get_transcript_with_manual_fallback(video_id: str) -> dict:
    """
    Ruft das Transkript für ein YouTube-Video ab.
    - Unterstützte Sprachen: de, en
    - Fallback: Englisch, wenn Deutsch nicht verfügbar
    - Optional: manuell eine neue URL angeben, wenn kein Transkript existiert

    RETURNS:
    {
        "transcript": str,
        "quotes": list[(timestamp, text)]
    }
    """
    ytt_api = YouTubeTranscriptApi()
    candidate_langs = LANGUAGES

    logger.info(f"Versuche Transkript für {video_id} mit Sprachen {candidate_langs}")

    # Erstversuch mit beiden Sprachen (de, en)
    data = _try_fetch(ytt_api, video_id, candidate_langs)

    # Falls kein Ergebnis, einzeln testen (Präferenz: de → en)
    if not data:
        for lang in candidate_langs:
            data = _try_fetch(ytt_api, video_id, [lang])
            if data:
                logger.info(f"Transkript gefunden mit Sprache '{lang}'")
                break

    # Wenn nichts gefunden, manueller Fallback
    if not data:
        logger.warning(f"Kein Transkript für Video {video_id} gefunden (de/en).")
        choice = input("\n Kein Transkript gefunden. Neue YouTube-URL eingeben (oder Enter zum Überspringen): ").strip()

        if choice:
            new_video_id = validate_video_id(get_video_id(choice))
            if not new_video_id:
                logger.error("Ungültige URL eingegeben. Abbruch.")
                return {
                    "transcript": f"[Hinweis: Kein gültiges Video angegeben (ursprüngliches Video: {video_id})]",
                    "quotes": []
                }
            logger.info(f"Versuche Transkript für neues Video: {new_video_id}")
            return get_transcript_with_manual_fallback(new_video_id)
        else:
            logger.info(f"Kein alternatives Video gewählt. Fahre mit Hinweis fort.")
            return {
                "transcript": f"[Hinweis: Für Video {video_id} liegt kein deutsches oder englisches Transkript vor.]",
                "quotes": []
            }

    # Transkript formatieren + optionale Zitate extrahieren
    lines, quotes = [], []
    for item in data:
        start = getattr(item, "start", 0.0)
        text = getattr(item, "text", "").strip()
        if not text:
            continue

        minutes, seconds = divmod(int(start), 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"

        # Zeitstempel optional einfügen
        lines.append(f"[{timestamp}] {text}" if INCLUDE_TIMESTAMPS else text)

        # Optional: Zitate
        if EXTRACT_QUOTES and len(text.split()) >= 8:
            quotes.append((timestamp, text))

    transcript = "\n".join(lines) if INCLUDE_TIMESTAMPS else " ".join(lines)

    logger.info(f"Transkript erfolgreich abgerufen ({len(data)} Segmente).")
    return {
        "transcript": sanitize_text(transcript),
        "quotes": quotes[:5]
    }
