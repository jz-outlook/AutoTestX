import os
import shutil
import subprocess
import time

from utils.get_path import GetPath

AutoTestX_path = GetPath().get_parent_directory()

directories_to_delete = []
files_to_delete = [
    '/Users/Wework/AutoTestX/task_executor/automation_executor.c',
    '/Users/Wework/AutoTestX/task_executor/automation_app/assert_operation.c',
    '/Users/Wework/AutoTestX/task_executor/automation_app/check_elements.c',
]


def initialize():
    print("Initializing project...")
    setup_file = AutoTestX_path + "/setup.py"
    if os.path.exists(setup_file):
        print(f"{setup_file} exists. Running build command...")
        # 需要创建的目录列表
        directories = ["auto_api", "automation_app", "automation_web"]
        # 检查并创建目录
        for dir_name in directories:
            if not os.path.exists(AutoTestX_path + "/" + dir_name):
                print(f"Creating directory: {AutoTestX_path + '/' + dir_name}")
                os.makedirs(AutoTestX_path + "/" + dir_name)  # 创建目录
                directories_to_delete.append(AutoTestX_path + "/" + dir_name)
            else:
                print(f"Directory {AutoTestX_path + '/' + dir_name} already exists.")

        print('执行下一步操作')
        print("python", setup_file, "build_ext", "--inplace")

        # 更改工作目录
        os.chdir(AutoTestX_path)
        try:
            subprocess.run(["python", setup_file, "build_ext", "--inplace"], capture_output=True, text=True)
            print("Command executed successfully.")
            time.sleep(3)
            # 移动删除控制中心
            shutil.move(AutoTestX_path + '/automation_executor.cpython-39-darwin.so', AutoTestX_path + '/task_executor')
            os.remove(AutoTestX_path + '/task_executor/automation_executor.c')
            # 移动删除App
            shutil.move(AutoTestX_path + '/automation_app/assert_operation.cpython-39-darwin.so',
                        AutoTestX_path + '/task_executor/automation_app')
            shutil.move(AutoTestX_path + '/automation_app/check_elements.cpython-39-darwin.so',
                        AutoTestX_path + '/task_executor/automation_app')
            os.remove(AutoTestX_path + '/task_executor/automation_app/assert_operation.c')
            os.remove(AutoTestX_path + '/task_executor/automation_app/check_elements.c')
            # 移动删除web
            shutil.move(AutoTestX_path + '/automation_web/SMS_verification.cpython-39-darwin.so',
                        AutoTestX_path + '/task_executor/automation_web')
            shutil.move(AutoTestX_path + '/automation_web/web.cpython-39-darwin.so',
                        AutoTestX_path + '/task_executor/automation_web')
            os.remove(AutoTestX_path + '/task_executor/automation_web/SMS_verification.c')
            os.remove(AutoTestX_path + '/task_executor/automation_web/web.c')
            # 删除目录及其内容
            shutil.rmtree(AutoTestX_path + '/automation_app')
            shutil.rmtree(AutoTestX_path + '/automation_web')
            shutil.rmtree(AutoTestX_path + '/auto_api')
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while executing command: {e}")
    else:
        print(f"{setup_file} does not exist. Please ensure setup file is present.")
# 调用初始化函数
initialize()
print(directories_to_delete)
