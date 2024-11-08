import time

import allure


async def capture_screenshot(driver, case_id, step_name="Final_Screenshot"):
    with allure.step(f"开始执行截图任务"):
        """在每个任务完成后捕获并附加截图到 Allure 报告中."""
        try:
            screenshot = driver.get_screenshot_as_png()

            if screenshot:
                # 确保附加截图操作在主线程执行
                time.sleep(1)  # 延迟片刻，确保截图完全生成
                allure.attach(screenshot, name=f'{step_name}_{case_id}', attachment_type=allure.attachment_type.PNG)
                print(f"{step_name} 完成，已生成截图并附加到 Allure 报告: {case_id}")
            else:
                print(f"{step_name} 截图失败: 无法获取截图内容")

        except Exception as e:
            print(f"{step_name} 截图异常: {e}")




