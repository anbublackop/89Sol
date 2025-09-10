
# 89Sol News Summarizer

A FastAPI-based microservice for fetching and caching news articles using [NewsAPI](https://newsapi.org/). Includes Redis caching and Docker support.

## Features

- Fetch articles from NewsAPI by source (`/get-articles`)
- Search for news articles by keyword and date (`/get-everything`)
- Redis caching for improved performance
- Dockerized for easy deployment

## Requirements

- Python 3.11+
- Docker & Docker Compose

## Setup

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd 89Sol

2. **Configure environment variables: Edit .env with your NewsAPI key:**
    ```
    SECRET_KEY=your_newsapi_key
    BASE_URL=https://newsapi.org/
    ARTICLE_EXTENSION=v1/articles/
    EVERYTHING_EXTENSION=v2/everything/
    ```

3. **Build and run with Docker Compose:**
    ```
    docker-compose up -d --build
    ```

The API will be available at http://localhost:8000/docs.

## Development

**Install dependencies:**
```pip install -r```

**Run locally:**
```uvicorn fixed_news_summarizer:app --reload```

**Starting and running redis locally on linux/mac:**
```https://redis.io/docs/latest/operate/oss_and_stack/install/archive/install-redis/install-redis-on-mac-os/```

## File Structure

```
fixed_news_summarizer.py — FastAPI app and logic
.env — Environment variables
requirements.txt — Python dependencies
Dockerfile & docker-compose.yaml — Container setup
```