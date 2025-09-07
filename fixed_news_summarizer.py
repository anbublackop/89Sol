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
    response = requests.get(url, params = params).json()
    return response

def get_cached_data(item, params):
    if 'article' in item:
        item_id = f"{item}{params.get('source').strip().lower()}"
    else:
        item_id = f"{item}{params.get('q').strip().lower()}-{params.get('from').strip().lower()}"
    key = f"item: {item_id}"
    cached_data = r.get(key)
    if cached_data:
        print(f"Cache hit for item {item_id}")
        return json.loads(cached_data)
    else:
        print(f"Cache miss for item {item_id}")
        data = get_data_from_source(item, params)
        r.setex(key, 300, json.dumps(data)) #saving data for 600 seconds 
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
        response = get_cached_data(articles_url, params)
        if response.get('status') == 'ok':
            articles = response.get('articles')
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
        response = get_cached_data(everything_url, params)
        if response.get('status') == 'ok':
            articles = response.get('articles')
            return articles
    except Exception as e:
        return {
            "message": str(e)
        }