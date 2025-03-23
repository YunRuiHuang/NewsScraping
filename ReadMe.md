# News Scraping

## RabbitMQ deploy

```sh
docker network create news-scraping-network
docker run -d --name rabbitmq --network news-scraping-network -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```



## MySQL Deploy



## RSS Update Scheduler



## Chrome and Selenium

