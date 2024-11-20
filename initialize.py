import os
import shutil
import subprocess
import time
from selenium import webdriver

from task_executor.automation_web.SMS_verification import sms_verification
from utils.get_path import GetPath
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

AutoTestX_path = os.getcwd()


def initialize():
    print("正在初始化项目...")
    setup_file = AutoTestX_path + "/setup.py"
    if os.path.exists(setup_file):
        print(f"{setup_file} 存在。正在运行构建命令...")
        # 更改工作目录
        os.chdir(AutoTestX_path)
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
                os.remove(AutoTestX_path + '/task_executor/automation_executor.py')
                os.remove(AutoTestX_path + '/setup.py')
                os.remove(AutoTestX_path + '/initialize.py')

                # 执行 chrome 命令
                # cmd = f'open -na "Google Chrome" --args --remote-debugging-port=9222 --user-data-dir={GetPath().get_project_root() + "/chrome"}'
                # process = subprocess.Popen(cmd, shell=True)
                # process.wait()
                # driver = webdriver.Chrome()
                # driver.get("https://admin-test.myaitalk.vip:6060/#/login")
                # print("请手动登录...")
                # time.sleep(60)  # 给足够时间手动登录

                options = Options()
                # 设置用户数据目录
                options.add_argument(f"--user-data-dir={GetPath().get_project_root()}/chrome")
                # 设置远程调试端口
                options.add_argument("--remote-debugging-port=9222")

                # 使用设置好的选项启动Chrome
                print('打开浏览器')
                driver = webdriver.Chrome(options=options)
                driver.get("https://admin-test.myaitalk.vip:6060/#/login")
                print('打开 URL ')
                driver.find_element(By.ID, "phone_number_input").send_keys("19900000001")  # 用户名
                driver.find_element(By.ID, "password_input").send_keys("Hy123...")  # 密码
                print('输入用户名密码')
                driver.find_element(By.CSS_SELECTOR,
                                    ".arco-btn.arco-btn-primary.arco-btn-size-default.arco-btn-shape-square.arco-btn-long").click()  # 点击登录
                elements = driver.find_elements(By.CSS_SELECTOR, ".arco-input.arco-verification-code-input")  # 输入验证码
                print('输入验证码')
                sms_verification(elements)
                driver.find_element(By.CSS_SELECTOR,
                                    ".arco-btn.arco-btn-primary.arco-btn-size-default.arco-btn-shape-square.arco-btn-long").click()  # 点击验证
                print('点击验证')
                time.sleep(10)
                driver.close()

            else:
                print("没有找到 .so 文件。请检查构建配置。")
        except subprocess.CalledProcessError as e:
            print(f"执行命令时发生错误: {e}")
    else:
        print(f"{setup_file} 不存在。请确保 setup 文件存在。")
