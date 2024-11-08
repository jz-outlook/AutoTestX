import asyncio
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
from utils.capture_screenshot import capture_screenshot
from utils.get_path import GetPath
from utils.read_excel_handler import OperationExcel


class Executor:
    driver_instance = None  # 静态变量，用于保存单例 App driver 实例
    web_driver_instance = None  # 静态变量，用于保存单例的 Web driver 实例
    _instance = None  # 单例实例
    _instance_lock = threading.Lock()  # 单例锁，确保多线程环境下的线程安全

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super(Executor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            # 初始化只在第一次调用时执行
            self.executor = ThreadPoolExecutor()
            self.timeout = 300  # 设置 5 分钟超时时间
            self.last_used = time.time()  # 记录最后一次使用时间
            self.last_task_name = None  # 记录上一次的任务名称
            self.initialized = True  # 防止再次初始化

            # 启动自动关闭线程
            self.auto_close_thread = threading.Thread(target=self.auto_close)
            self.auto_close_thread.daemon = True
            self.auto_close_thread.start()

    @classmethod
    def get_app_driver(cls):
        if cls.driver_instance is None:
            options = UiAutomator2Options()
            options.platform_name = "Android"
            options.platform_version = "14"
            options.device_name = "49MRGIFUYH6XQKQS"
            options.app_package = "vip.myaitalk.myai"
            options.app_activity = ".ui.SplashActivity"
            options.udid = "192.168.28.237:5555"
            options.ensure_webviews_have_pages = True
            options.native_web_screenshot = True
            options.new_command_timeout = 60
            options.auto_grant_permissions = True

            # 初始化 Appium driver
            cls.driver_instance = webdriver.Remote("http://0.0.0.0:4723/wd/hub", options=options)
            cls.driver_instance.implicitly_wait(10)
        return cls.driver_instance

    @classmethod
    def get_web_driver(cls):
        if cls.web_driver_instance is None:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            # 初始化 Chrome WebDriver 并保存为单例
            cls.web_driver_instance = selenium_webdriver.Chrome(options=chrome_options)
            cls.web_driver_instance.implicitly_wait(10)
        return cls.web_driver_instance

    async def execute_task(self, task_name, params):
        # 获取当前事件循环
        loop = asyncio.get_running_loop()

        # 如果当前任务名称与上一次不同，则延迟 5 秒
        if self.last_task_name is not None and task_name != self.last_task_name:
            print(f"任务类型改变，从 '{self.last_task_name}' 变为 '{task_name}'，即将延迟 5 秒...")
            # await asyncio.sleep(5)

        # 更新上一次的任务名称
        self.last_task_name = task_name

        with allure.step(f"执行任务: {task_name}"):
            if task_name == "app":
                driver = self.get_app_driver()
                result = await loop.run_in_executor(self.executor, self.run_app_automation, driver, params)
            elif task_name == "web":
                driver = self.get_web_driver()
                result = await loop.run_in_executor(self.executor, self.run_web_automation, driver, params)
            elif task_name == "api":
                result = await loop.run_in_executor(self.executor, self.run_api_automation, params)
            else:
                raise ValueError("Unknown task name")
            return result

    def run_app_automation(self, driver, params):
        with allure.step("运行 App 自动化任务"):
            allure.attach(str(params), "App自动化参数", allure.attachment_type.JSON)
            app_automation_test(driver, params)
        return "App Task Completed"

    def run_web_automation(self, driver, params):
        with allure.step("运行 Web 自动化任务"):
            allure.attach(str(params), "Web自动化参数", allure.attachment_type.JSON)
            web_automation_test(driver, params)
            return "Web Task Completed"

    def run_api_automation(self, params):
        with allure.step("运行 API 自动化任务"):
            allure.attach(str(params), "API自动化参数", allure.attachment_type.JSON)
            api_automation_test()
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

# 加载测试任务列表
data_directory = GetPath().get_data_case_path()
excel_data = OperationExcel(data_directory).read_excel()


@pytest.mark.parametrize("task", excel_data, ids=[f"{t['id']}_{t['tasks']}" for t in excel_data])
@pytest.mark.asyncio
async def test_main(task):
    executor = Executor()

    # 动态设置测试用例名称
    allure.dynamic.title(f"{task['id']}: {task['tasks']}: {task['procedure']}")

    task_name = task['tasks']
    action = task['action']
    if action == 'skip':
        pytest.skip("步骤为跳过步骤，将跳过此用例执行")
        print('步骤为跳过步骤，将跳过此用例执行')
    with allure.step(f"开始执行任务 {task['id']}"):
        result = await executor.execute_task(task_name, task)

    allure.attach(str(result), f"{task_name}任务执行结果", allure.attachment_type.TEXT)

    # 在最后一个测试用例之后关闭 driver
    if task == excel_data[-1]:
        executor.close_driver()
