import time

from utils.db_connection import MySQLConnector


def sms_verification(elements):

    if len(elements) >= 6:
        time.sleep(5)
        print(f"{len(elements)} == 6位，进行输入验证码操作")
        # 获取数据库中的验证码
        code = None
        with MySQLConnector() as db_connector:
            # 执行查询
            results = db_connector.query(
                "SELECT code FROM system_verification_codes ORDER BY code_id DESC LIMIT 1")
            # 处理查询结果
            if results:
                code = results[0].get('code')
                if code:
                    print(f"code: {code}")
                else:
                    print("没有可用的验证码")
            else:
                print("没有结果")
        # 确保 code 有效且长度为 6
        if code and len(code) == 6:
            # 将验证码逐位输入到元素中
            for i, element in enumerate(elements[:6]):
                element.send_keys(code[i])
        else:
            print("无效的验证码或长度不足 6 位")


# def verification(elements):
#
#     if len(elements) >= 6:
#         time.sleep(5)
#         print(f"{len(elements)} == 6位，进行输入验证码操作")
#         # 获取数据库中的验证码
#         code = None
#         with MySQLConnector() as db_connector:
#             # 执行查询
#             results = db_connector.query(
#                 "SELECT code FROM system_verification_codes ORDER BY code_id DESC LIMIT 1")
#             # 处理查询结果
#             if results:
#                 code = results[0].get('code')
#                 if code:
#                     print(f"code: {code}")
#                 else:
#                     print("没有可用的验证码")
#             else:
#                 print("没有结果")
#         # 确保 code 有效且长度为 6
#         if code and len(code) == 6:
#             # 将验证码逐位输入到元素中
#             for i, element in enumerate(elements[:6]):
#                 element.send_keys(code[i])
#         else:
#             print("无效的验证码或长度不足 6 位")