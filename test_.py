# test_main.py
import pytest
import allure
from initialize import initialize, kill_process_by_name
from task_executor.automation_executor import Executor
from utils.get_path import GetPath
from utils.read_excel_handler import OperationExcel

# 加载测试任务列表
data_directory = GetPath().get_data_case_path()
excel_data = OperationExcel(data_directory).read_excel()


@pytest.mark.parametrize("params", excel_data, ids=[f"{t['id']}_{t['tasks']}" for t in excel_data])
@pytest.mark.asyncio
async def test_main(params):
    executor = Executor()

    # 初始化内容
    # if params == excel_data[0]:
    #     initialize()
    #     kill_process_by_name("chromedriver")
    #     kill_process_by_name("chrome")

    # 动态设置测试用例名称
    allure.dynamic.title(f"{params['id']}: {params['tasks']}: {params['procedure']}")

    task_name = params['tasks']
    action = params['action']
    if action == 'skip':
        pytest.skip("步骤为跳过步骤，将跳过此用例执行")
        print('步骤为跳过步骤，将跳过此用例执行')

    with allure.step(f"开始执行任务 {params['id']}"):
        result = await executor.execute_task(task_name, params)

    allure.attach(str(result), f"{task_name}任务执行结果", allure.attachment_type.TEXT)

    # 在最后一个测试用例之后关闭 driver
    if params == excel_data[-1]:
        executor.close_driver()
