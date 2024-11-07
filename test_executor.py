import asyncio
import os
import threading
import time
import allure
import pytest
import atexit

from concurrent.futures import ThreadPoolExecutor
from appium import webdriver
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.options import Options  # 导入 ChromeOptions 类
from appium.options.android import UiAutomator2Options
from auto_api.api import api_automation_test
from automation_app.app_test import app_automation_test
from automation_web.web import web_automation_test
from utils.get_path import GetPath
from utils.read_excel_handler import OperationExcel


class Executor:
    driver_instance = None  # 静态变量，用于保存单例 driver 实例
    web_driver_instance = None  # 静态变量，用于保存单例的 Web 浏览器 driver 实例

    def __init__(self):
        self.executor = ThreadPoolExecutor()
        self.loop = asyncio.get_event_loop()
        self.app_driver = self.get_app_driver()  # 初始化 app driver
        self.web_driver = self.get_web_driver()  # 初始化 web driver
        self.timeout = 300  # 设置 5 分钟超时时间
        self.last_used = time.time()  # 记录最后一次使用时间

    @classmethod
    def get_app_driver(cls):
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

    @classmethod
    def get_web_driver(cls):
        if cls.web_driver_instance is None:
            # 配置 Web 浏览器的 ChromeOptions
            chrome_options = Options()
            # 去掉无头模式
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # 初始化 Chrome WebDriver 并保存为单例
            cls.web_driver_instance = selenium_webdriver.Chrome(options=chrome_options)
            cls.web_driver_instance.implicitly_wait(10)
        return cls.web_driver_instance

    async def execute_task(self, task_name, params):
        with allure.step(f"执行任务: {task_name}"):
            if task_name == "app":
                result = await self.loop.run_in_executor(self.executor, self.run_app_automation, self.app_driver,
                                                         params)
            elif task_name == "web":
                result = await self.loop.run_in_executor(self.executor, self.run_web_automation, self.web_driver,
                                                         params)
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

    def run_web_automation(self, driver, params):
        with allure.step("运行 Web 自动化任务"):
            allure.attach(str(params), "Web自动化参数", allure.attachment_type.JSON)
            web_automation_test(driver, params)  # 将 driver 传递给下层函数
            return "Web Task Completed"

    def run_api_automation(self, params):
        with allure.step("运行 API 自动化任务"):
            allure.attach(str(params), "API自动化参数", allure.attachment_type.JSON)
            api_automation_test()  # 无需 driver 参数
            return "API Task Completed"

    def reset_timeout(self):
        """在每次执行任务时调用此方法重置超时"""
        self.last_used = time.time()

    def auto_close(self):
        """检查超时并自动关闭 driver"""
        while True:
            time.sleep(1)
            if time.time() - self.last_used > self.timeout:
                self.close_driver()
                print("Driver 超时关闭")
                break

    @classmethod
    def close_driver(cls):
        if cls.driver_instance:
            cls.driver_instance.quit()
            cls.driver_instance = None
        if cls.web_driver_instance:
            cls.web_driver_instance.quit()
            cls.web_driver_instance = None


# 使用 atexit 注册退出时的关闭操作
atexit.register(Executor.close_driver)

# 启动自动关闭线程
executor_instance = Executor()
auto_close_thread = threading.Thread(target=executor_instance.auto_close)
auto_close_thread.daemon = True
auto_close_thread.start()

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


def run_tests():
    # 设置 Allure 结果目录
    os.environ["ALLURE_RESULTS_DIR"] = "./allure-results"

    # 运行 pytest 并生成 Allure 结果文件
    pytest.main(["-s", "test_executor.py", "--alluredir=./allure-results"])


if __name__ == "__main__":
    run_tests()

# """
# pytest test_executor.py --alluredir=./allure-results
# /Users/Wework/AutoTestX/allure/bin/allure generate ./allure-results -o ./allure-report --clean
# """
