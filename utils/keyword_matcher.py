import re
import jieba
from difflib import SequenceMatcher

class KeywordMatcher:
    # 中文常用词过滤列表
    CHINESE_COMMON_WORDS = {
        '的', '了', '和', '是', '就', '都', '而', '及', '与', '着',
        '或', '把', '被', '让', '给', '在', '从', '向', '到', '上',
        '下', '中', '内', '外', '前', '后', '里', '外', '时', '要',
        '这', '那', '这个', '那个', '实现', '完成', '编写', '设计',
        '开发', '创建', '修改', '使用', '如下', '以下', '请', '需要',
        '必须', '可以', '应该', '题目', '作业', '要求'
    }
    
    # 英文常用词过滤列表
    ENGLISH_COMMON_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 
        'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 
        'into', 'over', 'after', 'between', 'out', 'through',
        'implement', 'create', 'write', 'design', 'develop',
        'modify', 'use', 'using', 'please', 'must', 'should',
        'can', 'will', 'need', 'required', 'following'
    }

    # 中英文关键词映射字典
    KEYWORD_MAPPINGS = {
        # 学生相关
        '学生': ['student', 'stu', 'learner', 'user'],
        '成绩': ['score', 'grade', 'mark', 'result', 'record'],
        '管理': ['manage', 'admin', 'control', 'handle'],
        '系统': ['system', 'sys', 'platform', 'app'],
        '统计': ['stat', 'analytics', 'analysis', 'count'],
        '分析': ['analysis', 'analytics', 'analyze'],
        '数据库': ['db', 'database', 'storage', 'store'],
        '用户': ['user', 'account', 'member'],
        '登录': ['login', 'auth', 'signin'],
        '注册': ['register', 'signup', 'reg'],
        '信息': ['info', 'data', 'profile', 'detail'],
        '查询': ['query', 'search', 'find', 'select'],
        '修改': ['modify', 'update', 'edit', 'change'],
        '删除': ['delete', 'remove', 'del'],
        '添加': ['add', 'create', 'insert', 'new'],
        '列表': ['list', 'table', 'grid'],
        '详情': ['detail', 'info', 'profile'],
        '导入': ['import', 'upload', 'input'],
        '导出': ['export', 'download', 'output'],
        '配置': ['config', 'setting', 'setup'],
        '接口': ['api', 'interface', 'service'],
        '模块': ['module', 'component', 'part'],
        '工具': ['util', 'tool', 'helper'],
        '控制': ['control', 'controller', 'ctrl'],
        '模型': ['model', 'entity', 'schema'],
        '视图': ['view', 'page', 'screen'],
        '路由': ['route', 'router', 'url'],
        '服务': ['service', 'server', 'provider'],
        '验证': ['valid', 'verify', 'check'],
        '测试': ['test', 'check', 'verify'],
        
        # 前端相关
        '页面': ['page', 'view', 'screen'],
        '布局': ['layout', 'structure'],
        '样式': ['style', 'css', 'theme'],
        '脚本': ['script', 'js'],
        '组件': ['component', 'widget', 'element'],
        '表单': ['form', 'input'],
        '菜单': ['menu', 'nav', 'navigation'],
        
        # 小程序相关
        '小程序': ['miniapp', 'wxapp', 'applet'],
        '微信': ['wx', 'wechat', 'weixin'],
        '页面': ['page', 'view'],
        '组件': ['component', 'comp']
    }

    @staticmethod
    def similar(a, b, threshold=0.75):
        """检查两个字符串是否相似
        
        Args:
            a: 第一个字符串
            b: 第二个字符串
            threshold: 相似度阈值（0-1之间）
            
        Returns:
            bool: 是否相似
        """
        # 转换为小写进行比较
        a = a.lower()
        b = b.lower()
        
        # 如果字符串完全相同或一个包含另一个，返回True
        if a == b or a in b or b in a:
            return True
            
        # 使用序列匹配器计算相似度
        return SequenceMatcher(None, a, b).ratio() >= threshold

    @staticmethod
    def get_similar_keywords(word):
        """获取与给定词相似的关键词列表
        
        Args:
            word: 输入词
            
        Returns:
            set: 相似关键词集合
        """
        similar_words = set()
        
        # 检查中文映射
        for zh_key, en_list in KeywordMatcher.KEYWORD_MAPPINGS.items():
            if KeywordMatcher.similar(word, zh_key) or any(KeywordMatcher.similar(word, en) for en in en_list):
                similar_words.update(en_list)
                similar_words.add(zh_key)
        
        return similar_words

    @staticmethod
    def extract_keywords(text):
        """从文本中提取关键词
        
        Args:
            text: 文本内容
            
        Returns:
            set: 关键词集合
        """
        # 移除标点符号
        text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
        
        # 分别处理中文和英文
        keywords = set()
        
        # 处理中文部分（使用结巴分词）
        chinese_text = ''.join(re.findall(r'[\u4e00-\u9fff]+', text))
        if chinese_text:
            words = jieba.cut(chinese_text)
            for word in words:
                if word not in KeywordMatcher.CHINESE_COMMON_WORDS and len(word) > 1:
                    keywords.update(KeywordMatcher.get_similar_keywords(word))
        
        # 处理英文部分
        english_text = ''.join(re.findall(r'[a-zA-Z]+', text))
        if english_text:
            words = english_text.lower().split()
            for word in words:
                if word not in KeywordMatcher.ENGLISH_COMMON_WORDS and len(word) > 2:
                    keywords.update(KeywordMatcher.get_similar_keywords(word))
        
        return keywords
