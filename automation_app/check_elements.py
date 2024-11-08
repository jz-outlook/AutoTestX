import time
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

from automation_app.check_action import CheckAction


def wait_for_element(driver, by, value, timeout=20):
    """显性等待：等待元素出现在 DOM 中"""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


class CheckElements:
    def check_element(self, driver, params):
        try:
            self.perform_action(driver, params)
            self.action_sleep(params)
        except Exception as e:
            print(f"执行操作时发生异常: {e}")
            raise  # 暂停执行

    def perform_action(self, driver, params):
        element = wait_for_element(driver, params['by'], params['element'], timeout=20)
        assert element is not None, f"元素 {params['element']} 不存在或无法定位"
        CheckAction().check_action(driver, params)

    def action_sleep(self, params):
        # 获取 sleep 值
        sleep_value = params.get('sleep')
        # 检查 sleep_value 是否存在且不是空字符串
        if sleep_value:
            try:
                # 将 sleep 值转换为整数
                sleep_time = int(sleep_value)
                time.sleep(sleep_time)
                print('执行了等待操作')
            except ValueError:
                print(f"等待时间设置错误，需要的是一个整数，但得到了 '{sleep_value}'")
                raise
