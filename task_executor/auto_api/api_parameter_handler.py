# 文件名: api_param_manager.py
import json

from utils.config import load_config
import re
import requests
from utils.db_connection import MySQLConnector
from utils.get_path import GetPath

autotestX = GetPath().get_project_root()


class APIParamHandler:
    def __init__(self):
        """初始化API参数处理器，设置默认参数"""
        config_data = load_config(f'{autotestX}/config/config.ini', 'DEFAULT')
        self.console_url = config_data.get('console_url', '')
        self.app_url = config_data.get('app_url', '')

    def perform_operation(self, params):
        method, url, platform, files, pre_operation, post_operation, payload, headers = self.set_params(params)
        new_url = self.check_http_path(platform, url)
        new_payload = self.is_file_upload_advanced(files, payload)
        return method, new_url, platform, files, pre_operation, post_operation, new_payload, headers

    def is_file_upload_advanced(self, files, payload):
        """确定请求是否包含文件上传"""
        if not files:
            print("没有提供文件路径，无需上传文件。")
            new_payload = self.process_payload(payload)
        else:
            print(f"files参数 不为空，上传文件类型接口")
            new_payload = self.file_process_payload(payload)
        return new_payload

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
        config = load_config(f'{autotestX}/config/config.ini', 'api')
        method = params.get('by')  # 请求方式 & sql方法
        url = params.get('element')  # 请求地址 & sql
        platform = params.get('index')  # 请求平台（前台还是后台）
        files = params.get('action')  # 请求平台（前台还是后台）
        payload = params.get('send_keys')  # 请求参数
        pre_operation = params.get('expected_element_by')  # 前置
        post_operation = params.get('expected_element_value')  # 后置
        headers = {"Authorization": config.get('console_authorization'),
                   'Content-Type': 'application/json'}  # 请求头
        return method, url, platform, files, pre_operation, post_operation, payload, headers

    def apply_defaults(self, params):
        """将默认参数应用到给定参数字典中"""
        pass

    def to_dict(self, params):
        """将参数字典返回为标准字典"""
        return dict(params)

    def process_payload(self, payload):
        """
        处理传入的 payload，确保其是一个有效的字典，并检查是否为空。
        """
        # 判断 payload 是否为空
        if not payload:  # 检查 None、空字符串、空字典、空列表等
            print("Payload 为空或无效！")
            return None

        # 确保 payload 是一个字典
        if isinstance(payload, str):
            try:
                new_payload = json.loads(payload)
                # 再次检查解码后的结果是否为空
                if not new_payload:
                    print("解码后的 payload 为空！")
                    return None
            except json.JSONDecodeError as e:
                print(f"JSON 解码错误: {e}")
                return None
        elif isinstance(payload, dict):
            new_payload = payload
            # 检查字典是否为空
            if not new_payload:
                print("Payload 是一个空字典！")
                return None
        else:
            print("Payload 类型无效！应为字符串或字典。")
            return None

        return new_payload

    def file_process_payload(self, payload):
        if payload:
            try:
                # 如果传入的payload是字典，保持原样
                if isinstance(payload, dict):
                    data = payload
                    print('传入的payload是字典，保持原样')
                else:
                    # 尝试解析JSON字符串
                    data = json.loads(payload)
                    print('传入的payload不是字典，尝试解析JSON字符串')
                # 清理数据
                cleaned_data = {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}
                return cleaned_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return {}  # 返回空字典或适当的错误处理
        else:
            return {}  # 如果payload为空，返回空字典

    def check_http_path(self, platform, path):
        """检查URL格式是否有效"""
        if platform == 'app':
            url = path if path.startswith("http") else self.app_url + path
        else:
            url = path if path.startswith("http") else self.console_url + path
        # 检查 URL 中是否包含 {{}}
        if re.search(r'{{.*?}}', url):
            print(f"url需要进行前置操作，替换url: {url}")
            url = self.replace_url(url)
            print(f"替换之后的url: {url}")
        else:
            return url  # 如果没有发现 {{}}，则返回原始 URL
        return url

    def replace_url(self, url):
        """替换URL中的 {{占位}}"""
        # 确定加载哪个配置
        config_section = 'api'
        platform_data = load_config(GetPath().get_project_root() + '/config/config.ini', config_section)
        # 使用正则表达式找到所有 {{}} 中的内容
        matches = re.findall(r'{{(.*?)}}', url)
        # 替换所有匹配到的占位符
        for match in matches:
            placeholder = f'{{{{{match}}}}}'  # 将 {{}} 保留在替换格式中
            if match in platform_data:
                url = url.replace(placeholder, platform_data[match])
        return url

    def replace_payload(self, cleaned_data):
        """替换参数中的{{占位}}"""
        # pattern = re.compile(r'\$\{(\w+)\}')
        pattern = re.compile(r'\$\{(\w+)\}')
        context = load_config(autotestX + '/config/config.ini', 'api')

        def get_value_from_context(key):
            if key in context:
                return str(context[key])
            else:
                raise ValueError(f"缺少占位符的值: {key}")

        resolved_payload = {}
        for k, v in cleaned_data.items():
            if isinstance(v, str):
                match = pattern.search(v)
                if match:
                    placeholder = match.group(1)
                    resolved_value = get_value_from_context(placeholder)
                    resolved_payload[k] = pattern.sub(resolved_value, v)
                else:
                    resolved_payload[k] = v
            else:
                resolved_payload[k] = v
        return resolved_payload
