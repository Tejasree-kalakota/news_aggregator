import os
from flask import Flask, render_template
from dotenv import load_dotenv
from newsapi import NewsApiClient
from newspaper import Article
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Load API key from .env
NEWS_API_KEY = os.getenv("NEWSAPI_KEY")
newsapi = NewsApiClient(api_key=NEWS_API_KEY)
print(f"NEWS_API_KEY loaded: {NEWS_API_KEY}")



def fetch_articles():
    articles_data = []
    try:
        top_headlines = newsapi.get_top_headlines(language='en', page_size=10)
        for item in top_headlines['articles'][:5]:
            url = item.get('url')

            # Try parsing the article using Newspaper3k
            try:
                article = Article(url)
                article.download()
                article.parse()

                # Truncate content safely
                content = article.text[:400] + '...' if len(article.text) > 400 else article.text

                article_dict = {
                    'title': article.title or item.get('title'),
                    'content': content,
                    'source': url,
                    'timestamp': item.get('publishedAt'),
                    'image_url': article.top_image or item.get('urlToImage')
                }

                articles_data.append(article_dict)

            except Exception as e:
                print(f"⚠️ Skipping article due to parse error: {e}")
                continue

    except Exception as e:
        print(f"❌ Error fetching articles: {e}")

    return articles_data


@app.route('/')
def index():
    articles = fetch_articles()
    return render_template("index.html", articles=articles)


if __name__ == '__main__':
    app.run(debug=True)
