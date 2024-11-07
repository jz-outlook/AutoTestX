# import asyncio
# import allure
# import pytest
# from concurrent.futures import ThreadPoolExecutor
# from appium import webdriver
# from auto_api.api import api_automation_test
# from automation_app.app_test import app_automation_test
# from automation_web.web import web_automation_test
#
#
# class Executor:
#     def __init__(self):
#         self.executor = ThreadPoolExecutor()
#         self.loop = asyncio.get_event_loop()
#         self.driver = None  # 初始化 driver 为 None
#
#     async def execute_task(self, task_name, params):
#         # 使用独立的 Allure 步骤包裹每个任务的执行
#         with allure.step(f"执行任务: {task_name}"):
#             if task_name == "app":
#                 result = await self.loop.run_in_executor(self.executor, self.run_app_automation, params)
#             elif task_name == "web":
#                 result = await self.loop.run_in_executor(self.executor, self.run_web_automation, params)
#             elif task_name == "api":
#                 result = await self.loop.run_in_executor(self.executor, self.run_api_automation, params)
#             else:
#                 raise ValueError("Unknown task name")
#             return result
#
#     def run_app_automation(self, params):
#         with allure.step("运行 App 自动化任务"):
#             if not self.driver:
#                 caps = {
#                     "platformName": "Android",
#                     "appium:platformVersion": "14",
#                     "appium:deviceName": "49MRGIFUYH6XQKQS",
#                     "appium:appPackage": "vip.myaitalk.myai",
#                     "appium:appActivity": ".ui.SplashActivity",
#                     "appium:udid": "192.168.28.237:5555",
#                     "appium:noReset": True,
#                     "ensureWebviewsHavePages": True,
#                     "nativeWebScreenshot": True,
#                     "newCommandTimeout": 60,
#                     "autoGrantPermissions": True
#                 }
#                 self.driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", caps)
#                 self.driver.implicitly_wait(10)
#
#             print("执行 App 自动化任务..")
#             allure.attach(str(params), "App自动化参数", allure.attachment_type.JSON)
#             app_automation_test(params)
#             return "App Task Completed"
#
#     def run_web_automation(self, params):
#         with allure.step("运行 Web 自动化任务"):
#             print("执行 Web 自动化任务...")
#             allure.attach(str(params), "Web自动化参数", allure.attachment_type.JSON)
#             web_automation_test()
#             return "Web Task Completed"
#
#     def run_api_automation(self, params):
#         with allure.step("运行 API 自动化任务"):
#             print("执行 API 自动化任务...")
#             allure.attach(str(params), "API自动化参数", allure.attachment_type.JSON)
#             api_automation_test()
#             return "API Task Completed"
#
#     async def execute(self, task_params):
#         results = []
#         for task in task_params:
#             task_name = task.get("tasks")
#             result = await self.execute_task(task_name, task)
#             results.append({task_name: result})
#         return results
#
#     def close_driver(self):
#         if self.driver:
#             self.driver.quit()
#             self.driver = None
#
#
# task_params = [
#         {'id': 'TC001', 'tasks': 'app', 'Procedure': '同意', 'by': 'xpath',
#          'Element_value': '//android.widget.TextView[@resource-id="vip.myaitalk.myai:id/aui_dialog_btn_right"]',
#          'action': 'click'},
#         {'id': 'TC002', 'tasks': 'app', 'Procedure': '始终允许', 'by': 'xpath',
#          'Element_value': '//android.widget.Button[@text="始终允许"]', 'action': 'click'},
#         {'id': 'TC003', 'tasks': 'web', 'Procedure': ''},
#         {'id': 'TC004', 'tasks': 'api', 'Procedure': ''},
#         {'id': 'TC005', 'tasks': 'app', 'Procedure': '点击教材', 'by': 'xpath',
#          'Element_value': '//android.widget.TextView[@text="教材"]', 'action': 'click'}
#     ]
#
# @allure.feature("执行任务")
# @allure.story("多任务执行测试")
# @pytest.mark.parametrize("task", task_params, ids=[f"{t['id']}_{t['tasks']}" for t in task_params])
# @pytest.mark.asyncio
# async def test_main(task):
#     executor = Executor()
#     task_name = task['tasks']
#     print(task_name)
#     # 动态设置 Allure 测试用例名称
#     with allure.step("执行所有任务"):
#         result = await executor.execute_task(task_name, task)
#
#     allure.attach(str(result), f"{task_name}任务执行结果", allure.attachment_type.TEXT)
#     print("最终结果:", result)
#     executor.close_driver()
#
#
# # Allure 报告文件title
# # case_name = case.get('Menu', 'Menu数据为空') + case.get('name', '默认用例名称')  # 如果找不到 'name' 则使用默认值
# # allure.dynamic.title(case_name)  # 使用 allure.dynamic.title() 动态设置标题
#


