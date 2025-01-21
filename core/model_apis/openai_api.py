from typing import Optional, Dict, Any
from openai import OpenAI
from .base_api import BaseAPI
import json

class OpenAIAPI(BaseAPI):
    """OpenAI API 实现"""
    
    def __init__(self, api_key: str, **kwargs):
        """
        初始化 OpenAI API 客户端
        
        Args:
            api_key: OpenAI API 密钥
            **kwargs: 其他配置参数，如 model, api_base 等
        """
        super().__init__(api_key, **kwargs)
        self.client = OpenAI(api_key=api_key)
        self.model = kwargs.get('model', 'gpt-4-turbo-preview')
        self.max_tokens = kwargs.get('max_tokens', 4000)
        self.temperature = kwargs.get('temperature', 0.7)
        
    def get_response(self, prompt: str) -> str:
        """
        调用 OpenAI 的 API
        
        Args:
            prompt: 用户输入的提示
        
        Returns:
            生成的回复文本
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ConnectionError(f"OpenAI API 调用失败: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            包含模型信息的字典
        """
        return {
            "name": "OpenAI",
            "model": self.model,
            "type": "chat",
            "capabilities": ["chat", "code", "analysis"]
        }
