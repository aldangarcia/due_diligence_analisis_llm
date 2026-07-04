from langchain_core.tools import tool
from langchain_tavily import TavilySearch
import yfinance as yf
from newsapi import NewsApiClient
import os

from dotenv import load_dotenv
load_dotenv()

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def fetch_yfinance_news(symbol: str) -> list[str]:
    ticker = yf.Ticker(symbol)
    noticias = ticker.news
    textos = []
    for n in noticias:
        titulo = n.get("content", {}).get("title", "")
        resumen = n.get("content", {}).get("summary", "")
        textos.append(f"{titulo}. {resumen}")
    return textos

def fetch_tavily_news(company_name: str) -> list[str]:
    tavily = TavilySearch(max_results=5)
    resultados = tavily.invoke(company_name)
    return [r["content"] for r in resultados]

def fetch_newsapi_news(company_name: str) -> list[str]:
    newsapi = NewsApiClient(api_key=os.getenv("NEWSAPI_KEY"))
    response = newsapi.get_everything(q=company_name, language="es", page_size=5)
    textos = []
    for articulo in response["articles"]:
        titulo = articulo.get("title", "")
        descripcion = articulo.get("description", "")
        textos.append(f"{titulo}. {descripcion}")
    return textos

def build_retriever(textos: list[str]):
    # convertimos cada texto en un Document
    documentos = [Document(page_content=t) for t in textos if t.strip()]
    # troceamos
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split_documents(documentos)
    # embeddings + vectorstore
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def formatear_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

@tool
def get_sentiment(symbol: str, company_name: str, consulta: str) -> str:
    """
    Looks and analyze news from the company and recent opinions from experts. Gets the news from 
    yfinance, Tavily and NewsAPI, vectorize them and gives the more relevant parts for the query made.
    """
    texts = {
        fetch_yfinance_news(symbol) +
        fetch_tavily_news(company_name) +
        fetch_newsapi_news(company_name)
    }

    retriver = build_retriever(texts)

    docs = retriver.invoke(consulta)

    return formatear_docs(docs)