import asyncio
import os
import subprocess
import allure
import pytest
from concurrent.futures import ThreadPoolExecutor
from appium import webdriver
from auto_api.api import api_automation_test
from automation_app.app_test import app_automation_test
from automation_web.web import web_automation_test


class Executor:
    def __init__(self):
        self.executor = ThreadPoolExecutor()
        self.loop = asyncio.get_event_loop()
        self.driver = None  # 初始化 driver 为 None

    async def execute_task(self, task_name, params):
        with allure.step(f"执行任务: {task_name}"):
            if task_name == "app":
                result = await self.loop.run_in_executor(self.executor, self.run_app_automation, params)
            elif task_name == "web":
                result = await self.loop.run_in_executor(self.executor, self.run_web_automation, params)
            elif task_name == "api":
                result = await self.loop.run_in_executor(self.executor, self.run_api_automation, params)
            else:
                raise ValueError("Unknown task name")
            return result

    def run_app_automation(self, params):
        with allure.step("运行 App 自动化任务"):
            if not self.driver:
                caps = {
                    "platformName": "Android",
                    "appium:platformVersion": "14",
                    "appium:deviceName": "49MRGIFUYH6XQKQS",
                    "appium:appPackage": "vip.myaitalk.myai",
                    "appium:appActivity": ".ui.SplashActivity",
                    "appium:udid": "192.168.28.237:5555",
                    "appium:noReset": True,
                    "ensureWebviewsHavePages": True,
                    "nativeWebScreenshot": True,
                    "newCommandTimeout": 60,
                    "autoGrantPermissions": True
                }
                self.driver = webdriver.Remote("http://0.0.0.0:4723/wd/hub", caps)
                self.driver.implicitly_wait(10)

            allure.attach(str(params), "App自动化参数", allure.attachment_type.JSON)
            app_automation_test(params)
            return "App Task Completed"

    def run_web_automation(self, params):
        with allure.step("运行 Web 自动化任务"):
            allure.attach(str(params), "Web自动化参数", allure.attachment_type.JSON)
            web_automation_test()
            return "Web Task Completed"

    def run_api_automation(self, params):
        with allure.step("运行 API 自动化任务"):
            allure.attach(str(params), "API自动化参数", allure.attachment_type.JSON)
            api_automation_test()
            return "API Task Completed"

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None


# 定义测试任务列表
task_params = [
    {'id': 'TC001', 'tasks': 'app', 'Procedure': '同意', 'by': 'xpath',
     'Element_value': '//android.widget.TextView[@resource-id="vip.myaitalk.myai:id/aui_dialog_btn_right"]',
     'action': 'click'},
    {'id': 'TC002', 'tasks': 'app', 'Procedure': '始终允许', 'by': 'xpath',
     'Element_value': '//android.widget.Button[@text="始终允许"]', 'action': 'click'},
    {'id': 'TC003', 'tasks': 'web', 'Procedure': ''},
    {'id': 'TC004', 'tasks': 'api', 'Procedure': ''},
    {'id': 'TC005', 'tasks': 'app', 'Procedure': '点击教材', 'by': 'xpath',
     'Element_value': '//android.widget.TextView[@text="教材"]', 'action': 'click'}
]


@pytest.mark.parametrize("task", task_params, ids=[f"{t['id']}_{t['tasks']}" for t in task_params])
@pytest.mark.asyncio
async def test_main(task):
    # 动态设置测试用例名称
    allure.dynamic.title(f"{task['id']}: {task['tasks']}")

    executor = Executor()
    task_name = task['tasks']
    with allure.step(f"开始执行任务 {task['id']}"):
        result = await executor.execute_task(task_name, task)

    allure.attach(str(result), f"{task_name}任务执行结果", allure.attachment_type.TEXT)
    executor.close_driver()


def run_tests():
    # 设置 Allure 结果目录
    os.environ["ALLURE_RESULTS_DI"] = "./allure-results"

    # 运行 pytest 并生成 Allure 结果文件
    pytest.main(["test_executor.py", "--alluredir=./allure-results"])


if __name__ == "__main__":
    run_tests()
"""
pytest test_executor.py --alluredir=./allure-results
/Users/Wework/AutoTestX/allure/bin/allure generate ./allure-results -o ./allure-report --clean
"""