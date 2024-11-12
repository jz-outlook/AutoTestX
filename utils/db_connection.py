import pymysql
from utils.config import load_config

config_data = load_config('/Users/Wework/AutoTestX/config/config.ini', 'Mysql')
host = config_data.get('host')
user = config_data.get('user')
password = config_data.get('password')
database = config_data.get('database')

class MySQLConnector:
    def __init__(self, port=3306):
        """初始化MySQL数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,  # 请确保替换为您的密码
                database=database,
                port=port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
        except Exception as e:
            print(f"Error connecting to MySQL database: {e}")
            self.connection = None
            self.cursor = None

    def __enter__(self):
        """进入上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器，关闭数据库连接"""
        self.close()

    def query(self, sql, params=None):
        """执行SQL查询并返回所有结果"""
        if not self.cursor:
            print("Cursor not initialized. Cannot execute query.")
            return []

        try:
            self.cursor.execute(sql, params or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            return []

    def delete(self, sql):
        """执行SQL删除语句并返回结果信息"""

        if not self.cursor:
            print("Cursor not initialized. Cannot execute delete.")
            # 返回值表示没有成功执行
            return False, "Cursor not initialized."

        try:
            self.cursor.execute(sql)  # 直接使用sql参数，不使用额外的params
            # 获取这次操作影响的行数
            rows_affected = self.cursor.rowcount
            self.connection.commit()
            if rows_affected == 0:
                # 没有行被删除，可能是因为找不到匹配的数据
                return False, "No rows affected. Data might not exist."
            else:
                # 成功删除
                return True, f"{rows_affected} rows deleted."
        except Exception as e:
            print(f"Error executing delete: {e}")
            self.connection.rollback()
            # 返回值表示执行过程中遇到了异常
            return False, f"Error executing delete: {e}"

    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()


# 查询示例
# with MySQLConnector() as db_connector:
#     # 执行查询
#     results = db_connector.query("SELECT mobile FROM system_verification_codes ORDER BY code_id DESC LIMIT 1")
#     print(results)
