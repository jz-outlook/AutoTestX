import allure
import requests
import json
from utils.config import load_config, write_config
from utils.get_path import GetPath


class APIInitializer:
    def __init__(self):
        self.token = None

    def initialize_token(self):
        """
        执行 API 初始化操作，生成或刷新 Token。
        """
        config_path = GetPath().get_config_path()
        config_data = load_config(config_path, 'api')

        if 'console_authorization' in config_data and 'app_authorization' in config_data:
            print("Authorization 存在，值为:", config_data['console_authorization'], config_data['app_authorization'])
            # 验证 token 是否失效
            console_url = 'https://admin-test.myaitalk.vip:6060/#/school-manage/school-list'
            console_headers = {'Authorization': config_data['console_authorization']}
            response = requests.post(url=console_url, headers=console_headers)

            if response.status_code == 200 and response.json().get('message') == 'success':
                print(f'管理后台登录有效，无需重新登录. "response.json": {response.json()}')
            else:
                print('管理后台登录无效，需重新登录')
                self.get_console_token()

            app_url = 'https://api-test-ws.myaitalk.vip/profile/getUserProfile.php'
            app_headers = {'Authorization': config_data['app_authorization']}
            response = requests.post(url=app_url, headers=app_headers)

            if response.status_code == 200 and response.json().get('message') == 'success':
                print(f'app登录有效，无需重新登录. "response.json": {response.json()}')
            else:
                print('app登录无效，需重新登录')
                self.get_app_token()
        else:
            print('Authorization 不存在，初始化 Token...')
            self.get_console_token()
            self.get_app_token()

    def get_console_token(self):
        url = "https://api-test.myaitalk.vip/admin/login/login.php"
        payload = json.dumps({
            "phone_number": "19900000001",
            "password": "Ajf+nAFFntf3c0BjO24vMfssZ1bNKR3dsHn1UYzYFzc="
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        write_config('api', {'console_authorization': 'Bearer' + ' ' + response_json['data']['access_token']})

    def get_app_token(self):
        url = "https://api-test-ws.myaitalk.vip/register/userLogin.php"
        payload = json.dumps({"phone_number": "13523456789", "password": "Myai123"})
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        write_config('api', {'app_authorization': 'Bearer' + ' ' + response_json['data']['access_token']})
        print('登录成功，写入token')


APIInitializer().get_app_token()