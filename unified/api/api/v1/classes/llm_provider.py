from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
import os
from logging import getLogger

log = getLogger('api.v1.classes.llm_provider')

PROVIDERS = {
    "gemini": {
        "llm_class": ChatGoogleGenerativeAI,
        "api_key": os.getenv("GEMINI_API_KEY")
    },
    "openai": {
        "llm_class": ChatOpenAI,
        "api_key": os.getenv("OPENAI_API_KEY")
    }
}

def get_provider(provider: str):
    if provider not in PROVIDERS.keys():
        raise ValueError(f"Invalid provider: {provider}")
    return PROVIDERS.get(provider)

class LLMProvider:
    def __init__(self, name: str, temperature: float = 0.7):
        self.provider = get_provider(name)
        self.temperature = temperature

    def get_model(self, model: str):
        log.info('getting model: %s', self.provider)
        return self.provider.get('llm_class')(
            model=model,
            temperature=self.temperature,
            api_key=self.provider.get('api_key')
        )