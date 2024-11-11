# automation_executor.py
import threading
import time
import atexit
import asyncio
import allure
from concurrent.futures import ThreadPoolExecutor
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from task_executor.auto_api.api import api_automation_test
from task_executor.task_operations import app_automation_test, web_automation_test


class Executor:
    driver_instance = None
    web_driver_instance = None
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = super(Executor, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.executor = ThreadPoolExecutor()
            self.timeout = 300
            self.last_used = time.time()
            self.last_task_name = None
            self.initialized = True

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
            options.no_reset = False

            cls.driver_instance = webdriver.Remote("http://0.0.0.0:4723/wd/hub", options=options)
            cls.driver_instance.implicitly_wait(10)
        return cls.driver_instance

    @classmethod
    def get_web_driver(cls):
        if cls.web_driver_instance is None:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            # 使用webdriver-manager管理驱动路径
            service = Service(ChromeDriverManager().install())
            cls.web_driver_instance = selenium_webdriver.Chrome(service=service, options=chrome_options)
            cls.web_driver_instance.implicitly_wait(10)

        return cls.web_driver_instance

    async def execute_task(self, task_name, params):
        loop = asyncio.get_running_loop()
        if self.last_task_name is not None and task_name != self.last_task_name:
            print(f"任务类型改变，从 '{self.last_task_name}' 变为 '{task_name}'，即将延迟 5 秒...")
            await asyncio.sleep(5)

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
        self.last_used = time.time()

    def auto_close(self):
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
