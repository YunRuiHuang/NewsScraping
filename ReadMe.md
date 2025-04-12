# News Scraping

- [x] RSS Fetch
- [x] MySQL check duplicate and save
- [x] RabbitMQ send
- [x] RabbitMQ receive
- [x] Webpage fetch
- [x] MySQL save text
- [ ] AI summary
- [ ] AI Reading
- [ ] ffmpeg audio combine
- [ ] Addition
  - [ ] Support more webpage
  - [ ] Docker container

## RabbitMQ deploy

```sh
docker network create news-scraping-network
docker run -d --name rabbitmq --network news-scraping-network -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```



## MySQL Deploy

```sh
docker run --name news-mysql --network news-scraping-network -p 4000:3306 --restart always -e MYSQL_ROOT_PASSWORD=password -d mysql 
```

### Table

```sql
CREATE DATABASE news;
CREATE TABLE news (
    news_id INT PRIMARY KEY AUTO_INCREMENT,
    URL VARCHAR(512) UNIQUE,
    title VARCHAR(512),
    author VARCHAR(255),
    date TIMESTAMP,
    context TEXT,
    summary TEXT,
    news_company VARCHAR(255),
    category VARCHAR(255)
);
```



## RSS Update Scheduler

```sh
docker build -t rss-mq-app .
docker run --name rss-mq-app --network news-scraping-network -d rss-mq-app
```



## Chrome and Selenium

```sh
docker build -t mq-fetch-app .
docker run --name mq-fetch-app --network news-scraping-network -d mq-fetch-app
```

credit:

https://github.com/timoteostewart/dockerized-headfull-chrome-selenium



## AI Summary





## AI Reading

TTS
