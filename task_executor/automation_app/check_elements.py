import time
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from task_executor.automation_app.action_perform_operation import check_element_existence, perform_action


def wait_for_element(driver, by, value, timeout=20):
    """显性等待：等待元素出现在 DOM 中"""
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))


class AppElementsOperation:
    def element_check_operation(self, driver, params):
        try:
            # 执行操作并进行后续检查
            perform_action(driver, params)
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
