# API 配置
API_CONFIGS = {
    "ollama": {
        "api_key": "",
        "api_url": "http://localhost:11434",
        "model": "llama3.1",
        "max_tokens": 2000,
        "temperature": 0.7
    },
    "glm": {
        "api_key": "your-glm-api-key",
        "api_url": "https://open.bigmodel.cn/api/paas/v4/chat/completions",
        "model": "glm-4v",
        "max_tokens": 8000,
        "temperature": 0.7
    },
    "qwen": {
        "api_key": "your-qwen-api-key",
        "api_url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
        "model": "qwen-72b-chat",
        "max_tokens": 4000,
        "temperature": 0.7
    },
    "deepseek": {
        "api_key": "",
        "api_url": "https://api.deepseek.com/v1/chat/completions",
        "model": "deepseek-coder",
        "max_tokens": 4000,
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    },
    "kimi": {
        "api_key": "",
        "api_url": "https://api.moonshot.cn/v1/chat/completions",
        "model": "moonshot-v1-8k",
        "max_tokens": 8000,
        "temperature": 0.7
    },
    "openai": {
        "api_key": "your-openai-api-key",
        "api_url": "https://api.openai.com/v1/chat/completions",
        "model": "gpt-4-turbo-preview",
        "max_tokens": 4000,
        "temperature": 0.7
    },
    "claude": {
        "api_key": "your-anthropic-api-key",
        "api_url": "https://api.anthropic.com/v1/messages",
        "model": "claude-3-opus-20240229",
        "max_tokens": 4000,
        "temperature": 0.7
    }
}

# 默认使用的 API
DEFAULT_API = "deepseek"