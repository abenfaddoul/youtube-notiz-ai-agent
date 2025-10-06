import os
import logging
from groq import Groq
from mistralai import Mistral
from config import DEFAULT_MODEL, MISTRAL_MODEL

def get_ai_client(provider: str = None):
    """
    Liefert den AI-Client für Groq oder Mistral.
    """
    provider = (provider or os.environ.get("AI_PROVIDER", "groq")).lower()

    if provider == "groq":
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Fehlender GROQ_API_KEY")
        logging.info("Verwende Groq API (Llama 3)")
        return Groq(api_key=api_key), "groq"

    elif provider == "mistral":
        api_key = os.environ.get("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("Fehlender MISTRAL_API_KEY")
        logging.info("Verwende Mistral API")
        return Mistral(api_key=api_key), "mistral"

    else:
        raise ValueError(f"Fehler bei AI_PROVIDER: {provider}")
    

def generate_markdown_notes(prompt: str) -> str:
    """
    Sendet den Prompt an Groq oder Mistral.
    Returns:
        str: Generierter Markdown-Text oder Fehlermeldung.
    """
    providers = ["groq", "mistral"]  # Reihenfolge der Versuche
    last_error = None

    for provider in providers:
        try:
            client, current = get_ai_client(provider)
            logging.info(f"Versuche Modell von {current}")

            if current == "groq":
                response = client.chat.completions.create(
                    model=DEFAULT_MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content

            elif current == "mistral":
                # Mistral API nutzt etwas andere Struktur
                response = client.chat.complete(
                    model= MISTRAL_MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content

        except Exception as e:
            logging.warning(f"Fehler bei {provider}: {e}")
            last_error = e
            continue

    logging.error(f"Beide Modelle fehlgeschlagen. Letzter Fehler: {last_error}")
    return "[Fehler: Kein Modell verfügbar oder API nicht erreichbar]"
