FROM python:3.10.16

RUN apt-get update && apt-get install -y cron tzdata

ENV TZ=America/New_York

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Add the crontab file
COPY crontab.txt /etc/cron.d/my-cron-job

RUN sed -i 's/\r$//' /etc/cron.d/my-cron-job

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron-job

CMD ["cron", "-f"]
# CMD ["python3", "Daily-Summary.py"]