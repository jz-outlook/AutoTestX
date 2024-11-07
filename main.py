import asyncio
import os
import allure
import pytest
from concurrent.futures import ThreadPoolExecutor
from appium import webdriver
from appium.options.android import UiAutomator2Options
from auto_api.api import api_automation_test
from automation_app.app_test import app_automation_test
from automation_web.web import web_automation_test
from utils.get_path import GetPath
from utils.read_excel_handler import OperationExcel


class Executor:
    driver_instance = None  # 静态变量，用于保存单例 driver 实例

    def __init__(self):
        self.executor = ThreadPoolExecutor()
        self.loop = asyncio.get_event_loop()
        self.driver = self.get_driver()  # 获取单例 driver 实例

    @classmethod
    def get_driver(cls):
        if cls.driver_instance is None:
            # 设置 Desired Capabilities 使用 UiAutomator2Options
            options = UiAutomator2Options()
            options.platform_name = "Android"
            options.platform_version = "14"
            options.device_name = "49MRGIFUYH6XQKQS"
            options.app_package = "vip.myaitalk.myai"
            options.app_activity = ".ui.SplashActivity"
            options.udid = "192.168.28.237:5555"
            # options.no_reset = True           # 保持应用状态，不重置
            # options.full_reset = False        # 禁用完全重置
            options.ensure_webviews_have_pages = True
            options.native_web_screenshot = True
            options.new_command_timeout = 60
            options.auto_grant_permissions = True

            # 使用 options 参数初始化 WebDriver，并设置为单例
            cls.driver_instance = webdriver.Remote("http://0.0.0.0:4723/wd/hub", options=options)
            cls.driver_instance.implicitly_wait(10)
        return cls.driver_instance

    async def execute_task(self, task_name, params):
        with allure.step(f"执行任务: {task_name}"):
            if task_name == "app":
                result = await self.loop.run_in_executor(self.executor, self.run_app_automation, self.driver, params)
            elif task_name == "web":
                result = await self.loop.run_in_executor(self.executor, self.run_web_automation, self.driver, params)
            elif task_name == "api":
                result = await self.loop.run_in_executor(self.executor, self.run_api_automation, params)
            else:
                raise ValueError("Unknown task name")
            return result

    def run_app_automation(self, driver, params):
        with allure.step("运行 App 自动化任务"):
            allure.attach(str(params), "App自动化参数", allure.attachment_type.JSON)
            app_automation_test(driver, params)  # 将 driver 传递给下层函数
            return "App Task Completed"

    def run_web_automation(self, params):
        with allure.step("运行 Web 自动化任务"):
            allure.attach(str(params), "Web自动化参数", allure.attachment_type.JSON)
            web_automation_test()  # 将 driver 传递给下层函数
            return "Web Task Completed"

    def run_api_automation(self, params):
        with allure.step("运行 API 自动化任务"):
            allure.attach(str(params), "API自动化参数", allure.attachment_type.JSON)
            api_automation_test()  # 无需 driver 参数
            return "API Task Completed"

    @classmethod
    def close_driver(cls):
        if cls.driver_instance:
            cls.driver_instance.quit()
            cls.driver_instance = None


# 加载测试任务列表
data_directory = GetPath().get_data_case_path()
excel_data = OperationExcel(data_directory).read_excel()


@pytest.mark.parametrize("task", excel_data, ids=[f"{t['id']}_{t['tasks']}" for t in excel_data])
@pytest.mark.asyncio
async def test_main(task):
    # 动态设置测试用例名称
    allure.dynamic.title(f"{task['id']}: {task['tasks']}")

    executor = Executor()
    task_name = task['tasks']
    with allure.step(f"开始执行任务 {task['id']}"):
        result = await executor.execute_task(task_name, task)

    allure.attach(str(result), f"{task_name}任务执行结果", allure.attachment_type.TEXT)

    # 在最后一个测试用例之后关闭 driver
    if task == excel_data[-1]:
        executor.close_driver()


if __name__ == "__main__":
    asyncio.run(test_main())






