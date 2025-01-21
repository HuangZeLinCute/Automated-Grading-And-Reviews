# 支持的编程语言配置
SUPPORTED_LANGUAGES = {
    "python": {
        "name": "Python",
        "file_extension": ".py",
        "weights": {
            "correctness": 0.4,    # 正确性
            "style": 0.3,         # 代码风格
            "efficiency": 0.3     # 效率
        },
        "project_weights": {
            "functionality": 0.4,  # 功能完整性
            "architecture": 0.3,   # 架构设计
            "code_quality": 0.3    # 代码质量
        },
        "project_indicators": {
            "min_files": 3,       # 最少文件数
            "min_dirs": 2,        # 最少目录数
            "file_patterns": [".py"]  # 项目相关文件类型
        }
    },
    "java": {
        "name": "Java",
        "file_extension": ".java",
        "weights": {
            "correctness": 0.4,
            "style": 0.3,
            "efficiency": 0.3
        },
        "project_weights": {
            "functionality": 0.4,
            "architecture": 0.3,
            "code_quality": 0.3
        },
        "project_indicators": {
            "min_files": 3,
            "min_dirs": 2,
            "file_patterns": [".java"]
        }
    },
    "cpp": {
        "name": "C++",
        "file_extension": ".cpp",
        "weights": {
            "correctness": 0.4,
            "style": 0.3,
            "efficiency": 0.3
        },
        "project_weights": {
            "functionality": 0.4,
            "architecture": 0.3,
            "code_quality": 0.3
        },
        "project_indicators": {
            "min_files": 3,
            "min_dirs": 2,
            "file_patterns": [".cpp", ".hpp", ".h"]
        },
        "scala": {
            "name": "Scala",
            "file_extension": ".scala",
            "weights": {
                "correctness": 0.4,
                "style": 0.3,
                "efficiency": 0.3
            },
            "project_weights": {
                "functionality": 0.4,
                "architecture": 0.3,
                "code_quality": 0.3
            },
            "project_indicators": {
                "min_files": 3,
                "min_dirs": 2,
                "file_patterns": [".scala", ".sbt"]
            }
        }
    },
    "html": {
        "name": "HTML",
        "file_extension": ".html",
        "weights": {
            "structure": 0.4,        
            "style": 0.3,           
            "functionality": 0.3     
        },
        "project_weights": {
            "functionality": 0.4,    
            "architecture": 0.3,     
            "code_quality": 0.3      
        },
        "project_indicators": {
            "min_files": 3,
            "min_dirs": 1,
            "file_patterns": [".html", ".css", ".js", ".jsx", ".ts", ".tsx"]
        }
    },
    "wxapp": {
        "name": "微信小程序",
        "file_extension": ".wxml",
        "weights": {
            "ui_design": 0.3,        # 界面设计
            "functionality": 0.4,     # 功能实现
            "code_quality": 0.3      # 代码质量
        },
        "project_weights": {
            "functionality": 0.4,    # 功能完整性
            "architecture": 0.3,     # 架构设计
            "code_quality": 0.3      # 代码质量
        },
        "project_indicators": {
            "min_files": 4,
            "min_dirs": 2,
            "file_patterns": [".wxml", ".wxss", ".js", ".json"]
        }
    }
}

# Token配置
TOKEN_CONFIG = {
    "max_tokens": 8000,           # 单次输入的最大token数
    "chars_per_token": 4,         # 每个token平均字符数
    "batch_size": 3000           # 分批处理时的token大小
}

# 核心文件判断配置
CORE_FILE_PATTERNS = {
    "python": {
        "core_patterns": ["main", "app", "core", "service", "controller", "model"],
        "test_patterns": ["test_", "_test", "tests"],
        "ignore_patterns": ["__init__", "utils", "helpers", "config"]
    },
    "java": {
        "core_patterns": ["Main", "App", "Service", "Controller", "Model"],
        "test_patterns": ["Test"],
        "ignore_patterns": ["Utils", "Helper", "Config"]
    },
    "cpp": {
        "core_patterns": ["main", "app", "core"],
        "test_patterns": ["test_", "_test"],
        "ignore_patterns": ["utils", "helper", "config"]
    },
    "html": {
        "core_patterns": ["index", "main", "app"],
        "test_patterns": ["test"],
        "ignore_patterns": ["vendor", "lib"]
    },
    "wxapp": {
        "core_patterns": ["app", "pages/index", "pages/main", "pages/home"],
        "test_patterns": ["test", "mock"],
        "ignore_patterns": ["utils", "components", "config"]
    }
}

# 评分标准
SCORE_RANGES = {
    "A": (90, 100),
    "B": (80, 89),
    "C": (70, 79),
    "D": (60, 69),
    "F": (0, 59)
}

