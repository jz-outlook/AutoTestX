import configparser
import os

from utils.get_path import GetPath


def load_config(config_path, section=None):
    config = configparser.ConfigParser()
    # 确保文件存在
    try:
        config.read(config_path)
        if not section:  # 如果 section 为空，设为 'DEFAULT'
            section = 'DEFAULT'
        if not config.has_section(section) and section != 'DEFAULT':
            raise KeyError(f"在配置文件中未找到'{section}'")
        config_dict = dict(config[section])
    except FileNotFoundError:
        raise FileNotFoundError(f"配置文件{config_path} 不存在。")
    return config_dict


def write_config(section, options):
    """ 将配置项写入配置文件中的指定部分。

    参数:
        section (str): 配置文件中的部分。
        options (dict): 要写入的配置项字典。
    返回:
        None
    """
    try:
        config_path = GetPath().get_project_root() + '/config/config.ini'
        config = configparser.ConfigParser()

        # 读取现有配置
        if os.path.exists(config_path):
            config.read(config_path)

        if not config.has_section(section):
            config.add_section(section)

        for key, value in options.items():
            config.set(section, key, value)

        with open(config_path, 'w') as configfile:
            config.write(configfile)
        print(f"配置文件 {config_path} 已更新。写入内容：{options}")
        # 文件写入成功
        return True  # 返回 True 表示写入成功
    except Exception as e:  # 捕获所有可能的异常
        print(f"写入配置文件失败: {e}")
        return False  # 返回 False 表示写入失败

def get_config(name=None):
    return load_config("/Users/Wework/AutoTestX/config/config.ini", name)

# 使用示例
# print(load_config("/Users/Wework/AutoTestX/config/config.ini"))
# write_config('api', {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Nzk3LCJleHAiOjE3MzE5MDM0NjB9.DYgXYlTTYP+Y2WKpfcabNlXClaC3Cy/xrzRZlzfgZbw=', 'option2': 'value2'})


data = load_config("/Users/Wework/AutoTestX/config/config.ini", "app")
print(data)
print(data.get('platform_name'))