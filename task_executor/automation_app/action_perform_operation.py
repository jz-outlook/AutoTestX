import time
import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


def wait_for_element(driver, by, value, timeout=20):
    """显性等待：等待元素出现在 DOM 中"""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def assert_and_capture_screenshot(driver, case, assert_condition, success_msg, failure_msg):
    """
    检查元素是否符合预期并捕获截图。

    参数:
        driver: WebDriver 实例
        case: 测试用例字典，包含 'id'、'expected_element_by'、'expected_element_value' 等信息
        assert_condition: 布尔值，表示断言条件是否满足
        success_msg: 成功信息字符串
        failure_msg: 失败信息字符串
    """
    case_id = case.get('id', 'unknown_case')

    try:
        if assert_condition:
            allure.attach(driver.get_screenshot_as_png(), name=f'Success_Screenshot_{case_id}',
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(success_msg, name=f"Success_{case_id}", attachment_type=allure.attachment_type.TEXT)
            print(success_msg)
        else:
            raise AssertionError(failure_msg)

    except AssertionError as e:
        allure.attach(driver.get_screenshot_as_png(), name=f'Screenshot_{case_id}',
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(failure_msg, name=f"Error_{case_id}", attachment_type=allure.attachment_type.TEXT)
        print(f"断言失败 {case_id}: {e}")
        pytest.fail(failure_msg)


def check_element_existence(driver, case):
    """
    检查预期元素是否存在，并附加结果到 Allure 报告中。
    """
    expected_by = case.get('expected_element_by')
    expected_value = case.get('expected_element_value')
    case_id = case.get('id', 'unknown_case')

    if not expected_by or not expected_value:
        msg = f"用例 {case_id} 缺少断言必要的定位参数: expected_element_by 或 expected_element_value"
        print(msg)
        allure.attach(msg, "断言必要的定位参数缺失", allure.attachment_type.TEXT)
        pytest.fail(msg)

    try:
        print(f"断言执行元素检查，Case ID: {case_id}, Expected By: {expected_by}, Expected Value: {expected_value}")

        # 等待期望元素的出现
        with allure.step(f"验证元素 {expected_value} 是否存在"):
            expected_element = wait_for_element(driver, expected_by, expected_value, timeout=10)
            assert expected_element is not None, f"操作后预期元素 {expected_value} 不存在"
            print(f"操作后预期元素 {expected_value} 存在")

    except (InvalidSelectorException, NoSuchElementException) as e:
        allure.attach(f"定位元素失败: {e}", name=f"Error_{case_id}", attachment_type=allure.attachment_type.TEXT)
        print(f"元素定位失败 {case_id}: {e}")
        pytest.fail(f"定位元素失败 {case_id}: {e}")

    except AssertionError as e:
        allure.attach(str(e), name=f"Error_{case_id}", attachment_type=allure.attachment_type.TEXT)
        print(f"断言失败 {case_id}: {e}")
        pytest.fail(str(e))


def perform_action(driver, params):
    """根据定位信息查找元素并执行指定操作"""
    locator_by, element_value, action, send_keys = parse_action_params(params)

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
            slide_up_aperation(driver)
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


def parse_action_params(params):
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


def slide_up_aperation(driver):
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
