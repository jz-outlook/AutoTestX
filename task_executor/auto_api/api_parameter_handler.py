# 文件名: api_param_manager.py
from utils.config import load_config
import re


class APIParamHandler:
    def __init__(self):
        """初始化API参数处理器，设置默认参数"""
        config_data = load_config('/Users/Wework/AutoTestX/config/config.ini', 'DEFAULT')
        self.console_url = config_data.get('console_url', '')
        self.app_url = config_data.get('app_url', '')

    def validate_params(self, params):
        """验证给定参数字典的有效性"""
        # 实现检查逻辑
        return True  # 假设通过检查，实际可根据需要返回True或False

    def is_param_valid(self, param_name, param_value):
        """检查单个参数是否有效"""
        # 实现具体检查逻辑
        return True

    def replace_param(self, params, param_name, new_value):
        """替换单个参数的值"""
        if param_name in params:
            params[param_name] = new_value

    def replace_params(self, params, replacements):
        """批量替换参数值"""
        for key, value in replacements.items():
            params[key] = value

    def set_params(self, params):
        """设置默认参数"""
        method = params.get('by')
        url = params.get('element')
        self.check_http_path(url, params)
        payload = {}
        headers = {}
        print(f'url：{url}')
        print(f'url：{payload}')
        print(f'url：{headers}')
        return method, url, payload, headers

    def apply_defaults(self, params):
        """将默认参数应用到给定参数字典中"""
        pass

    def to_dict(self, params):
        """将参数字典返回为标准字典"""
        return dict(params)

    def check_http_path(self, path, params):
        if params.get('tasks') == 'app':
            url = path if path.startswith("http") else self.app_url + path
        else:
            url = path if path.startswith("http") else self.console_url + path
        # 检查 URL 中是否包含 {{}}
        if re.search(r'{{.*?}}', url):
            print(f"url需要进行前置操作，替换url: {url}")
            url = self.replace_url(params, url)
            print(f"替换之后的url: {url}")
        else:
            return url  # 如果没有发现 {{}}，则返回原始 URL
        return url
