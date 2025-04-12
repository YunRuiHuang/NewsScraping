import pika;
import json;
import time;
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import mysql.connector;
from webdriver_manager.chrome import ChromeDriverManager

mq_host = 'rabbitmq'
mq_port = 5672
mysql_host = 'news-mysql'
mysql_port = 3306
#driver_path = '/usr/bin/chromedriver' #'C:\\chromedriver-win64\\chromedriver.exe' 
extension_path = './bypass-paywalls-firefox-clean-master.crx'
sql = "UPDATE news SET context = %s WHERE URL = %s;"

# setup MQ connect
mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host, port=mq_port))
channel = mq_conn.channel()

# setup db connect
db_conn = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user="root",
    password="password",
    database="news"
)
cursor = db_conn.cursor()

# setup chrome driver
# service = Service(executable_path=driver_path)
service = Service(ChromeDriverManager().install())
option = Options()
option.add_argument("--no-sandbox")
option.add_argument("--disable-dev-shm-usage")
option.add_extension(extension=extension_path)
web = webdriver.Chrome(service=service,options=option)

def webGet(url):
  web.get(url=url)
  textdata = web.find_elements(By.CLASS_NAME, 'evys1bk0')
  artifact = ''
  for data in textdata:
    artifact = artifact + data.text
  return artifact
  

channel.basic_qos(prefetch_count=1)
try:
  while True:
    method_frame, header_frame, body = channel.basic_get(queue='nytime', auto_ack=False)

    if method_frame:

      if not db_conn.is_connected():
        print(" [!] Reconnecting to MySQL...")
        db_conn.reconnect(attempts=3, delay=5)
        cursor = db_conn.cursor()

      data = json.loads(body)
      print(f" [x] Received title={data['title']}.\n author={data['author']},\n time = {data['date']}")
      output = webGet(data['url'])
      cursor.execute(sql, (output, data['url']))
      db_conn.commit()
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