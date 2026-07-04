from dotenv import load_dotenv
import os

load_dotenv()  # lee el .env y mete todo en os.environ automáticamente

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")