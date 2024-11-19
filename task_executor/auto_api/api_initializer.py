import allure
import requests
import json
from utils.config import load_config, write_config
from utils.get_path import GetPath


class APIInitializer:
    def __init__(self):
        self.token = None

    def initialize_token(self, params):
        """
        执行 API 初始化操作，例如生成或刷新 Token。
        """
        config_path = GetPath().get_config_path()
        config_data = load_config(config_path, 'api')

        with allure.step("初始化 API Token"):
            if params['index'] == 'console':
                if 'console_authorization' in config_data:
                    print("Authorization 存在，值为:", config_data['console_authorization'])
                    headers = {"Authorization": config_data['console_authorization']}
                    response = requests.request(method=params['by'], url=params['element'], headers=headers)
                    if response.json()['code'] == 200 and response.json()['message'] == 'success':
                        print('用户登录有效，无需重新登录. "response.json":{}'.format(response.json()))
                    else:
                        print('用户登录无效，需重新登录')
                        self.get_authorization()
                else:
                    print('Authorization 不存在，初始化 Token...')
                    self.get_authorization()
            else:
                # 暂时留着先，初始化app相关内容
                pass

    def get_authorization(self):
        url = "https://api-test.myaitalk.vip/admin/login/login.php"
        payload = json.dumps({
            "phone_number": "19900000001",
            "password": "Ajf+nAFFntf3c0BjO24vMfssZ1bNKR3dsHn1UYzYFzc="
        })
        headers = {
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Nzk3LCJleHAiOjE3MzE5MDM0NjB9.DYgXYlTTYP+Y2WKpfcabNlXClaC3Cy/xrzRZlzfgZbw=',
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response_json = json.loads(response.text)
        write_config('api', {'console_authorization': 'Bearer' + ' ' + response_json['data']['access_token']})
