from .base_api import BaseAPI
import requests
import re
import json

class DeepseekAPI(BaseAPI):
    """Deepseek API 实现"""
    
    def __init__(self, api_key, **kwargs):
        super().__init__(api_key, **kwargs)
        self.api_url = kwargs.get('api_url', 'https://api.deepseek.com/v1/chat/completions')
        self.model = kwargs.get('model', 'deepseek-chat')
        self.temperature = kwargs.get('temperature', 0.7)
        self.max_tokens = kwargs.get('max_tokens', 2000)
        self.messages = []  # 存储对话历史
        
    def get_response(self, prompt):
        """调用 Deepseek 的 API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # 添加系统消息来要求JSON格式输出
        system_message = {
            "role": "system",
            "content": "请以JSON格式返回评分结果，包含total_score、details和feedback字段。"
        }
        
        # 添加新的用户消息
        user_message = {
            "role": "user",
            "content": prompt
        }
        
        # 构建消息历史
        messages = [system_message]
        messages.extend(self.messages)
        messages.append(user_message)
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "response_format": {"type": "json_object"}  # 使用正确的格式
        }
        
        try:
            print(f"\n调试信息 - 发送到Deepseek API的请求:")
            print(f"URL: {self.api_url}")
            print(f"Headers: {headers}")
            print(f"Data: {data}\n")
            
            response = requests.post(self.api_url, headers=headers, json=data)
            
            print(f"调试信息 - Deepseek API响应:")
            print(f"Status Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            print(f"Response Body: {response.text}\n")
            
            response.raise_for_status()
            result = response.json()
            
            # 从响应中提取文本内容
            assistant_message = result['choices'][0]['message']
            content = assistant_message.get('content', '')
            
            # 清理响应内容中的Markdown格式
            if content:
                # 移除可能的Markdown代码块标记
                content = re.sub(r'^```json\s*', '', content)
                content = re.sub(r'\s*```$', '', content)
                # 尝试解析JSON字符串
                try:
                    content = json.loads(content)
                    content = json.dumps(content)  # 重新序列化为标准JSON字符串
                except json.JSONDecodeError:
                    pass  # 如果不是JSON格式，保持原样
            
            # 将助手的回复添加到对话历史
            if content:
                self.messages.append(user_message)  # 保存用户消息
                self.messages.append({              # 保存助手回复
                    "role": "assistant",
                    "content": content
                })
            
            return content
            
        except requests.exceptions.RequestException as e:
            print(f"Deepseek API 请求错误: {str(e)}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"错误响应: {e.response.text}")
            return None
        except Exception as e:
            print(f"Deepseek API 错误: {str(e)}")
            return None
            
    def reset_conversation(self):
        """重置对话历史"""
        self.messages = [] 