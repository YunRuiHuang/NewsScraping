from google import genai
from google.genai import types
import pika;
import json;
import time;
import mysql.connector;

mq_host = 'rabbitmq'
mq_port = 5672
mysql_host = 'news-mysql'
mysql_port = 3306
gemini_key = ''
get_sql = "SELECT context FROM news WHERE URL = %s"
update_sql = "UPDATE news SET summary = %s WHERE URL = %s;"

with open("config", "r", encoding="utf-8") as f:
  gemini_key = f.read()

mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host, port=mq_port))
channel = mq_conn.channel()

db_conn = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user="root",
    password="password",
    database="news"
)
cursor = db_conn.cursor(dictionary=True)

channel.basic_qos(prefetch_count=1)
try:
  while True:
    method_frame, header_frame, body = channel.basic_get(queue='summary', auto_ack=False)

    if method_frame:

      if not db_conn.is_connected():
        print(" [!] Reconnecting to MySQL...")
        db_conn.reconnect(attempts=3, delay=5)
        cursor = db_conn.cursor(dictionary=True)
      
      data = json.loads(body)
      print(f" [x] Received title={data['title']}.\n author={data['author']},\n time = {data['date']}")
      cursor.execute(get_sql,(data['url'],))
      rows = cursor.fetchall()
      text_input=rows[0]['context']

      client = genai.Client(api_key=gemini_key)
      response = client.models.generate_content(
        model="gemini-2.0-flash", 
        config=types.GenerateContentConfig(
          system_instruction=(
            "You are an expert summarizer. Your task is to summarize long texts into a clear, informative summary "
            "written in well-structured paragraphs. The summary should be less than 300 words. "
            "Do not use bullet points or numbered lists. "
            "Focus on capturing the key points, main arguments, and important details. "
            "Avoid unnecessary repetition and do not include personal opinions."
          )
        ),
        contents=text_input
      )

      cursor.execute(update_sql,(response.text,data['url']))
      db_conn.commit()
      channel.basic_publish(exchange='news.summary', routing_key='tts', body=body)
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