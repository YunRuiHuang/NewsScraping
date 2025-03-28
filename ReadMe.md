# News Scraping

- [x] RSS Fetch
- [ ] MySQL check duplicate and save
- [x] RabbitMQ send
- [x] RabbitMQ receive
- [x] Webpage fetch
- [ ] MySQL save text
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



## RSS Update Scheduler



## Chrome and Selenium

