from .base_api import BaseAPI
import dashscope
from dashscope import Generation
from http import HTTPStatus

class QwenAPI(BaseAPI):
    """Qwen API 实现"""
    
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key, **kwargs)
        dashscope.api_key = self.api_key
        self.model = kwargs.get('model', 'qwen-72b-chat')
        
    def get_response(self, prompt):
        """调用 Qwen 的 API"""
        try:
            response = Generation.call(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': prompt}
                ],
                result_format='message'
            )
            
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0]['message']['content']
            else:
                print(f'请求失败: {response.code}, {response.message}')
                return None
                
        except Exception as e:
            print(f"Qwen API 调用错误: {str(e)}")
            return None 