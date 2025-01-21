import os
from config.config import SUPPORTED_LANGUAGES, TOKEN_CONFIG
from .file_analyzer import FileAnalyzer

class SubmissionHandler:
    @staticmethod
    def read_submission(file_path):
        """读取提交的代码文件
        
        Args:
            file_path: 文件路径或目录路径
            
        Returns:
            str/dict: 文件内容或文件内容字典
        """
        try:
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif os.path.isdir(file_path):
                files = {}
                for root, _, filenames in os.walk(file_path):
                    for filename in filenames:
                        file_type = FileAnalyzer.get_file_type(filename)
                        if file_type in SUPPORTED_LANGUAGES:
                            full_path = os.path.join(root, filename)
                            with open(full_path, 'r', encoding='utf-8') as f:
                                rel_path = os.path.relpath(full_path, file_path)
                                files[rel_path] = f.read()
                return files
            return None
        except Exception as e:
            print(f"读取文件错误: {str(e)}")
            return None

    @staticmethod
    def get_student_submissions(submissions_dir):
        """获取学生提交的作业
        
        Args:
            submissions_dir: 提交目录路径
            
        Returns:
            list: 提交信息列表
        """
        submissions = []
        try:
            # 检查目录是否存在
            if not os.path.exists(submissions_dir):
                print(f"提交目录不存在: {submissions_dir}")
                return []
                
            # 遍历目录下的所有文件和文件夹
            for item in os.listdir(submissions_dir):
                try:
                    item_path = os.path.join(submissions_dir, item)
                    print(f"正在处理: {item_path}")
                    
                    # 如果是文件，检查是否为支持的语言类型
                    if os.path.isfile(item_path):
                        file_type = FileAnalyzer.get_file_type(item_path)
                        if file_type in SUPPORTED_LANGUAGES:
                            # 从文件名中提取学生ID（移除扩展名）
                            student_id = os.path.splitext(item)[0]
                            submissions.append({
                                'student_id': student_id,
                                'file_path': item_path,
                                'language': file_type,
                                'is_project': False
                            })
                            print(f"找到有效提交: {student_id}, 类型: {file_type}")
                    
                    # 如果是目录，检查是否为项目目录
                    elif os.path.isdir(item_path):
                        if FileAnalyzer.is_project_directory(item_path):
                            project_type = SubmissionHandler._determine_project_type(item_path)
                            if project_type:
                                submissions.append({
                                    'student_id': item,
                                    'file_path': item_path,
                                    'language': project_type,
                                    'is_project': True
                                })
                                print(f"找到项目提交: {item}, 类型: {project_type}")
                        # 检查学生目录下的文件
                        else:
                            for sub_item in os.listdir(item_path):
                                sub_path = os.path.join(item_path, sub_item)
                                if os.path.isfile(sub_path):
                                    file_type = FileAnalyzer.get_file_type(sub_path)
                                    if file_type in SUPPORTED_LANGUAGES:
                                        submissions.append({
                                            'student_id': item,
                                            'file_path': sub_path,
                                            'language': file_type,
                                            'is_project': False
                                        })
                                        print(f"找到学生目录下的提交: {item}/{sub_item}, 类型: {file_type}")
                except Exception as e:
                    print(f"处理文件 {item} 时出错: {str(e)}")
                    continue
                    
            if not submissions:
                print(f"在目录 {submissions_dir} 中没有找到有效的提交")
            else:
                print(f"共找到 {len(submissions)} 个有效提交")
                
            return submissions
        except Exception as e:
            print(f"获取提交信息错误: {str(e)}")
            return []

    @staticmethod
    def _determine_project_type(project_dir):
        """确定项目类型
        
        Args:
            project_dir: 项目目录路径
            
        Returns:
            str: 项目类型
        """
        # 统计各种类型文件的数量
        file_types = {}
        for root, _, files in os.walk(project_dir):
            for file in files:
                ext = FileAnalyzer.get_file_type(file)
                # 查找对应的语言类型
                for lang, config in SUPPORTED_LANGUAGES.items():
                    if ext == config['file_extension']:
                        file_types[lang] = file_types.get(lang, 0) + 1
                        break
        
        # 返回最多的文件类型
        return max(file_types.items(), key=lambda x: x[1])[0] if file_types else None

    @staticmethod
    def read_frontend_submission(submission_path):
        """读取前端作业提交
        
        Args:
            submission_path: 提交路径
            
        Returns:
            dict: 文件内容字典
        """
        try:
            files = {}
            if os.path.isfile(submission_path):
                # 单个HTML文件
                if submission_path.endswith('.html'):
                    with open(submission_path, 'r', encoding='utf-8') as f:
                        files[os.path.basename(submission_path)] = f.read()
            elif os.path.isdir(submission_path):
                # 前端项目目录
                for root, _, filenames in os.walk(submission_path):
                    for filename in filenames:
                        if filename.endswith(('.html', '.css', '.js')):
                            file_path = os.path.join(root, filename)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                rel_path = os.path.relpath(file_path, submission_path)
                                files[rel_path] = f.read()
            return files if files else None
        except Exception as e:
            print(f"读取前端文件错误: {str(e)}")
            return None

    @staticmethod
    def read_wxapp_submission(project_path):
        """读取微信小程序项目提交
        
        Args:
            project_path: 项目根目录路径
            
        Returns:
            dict: 文件内容字典
        """
        try:
            files = {}
            if os.path.isdir(project_path):
                for root, _, filenames in os.walk(project_path):
                    for filename in filenames:
                        if filename.endswith(('.js', '.wxml', '.wxss', '.json')):
                            file_path = os.path.join(root, filename)
                            with open(file_path, 'r', encoding='utf-8') as f:
                                rel_path = os.path.relpath(file_path, project_path)
                                files[rel_path] = f.read()
            return files if files else None
        except Exception as e:
            print(f"读取小程序文件错误: {str(e)}")
            return None
