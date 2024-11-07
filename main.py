import asyncio
import os
import allure
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
        if params is None:
            params = {}

        # 根据任务名称动态调用对应的方法并传递参数
        with allure.step(f"使用参数执行任务: {task_name}"):
            if task_name == "app":
                result = await self.loop.run_in_executor(self.executor, self.run_app_automation, params)
            elif task_name == "web":
                result = await self.loop.run_in_executor(self.executor, self.run_web_automation, params)
            elif task_name == "api":
                result = await self.loop.run_in_executor(self.executor, self.run_api_automation, params)
            else:
                raise ValueError("Unknown task name")

        print(f"Result of {task_name} task: {result}")
        return result

    def run_app_automation(self, params):
        # 在 Allure 中记录步骤
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

            print("执行 App 自动化任务..")
            print(f"使用参数执行应用程序自动化任务: {params}")
            app_automation_test(params)
            return "App Task Completed"

    def run_web_automation(self, params):
        with allure.step("运行 Web 自动化任务"):
            print("执行 Web 自动化任务...")
            print(f"使用参数执行 Web 自动化任务: {params}")
            web_automation_test()
            return "Web Task Completed"

    def run_api_automation(self, params):
        with allure.step("运行 API 自动化任务"):
            print("执行 API 自动化任务...")
            api_automation_test()
            print(f"使用参数执行 API 自动化任务: {params}")
            return "API Task Completed"

    async def execute(self, task_params):
        results = []
        for task in task_params:
            task_name = task.get("tasks")
            result = await self.execute_task(task_name, task)
            results.append({task_name: result})
        return results

    def close_driver(self):
        if self.driver:
            self.driver.quit()
            self.driver = None


# 手动调用执行器并生成 Allure 报告
async def main():
    executor = Executor()

    # 设置 Allure 报告存储目录
    os.makedirs("./allure-results", exist_ok=True)
    # os.environ["ALLURE_RESULTS_DIR"] = "./allure-results"
    os.environ["ALLURE_RESULTS_DIR"] = "/Users/Wework/AutoTestX/allure-results"

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

    # 执行任务并生成结果
    with allure.step("执行所有任务"):
        results = await executor.execute(task_params)

    print("最终结果:", results)
    executor.close_driver()


if __name__ == "__main__":
    asyncio.run(main())