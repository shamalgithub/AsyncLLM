from fastapi import FastAPI
from routes import openai_route as openai_routes
from dotenv import load_dotenv


load_dotenv()
app = FastAPI(title="AsyncLLM", description="API for OpenAI and Claude models")
app.include_router(openai_routes.router, prefix="/openai", tags=["OpenAI"])
