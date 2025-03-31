FROM python:3.10.16

RUN apt-get update && apt-get install -y cron

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add the crontab file
COPY crontab.txt /etc/cron.d/rss-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/rss-cron

CMD ["cron", "-f"]