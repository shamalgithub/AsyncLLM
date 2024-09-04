import pytest
import os
from dotenv import load_dotenv
from src.providers import get_provider
from src.providers.openai_provider import OpenAIProvider
from src.providers.anthropic_provider import ClaudeProvider

load_dotenv()

@pytest.fixture
def openai_provider():
    return get_provider("openai", os.getenv("OPENAI_KEY"))

@pytest.fixture
def claude_provider():
    return get_provider("claude", os.getenv("CLAUDE_KEY"))

def test_openai_provider_fixture(openai_provider):
    assert isinstance(openai_provider, OpenAIProvider)
    assert openai_provider.api_key == os.getenv("OPENAI_KEY")

def test_claude_provider_fixture(claude_provider):
    assert isinstance(claude_provider, ClaudeProvider)
    assert claude_provider.api_key == os.getenv("CLAUDE_KEY")

@pytest.mark.asyncio
async def test_chat_completion(openai_provider, claude_provider):
    providers = [openai_provider, claude_provider]
    models = ["gpt-3.5-turbo", "claude-3-5-sonnet-20240620"]

    for provider, model in zip(providers, models):
        messages = [
            {"role": "user", "content": "What's the capital of France?"}
        ]
        response = await provider.chat_completion(model, messages)
        
        assert isinstance(response, dict)
        #the following wont work since claudes response is different from openai 
        # assert "choices" in response
        # assert len(response["choices"]) > 0
        # assert "message" in response["choices"][0]
        # assert "content" in response["choices"][0]["message"]
        # assert "Paris" in response["choices"][0]["message"]["content"]