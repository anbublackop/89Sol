from fastapi import FastAPI
import requests, json
import os
from dotenv import load_dotenv
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

load_dotenv()

api_key = os.getenv("SECRET_KEY")
base_url = os.getenv("BASE_URL")
article_extension = os.getenv("ARTICLE_EXTENSION")
everything_extension = os.getenv("EVERYTHING_EXTENSION")

app = FastAPI()

def summarize(articles):
    for art in articles:
        print("Title:", art['title'])
        print("Description:", art['description'])
        print("URL:", art['url'])
        print("----")

def get_data_from_source(url, params):
    print(f"Fetching data for item {url} from source...")
    return requests.get(url, params = params)

def get_cached_data(item, params):
    item_id = f"{item}-{params.get('source')}"
    key = f"item: {item_id}"
    cached_data = r.get(key)
    if cached_data:
        print(f"Cache hit for item {item_id}")
        return json.loads(cached_data)
    else:
        print(f"Cache miss for item {item_id}")
        data = get_data_from_source(item, params)
        # Store data in Redis with an expiration time (e.g., 60 seconds)
        r.setex(key, 60, json.dumps(data)) 
        return data


@app.get('/')
async def root():
    return {
        "This is the index page"
    }

@app.get('/get-articles')
async def get_articles(source: str = "bbc-news"):
    articles_url = f"{base_url}{article_extension}"
    params = {
        "source": source,
        "apiKey": api_key
    }
    try:
        # response = requests.get(articles_url, params = params)
        response = get_cached_data(articles_url, params)
        if response.status_code == 200:
            articles = response.json().get('articles')
            return articles
    except Exception as e:
        return {
            "message": str(e)
        }
    
@app.get('/get-everything')
async def get_everything(keyword: str, from_date: str = "2025-09-03"):
    everything_url = f"{base_url}{everything_extension}"
    params = {
        "q": keyword,
        "from": from_date,
        "sortBy": "popularity",
        "apiKey": api_key
    }
    try:
        # response = requests.get(everything_url, params = params)
        response = get_cached_data(everything_url, params)
        if response.status_code == 200:
            articles = response.json().get('articles')
            return articles
    except Exception as e:
        return {
            "message": str(e)
        }