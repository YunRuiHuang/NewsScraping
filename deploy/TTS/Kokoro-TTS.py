from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment
import pika;
import json;
import time;
import mysql.connector;
import requests

mq_host = 'rabbitmq'
mq_port = 5672
mysql_host = 'news-mysql'
mysql_port = 3306
url = "http://file-app:3000/file"
get_sql = "SELECT news_id, summary, title, author FROM news WHERE URL = %s"

mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host, port=mq_port))
channel = mq_conn.channel()
channel.basic_qos(prefetch_count=1)

db_conn = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user="root",
    password="password",
    database="news"
)
cursor = db_conn.cursor(dictionary=True)

pipeline = KPipeline(lang_code='a')

try:
  while True:
    method_frame, header_frame, body = channel.basic_get(queue='tts', auto_ack=False)

    if method_frame:
      time.sleep(10)
      if not db_conn.is_connected():
        print(" [!] Reconnecting to MySQL...")
        db_conn.reconnect(attempts=3, delay=5)
        cursor = db_conn.cursor(dictionary=True)
      
      data = json.loads(body)
      print(f" [x] Received title={data['title']}.\n author={data['author']},\n time = {data['date']}")
      for attempt in range(3):
        cursor.execute(get_sql, (data['url'],))
        rows = cursor.fetchall()

        if rows and 'summary' in rows[0]:  # if found
            summary = rows[0]['summary']
            title = rows[0]['title']
            author = rows[0]['author']
            new_id = rows[0]['news_id']
            text = f"\"{title}\" written by {author}. {summary}"
            break  # exit the retry loop
        else:
            print(f"Summary not found, retry {attempt + 1}/{3}...")
            time.sleep(10)

      generator = pipeline(text, voice='af_heart')
      n = 0
      for i, (gs, ps, audio) in enumerate(generator):
          n = i
          print(i, gs, ps)
          sf.write(f'{i}.wav', audio, 24000)

      output = AudioSegment.empty()
      for i in range(n + 1):  # include 0.wav to n.wav
          file_name = f"{i}.wav"
          audio = AudioSegment.from_wav(file_name)
          output += audio  # append

      output.export("output.wav", format="wav")

      files = {
        "file": open("output.wav", "rb")
      }

      data = {
        "fileName": new_id,
        "fileType": "wav"
      }

      response = requests.post(url, files=files, data=data)

      channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    else:
      print(" [*] No messages in queue.")

    time.sleep(60)
except KeyboardInterrupt:
  print("\n [*] Exiting.")
finally:
  mq_conn.close()
  cursor.close()
  db_conn.close()
