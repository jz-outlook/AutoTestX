import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

import pytest

from task_executor.automation_app.assert_operation import check_element_existence
from utils.capture_screenshot import capture_screenshot


def wait_for_element(driver, by, value, timeout=20):
    """显性等待：等待元素出现在 DOM 中"""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


class AppElementsOperation:
    def element_check_operation(self, driver, params):
        try:
            # 执行操作并进行后续检查
            self.perform_action(driver, params)
            self.action_sleep(params)
            # 验证操作的结果
            # self.verify_action(element, params)
            # 检查操作后的状态
            check_element_existence(driver, params)

        except Exception as e:
            # 在发生异常时捕获截图
            name = params['id']
            allure.attach(f"步骤 {name} 执行失败，异常信息: {e}", name=f"Error_{name}",
                          attachment_type=allure.attachment_type.TEXT)
            print(f'元素加载失败 {name}: {e}')
            pytest.fail(f"步骤 {name} 执行失败: {e}")

    def perform_action(self, driver, params):
        """根据定位信息查找元素并执行指定操作"""
        locator_by, element_value, action, send_keys = self.parse_action_params(params)

        if not element_value or not action:
            allure.attach("缺少必要参数", "操作状态", allure.attachment_type.TEXT)
            print("缺少必要参数：element_value 或 action")
            return None  # 返回 None 以便调用者处理异常情况
        try:
            element = wait_for_element(driver, locator_by, element_value)
            assert element is not None, f"ID:{params['id']} 元素 {element_value} 不存在或无法定位"

            # 执行操作
            if action == "click":
                element.click()
                allure.attach("点击操作成功", "操作状态", allure.attachment_type.TEXT)
                print("点击操作成功")
            elif action == "send_keys":
                element.clear()  # 可选：清空输入框
                element.send_keys(send_keys)
                allure.attach(f"输入操作成功: {send_keys}", "操作状态", allure.attachment_type.TEXT)
                print(f"输入操作成功: {send_keys}")
            elif action == "up_sliding":
                allure.attach(f"屏幕上滑成功: {send_keys}", "操作状态", allure.attachment_type.TEXT)
                self.slide_up_aperation(driver)
                print(f"屏幕上滑成功")
            else:
                allure.attach("未知的操作类型", "操作状态", allure.attachment_type.TEXT)
                print("未知的操作类型")
                return None
            return element  # 返回找到的元素，以便后续操作验证
        except Exception as e:
            allure.attach(f"操作失败: {str(e)}", "操作状态", allure.attachment_type.TEXT)
            print(f"操作失败ID:{params['id']}元素不可操作 {e}")
            print(f'{e}')
            pytest.fail(f"操作失败: {str(e)}")  # 在失败时使用 pytest.fail() 引发异常
            return None

    def parse_action_params(self, params):
        """解析并返回操作所需的定位方式、元素值、操作类型及输入文本"""
        element_by = params.get('by', 'xpath').lower()  # 默认使用 xpath
        element_value = params.get('element')  # 元素定位符
        action = params.get('action', '').lower()  # 操作类型，例如 'click' 或 'send_keys'
        send_keys = params.get('send_keys', '')  # 要输入的文本，默认为空

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
        }.get(element_by, By.XPATH)

        return locator_by, element_value, action, send_keys

    def action_sleep(self, params):
        """获取并执行等待时间"""
        sleep_value = params.get('sleep')
        if sleep_value:
            try:
                sleep_time = int(sleep_value)
                time.sleep(sleep_time)
                print(f'执行了等待操作{sleep_time}秒')
            except ValueError:
                print(f"等待时间设置错误，需要的是一个整数，但得到了 '{sleep_value}'")
                raise

    def verify_action(self, element, params):
        """执行操作后验证操作成功或失败"""
        # 添加后续验证步骤（可以根据实际需求自定义）
        # 例如检查页面上的其他元素状态
        verification_text = params.get("verification_text", "")
        if verification_text:
            try:
                assert verification_text in element.text, f"期望文本 '{verification_text}' 未找到"
                allure.attach(f"验证通过，找到期望文本: {verification_text}", "验证状态", allure.attachment_type.TEXT)
                print(f"验证通过，找到期望文本: {verification_text}")
            except AssertionError as e:
                allure.attach(str(e), "验证状态", allure.attachment_type.TEXT)
                print(f"验证失败: {e}")

    def slide_up_aperation(self, driver):
        # 需要定位到要滑动的页面上的元素
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        # 屏幕中央起始位置
        actions.w3c_actions.pointer_action.move_to_location(500, 1500)
        actions.w3c_actions.pointer_action.pointer_down()
        # 滑动半屏
        actions.w3c_actions.pointer_action.move_to_location(500, 600)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        time.sleep(10)
        pass
