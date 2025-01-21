from .base_api import BaseAPI
import requests
import json

class GLMAPI(BaseAPI):
    """GLM API 实现"""
    
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_url = kwargs.get('api_url', 'https://open.bigmodel.cn/api/paas/v4/chat/completions')
        self.model = kwargs.get('model', 'glm-4v')
        
    def get_response(self, prompt):
        """调用 GLM 的 API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            "temperature": 0.7,
            "top_p": 0.7,
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content']
        except Exception as e:
            print(f"GLM API 调用错误: {str(e)}")
            return None 