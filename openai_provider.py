from abstract_basellm import BaseLLMProvider
import httpx 
from typing import List 

class OpenAIProvider(BaseLLMProvider):
    def __init__(self , api_key:str)->None:
        super().__init__()
        self.base_url = "https://api.openai.com/v1"
        self.api_key = api_key

    async def chat_completion(self , 
                              model:str , 
                              messages:List[str] ,):
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Content-Type":"application/json",
            "Authorization" :f"Bearer {self.api_key}"
        }
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
