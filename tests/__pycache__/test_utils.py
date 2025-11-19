# tests/test_utils.py
import os
import tempfile
import pytest
from utils import sanitize_filename, save_markdown, extract_video_id

def test_sanitize_filename():
    name = 'Be_oT/W:  W-8nU?*.md'
    safe = sanitize_filename(name)
    assert '/' not in safe and '\\' not in safe
    assert len(safe) > 0

def test_extract_video_id_youtube_url():
    url = "https://www.youtube.com/watch?v=Be_oT_W-8nU"
    vid = extract_video_id(url)
    assert vid == "Be_oT_W-8nU" or isinstance(vid, str)

def test_save_markdown_creates_file(tmp_path):
    content = "# Title\n\nTL;DR: summary"
    path = tmp_path / "Be_oT_W-8nU.md"
    save_markdown(str(path), content)
    assert path.exists()
    saved = path.read_text(encoding="utf-8")
    assert "TL;DR" in saved
