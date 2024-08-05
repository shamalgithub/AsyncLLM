import httpx 
from abc import ABC  , abstractmethod


class BaseLLMProvider(ABC):
    def __init__(self) -> None: 
        self.client = httpx.AsyncClient(http2=True)
    async def __aenter__(self):
        return self 
    async def __aexit__(self , exc_type , exc_val , exc_tb):
        await  self.client.aclose()


        
        



    
    