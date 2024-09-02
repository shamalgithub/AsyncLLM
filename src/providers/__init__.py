from .openai_provider import OpenAIProvider
from .anthropic_provider import ClaudeProvider

def get_supported_providers():
    supported_providers = ['openai' , 'claude']
    return f"The following LLM providers are supported \n {supported_providers}"

def get_provider(provider_name: str, api_key: str):
    
    if provider_name.lower() == "openai":
        return OpenAIProvider(api_key=api_key)
    elif provider_name.lower() == "claude":
        return ClaudeProvider(api_key=api_key)
    else:
        raise ValueError(f"Unknown provider: {provider_name}. \nSupported Providers : {get_supported_providers()}")
    

