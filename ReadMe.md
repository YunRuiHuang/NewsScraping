# News Scraping

- [x] RSS Fetch
- [x] MySQL check duplicate and save
- [x] RabbitMQ send
- [x] RabbitMQ receive
- [x] Webpage fetch
- [x] MySQL save text
- [x] AI summary
- [ ] AI Reading
- [ ] File API (save audio)
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

### File 

*bypass-paywalls-firefox-clean-master.crx* : add-on file for Chrome

```sh
docker build -t mq-fetch-app .
docker run --name mq-fetch-app --network news-scraping-network -d mq-fetch-app
docker run --name mq-fetch-app -p 3002:3000 -d mq-fetch-app
```

credit:

https://github.com/timoteostewart/dockerized-headfull-chrome-selenium



## AI Summary

### File

*config* : put the Google Gemini API key here

```sh
docker build -t gemini-summary-app .
docker run --name gemini-summary-app --network news-scraping-network -d gemini-summary-app
```



## File API

### File

*mount_smb.sh* : add the user name, password and IP address of SMB server

```sh
docker build -t file-app .

docker run --privileged --name file-app -p 3007:3000 --network news-scraping-network -d file-app

docker run --privileged --name file-app -p 3007:3000 -d file-app
```



## AI Reading

```sh
docker build -t kokoro-tts-app .
docker run --name kokoro-tts-app --network news-scraping-network -d kokoro-tts-app
docker run --name kokoro-tts-app -d kokoro-tts-app
```

