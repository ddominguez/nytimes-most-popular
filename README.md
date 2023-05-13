# NY Times Most Popular Articles

Flask application that displays the most popular articles on NYTimes.com based on emails, shares, or views.

# Requirements

* NYTimes Developer API Key - https://developer.nytimes.com/get-started
* Redis Stack (If not using Docker) - https://redis.io/download/

# Setup for local environment

### Create .env file
```
FLASK_DEBUG=true
FLASK_NYT_API_KEY=<YOUR API KEY>
FLASK_CACHE_TYPE=RedisCache
FLASK_CACHE_DEFAULT_TIMEOUT=300
FLASK_CACHE_REDIS_HOST=redis
FLASK_CACHE_REDIS_DB=0
```

### Create docker-compose.override.yml file
```
services:
  web:
    env_file:
      - ./.env
```

# Start App
```
make web-up
```

* Open Flask App - `http://localhost:5000/`
* Open RedisStack Browser - `http://localhost:8001/`
