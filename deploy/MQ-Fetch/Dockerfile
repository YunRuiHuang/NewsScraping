FROM selenium/standalone-chrome:131.0

USER root

RUN apt-get update && apt-get install -y python3-pip python3-venv xvfb build-essential libffi-dev python3-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix

RUN chown -R seluser:seluser /opt/venv /app
USER seluser

CMD ["sh", "-c", "Xvfb :99 -ac 2>/dev/null & python3 -u MQ-fetch.py"]