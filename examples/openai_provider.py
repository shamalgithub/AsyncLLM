import asyncio
import os
from dotenv import load_dotenv
from src.providers import get_provider
import logging
from pydantic import BaseModel
import sys 
"""
OpenAI Provider Usage Examples

This script demonstrates the usage of the OpenAI provider for various API calls:
1. Chat Completion: Simple question-answering.
2. Function Call: Demonstrating function calling capability.
3. Streaming Chat Completion: Receiving responses in chunks.

The script uses asyncio to run these examples concurrently, showcasing
the asynchronous nature of the API calls.

Usage:
    Ensure the OPENAI_KEY environment variable is set or present in a .env file.
    Run the script to see outputs from all three types of API calls.

Note: 
    This is an example file and should not be used in production without proper
    error handling and security measures.
"""

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

try:
    openai_provider = get_provider(provider_name="openai", api_key=os.getenv("OPENAI_KEY"))
except ValueError as e:
    logger.error(f"Failed to initialize OpenAI provider: {e}")
    exit(1)

async def chat_completion_example():
    try:
        model = "gpt-3.5-turbo"
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What's the capital of France?"}
        ]
        response = await openai_provider.chat_completion(model, messages)
        logger.info(f"Chat Completion Response: {response}")
    except Exception as e:
        logger.error(f"Error in chat completion: {e}")

async def structured_output_example():

    class Step(BaseModel):
        explanation: str
        output: str


    class MathResponse(BaseModel):
        steps: list[Step]
        final_answer: str

    try:
        model = "gpt-4o-mini"
        messages = [
            {"role": "system", "content": "You are a helpful math tutor."},
            {"role": "user", "content": "solve 8x+31 = 2"}
        ]
        response = await openai_provider.structured_output(model, messages , response_format=MathResponse)
        logger.info(f"Structured Output Response: {response}")
    except Exception as e:
        logger.error(f"Error in Structured Output completion: {e}")




async def function_call_example():
    try:
        model = "gpt-4-turbo"
        messages = [
            {"role": "user", "content": "Translate 'Hello, how are you?' to French."}
        ]
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "translate_text",
                    "description": "Translate text from one language to another",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "The text to be translated"},
                            "source_language": {"type": "string", "description": "The language of the input text (ISO 639-1 code)"},
                            "target_language": {"type": "string", "description": "The language to translate into (ISO 639-1 code)"}
                        },
                        "required": ["text", "target_language"]
                    }
                }
            }
        ]
        tool_choice = {"type": "function", "function": {"name": "translate_text"}}
        
        response = await openai_provider.function_call(model, messages, tools, tool_choice)
        logger.info(f"Function Call Response: {response}")
    except Exception as e:
        logger.error(f"Error in function call: {e}")

async def stream_chat_completion_example():
    try:
        model = "gpt-3.5-turbo"
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a short poem about coding."}
        ]
        async for chunk in openai_provider.stream_chat_completion(model, messages):
            logger.info(f"Streamed Chunk: {chunk}")
    except Exception as e:
        logger.error(f"Error in stream chat completion: {e}")

async def main():
    tasks = [
        # asyncio.create_task(chat_completion_example()),
        asyncio.create_task(function_call_example()),
        #asyncio.create_task(stream_chat_completion_example()),
        asyncio.create_task(structured_output_example())
    ]
    
    try:
        await asyncio.gather(*tasks)
    except Exception as e:
        logger.error(f"Error in main execution: {e}")



if __name__ == "__main__":
    asyncio.run(main())