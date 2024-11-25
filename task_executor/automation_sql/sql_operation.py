import re

from utils.config import load_config
from utils.db_connection import MySQLConnector
from utils.get_path import GetPath


class SqlOperation:
    def contains_sql_operations(self, params):
        """检查给定查询中是否包含SQL操作关键字，并执行"""
        sql = params["element"]
        new_sql = self.replace_sql(sql)
        if params.get('by') == 'select':
            print('执行查询操作sql：{}'.format(new_sql))
            results = MySQLConnector().query(new_sql)
            print('sql查询结果：{}'.format(results))
        elif params.get('by') == 'delete':
            print('执行删除操作，sql：{}'.format(new_sql))
            results = MySQLConnector().delete(new_sql)
            print(results)
        else:
            print(f'执行sql异常，没有指定method方法为空或错误：{params["by"]}')

    def check_sql(self, sql):
        """查询sql中的 {{占位}}"""
        # 检查 URL 中是否包含 {{}}
        if re.search(r'{{.*?}}', sql):
            print(f"url需要进行前置操作，替换url: {sql}")
            new_sql = self.replace_sql(sql)
            print(f"替换之后的url: {sql}")
        else:
            return sql  # 如果没有发现 {{}}，则返回原始 URL
        return new_sql

    def replace_sql(self, sql):
        """替换URL中的 {{占位}}"""
        # 确定加载哪个配置
        config_section = 'api'
        platform_data = load_config(GetPath().get_project_root() + '/config/config.ini', config_section)
        # 使用正则表达式找到所有 {{}} 中的内容
        matches = re.findall(r'{{(.*?)}}', sql)
        # 替换所有匹配到的占位符
        for match in matches:
            placeholder = f'{{{{{match}}}}}'  # 将 {{}} 保留在替换格式中
            if match in platform_data:
                sql = sql.replace(placeholder, platform_data[match])
        return sql
