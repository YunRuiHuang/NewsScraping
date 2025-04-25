from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment
import mysql.connector;
import requests
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os

mysql_host = 'news-mysql'
mysql_port = 3306
file_app_url = "http://file-app:3000/file"
hour = 24
get_sql = f"select news_id, news_company from news where date >= NOW() - INTERVAL {hour} HOUR;"

db_conn = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user="root",
    password="password",
    database="news"
)
cursor = db_conn.cursor(dictionary=True)
cursor.execute(get_sql)
rows = cursor.fetchall()

news_id = list()
for r in rows:
  news_id.append(r['news_id'])
companies = {row['news_company'] for row in rows if row['news_company']}

def download_wav(id):
  url = f"{file_app_url}?fileName={id}.wav"
  try:
      response = requests.get(url, stream=True)
      if response.status_code == 200:
          filename = f"{id}.wav"
          with open(filename, 'wb') as f:
              for chunk in response.iter_content(chunk_size=8192):
                  if chunk:
                      f.write(chunk)
          print(f"Downloaded {filename}")
      else:
          print(f"Failed to download {id}.wav, status code: {response.status_code}")
  except Exception as e:
      print(f"Error downloading {id}.wav: {e}")

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(download_wav, news_id)

output = AudioSegment.empty()
for i in news_id:  # include 0.wav to n.wav
    output += AudioSegment.from_wav("next.wav")
    file_name = f"{i}.wav"
    audio = AudioSegment.from_wav(file_name)
    output += audio  # append

output.export("output.wav", format="wav")

duration = int(len(output) / 1000.0 / 60)

def get_greeting(hour):
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    elif 18 <= hour < 22:
        return "Good evening"
    else:
        return "Good night"
    
greeting = get_greeting(datetime.now().hour)
date_str = datetime.now().strftime("%B %d, %Y")
total_news = len(rows)
company_str = ", ".join(companies) if companies else "various sources"
message = f"{greeting}! Today is {date_str}. There are {total_news} news articles from {company_str} in the past {hour} hours. It will take about {duration} minutes to go through them."

pipeline = KPipeline(lang_code='a')
generator = pipeline(message, voice='af_heart')
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

output += AudioSegment.from_wav("output.wav")
output += AudioSegment.from_wav("end.wav")

output.export("daily.wav", format="wav")

files = {
  "file": open("daily.wav", "rb")
}

data = {
  "fileName": "daily",
  "fileType": "wav"
}

response = requests.post(file_app_url, files=files, data=data)

for id in news_id:
    filename = f"{id}.wav"
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print(f"Deleted {filename}")
        except Exception as e:
            print(f"Error deleting {filename}: {e}")