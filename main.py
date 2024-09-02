from openai_provider import OpenAIProvider
import asyncio
import os
from dotenv import load_dotenv
from typing import List
import json 
from pydantic import BaseModel , Field 
try:
    load_dotenv(r"/home/shamal/AsyncLLM/.env")
except FileNotFoundError:
    print("No .Env File found.Please add .env file")


api_key = os.environ.get("OPENAI_KEY")
class isQuestion(BaseModel):
    is_question :bool = Field(... , description="is the user requestion a question or not")

tool_extract_yandx_columns = {
    "type" : "function" ,
    "function" : {
        "name" : "is_user_request_ambiguous" , 
        "description" : "Given a user request decide if the user request is ambigous or not" ,
        "parameters" : isQuestion.model_json_schema()
    }}

async def main(api_key):


    async with OpenAIProvider(api_key=api_key) as provider:
        messages = [
            {
                "role":"system",
                "content" : "you are helpful assistant"
            },
            {
                "role":"user",
                "content": "Explain asyncio to me like am 5"
            }
        ]
        async for chunk in provider.stream_chat_completion(model='gpt-4o-mini' , messages=messages):
            print(f"chunk :{chunk}" )
        print("stream completed")



class Step(BaseModel):

    explanation: str
    output: str

class MathResponse(BaseModel):

    steps: list[Step]
    final_answer: str




response_format = {
    "type": "json_schema",
    "json_schema": {
      "name": "math_response",
      "strict": True,
      "schema": {
        "type": "object",
        "properties": {
          "steps": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "explanation": {
                  "type": "string"
                },
                "output": {
                  "type": "string"
                }
              },
              "required": ["explanation", "output"],
              "additionalProperties": False
            }
          },
          "final_answer": {
            "type": "string"
          }
        },
        "required": ["steps", "final_answer"],
        "additionalProperties": False
      }
    }
  }

# from test_2 import convert_pydantic_schema

# response_format = {
#     "type": "json_schema",
#     "json_schema": {
#       "name": "math_response",
#       "strict": True,
#       "schema": str((convert_pydantic_schema(MathResponse.model_json_schema()))['schema'])
#   }
# }

# print(MathResponse.model_json_schema())


async def structured_function(api_key):
    async with OpenAIProvider(api_key=api_key) as provider:
        messages = [
            {
                "role":"system" ,
                "content": "you are a helpful assistant"
            } ,
            {
                "role":"user",
                "content":"how to solve 3x + 6 = 12"
            }
        ]

    

        response = await provider.structured_output(model='gpt-4o-2024-08-06' , response_format=response_format , messages=messages)
        print (response)




asyncio.run(structured_function(api_key=api_key))
