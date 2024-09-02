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