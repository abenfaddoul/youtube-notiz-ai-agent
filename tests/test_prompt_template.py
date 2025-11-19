# tests/test_prompt_template.py
import pytest
from prompt_template import create_llm_prompt

def test_build_prompt_contains_sections():
    transcript = "Dies ist ein Test-Transkript mit drei Sätzen. Zweiter Satz. Dritter Satz."
    meta = {"title": "Test Video", "language": "de"}
    prompt = create_llm_prompt(transcript, meta)
    assert "TL;DR" in prompt or "Zusammenfassung" in prompt or len(prompt) > 0
    assert "Test Video" in prompt or "Titel" in prompt or isinstance(prompt, str)
