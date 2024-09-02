from src.providers.abstract_basellm import BaseLLMProvider
from src.utils.pydantic_to_json import transform_schema
import httpx 
from typing import List , Dict
import json 


class OpenAIProvider(BaseLLMProvider):
    def __init__(self , api_key:str)->None:
        super().__init__()
        self.base_url = "https://api.openai.com/v1/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Content-Type":"application/json",
            "Authorization" :f"Bearer {self.api_key}"
        }


    async def chat_completion(self , 
                              model:str , 
                              messages:List[str] ,):
        url = self.base_url
        headers = self.headers
        data = {
            "model":model,
            "messages" : messages ,
            "stream" : False, 
        }
        try:
            response = await self.client.post(url=url , json=data , headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e: 
            return f"ERROR {e}"
    



    async def structured_output(self , 
                              model:str , 
                              messages:List[str] , response_format):
        url = self.base_url
        headers = self.headers
        data = {
            "model":model,
            "messages" : messages ,
            "stream" : False, 
            "response_format" : transform_schema(response_format)
        }
        try:
            response = await self.client.post(url=url , json=data , headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e: 
            return f"ERROR {e}"

    async def function_call(self,model:str , messages:List[str] , tools:List[Dict], tool_choice:str|Dict):
        url = self.base_url
        headers = self.headers
        data = {
            "model" : model , 
            "messages" : messages , 
            "stream" : False , 
            "tools" : tools , 
            "tool_choice" : tool_choice
        }
        try:
            response = await self.client.post(url=url , json=data , headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e: 
            return f"ERROR {e}"
    
    async def stream_chat_completion(self,model:str , messages:List[str] ):
        url = self.base_url 
        headers = self.headers
        data = {
            "model" : model , 
            "messages" : messages , 
            "stream" : True , 
        }

        try:
            async with self.stream_client.stream("POST", url=url, json=data, headers=headers) as response:
                response.raise_for_status()
                buffer = b""
                async for chunk in response.aiter_bytes():
                    buffer += chunk
                    while b"\n\n" in buffer:
                        line, buffer = buffer.split(b"\n\n", 1)
                        line = line.decode('utf-8').strip()
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
        except httpx.RequestError as e :
            yield f"ERROR {e}"
        




