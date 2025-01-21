# AGAR (Automated Grading And Reviews)

基于大语言模型的自动作业评分系统，支持多种语言以及工程项目的批量评分。

# 特性

- 支持多种语言评分类型：
  - Python
  - Java
  - C / C++
  - Scala
  - HTML / CSS / JavaScript
  - 微信小程序

- 智能评分功能：
  - 分档评分(90-100,80-89,70-79,60-69,0-59)
  - 详细评语和反馈
  - 统计分析和可视化

- 批量处理：
  - 自动判断是否是工程项目
  - 自动识别学生ID(基于文件夹名)
  - 生成CSV格式评分报告

- 可用的API（目前只测试过Deepseek、Kimi、Ollama）：
  - ChatGPT
  - Claude
  - Qwen
  - Deepseek
  - Kimi
  - Glm
  - Ollama（本地）

# 使用方法

- API更换
  - 在api_config.py，把api-key换掉即可
  - 在api_config.py，把DEFAULT_API换成你用的模型

- 题目输入
  - 题目输入在main函数里的question这里填，不填也没事，会根据代码评分，提交作业在submissions文件里