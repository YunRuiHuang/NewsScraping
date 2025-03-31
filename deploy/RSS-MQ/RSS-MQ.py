import feedparser;
import pika;
import json;
import mysql.connector;
from mysql.connector import IntegrityError
from datetime import datetime
import time;

rss_url = 'https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml'
news_company = "nytime"
category = "Asia"
mq_host = 'rabbitmq'
mq_port = 5672
mysql_host = 'news-mysql'
mysql_port = 3306

feed = feedparser.parse(rss_url)

mq_conn = pika.BlockingConnection(pika.ConnectionParameters(host=mq_host, port=5672))
channel = mq_conn.channel()

db_conn = mysql.connector.connect(
    host=mysql_host,
    port=mysql_port,
    user="root",
    password="password",
    database="news"
)
cursor = db_conn.cursor()

sql = "INSERT INTO news (URL, title, author, date,  news_company, category) VALUES (%s, %s, %s, %s, %s, %s)"

for entrie in feed.entries:

    output = {
        'id':entrie.id,
        'title':entrie.title,
        'url':entrie.link,
        'author':entrie.author,
        'date':entrie.published
    }
    val = (
        entrie.link,
        entrie.title,
        entrie.author,
        datetime.strptime(entrie.published, "%a, %d %b %Y %H:%M:%S %z"),
        news_company,
        category
    )
    try:
        cursor.execute(sql, val)
        db_conn.commit()
        channel.basic_publish(exchange='news.rss', routing_key='nytime', body=json.dumps(output))
    except IntegrityError as e:
        if e.errno == 1062:
            print("URL already exists. Skipping insert.")
        else:
            print("Insert failed:", e)
            db_conn.rollback()
    except Exception as e:
        print(f"Unhandled error: {e}")
        
cursor.close()
db_conn.close()
mq_conn.close()