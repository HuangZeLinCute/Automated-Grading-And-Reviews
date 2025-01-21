import os
import pandas as pd
from core.grader import Grader
from core.api_manager import APIManager
from core.score_analyzer import ScoreAnalyzer
from utils.submission_handler import SubmissionHandler
from utils.result_handler import ResultHandler

def main():
    # 初始化API管理器和评分器
    api_manager = APIManager()  # 使用默认API（kimi）
    grader = Grader(api_manager)
    
    # 获取题目要求
    question = """
    
    """
    
    # 设置输入输出路径
    submissions_dir = "submissions"
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)
    
    # 批量评分
    submissions = SubmissionHandler.get_student_submissions(submissions_dir)
    results = []
    
    for submission in submissions:
        if submission['is_project']:
            # 项目评分
            if score_result := grader.grade_project(
                submission['file_path'], 
                question, 
                submission['language']
            ):
                score_result['student_id'] = submission['student_id']
                results.append(score_result)
        else:
            # 普通代码文件评分
            if score_result := grader.grade_code(
                submission['file_path'], 
                question, 
                submission['language']
            ):
                score_result['student_id'] = submission['student_id']
                results.append(score_result)
    
    # 保存结果
    if results:
        # 保存原始评分结果
        output_file = os.path.join(output_dir, 'grading_results.csv')
        ResultHandler.save_results_to_csv(results, output_file)
        print(f"评分完成，结果已保存到: {output_file}")
        
        # 生成统计分析
        results_df = pd.DataFrame(results)
        analyzer = ScoreAnalyzer(results_df)
        
        # 生成基本统计信息
        stats = analyzer.generate_statistics()
        print("\n成绩统计信息:")
        for key, value in stats.items():
            print(f"{key}: {value:.2f}")
        
        # 生成可视化图表
        print("\n正在生成可视化图表...")
        analyzer.generate_visualizations(output_dir)
        print(f"可视化图表已保存到: {output_dir}")
    else:
        print("没有找到有效的提交")

if __name__ == "__main__":
    main()