import requests
import json
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, DEEPSEEK_MODEL_NAME
class DeepSeekAPI:
    def __init__(self):
        self.base_url = DEEPSEEK_API_URL + "/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
        }

    def translate(self, text, target_language, system_prompt, requirements=None):
        try:
            user_content = f"Translate the following text to {target_language}."
            if requirements:
                user_content += f" Requirements: {requirements}"
            user_content += f"\n\nText: {text}"

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ]
            
            payload = {
                "model": DEEPSEEK_MODEL_NAME,
                "messages": messages,
                "stream": False,
                "temperature": 1.3,
                "response_format": {
                    'type': 'json_object'
                }
            }
            
            response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            
            result = response.json()
            print("Full DeepSeek API response:")
            print(json.dumps(result, indent=2))
            
            return result['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"DeepSeek API translation error: {str(e)}")
            return None