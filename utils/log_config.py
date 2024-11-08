import logging
import os
import datetime



def get_main_path():
    current_directory = os.getcwd()
    parent_directory = os.path.dirname(current_directory)
    return parent_directory

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', env="Development", phase="Initialization", api="General"):
        super().__init__(fmt, datefmt, style)
        self.env = env
        self.phase = phase
        self.api = api

    """自定义日志格式器，根据日志级别设置不同的输出格式。"""

    def format(self, record):
        record.env = self.env
        record.phase = self.phase
        record.api = self.api
        # 根据日志级别动态设置日志格式
        if record.levelno == logging.DEBUG:
            # 添加了 %(filename)s 和 %(lineno)d 以显示文件名和行号
            # self._style._fmt = f"[%(asctime)s] [TestEnv: {self.env}] [Phase: {self.phase}] [API: {self.api}] - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
            self._style._fmt = f"[%(asctime)s] - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        else:
            # 对于INFO及以上级别的日志，使用固定前缀和不包括文件名和行号
            self._style._fmt = "%(asctime)s - %(levelname)s - %(message)s"
        return super().format(record)


def setup_logger(level='INFO'):
    """
    配置并返回一个日志器。

    :param level: 日志级别，默认为'INFO'
    :return: 配置好的日志器
    """
    # 获取或创建一个日志器
    logger = logging.getLogger("APITestFrameworkLogger")
    # 设置日志级别，将字符串转换为对应的日志级别常数
    level_numeric = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level_numeric)

    # 检查日志文件存放目录是否存在，若不存在则创建
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    # 获取当前日期
    today = datetime.date.today()
    date_str = today.strftime('%Y-%m-%d')  # 格式化日期为 YYYY-MM-DD

    # 日志文件路径
    log_dir = get_main_path() + '/logs'
    log_file = os.path.join(log_dir, f'{date_str}_test.log')

    # 创建一个文件处理器，并设置日志格式
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(CustomFormatter())

    # 创建一个控制台处理器，并设置日志格式
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomFormatter())

    # 清除现有的处理器，以防重复添加
    logger.handlers.clear()
    # 添加文件和控制台处理器到日志器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


# 初始化和配置日志器
logger = setup_logger('INFO')  # 设置初始日志级别为INFO
# logger = setup_logger('DEBUG')  # 设置初始日志级别为DEBUG

# 测试日志记录，输出目录在logger/log目录下
logger.info("This is an informational message with fixed prefix")
# logger.debug("This is a debug message with file and line number details")
