# Dockerfile

# Basis-Image (Python)
FROM python:3.11-slim

# Arbeitsverzeichnis festlegen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Befehl zum Starten der Anwendung (z.B. ein Flask/FastAPI-Server für den Agenten)
CMD ["python", "main.py"]