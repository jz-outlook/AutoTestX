import allure
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSelectorException, NoSuchElementException

from utils.capture_screenshot import capture_screenshot


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
        msg = f"用例 {case_id} 缺少必要的定位参数: expected_element_by 或 expected_element_value"
        allure.attach(msg, "定位参数缺失", allure.attachment_type.TEXT)
        print(msg)
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
