from utils.db_connection import MySQLConnector


class SqlOperation:
    def contains_sql_operations(self, params):
        """检查给定查询中是否包含SQL操作关键字，并执行"""
        sql = params["element"]
        new_sql = self.replace_sql(sql)
        if params.get('by') == 'select':
            print('执行查询操作sql：{}'.format(new_sql))
            results = MySQLConnector().query(new_sql)
            print('sql查询结果：{}'.format(results))
            # post_dependent(case, results)
        elif params.get('by') == 'delete':
            print('执行删除操作，sql：{}'.format(new_sql))
            MySQLConnector().delete(new_sql)
        else:
            print('执行sql异常，没有指定方法：method为空')

    def replace_sql(self, sql):
        """替换sql中的 {{占位}}"""
        return sql
