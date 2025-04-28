# News Scraping

- [x] RSS Fetch
- [x] MySQL check duplicate and save
- [x] RabbitMQ send
- [x] RabbitMQ receive
- [x] Webpage fetch
- [x] MySQL save text
- [x] AI summary
- [x] AI Reading
- [x] File API (save audio)
- [x] ffmpeg audio combine
- [ ] Addition
  - [ ] Support more webpage
  - [x] Docker container



## News Company

| Company                       | Category                                          | Class Name | RSS URL                                                      |
| ----------------------------- | ------------------------------------------------- | ---------- | ------------------------------------------------------------ |
| BBC                           | World<br />Asia<br />US & Canada                  |            | http://feeds.bbci.co.uk/news/world/rss.xml<br />http://feeds.bbci.co.uk/news/world/asia/rss.xml<br />http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml |
| CNN                           |                                                   |            | N/A                                                          |
| Reuters                       | World<br />China<br />Asia-pacific                |            | http://rsshub:1200/reuters/world<br />http://rsshub:1200/reuters/world/china<br />http://rsshub:1200/reuters/world/asia-pacific |
| Al Jazeera                    |                                                   |            |                                                              |
| New York Times World          | World<br />Asia-Pacific                           |            | https://rss.nytimes.com/services/xml/rss/nyt/World.xml<br />https://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml |
| CNBC                          | World<br />US<br />Asia<br />Economy<br />Finance |            | https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=100727362<br />https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15837362<br />https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=19832390<br />https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=20910258<br />https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664 |
| Bloomberg Tech                |                                                   |            |                                                              |
| TechCrunch                    | Tech                                              |            | https://techcrunch.com/feed/                                 |
| The Verge                     | Tech                                              |            | https://www.theverge.com/rss/index.xml                       |
| The Straits Times (Singapore) | World<br />Singapore<br />Asia                    |            | https://www.straitstimes.com/news/world/rss.xml<br />https://www.straitstimes.com/news/singapore/rss.xml<br />https://www.straitstimes.com/news/asia/rss.xml |
| Channel NewsAsia (CNA)        | World<br />Singapore<br />Asia                    |            | https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6311<br />https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=10416<br />https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=6511 |
| The Japan Times               |                                                   |            | https://www.japantimes.co.jp/feed/                           |
| Nikkei Asia                   | Asia                                              |            | http://rsshub:1200/nikkei/asia                               |
| The Korea Herald              | World                                             |            | https://www.koreaherald.com/rss/kh_World                     |
| The Korea Times               |                                                   |            |                                                              |
| South China Morning Post      | World<br />Asia<br />China                        |            | https://www.scmp.com/rss/5/feed<br />https://www.scmp.com/rss/3/feed<br />https://www.scmp.com/rss/4/feed |
| Taiwan News                   |                                                   |            |                                                              |







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



## Daily Summary

```sh
docker build -t daily-summary-app .
docker run --name daily-summary-app --network news-scraping-network -d daily-summary-app
docker run --name daily-summary-app -d daily-summary-app
```

