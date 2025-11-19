# tests/test_llm_client.py
import pytest
from unittest.mock import patch, MagicMock
from llm_client import llm_client  # oder wie deine Klasse heißt

@pytest.fixture
def dummy_response():
    return {"choices": [{"text": "TL;DR: Das ist eine Zusammenfassung."}]}

@patch("llm_client.requests")  # falls llm_client requests benutzt
def test_llm_client_send_prompt(mock_requests, dummy_response):
    # Configure the fake requests.post to return a fake response object
    fake_resp = MagicMock()
    fake_resp.json.return_value = dummy_response
    fake_resp.status_code = 200
    mock_requests.post.return_value = fake_resp

    client = llm_client(api_key="fake-key")
    resp = client.send_prompt("Hallo Welt")
    # Je nachdem wie deine Methode Antwort zurückgibt, prüfe das Feld
    assert isinstance(resp, dict) or isinstance(resp, str)
    # Wenn deine Methode z.B. resp["choices"][0]["text"] zurückgibt:
    # assert "TL;DR" in resp["choices"][0]["text"] or "Zusammenfassung" in resp["choices"][0]["text"]
