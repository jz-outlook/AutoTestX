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
        method = params.get('by')  # 请求方式
        url = params.get('element')  # 请求地址
        platform = params.get('index')  # 请求平台（前台还是后台）
        pre_operation = params.get('send_keys')  # 前置
        post_operation = params.get('expected_element_by')  # 后置
        payload = params.get('payload')  # 请求参数
        headers = {}  # 请求头
        new_url = self.check_http_path(url, platform, pre_operation)
        print(f'method：{method}')
        print(f'url：{url}')
        print(f'platform：{platform}')
        print(f'pre_operation：{pre_operation}')
        print(f'post_operation：{post_operation}')
        print(f'payload：{payload}')
        print(f'headers：{headers}')
        return method, new_url, platform, pre_operation, post_operation, payload, headers

    def apply_defaults(self, params):
        """将默认参数应用到给定参数字典中"""
        pass

    def to_dict(self, params):
        """将参数字典返回为标准字典"""
        return dict(params)

    def check_http_path(self, path, platform, pre_operation):
        if path:
            url = path if path.startswith("http") else self.app_url + path
        else:
            url = path if path.startswith("http") else self.console_url + path
        # 检查 URL 中是否包含 {{}}
        if re.search(r'{{.*?}}', url):
            print(f"url需要进行前置操作，替换url: {url}")
            url = self.replace_url(url, platform, pre_operation)
            print(f"替换之后的url: {url}")
        else:
            return url  # 如果没有发现 {{}}，则返回原始 URL
        return url

    # def replace_url(self, url, platform, pre_operation):
    #     # 确定加载哪个配置
    #     config_section = 'App' if platform == 'App' else 'console'
    #     platform_data = load_config(get_project_root() + '/config/config.ini', config_section)
    #     print(platform_data)
    #     print(pre_operation)
    #     new_url = url
    #
    #     for key in pre_operation.split(','):
    #         key = key.strip()  # 去掉多余的空格
    #         # 获取替换数据
    #         replace_data = platform_data.get(key)
    #         print(f"替换数据: {replace_data}")
    #
    #         if replace_data is None:
    #             print(f"没有找到替换数据，{key} 为空。")
    #             continue  # 如果没有找到替换数据，继续下一个变量
    #
    #         # 替换 URL 中的占位符
    #         new_url = re.sub(rf'{{{{{key}}}}}', replace_data, url)  # 使用正则表达式替换
    #         print(f"替换之后的 URL: {new_url}")
    #
    #     return new_url

