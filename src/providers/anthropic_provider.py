from src.providers.abstract_basellm import BaseLLMProvider
import httpx
from typing import List, Dict
import json


class ClaudeProvider(BaseLLMProvider):
    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.api_key = api_key
        self.headers = {
            "content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
    
  
    async def chat_completion(self, 
                              model: str, 
                              messages: List[Dict[str, str]],
                              max_tokens: int = 1024):
        url = self.base_url
        headers = self.headers
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens # MAX TOKENS ARE REQUIRED !! 
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url=url, json=data, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.RequestError as e:
            return f"ERROR {e}"

    async def stream_chat_completion(self, model: str, messages: List[Dict[str, str]], max_tokens: int = 1024):
        url = self.base_url
        headers = self.headers
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens, # MAX TOKENS ARE REQUIRED !! 
            "stream": True
        }

        try:
            async with httpx.AsyncClient() as client:
                async with client.stream("POST", url=url, json=data, headers=headers) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            line = line[6:]
                            if line == "[DONE]":
                                yield "Stream Complete"
                            else:
                                try:
                                    chunk_data = json.loads(line)
                                    yield json.dumps(chunk_data, indent=2)
                                except json.JSONDecodeError:
                                    yield f"ERROR decoding line {line}"
        except httpx.RequestError as e:
            yield f"ERROR {e}"

