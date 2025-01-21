import os
from config.config import CORE_FILE_PATTERNS, SUPPORTED_LANGUAGES
from .keyword_matcher import KeywordMatcher

class FileAnalyzer:
    @staticmethod
    def is_core_file(file_path, language, question=""):
        """判断是否为核心文件
        
        Args:
            file_path: 文件路径
            language: 编程语言
            question: 题目要求（可选）
        
        Returns:
            bool: 是否为核心文件
        """
        try:
            patterns = CORE_FILE_PATTERNS.get(language, {})
            if not patterns:
                return True  # 如果没有配置，则认为所有文件都是核心文件
            
            file_name = os.path.basename(file_path)
            name_without_ext = os.path.splitext(file_name)[0].lower()
            rel_path = os.path.relpath(file_path, os.path.dirname(file_path)).lower()
            
            # 检查是否为测试文件
            if any(p.lower() in name_without_ext for p in patterns.get('test_patterns', [])):
                return False
                
            # 检查是否为忽略文件
            if any(p.lower() in name_without_ext for p in patterns.get('ignore_patterns', [])):
                return False
            
            # 检查是否为核心文件
            is_core = any(p.lower() in rel_path for p in patterns.get('core_patterns', []))
            
            # 如果有题目要求，检查文件名是否与题目关键词相关
            if question and not is_core:
                # 提取题目关键词及其相似词
                keywords = KeywordMatcher.extract_keywords(question)
                # 检查文件名是否包含任何关键词或其相似词
                for keyword in keywords:
                    if KeywordMatcher.similar(keyword, name_without_ext):
                        is_core = True
                        break
            
            return is_core
            
        except Exception as e:
            print(f"核心文件判断错误: {str(e)}")
            return True  # 出错时保守处理，认为是核心文件

    @staticmethod
    def get_file_type(file_path):
        """获取文件类型
        
        Args:
            file_path: 文件路径
            
        Returns:
            str: 文件类型（如 python, java 等）
        """
        try:
            _, ext = os.path.splitext(file_path)
            ext = ext.lower() if ext else ""
            
            # 根据扩展名查找对应的语言类型
            for lang, config in SUPPORTED_LANGUAGES.items():
                if config['file_extension'] == ext:
                    return lang
            return None
        except Exception as e:
            print(f"获取文件类型错误: {str(e)}")
            return None

    @staticmethod
    def is_project_directory(directory):
        """判断是否为项目目录
        
        Args:
            directory: 目录路径
            
        Returns:
            bool: 是否为项目目录
        """
        try:
            # 检查目录下是否有支持的语言类型的文件
            for root, _, files in os.walk(directory):
                for file in files:
                    file_type = FileAnalyzer.get_file_type(file)
                    if file_type in SUPPORTED_LANGUAGES:
                        return True
            return False
        except Exception as e:
            print(f"项目目录判断错误: {str(e)}")
            return False
