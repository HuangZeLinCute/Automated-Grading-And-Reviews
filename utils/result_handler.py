import pandas as pd
import os

class ResultHandler:
    @staticmethod
    def save_results_to_csv(results, output_file):
        """保存评分结果到CSV文件
        
        Args:
            results: 评分结果列表
            output_file: 输出文件路径
        """
        try:
            # 转换结果为DataFrame
            df = pd.DataFrame(results)
            
            # 确保目录存在
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # 保存到CSV
            df.to_csv(output_file, index=False, encoding='utf-8')
            
        except Exception as e:
            print(f"保存结果错误: {str(e)}")

    @staticmethod
    def format_feedback(feedback):
        """格式化反馈信息
        
        Args:
            feedback: 反馈信息字典
            
        Returns:
            str: 格式化的反馈文本
        """
        try:
            formatted = []
            for category, comments in feedback.items():
                formatted.append(f"{category}:")
                if isinstance(comments, str):
                    formatted.append(f"  - {comments}")
                elif isinstance(comments, list):
                    for comment in comments:
                        formatted.append(f"  - {comment}")
                formatted.append("")
            return "\n".join(formatted)
        except Exception as e:
            print(f"格式化反馈错误: {str(e)}")
            return str(feedback)

    @staticmethod
    def merge_results(results):
        """合并多个评分结果
        
        Args:
            results: 评分结果列表
            
        Returns:
            dict: 合并后的结果
        """
        if not results:
            return None
            
        try:
            # 如果只有一个结果，直接返回
            if len(results) == 1:
                return results[0]
            
            # 合并多个结果
            merged = {
                'details': {},
                'total_score': 0,
                'feedback': {}
            }
            
            # 计算加权平均分
            weights = [len(str(r.get('details', ''))) for r in results]
            total_weight = sum(weights)
            
            for result, weight in zip(results, weights):
                w = weight / total_weight
                
                # 合并详细得分
                for key, score in result.get('details', {}).items():
                    if key not in merged['details']:
                        merged['details'][key] = 0
                    merged['details'][key] += score * w
                
                # 合并总分
                merged['total_score'] += result.get('total_score', 0) * w
                
                # 合并反馈
                for key, feedback in result.get('feedback', {}).items():
                    if key not in merged['feedback']:
                        merged['feedback'][key] = []
                    if isinstance(feedback, str):
                        merged['feedback'][key].append(feedback)
                    elif isinstance(feedback, list):
                        merged['feedback'][key].extend(feedback)
            
            # 四舍五入分数
            merged['total_score'] = round(merged['total_score'])
            for key in merged['details']:
                merged['details'][key] = round(merged['details'][key])
            
            # 去重反馈
            for key in merged['feedback']:
                merged['feedback'][key] = list(set(merged['feedback'][key]))
            
            return merged
            
        except Exception as e:
            print(f"合并结果错误: {str(e)}")
            return None