# 提示词模板
PROMPTS = {
    "grade_code": """
    你是一个{language}编程作业的评分助手。请根据以下题目要求和学生提交的代码进行评分。如果题目要求是空，则根据代码的正确性、风格和效率进行评分。

    题目要求：
    {question}

    学生提交的代码：
    {code}

    请从以下三个维度进行评分：
    1. 代码正确性 (40分)：代码是否正确实现了题目要求的功能，语法是否正确
    2. 代码风格 (30分)：代码的可读性、命名规范、注释、{language}语言的最佳实践等
    3. 代码效率 (30分)：代码的时间复杂度、空间复杂度、算法选择、{language}语言特定的性能优化等

    请严格按照以下JSON格式输出评分结果：
    {{
        "details": {{
            "code_correctness": <正确性得分>,
            "code_style": <风格得分>,
            "code_efficiency": <效率得分>
        }},
        "total_score": <总分>,
        "feedback": {{
            "correctness_feedback": "<代码正确性相关的具体评价和建议>",
            "style_feedback": "<代码风格相关的具体评价和建议>",
            "efficiency_feedback": "<代码效率相关的具体评价和建议>"
        }}
    }}

    注意：
    1. 各维度得分必须是整数
    2. 总分是各维度得分的加权和
    3. 每个维度都需要给出具体的评价和改进建议
    4. 代码正确性应该严格对照题目要求进行评判
    5. 评价时要考虑{language}语言的特点和最佳实践
    """,
    "grade_project": """
    你是一个{language}工程项目作业的评分助手。请根据以下项目要求和学生提交的项目代码进行评分。如果题目要求是空，则根据代码的正确性、风格和效率进行评分。

    题目要求：
    {question}

    项目代码：
    {code}

    请从以下三个维度进行评分：
    1. 功能完整性 (40分)：项目是否实现了所有要求的功能，功能是否正确，是否有完整的错误处理
    2. 架构设计 (30分)：项目结构、模块划分、依赖管理、设计模式的使用等
    3. 代码质量 (30分)：代码可读性、命名规范、注释、代码复用性、{language}语言的最佳实践等

    请严格按照以下JSON格式输出评分结果：
    {{
        "details": {{
            "functionality": <功能完整性得分>,
            "architecture": <架构设计得分>,
            "code_quality": <代码质量得分>
        }},
        "total_score": <总分>,
        "feedback": {{
            "functionality_feedback": "<功能完整性相关的具体评价和建议>",
            "architecture_feedback": "<架构设计相关的具体评价和建议>",
            "code_quality_feedback": "<代码质量相关的具体评价和建议>"
        }}
    }}

    注意：
    1. 各维度得分必须是整数
    2. 总分是各维度得分的加权和
    3. 每个维度都需要给出具体的评价和改进建议
    4. 评价时要考虑{language}语言的工程最佳实践
    """,
    "grade_frontend": """
    你是一个前端开发作业的评分助手。请根据以下要求和学生提交的代码进行评分。如果题目要求是空，则根据代码的正确性、风格和效率进行评分。

    题目要求：
    {question}

    提交的代码：
    {code}

    请从以下维度进行评分：
    1. HTML结构 (40分)：
       - HTML语义化使用是否合理
       - 文档结构是否清晰
       - 标签使用是否规范
       - 无障碍性考虑
       
    2. CSS样式 (30分)：
       - 样式设计是否美观
       - 响应式设计实现
       - CSS组织是否合理
       - 兼容性考虑
       
    3. JavaScript功能 (30分)：
       - 功能实现完整性
       - 代码逻辑清晰度
       - 交互体验
       - 性能考虑

    请严格按照以下JSON格式输出评分结果：
    {{
        "details": {{
            "structure": <HTML结构得分>,
            "style": <CSS样式得分>,
            "functionality": <JavaScript功能得分>
        }},
        "total_score": <总分>,
        "feedback": {{
            "structure_feedback": "<HTML结构相关的具体评价和建议>",
            "style_feedback": "<CSS样式相关的具体评价和建议>",
            "functionality_feedback": "<JavaScript功能相关的具体评价和建议>"
        }}
    }}

    注意：
    1. 各维度得分必须是整数
    2. 总分是各维度得分的加权和
    3. 每个维度都需要给出具体的评价和改进建议
    4. 评价时要考虑前端开发的最佳实践
    """,
    "grade_wxapp": """
    你是一个微信小程序开发作业的评分助手。请根据以下要求和学生提交的代码进行评分。如果题目要求是空，则根据代码的正确性、风格和效率进行评分。

    题目要求：
    {question}

    提交的代码：
    {code}

    请从以下维度进行评分：
    1. 界面设计 (30分)：
       - 页面布局合理性
       - 视觉设计美观度
       - 交互设计友好性
       - 符合小程序设计规范
       
    2. 功能实现 (40分)：
       - 需求完成度
       - 功能正确性
       - 性能优化
       - 错误处理
       
    3. 代码质量 (30分)：
       - 代码组织结构
       - 命名规范
       - 组件复用性
       - 最佳实践遵循

    请严格按照以下JSON格式输出评分结果：
    {{
        "details": {{
            "ui_design": <界面设计得分>,
            "functionality": <功能实现得分>,
            "code_quality": <代码质量得分>
        }},
        "total_score": <总分>,
        "feedback": {{
            "ui_design_feedback": "<界面设计相关的具体评价和建议>",
            "functionality_feedback": "<功能实现相关的具体评价和建议>",
            "code_quality_feedback": "<代码质量相关的具体评价和建议>"
        }}
    }}

    注意：
    1. 各维度得分必须是整数
    2. 总分是各维度得分的加权和
    3. 每个维度都需要给出具体的评价和改进建议
    4. 评价时要考虑微信小程序开发的最佳实践和规范
    """
}