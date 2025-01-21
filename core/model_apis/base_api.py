from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class BaseAPI(ABC):
    """基础 API 接口类，定义所有 LLM API 必须实现的方法"""
    
    @abstractmethod
    def __init__(self, api_key: str, **kwargs):
        """
        初始化 API 客户端
        
        Args:
            api_key: API 密钥
            api_url: API 端点
            model: 模型名称
            max_tokens: 最大生成的 token 数量
            temperature: 温度参数，控制输出的随机性
            **kwargs: 其他配置参数
        """
        self.api_key = api_key
        self.api_url = kwargs.get('api_url')
        self.model = kwargs.get('model')
        self.max_tokens = kwargs.get('max_tokens', 2000)
        self.temperature = kwargs.get('temperature', 0.7)
        self.kwargs = kwargs
    
    @abstractmethod
    def get_response(self, prompt: str) -> str:
        """
        获取模型响应
        
        Args:
            prompt: 用户输入的提示
            
        Returns:
            模型生成的回复文本
        """
        pass