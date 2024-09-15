from celery import Celery
import requests

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def scrape_news_articles():
    url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    articles = response.json().get('articles', [])

    for article in articles:
        content = article.get('content', '')
        store_document(content)
