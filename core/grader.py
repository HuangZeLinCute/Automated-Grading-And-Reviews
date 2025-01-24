from config.config import PROMPTS, SCORE_RANGES, TOKEN_CONFIG
from utils.submission_handler import SubmissionHandler
from utils.file_analyzer import FileAnalyzer
from utils.result_handler import ResultHandler
import json
import re

class Grader:
    def __init__(self, api_manager=None):
        self.api_manager = api_manager

    def grade_code(self, file_path, question, language):
        """对单个代码文件进行评分"""
        # 重置对话历史
        if hasattr(self.api_manager.api, 'reset_conversation'):
            self.api_manager.api.reset_conversation()
            
        code = SubmissionHandler.read_submission(file_path)
        if not code:
            return None
            
        prompt = PROMPTS["grade_code"].format(
            code=code,
            question=question,
            language=language
        )
        
        response = self.api_manager.get_response(prompt)
        print(f"\n调试信息 - API响应:\n{response}\n")  # 添加调试信息
        
        try:
            scores = self._parse_grading_response(response)
            scores['grade_level'] = self.get_grade_level(scores['total_score'])
            scores['language'] = language
            return scores
        except Exception as e:
            print(f"解析评分结果时出错: {e}")
            print(f"原始响应内容: {response}")  # 添加原始响应内容
            return None

    def grade_project(self, project_path, question, language):
        """对工程项目进行评分"""
        # 重置对话历史
        if hasattr(self.api_manager.api, 'reset_conversation'):
            self.api_manager.api.reset_conversation()
            
        # 读取项目文件
        files = SubmissionHandler.read_submission(project_path)
        if not files:
            return None
        
        # 处理项目文件（识别核心文件并分段）
        code_sections = []
        total_chars = 0
        current_section = ""
        
        for file_path, content in files.items():
            # 检查是否为核心文件
            if not FileAnalyzer.is_core_file(file_path, language, question):
                continue
                
            # 添加文件标识符
            file_content = f"# {file_path}\n{content}\n\n"
            
            # 如果添加这个文件会超出token限制，创建新的section
            if (total_chars + len(file_content)) > TOKEN_CONFIG['chars_per_token'] * TOKEN_CONFIG['batch_size']:
                if current_section:
                    code_sections.append(current_section)
                current_section = file_content
                total_chars = len(file_content)
            else:
                current_section += file_content
                total_chars += len(file_content)
        
        # 添加最后一个section
        if current_section:
            code_sections.append(current_section)
        
        # 分段评分
        section_scores = []
        for i, code in enumerate(code_sections):
            prompt = PROMPTS["grade_project"].format(
                code=code,
                question=question,
                language=language
            )
            response = self.api_manager.get_response(prompt)
            
            try:
                scores = self._parse_project_grading_response(response)
                section_scores.append(scores)
            except Exception as e:
                print(f"解析第{i+1}段评分结果时出错: {e}")
                continue
        
        if not section_scores:
            return None
        
        # 合并评分结果
        final_scores = ResultHandler.merge_results(section_scores)
        final_scores['grade_level'] = self.get_grade_level(final_scores['total_score'])
        final_scores['language'] = language
        return final_scores

    def grade_frontend(self, submission_path, question):
        """对前端作业进行评分"""
        # 重置对话历史
        if hasattr(self.api_manager.api, 'reset_conversation'):
            self.api_manager.api.reset_conversation()
            
        # 读取前端文件
        files = SubmissionHandler.read_frontend_submission(submission_path)
        if not files:
            return None
        
        # 处理项目文件
        code_sections = []
        total_chars = 0
        current_section = ""
        
        for file_path, content in files.items():
            # 添加文件标识符
            file_content = f"# {file_path}\n{content}\n\n"
            
            # 如果添加这个文件会超出token限制，创建新的section
            if (total_chars + len(file_content)) > TOKEN_CONFIG['chars_per_token'] * TOKEN_CONFIG['batch_size']:
                if current_section:
                    code_sections.append(current_section)
                current_section = file_content
                total_chars = len(file_content)
            else:
                current_section += file_content
                total_chars += len(file_content)
        
        # 添加最后一个section
        if current_section:
            code_sections.append(current_section)
        
        # 分段评分
        section_scores = []
        for i, code in enumerate(code_sections):
            prompt = PROMPTS["grade_frontend"].format(
                code=code,
                question=question
            )
            response = self.api_manager.get_response(prompt)
            
            try:
                scores = self._parse_frontend_grading_response(response)
                section_scores.append(scores)
            except Exception as e:
                print(f"解析第{i+1}段评分结果时出错: {e}")
                continue
        
        if not section_scores:
            return None
        
        # 合并评分结果
        final_scores = ResultHandler.merge_results(section_scores)
        final_scores['grade_level'] = self.get_grade_level(final_scores['total_score'])
        final_scores['language'] = 'html'
        return final_scores

    def grade_wxapp(self, project_path, question):
        """对微信小程序项目进行评分"""
        # 重置对话历史
        if hasattr(self.api_manager.api, 'reset_conversation'):
            self.api_manager.api.reset_conversation()
            
        # 读取小程序项目文件
        files = SubmissionHandler.read_wxapp_submission(project_path)
        if not files:
            return None
        
        # 处理项目文件
        code_sections = []
        total_chars = 0
        current_section = ""
        
        for file_path, content in files.items():
            # 添加文件标识符
            file_content = f"# {file_path}\n{content}\n\n"
            
            # 如果添加这个文件会超出token限制，创建新的section
            if (total_chars + len(file_content)) > TOKEN_CONFIG['chars_per_token'] * TOKEN_CONFIG['batch_size']:
                if current_section:
                    code_sections.append(current_section)
                current_section = file_content
                total_chars = len(file_content)
            else:
                current_section += file_content
                total_chars += len(file_content)
        
        # 添加最后一个section
        if current_section:
            code_sections.append(current_section)
        
        # 分段评分
        section_scores = []
        for i, code in enumerate(code_sections):
            prompt = PROMPTS["grade_wxapp"].format(
                code=code,
                question=question
            )
            response = self.api_manager.get_response(prompt)
            
            try:
                scores = self._parse_wxapp_grading_response(response)
                section_scores.append(scores)
            except Exception as e:
                print(f"解析第{i+1}段评分结果时出错: {e}")
                continue
        
        if not section_scores:
            return None
        
        # 合并评分结果
        final_scores = ResultHandler.merge_results(section_scores)
        final_scores['grade_level'] = self.get_grade_level(final_scores['total_score'])
        final_scores['language'] = 'wxapp'
        return final_scores

    def _parse_grading_response(self, response):
        """解析评分结果"""
        try:
            if not response:
                raise ValueError("API返回空响应")
                
            # 提取JSON部分
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if not json_match:
                raise ValueError("未找到有效的JSON内容")
                
            json_content = json_match.group(0)
            
            # 尝试解析JSON
            try:
                result = json.loads(json_content)
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                print(f"原始响应内容: {response}")
                raise
            
            # 验证总分
            if not isinstance(result.get('total_score'), (int, float)):
                raise ValueError("总分必须是数字")
                
            # 验证详细得分
            details = result.get('details', {})
            required_fields = ['code_correctness', 'code_style', 'code_efficiency']
            if not all(k in details for k in required_fields):
                raise ValueError(f"详细得分缺少必要维度: {required_fields}")
            
            return {
                "total_score": result['total_score'],
                "details": details,
                "feedback": result.get('feedback', {})
            }
            
        except Exception as e:
            print(f"评分解析错误: {str(e)}")
            # 返回默认值
            return {
                "total_score": 0,
                "details": {
                    "code_correctness": 0,
                    "code_style": 0,
                    "code_efficiency": 0
                },
                "feedback": {
                    "correctness_feedback": "评分解析失败",
                    "style_feedback": "评分解析失败",
                    "efficiency_feedback": "评分解析失败"
                }
            }

    def _parse_project_grading_response(self, response):
        """解析项目评分结果"""
        try:
            # 尝试解析JSON
            result = json.loads(response)
            
            # 验证总分
            if not isinstance(result.get('total_score'), (int, float)):
                raise ValueError("总分必须是数字")
                
            # 验证详细得分
            details = result.get('details', {})
            required_fields = ['functionality', 'architecture', 'code_quality']
            if not all(k in details for k in required_fields):
                raise ValueError(f"详细得分缺少必要维度: {required_fields}")
            
            return {
                "total_score": result['total_score'],
                "details": details,
                "feedback": result.get('feedback', {})
            }
            
        except Exception as e:
            print(f"项目评分解析错误: {str(e)}")
            # 返回默认值
            return {
                "total_score": 0,
                "details": {
                    "functionality": 0,
                    "architecture": 0,
                    "code_quality": 0
                },
                "feedback": {
                    "functionality_feedback": "评分解析失败",
                    "architecture_feedback": "评分解析失败",
                    "code_quality_feedback": "评分解析失败"
                }
            }

    def _parse_frontend_grading_response(self, response):
        """解析前端评分结果"""
        try:
            # 尝试解析JSON
            result = json.loads(response)
            
            # 验证总分
            if not isinstance(result.get('total_score'), (int, float)):
                raise ValueError("总分必须是数字")
                
            # 验证详细得分
            details = result.get('details', {})
            required_fields = ['structure', 'style', 'functionality']
            if not all(k in details for k in required_fields):
                raise ValueError(f"详细得分缺少必要维度: {required_fields}")
            
            return {
                "total_score": result['total_score'],
                "details": details,
                "feedback": result.get('feedback', {})
            }
            
        except Exception as e:
            print(f"前端评分解析错误: {str(e)}")
            # 返回默认值
            return {
                "total_score": 0,
                "details": {
                    "structure": 0,
                    "style": 0,
                    "functionality": 0
                },
                "feedback": {
                    "structure_feedback": "评分解析失败",
                    "style_feedback": "评分解析失败",
                    "functionality_feedback": "评分解析失败"
                }
            }

    def _parse_wxapp_grading_response(self, response):
        """解析小程序评分结果"""
        try:
            # 尝试解析JSON
            result = json.loads(response)
            
            # 验证总分
            if not isinstance(result.get('total_score'), (int, float)):
                raise ValueError("总分必须是数字")
                
            # 验证详细得分
            details = result.get('details', {})
            required_fields = ['ui_design', 'functionality', 'code_quality']
            if not all(k in details for k in required_fields):
                raise ValueError(f"详细得分缺少必要维度: {required_fields}")
            
            return {
                "total_score": result['total_score'],
                "details": details,
                "feedback": result.get('feedback', {})
            }
            
        except Exception as e:
            print(f"小程序评分解析错误: {str(e)}")
            # 返回默认值
            return {
                "total_score": 0,
                "details": {
                    "ui_design": 0,
                    "functionality": 0,
                    "code_quality": 0
                },
                "feedback": {
                    "ui_design_feedback": "评分解析失败",
                    "functionality_feedback": "评分解析失败",
                    "code_quality_feedback": "评分解析失败"
                }
            }

    def get_grade_level(self, score):
        """根据分数确定等级"""
        for level, (min_score, max_score) in SCORE_RANGES.items():
            if min_score <= score <= max_score:
                return level
        return "F"
