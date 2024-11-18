import os


class GetPath:

    def __init__(self):
        abs_path = os.path.abspath(__file__)
        root_path = os.path.dirname(abs_path)
        # 项目根目录的绝对路径
        self.path = os.path.dirname(root_path)

    def get_parent_directory(self):
        """获取当前工作目录的上级目录"""
        return os.path.dirname(os.getcwd())

    def get_login_case_path(self):
        path = self.path + '/data/login/login.xls'
        return str(path)

    def get_data_case_path(self):
        path = self.path + '/tests/data.xls'
        return str(path)

    def get_project_root(self, project_name="AutoTestX"):
        """
        获取项目根路径函数，无论在哪个层级调用都能返回项目根目录。
        :param project_name: 项目名称（根目录文件夹名），默认值为 "AutoTestX"
        :return: 项目根路径字符串
        """
        current_path = os.path.abspath(__file__)  # 当前文件路径
        while True:
            # 获取当前路径的父路径和文件夹名称
            parent_path, current_folder = os.path.split(current_path)

            if current_folder == project_name:
                return os.path.join(parent_path, current_folder)  # 返回完整路径

            if not parent_path or parent_path == current_path:  # 已到根目录，未找到
                raise RuntimeError(f"项目根目录 '{project_name}' 未找到，请确认项目结构。")

            current_path = parent_path  # 向上层路径移动

    def get_config_path(self):
        return self.get_project_root() + "/config/config.ini"


# # 使用示例
# mp3_directory = GetPath().get_data_case_path()
# print(f"当前工作目录是: {mp3_directory}")
