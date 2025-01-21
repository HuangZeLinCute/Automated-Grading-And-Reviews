from typing import Optional, Dict, Any
from anthropic import Anthropic
from .base_api import BaseAPI
import json

class ClaudeAPI(BaseAPI):
    """Claude API 实现"""
    
    def __init__(self, api_key: str, **kwargs):
        """
        初始化 Claude API 客户端
        
        Args:
            api_key: Anthropic API 密钥
            **kwargs: 其他配置参数，如 model 等
        """
        super().__init__(api_key, **kwargs)
        self.client = Anthropic(api_key=api_key)
        self.model = kwargs.get('model', 'claude-3-opus-20240229')
        self.max_tokens = kwargs.get('max_tokens', 4000)
        self.temperature = kwargs.get('temperature', 0.7)
        
    def get_response(self, prompt: str) -> str:
        """
        调用 Claude 的 API
        
        Args:
            prompt: 用户输入的提示
        
        Returns:
            生成的回复文本
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.content[0].text
        except Exception as e:
            raise ConnectionError(f"Claude API 调用失败: {str(e)}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        获取模型信息
        
        Returns:
            包含模型信息的字典
        """
        return {
            "name": "Claude",
            "model": self.model,
            "type": "chat",
            "capabilities": ["chat", "code", "analysis", "reasoning"]
        }
