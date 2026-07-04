from dotenv import load_dotenv
load_dotenv()

from newsapi import NewsApiClient
import os

newsapi = NewsApiClient(api_key=os.environ["NEWSAPI_KEY"])
articulos = newsapi.get_everything(
    q="Inditex",
    language="es",
    sort_by="publishedAt",
    page_size=5
)
# devuelve dict con 'articles', cada uno con 'title', 'description', 'content'

print(articulos)