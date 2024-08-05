from openai_provider import OpenAIProvider
import asyncio
import os
from dotenv import load_dotenv
from typing import List
import json 

try:
    load_dotenv(r"/home/shamal/AsyncLLM/.env")
except FileNotFoundError:
    print("No .Env File found.Please add .env file")


api_key = os.environ.get("OPENAI_KEY")


async def main(api_key):
    async with OpenAIProvider(api_key=api_key) as provider:
        messages = [
        {
            "role" :"system" ,
            "content" : "you are a helpful assistant"
        } ,
        {
            'role' : "user" ,
            "content": f"hello there"
        } ] 
        try:
            response = await provider.chat_completion(
                model="gpt-4o-mini",
                messages=messages
            )
            print(response)
        except Exception as e:
            print("ERROR" , e)

asyncio.run(main(api_key=api_key))
