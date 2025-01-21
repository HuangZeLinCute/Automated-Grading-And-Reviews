import pandas as pd
from pylab import mpl
import matplotlib.pyplot as plt

class ScoreAnalyzer:
    def __init__(self, results_df):
        self.df = results_df
        
    def generate_statistics(self):
        """生成基本统计信息"""
        return {
            "平均分": self.df['total_score'].mean(),
            "最高分": self.df['total_score'].max(),
            "最低分": self.df['total_score'].min(),
            "标准差": self.df['total_score'].std(),
            "及格率": (self.df['total_score'] >= 60).mean() * 100
        }
    
    def generate_visualizations(self, output_dir):
        """生成所有可视化图表"""
        # 设置中文显示字体
        mpl.rcParams["font.sans-serif"] = ["SimHei"]
        mpl.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        self.plot_score_distribution(f"{output_dir}/score_distribution.png")
        self.plot_grade_levels(f"{output_dir}/grade_levels.png")
    
    def plot_score_distribution(self, save_path):
        """绘制分数分布图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        self.df['total_score'].plot(kind='hist', bins=20, rwidth=0.9, ax=ax)
        ax.set_title('分数分布')
        ax.set_xlabel('分数')
        ax.set_ylabel('频次')
        plt.savefig(save_path)
        plt.close()
    
    def plot_grade_levels(self, save_path):
        """绘制等级分布饼图"""
        grade_counts = self.df['grade_level'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 8))
        grade_counts.plot(kind='pie', autopct='%1.1f%%', labels=grade_counts.index, legend=False, ax=ax)
        ax.set_title('等级分布')
        plt.savefig(save_path)
        plt.close()
