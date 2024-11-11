import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains  # 可选：用于复杂操作

from task_executor.automation_web.SMS_verification import sms_verification
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
                expected_element_by = params.get('expected_element_by', '')  # 断言的类型
                expected_element_value = params.get('expected_element_value', '')  # 断言的类型

                # 调试信息：输出关键参数
                print(
                    f"element_by: {element_by}, element_value: {element_value}, action: {action}, send_keys: {send_keys}")

                # 执行具体的操作
                self._perform_action(params, element_by, element_value, action, send_keys)
                # 断言操作
                if expected_element_by == 'url':
                    self.assert_verification_success(expected_element_value)
                elif expected_element_by == 'xpath':
                    self.assert_element_visible(expected_element_by, expected_element_value)

        return "Web renwu Completed"

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
                sms_verification(elements)
                print("输入验证码操作")
            else:
                allure.attach("未知的操作类型", "操作状态", allure.attachment_type.TEXT)
                print(f"{params['procedure']},未知的操作类型或缺少必要参数")
                return "Web Task Incomplete"

        except Exception as e:
            allure.attach(f"操作失败: {str(e)}", "操作状态", allure.attachment_type.TEXT)
            print(f"{params['procedure']},操作失败: {e}")
            return "Web Task Failed"

    def assert_verification_success(self, expected_url):
        # 等待页面加载完成，并断言 URL 是否匹配
        WebDriverWait(self.driver, 10).until(EC.url_to_be(expected_url))
        print(f"断言预期url为: {expected_url},预期通过")
        assert self.driver.current_url == expected_url, f"预期跳转到 URL {expected_url}，但实际为 {self.driver.current_url}"

    def assert_verification_message(self, expected_message):
        # 等待消息元素出现并检查其文本内容
        message_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "success_message"))  # 使用正确的定位器
        )
        assert message_element.text == expected_message, f"预期消息为 '{expected_message}'，但实际显示为 '{message_element.text}'"

    def assert_element_visible(self, locator_by, locator):
        # 等待特定元素变为可见
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((locator_by, locator))
        )
        print(f"断言预期元素可见{locator},预期通过")
        assert element.is_displayed(), f"预期元素（定位符：{locator}）可见，但实际不可见"
