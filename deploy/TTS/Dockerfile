FROM python:3.10.16

WORKDIR /app

USER root

RUN apt-get update && apt-get -y install espeak-ng && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "Kokoro-TTS.py"]