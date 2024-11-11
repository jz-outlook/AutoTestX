import configparser

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


