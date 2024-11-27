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
        self.request_action(files, method, url, headers, payload)
        return method, new_url, platform, files, pre_operation, post_operation, headers

    def request_action(self, files, method, url, headers, payload):
        new_payload = self.is_file_upload_advanced(files, payload)
        if not files:
            if new_payload:
                response = requests.request(method=method, url=url, headers=headers, json=new_payload)
                print(response.text)
            else:
                response = requests.request(method=method, url=url, headers=headers)
                print(response.text)
        else:
            try:
                files = [
                    ('upload',
                     (f'{files}', open(f'{GetPath().get_project_root() + "/upload/"}{files}', 'rb'),
                      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
                ]
                # 发送请求
                response = requests.request(method=method, url=url, headers=headers, data=new_payload, files=files)
                # 检查响应
                if response.status_code == 200:
                    print("文件上传成功:", response.json())
                else:
                    print("文件上传失败:", response.status_code, response.text)
            except Exception as e:
                print("发生错误:", str(e))

    def is_file_upload_advanced(self, files, payload):
        # 如果未提供文件
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
        files = params.get('files')  # 上传文件
        payload = params.get('send_keys')  # 请求参数
        pre_operation = params.get('expected_element_by')  # 前置
        post_operation = params.get('expected_element_value')  # 后置
        headers = {"authorization": config.get('console_authorization')}  # 请求头
        return method, url, platform, files, pre_operation, post_operation, payload, headers

    def apply_defaults(self, params):
        """将默认参数应用到给定参数字典中"""
        pass

    def to_dict(self, params):
        """将参数字典返回为标准字典"""
        return dict(params)

    def process_payload(self, payload):
        if payload:
            try:
                print(f"原始 payload: {payload}")
                # 如果传入的payload是字典，先转换为JSON字符串
                if isinstance(payload, dict):
                    payload = json.dumps(payload)
                # 尝试解析JSON字符串
                data = json.loads(payload)
                print(f"解析后的数据: {data}")
                # 清理数据: 对于字符串，进行strip()；对于其他类型的数据，保留原样
                cleaned_data = {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}
                print(f"清理后的数据: {cleaned_data}")
                new_payload = self.replace_payload(cleaned_data)
                return new_payload
            except json.JSONDecodeError as e:
                print(f"解码 JSON 时出错: {e}")
                return None
        else:
            print("payload 为空，返回空的 JSON")
            return payload  # 如果payload为空，返回空的JSON字符串

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
