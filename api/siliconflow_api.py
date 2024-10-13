import requests
from config import SILICONFLOW_API_KEY, SILICONFLOW_API_URL, SILICONFLOW_MODEL_NAME

class SiliconFlowAPI:
    def __init__(self):
        self.model_name = SILICONFLOW_MODEL_NAME
        self.api_url = SILICONFLOW_API_URL
        self.api_key = SILICONFLOW_API_KEY

    def translate(self, text, system_prompt, requirements):
        url = f"{self.api_url}/v1/chat/completions"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Requirements: {requirements}\n\nText to translate: {text}"}
        ]
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": 1.3,
            "stream": False,
            "top_p": 0.7,
            "top_k": 50,
            "frequency_penalty": 0.5,
            "n": 1,
            "response_format": {"type": "json_object"}
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # 打印 API 输入
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
            
            # 打印 API 响应
            print("API Response:")
            print(result)
            
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            # Print the error details
            print(f"Error occurred: {str(e)}")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
            
            raise Exception(f"Translation failed: {str(e)}")