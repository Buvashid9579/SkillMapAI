import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_tavily import TavilySearch

# Load environment variables
load_dotenv()

# API Keys
GOOGLE_API_KEY = os.getenv("GEMINI_API")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")

# Validate keys
if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API key not found in .env")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env")

if not RAPID_API_KEY:
    raise ValueError("RAPID_API_KEY not found in .env")

# Gemini Model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)

# Tavily Search Tool
tavily = TavilySearch(
    max_results=5,
    topic="general",
    search_depth="advanced",
    tavily_api_key=TAVILY_API_KEY,
)