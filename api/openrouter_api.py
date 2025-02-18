from config import OPENROUTER_MODEL_NAME, OPENROUTER_API_URL, OPENROUTER_API_KEY
import requests

class OpenRouterAPI:
    def __init__(self):
        self.model_name = OPENROUTER_MODEL_NAME
        self.api_url = OPENROUTER_API_URL
        self.api_key = OPENROUTER_API_KEY

    def translate(self, text, system_prompt, requirements):
        url = f"{self.api_url}/api/v1/chat/completions"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Requirements: {requirements}\n\nText to translate: {text}"}
        ]
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "response_format": {"type": "json_object"}
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Print API input for debugging
        print("API Input:")
        print(f"URL: {url}")
        print("Headers:")
        print(headers)
        print("Payload:")
        print(payload)

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()
            
            # Print API response for debugging
            print("API Response:")
            print(result)
            
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            # Print error details
            print(f"Error occurred: {str(e)}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            raise Exception(f"Translation failed: {str(e)}")
