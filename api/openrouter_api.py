from config import OPENROUTER_MODEL_NAME, OPENROUTER_API_URL, OPENROUTER_API_KEY

class OpenRouterAPI:
    def __init__(self):
        self.model_name = OPENROUTER_MODEL_NAME
        self.api_url = OPENROUTER_API_URL
        self.api_key = OPENROUTER_API_KEY

    def translate(self, text, system_prompt, requirements):
        pass
