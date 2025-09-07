from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("SECRET_KEY")
base_url = os.getenv("BASE_URL")

app = FastAPI()

def summarize(articles):
    for art in articles:
        print("Title:", art['title'])
        print("Description:", art['description'])
        print("URL:", art['url'])
        print("----")
        
@app.get('/')
async def root():
    return {
        "This is the index page"
    }

@app.get('/get-articles')
async def get_articles(source: str = "bbc-news"):
    articles_url = f"{base_url}v1/articles"
    params = {
        "source": source,
        "apiKey": api_key
    }
    try:
        response = requests.get(articles_url, params = params)
        if response.status_code == 200:
            articles = response.json().get('articles')
            return articles
    except Exception as e:
        return {
            "message": str(e)
        }
    
@app.get('/get-everything')
async def get_everything(keyword: str, from_date: str = "2025-09-03"):
    everything_url = f"{base_url}v2/everything"
    params = {
        "q": keyword,
        "from": from_date,
        "sortBy": "popularity",
        "apiKey": api_key
    }
    try:
        response = requests.get(everything_url, params = params)
        if response.status_code == 200:
            articles = response.json().get('articles')
            return articles
    except Exception as e:
        return {
            "message": str(e)
        }