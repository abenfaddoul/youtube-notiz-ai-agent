# AI YouTube Notizen-Agent

Ein KI-gestützter Agent, der 2–5-minütige YouTube-Videos analysiert und automatisch prägnante, strukturierte Notizen im Markdown-Format erstellt. Ideal für das schnelle Erfassen von Inhalten aus Vorträgen, Tutorials oder Diskussionen.

### Über das Projekt

Dieses Tool automatisiert den Prozess der Notizerstellung von YouTube-Videos. Es extrahiert das Transkript eines Videos, sendet es an ein fortschrittliches Sprachmodell (LLM) und formatiert die Antwort als saubere Markdown-Datei.

### Kernfunktionen:

* Automatische Transkript-Extraktion: Findet automatisch das bestmögliche Transkript in bevorzugten Sprachen (z.B. Deutsch, Englisch).

* KI-basierte Analyse: Nutzt leistungsstarke LLMs (via Groq oder Mistral) zur Erstellung von Zusammenfassungen, Kernaussagen und einer Gliederung.

* Strukturierte Markdown-Ausgabe: Generiert eine übersichtliche .md-Datei mit Titel, TL;DR, Kernaussagen und optionalen Zitaten.

* Hohe Konfigurierbarkeit: Alle wichtigen Parameter können einfach über eine .env-Datei gesteuert werden, ohne den Code zu ändern.

* Robuste Ausführung: Implementiert eine automatische Fallback-Logik (z.B. von Groq zu Mistral) und Retry-Mechanismen, um eine hohe Zuverlässigkeit zu gewährleisten.


## Getting Started

Folge diesen Schritten, um den Agenten lokal einzurichten und zu verwenden.

### Voraussetzungen

Python 3.8  
pip (Python package installer)

### Installation

Repository klonen:

git clone https://github.com/abenfaddoul/youtube-notiz-ai-agent

cd DEIN_REPO

### Virtuelle Umgebung erstellen (empfohlen):

## Für macOS/Linux
python3 -m venv venv

source venv/bin/activate

## Für Windows
python -m venv venv

.\venv\Scripts\activate

## Abhängigkeiten installieren:

pip install -r requirements.txt

## Konfigurationsdatei einrichten:
Kopiere die Vorlage .env.example zu einer neuen Datei namens .env.
cp .env.example .env
Öffne die .env-Datei und trage deine API-Schlüssel für GROQ_API_KEY und MISTRAL_API_KEY ein.

## Benutzung
Führe das Skript von der Kommandozeile aus und übergebe die URL des gewünschten YouTube-Videos als Argument.

## Syntax:
python main.py "YOUTUBE_VIDEO_URL"

## Beispiel:
python main.py "https://www.youtube.com/watch?v=jg6q0uF-LO8"

Nach erfolgreicher Ausführung findest du die generierte Markdown-Datei im output-Verzeichnis. Der Dateiname wird aus der Video-ID abgeleitet (z.B. Be_oT_W-8nU.md).

## Konfiguration
Alle Einstellungen werden in der .env-Datei vorgenommen.

