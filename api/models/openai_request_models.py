from pydantic import BaseModel
from typing import List, Dict, Any

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]
    
