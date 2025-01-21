from .base_api import BaseAPI
import requests
import json
from typing import List, Optional

class OllamaAPI(BaseAPI):
    """Ollama API 实现"""
    
    def __init__(self, api_key: str, **kwargs):
        """
        初始化 Ollama API 客户端
        
        Args:
            api_key: API 密钥（Ollama 不需要，但为了统一接口保留）
            api_url: API 端点，默认为 http://localhost:11434
            model: 模型名称，默认为 llama2
            max_tokens: 最大生成的 token 数量
            temperature: 温度参数，控制输出的随机性
            **kwargs: 其他配置参数
        """
        super().__init__(api_key, **kwargs)
        self.api_url = kwargs.get('api_url', 'http://localhost:11434')
        self.model = kwargs.get('model', 'llama2')
        
    def get_response(self, prompt: str) -> str:
        """调用 Ollama 的 API"""
        url = f"{self.api_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "num_predict": self.max_tokens
            }
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Ollama API 调用错误: {str(e)}")
            return None
            
    def list_models(self) -> List[str]:
        """获取本地可用的模型列表"""
        url = f"{self.api_url}/api/tags"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return [model['name'] for model in response.json()['models']]
        except Exception as e:
            print(f"获取模型列表失败: {str(e)}")
            return []
            
    def switch_model(self, model_name: str) -> bool:
        """
        切换到其他本地模型
        
        Args:
            model_name: 要切换到的模型名称
            
        Returns:
            切换是否成功
        """
        if model_name in self.list_models():
            self.model = model_name
            return True
        print(f"模型 {model_name} 不存在，可用的模型有: {', '.join(self.list_models())}")
        return False
        
    def pull_model(self, model_name: str) -> bool:
        """
        拉取新的模型
        
        Args:
            model_name: 要拉取的模型名称，如 llama2:latest
            
        Returns:
            拉取是否成功
        """
        url = f"{self.api_url}/api/pull"
        try:
            response = requests.post(url, json={"name": model_name}, stream=True)
            response.raise_for_status()
            
            # 打印下载进度
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "status" in data:
                        print(f"下载进度: {data['status']}")
                    if "error" in data:
                        print(f"下载错误: {data['error']}")
                        return False
            return True
        except Exception as e:
            print(f"拉取模型失败: {str(e)}")
            return False
