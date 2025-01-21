from .model_apis import (
    GLMAPI, QwenAPI, DeepseekAPI, KimiAPI,
    OpenAIAPI, ClaudeAPI, OllamaAPI
)
from config.api_config import API_CONFIGS, DEFAULT_API
from typing import List, Optional

class APIManager:
    def __init__(self, api_name=None):
        self.api_name = api_name or DEFAULT_API
        self.config = API_CONFIGS[self.api_name]
        self._init_api()
        
    def _init_api(self):
        """初始化选择的 API"""
        if self.api_name == "glm":
            self.api = GLMAPI(**self.config)
        elif self.api_name == "qwen":
            self.api = QwenAPI(**self.config)
        elif self.api_name == "deepseek":
            self.api = DeepseekAPI(**self.config)
        elif self.api_name == "kimi":
            self.api = KimiAPI(**self.config)
        elif self.api_name == "ollama":
            self.api = OllamaAPI(**self.config)
        elif self.api_name == "openai":
            self.api = OpenAIAPI(**self.config)
        elif self.api_name == "claude":
            self.api = ClaudeAPI(**self.config)
        else:
            raise ValueError(f"不支持的API: {self.api_name}")
    
    def get_available_apis(self) -> List[str]:
        """获取所有可用的API列表"""
        return list(API_CONFIGS.keys())
    
    def switch_api(self, api_name: str):
        """切换到其他API"""
        if api_name not in API_CONFIGS:
            raise ValueError(f"不支持的API: {api_name}")
        self.api_name = api_name
        self.config = API_CONFIGS[api_name]
        self._init_api()
    
    def get_response(self, prompt: str) -> Optional[str]:
        """获取模型响应"""
        return self.api.get_response(prompt)
        
    def list_local_models(self) -> List[str]:
        """获取本地可用的模型列表（仅支持 Ollama）"""
        if not isinstance(self.api, OllamaAPI):
            raise ValueError("只有 Ollama API 支持列出本地模型")
        return self.api.list_models()
        
    def switch_local_model(self, model_name: str) -> bool:
        """切换本地模型（仅支持 Ollama）"""
        if not isinstance(self.api, OllamaAPI):
            raise ValueError("只有 Ollama API 支持切换本地模型")
        return self.api.switch_model(model_name)
        
    def pull_model(self, model_name: str) -> bool:
        """拉取新的模型（仅支持 Ollama）"""
        if not isinstance(self.api, OllamaAPI):
            raise ValueError("只有 Ollama API 支持拉取新模型")
        return self.api.pull_model(model_name)