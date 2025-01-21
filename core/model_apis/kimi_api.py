from .base_api import BaseAPI
import requests

class KimiAPI(BaseAPI):
    """Kimi API 实现"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = kwargs.get('api_url', 'https://api.moonshot.cn/v1/chat/completions')
        self.model = kwargs.get('model', 'moonshot-v1-8k')
        
    def get_response(self, prompt):
        """调用 Kimi 的 API"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Kimi API调用错误: {str(e)}")
            return None 