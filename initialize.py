import os
import shutil
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from task_executor.automation_web.SMS_verification import sms_verification
from utils.get_path import GetPath
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import signal
import psutil  # 需要安装 psutil: pip install psutil

AutoTestX_path = os.getcwd()


def initialize():
    print("正在初始化项目...")
    setup_file = AutoTestX_path + "/setup.py"
    if os.path.exists(setup_file):
        print(f"{setup_file} 存在。正在运行构建命令...")
        # 更改工作目录
        os.chdir(AutoTestX_path)

        directory_path = os.path.join(AutoTestX_path, 'automation_api')
        os.makedirs(directory_path, exist_ok=True)
        directory_path = os.path.join(AutoTestX_path, 'automation_app')
        os.makedirs(directory_path, exist_ok=True)
        directory_path = os.path.join(AutoTestX_path, 'automation_web')
        os.makedirs(directory_path, exist_ok=True)

        try:
            # 执行构建命令
            subprocess.run(
                ["python3", setup_file, "build_ext", "--inplace"],
                capture_output=True,
                text=True
            )
            print("命令执行成功。")
            time.sleep(3)

            # 检查 .so 文件是否存在
            so_files = [f for f in os.listdir(AutoTestX_path) if f.endswith('.so')]
            if so_files:
                # 列出目录中的所有文件
                files_in_directory = os.listdir(AutoTestX_path)
                # 筛选出以 'automation_executor' 开头的 .so 文件
                filtered_files = [file for file in files_in_directory if
                                  file.startswith('automation_executor') and file.endswith('.so')]
                print("找到以下 .so 文件:")
                print(filtered_files)

                shutil.move(AutoTestX_path + '/' + filtered_files[0], AutoTestX_path + '/task_executor')

                # 处理 automation_api
                handle_directory(
                    source_path=os.path.join(AutoTestX_path, 'automation_api'),
                    target_path=os.path.join(AutoTestX_path, 'task_executor/automation_api'),
                    file_to_remove=os.path.join(AutoTestX_path, 'task_executor/automation_api/api_parameter_handler.py')
                )

                # 处理 automation_app
                handle_directory(
                    source_path=os.path.join(AutoTestX_path, 'automation_app'),
                    target_path=os.path.join(AutoTestX_path, 'task_executor/automation_app'),
                    file_to_remove=os.path.join(AutoTestX_path,
                                                'task_executor/automation_app/action_perform_operation.py')
                )

                # 处理 automation_web
                handle_directory(
                    source_path=os.path.join(AutoTestX_path, 'automation_web'),
                    target_path=os.path.join(AutoTestX_path, 'task_executor/automation_web'),
                    file_to_remove=os.path.join(AutoTestX_path, 'task_executor/automation_app/web.py')
                )

                os.rmdir(AutoTestX_path + 'setup.py')
                os.rmdir(AutoTestX_path + 'initialize.py')
                os.rmdir(AutoTestX_path + 'task_executor/automation_executor.py')
                time.sleep(3)
                login_operation()
            else:
                print("没有找到 .so 文件。请检查构建配置。")
        except subprocess.CalledProcessError as e:
            print(f"执行命令时发生错误: {e}")
    else:
        print(f"{setup_file} 不存在。请确保 setup 文件存在。")


def login_operation():
    options = Options()
    # 设置用户数据目录
    options.add_argument(f"--user-data-dir={GetPath().get_project_root()}/chrome")
    # 设置远程调试端口
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    options.add_argument("--no-sandbox")  # 无沙盒模式

    driver = webdriver.Chrome(options=options)
    driver.get("https://admin-test.myaitalk.vip:6060/#/login")
    print('打开 URL ')

    # 等待用户名输入框加载完成
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "phone_number_input"))
    ).send_keys("19900000001")  # 输入用户名

    # 等待密码输入框加载完成
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "password_input"))
    ).send_keys("Hy123...")  # 输入密码

    print('输入用户名密码')

    # 等待登录按钮可点击并点击登录
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".arco-btn.arco-btn-primary.arco-btn-size-default.arco-btn-shape-square.arco-btn-long"))
    )
    login_button.click()  # 点击登录

    print('尝试登录')

    # 等待验证码输入框加载完成
    elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".arco-input.arco-verification-code-input"))
    )
    print('输入验证码')
    sms_verification(elements)  # 假设这是一个你自定义的函数来处理验证码输入

    # 等待验证按钮可点击并点击验证
    verify_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".arco-btn.arco-btn-primary.arco-btn-size-default.arco-btn-shape-square.arco-btn-long"))
    )
    verify_button.click()  # 点击验证

    print('点击验证')

    time.sleep(10)
    driver.close()


def handle_directory(source_path, target_path, file_to_remove):
    # 检查源目录是否存在
    if not os.path.exists(source_path):
        print(f"源目录 {source_path} 不存在，跳过处理")
        return

    # 获取目录中的文件列表
    files_in_directory = os.listdir(source_path)
    if not files_in_directory:
        print(f"目录 {source_path} 中没有文件")
    else:
        # 移动第一个文件到目标路径
        file_to_move = files_in_directory[0]
        shutil.move(f"{source_path}/{file_to_move}", target_path)
        print(f"文件 {file_to_move} 已移动到 {target_path}")

    # 删除源目录
    os.rmdir(source_path)
    print(f"目录 {source_path} 已删除")

    # 删除指定文件
    if os.path.exists(file_to_remove):
        os.remove(file_to_remove)
        print(f"文件 {file_to_remove} 已删除")
    else:
        print(f"文件 {file_to_remove} 不存在，跳过删除")