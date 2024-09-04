from pydantic import BaseModel , Field
from typing import List, Dict, Any , Literal

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Message]

class FunctionParameters(BaseModel):
    type: str = Field(default="object") #Not needed for correct functionality 
    properties: Dict[str, Dict[str, Any]]
    required: List[str] = Field(default_factory=list) #Not needed for correct functionality 

class Function(BaseModel):
    name: str 
    description: str 
    parameters: FunctionParameters

class Tool(BaseModel):
    type: Literal['function']
    function: Function

class ToolChoice(BaseModel):
    type: Literal["function"]
    function: Dict[str, str]

class FunctionCallRequest(ChatCompletionRequest):
    tools: List[Tool]
    tool_choice: ToolChoice




    
