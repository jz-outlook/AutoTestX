import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains  # 可选：用于复杂操作

from task_executor.automation_web.SMS_verification import sms_verification


class WebAutomation:
    def __init__(self, driver):
        self.driver = driver

    def web_automation_test(self, params):
        """执行 Web 自动化测试任务"""
        with allure.step("执行 Web 自动化测试任务"):
            # 将传入的参数附加到 Allure 报告中
            allure.attach(str(params), "Web自动化参数", allure.attachment_type.JSON)

            # 访问 URL（如果指定了 url 参数）
            url = params.get('url')
            if url:
                self._open_url(url)
            else:
                # 从 params 中提取操作信息
                element_by = params.get('by', 'xpath').lower()  # 默认使用 xpath
                element_value = params.get('element')  # 元素定位符
                action = params.get('action', '').lower()  # 操作类型，例如 'click' 或 'send_keys'
                send_keys = params.get('send_keys', '')  # 要输入的文本，默认为空

                # 调试信息：输出关键参数
                print(
                    f"element_by: {element_by}, element_value: {element_value}, action: {action}, send_keys: {send_keys}")

                # 执行具体的操作
                self._perform_action(params, element_by, element_value, action, send_keys)

        return "Web Task Completed"

    def _open_url(self, url):
        """打开指定的 URL 并在 Allure 报告中附加信息"""
        try:
            self.driver.get(url)
            time.sleep(3)
            allure.attach(f"访问 URL: {url}", "URL 访问状态", allure.attachment_type.TEXT)
            print(f"访问 URL: {url}")
        except Exception as e:
            allure.attach(f"访问 URL 失败: {str(e)}", "操作状态", allure.attachment_type.TEXT)
            print(f"访问 URL 失败: {e}")

    def _perform_action(self, params, element_by, element_value, action, send_keys=None):
        """根据指定操作查找元素并执行点击、输入等操作"""
        # 根据不同的定位方式设置 By 对象
        locator_by = {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'class_name': By.CLASS_NAME,
            'tag_name': By.TAG_NAME,
            'link_text': By.LINK_TEXT,
            'partial_link_text': By.PARTIAL_LINK_TEXT
        }.get(element_by, By.CSS_SELECTOR)  # 默认使用 css_selector

        # 检查参数是否齐全
        if not element_value or not action:
            allure.attach("缺少必要参数", "操作状态", allure.attachment_type.TEXT)
            print("缺少必要参数：element_value 或 action")
            return "Web Task Incomplete"

        # 查找元素并执行操作
        try:
            element = self.driver.find_element(locator_by, element_value)

            if action == "click":
                element.click()
                allure.attach("点击操作成功", "操作状态", allure.attachment_type.TEXT)
                print(f"{params['procedure']},点击操作成功")

            elif action == "send_keys":
                element.clear()  # 可选：清空输入框
                element.send_keys(send_keys)
                allure.attach(f"输入操作成功: {send_keys}", "操作状态", allure.attachment_type.TEXT)
                print(f"{params['procedure']},输入操作成功: {send_keys}")

            elif action == "sms_verification":
                elements = self.driver.find_elements(locator_by, element_value)
                sms_verification(locator_by, elements, self.driver)
                print("输入验证码操作")
            else:
                allure.attach("未知的操作类型", "操作状态", allure.attachment_type.TEXT)
                print(f"{params['procedure']},未知的操作类型或缺少必要参数")
                return "Web Task Incomplete"

        except Exception as e:
            allure.attach(f"操作失败: {str(e)}", "操作状态", allure.attachment_type.TEXT)
            print(f"{params['procedure']},操作失败: {e}")
            return "Web Task Failed"
