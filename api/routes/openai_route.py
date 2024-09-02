from fastapi import APIRouter, Depends, HTTPException
from src.providers import get_provider
from models.openai_request_models import ChatCompletionRequest
import json 
import os

router = APIRouter()

def get_openai_provider():
    return get_provider(provider_name="openai", api_key=os.getenv("OPENAI_KEY"))

@router.post("/chat_completion")
async def chat_completion(request: ChatCompletionRequest, provider=Depends(get_openai_provider)):
    try:
        request_dict = json.loads(request.model_dump_json())
        print(request_dict)
        response = await provider.chat_completion(request_dict["model"], request_dict["messages"])
        return response 
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# @router.post("/function_call")
# async def function_call(request: FunctionCallRequest, provider=Depends(get_openai_provider)):
#     try:
#         response = await provider.function_call(request.model, request.messages, request.tools, request.tool_choice)
#         return response
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))