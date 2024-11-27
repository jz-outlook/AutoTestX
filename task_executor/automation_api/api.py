import json

import requests
import allure
from task_executor.automation_api.api_parameter_handler import APIParamHandler


class ApiAutomation:
    def api_automation_test(self, params):
        """执行 Web 自动化测试任务"""
        with allure.step("执行 Web 自动化测试任务"):
            # 将传入的参数附加到 Allure 报告中
            allure.attach(str(params), "Web自动化参数", allure.attachment_type.JSON)
            APIParamHandler().perform_operation(params)

