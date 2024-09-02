import asyncio
import logging
import os
from dotenv import load_dotenv
from src.providers import get_provider  # Adjust this import based on your project structure

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

try:
    claude_provider = get_provider(provider_name="claude", api_key=os.getenv("CLAUDE_KEY"))
except ValueError as e:
    logger.error(f"Failed to initialize Claude provider: {e}")
    exit(1)

async def chat_completion_example():
    try:
        model = "claude-3-5-sonnet-20240620"
        messages = [
            {"role": "user", "content": "Hello , Claude"}
        ]
        response = await claude_provider.chat_completion(model, messages)
        logger.info(f"Chat Completion Response: {response}")
    except Exception as e:
        logger.error(f"Error in chat completion: {e}")

async def stream_chat_completion_example():
    try:
        model = "claude-3-5-sonnet-20240620"
        messages = [
            {"role": "user", "content": "Write a short poem about artificial intelligence."}
        ]
        async for chunk in claude_provider.stream_chat_completion(model, messages):
            logger.info(f"Streamed Chunk: {chunk}")
    except Exception as e:
        logger.error(f"Error in stream chat completion: {e}")

async def main():
    tasks = [
        asyncio.create_task(chat_completion_example()),
        asyncio.create_task(stream_chat_completion_example())
    ]
    
    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"Error in main execution: {e}")

if __name__ == "__main__":
    asyncio.run(main())