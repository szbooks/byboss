import datetime
import io

from flask import make_response, redirect, url_for, flash, current_app

from flask import current_app, jsonify
import requests as http_requests

from app.config import initial_order_url
from app.db import get_db_connection, get_db_connection_w, get_db_connection_read


# 读取客户运营人员列表
def get_account_id(company_id=None, channel=None):
    # 获取数据库连接
    conn_read = get_db_connection_read()
    try:
        with conn_read.cursor() as cursor:
            sql_conditions = []
            query_params = []

            # 优先判断 company_id 是否有效
            if company_id is not None and company_id.strip() != '':
                sql_conditions.append("company_id = %s")
                query_params.append(company_id)

                # 如果 company_id 有效，再判断 channel 是否有效
                if channel not in (None, ''):
                    sql_conditions.append("channel = %s")
                    query_params.append(channel)

            # 构建基础 SQL 查询
            sql = '''
                SELECT * FROM channel_account where state="S" and
            '''

            # 添加 WHERE 子句（如果有条件）
            if sql_conditions:
                sql += " AND ".join(sql_conditions)

            # 添加排序规则
            sql += " ORDER BY channel"

            # 执行查询
            cursor.execute(sql, query_params)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_account_id: {e}")
    finally:
        # 确保连接被正确关闭
        conn_read.close()


def get_initial_order_log():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 定义 SQL 查询
            sql = """
                
SELECT o.operation_time, o.operation_type, a.username, o.operation_desc, o.operation_id 
                FROM t_operation_log o 
                LEFT JOIN t_account a 
                ON o.user_id = a.id 
                WHERE o.operation_type = "initial_order:send" 
                ORDER BY o.id DESC;
            """
            # 执行 SQL 查询
            cursor.execute(sql)
            # 获取查询结果
            log_results = cursor.fetchall()
            return log_results
    except Exception as e:
        print(f"Error logging operation: {e}")
    finally:
        # 确保连接关闭
        conn.close()

# def initial_orde_do(id=None):
#     # 获取数据库连接
#     try:
#     # 拼接完整的请求地址
#         full_url = f"{initial_order_url}{id}"
#         print("full_url",full_url)
#         return redirect(full_url)
#
#     except Exception as e:
#         return f"发生错误: {str(e)}", 500

# 发送 GET 请求
# response = http_requests.get(full_url)
#
# # 检查响应状态码
# if response.status_code != 200:
#     return jsonify({'success': False, 'message': f'请求失败: {response.text}'}), response.status_code

# 解析响应数据
# data = response.json()
# conn_read = get_db_connection_read()
# try:
#     with conn_read.cursor() as cursor:
#         sql_conditions = []
#         query_params = []
#
#         # 优先判断 company_id 是否有效
#         if company_id is not None and company_id.strip() != '':
#             sql_conditions.append("company_id = %s")
#             query_params.append(company_id)
#
#         # 构建基础 SQL 查询
#         sql = '''
#             SELECT * FROM channel_account
#         '''
#
#         # 添加 WHERE 子句（如果有条件）
#         if sql_conditions:
#             sql += " WHERE " + " AND ".join(sql_conditions)
#
#         # 添加排序规则
#         sql += " ORDER BY channel"
#
#         # 执行查询
#         cursor.execute(sql, query_params)
#         results = cursor.fetchall()
#         return results
# except Exception as e:
#     print(f"Error get_account_id: {e}")
# finally:
#     # 确保连接被正确关闭
#     conn_read.close()
