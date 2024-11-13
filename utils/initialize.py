import os
import shutil
import subprocess
import time

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
            result = subprocess.run(
                ["python3", setup_file, "build_ext", "--inplace"],
                capture_output=True,
                text=True
            )
            print("命令执行成功。")
            time.sleep(3)

            # 检查 .so 文件是否存在
            so_files = [f for f in os.listdir(AutoTestX_path) if f.endswith('.so')]
            if so_files:
                print("找到以下 .so 文件:")
                for so_file in so_files:
                    print(f"- {so_file}")
                    shutil.move(AutoTestX_path + '/' + so_file, AutoTestX_path + '/task_executor')
                    os.remove(AutoTestX_path + '/task_executor/automation_executor.py')
                    os.remove(AutoTestX_path + '/setup.py')
            else:
                print("没有找到 .so 文件。请检查构建配置。")
        except subprocess.CalledProcessError as e:
            print(f"执行命令时发生错误: {e}")
    else:
        print(f"{setup_file} 不存在。请确保 setup 文件存在。")
