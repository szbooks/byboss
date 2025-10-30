import datetime
import io

from flask import make_response, redirect, url_for, flash

from app.db import get_db_connection, get_db_connection_w, get_db_connection_read
from datetime import datetime

import urllib.parse  # 用于编码文件名
from base64 import b64encode

from app.utils import updata_operating_sub, updata_operating_sub_singer


# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取客户运营人员列表
def get_operating_sub(phone_code):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_conditions = []
            query_params = []

            # 动态构建查询条件
            if phone_code is not None and phone_code.strip() != '':
                sql_conditions.append("(phone LIKE %s OR name LIKE %s)")
                query_params.extend([f"%{phone_code}%", f"%{phone_code}%"])

            # 构建基础 SQL 查询
            sql = '''
                SELECT * FROM t_operating_sub
            '''

            # 添加 WHERE 子句（如果有条件）
            if sql_conditions:
                sql += " WHERE " + " AND ".join(sql_conditions)

            # 添加排序规则
            sql += " ORDER BY id DESC"

            # 执行查询
            cursor.execute(sql, query_params)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_operating_sub: {e}")
    finally:
        conn.close()


def add_operating_sub(phone, name):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    company_ids = []

    conn = None
    conn_read = None
    try:
        conn = get_db_connection()
        conn_read = get_db_connection_read()
        with conn.cursor() as cursor:
            operating_sub_search_sql='''
                        select * from t_operating_sub where phone=%s
            '''
            cursor.execute(operating_sub_search_sql, (phone,))
            search_result = cursor.fetchone()
            if search_result:
                result = 1
                return result

        with conn_read.cursor() as cursor_read:
            read_sql = '''
                SELECT company_id 
                FROM `user` 
                WHERE mobile = %s AND empl_type = 'E' 
                GROUP BY company_id;
            '''
            cursor_read.execute(read_sql, (phone,))
            results = cursor_read.fetchall()
            if results:
                for result in results:
                    company_id = result['company_id']  # 根据实际字段索引调整
                    company_ids.append(str(company_id))

                company_ids_str = ','.join(company_ids)
            else:
                company_ids_str =""
        with conn.cursor() as cursor_write:
            sql = '''
                INSERT INTO `dh_support`.`t_operating_sub` (`name`, `phone`, `company_id`, `create_date`) 
                VALUES (%s, %s, %s, %s);
            '''
            cursor_write.execute(sql, (name, phone, company_ids_str, formatted_time))
            conn.commit()
            return cursor_write.lastrowid
    except Exception as e:
        print(f"Error add_operating_sub: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn_read:
            conn_read.close()
        if conn:
            conn.close()

#获取记录
def get_operating_sub_id(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_operating_sub
                WHERE id = %s
            '''
            cursor.execute(sql, id)
            resultid = cursor.fetchone()

            return resultid
    except Exception as e:
        print(f"Error get_operating_sub: {e}")
    finally:
        conn.close()


def edit_operating_sub(phone, name,id):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    sql = ""

    try:
        with conn.cursor() as cursor:
            operating_sub_search_sql = '''
                               select * from t_operating_sub where phone=%s and id<>%s
                   '''
            cursor.execute(operating_sub_search_sql, (phone,id))
            search_result = cursor.fetchone()
            if search_result:
               return 1

            sql = '''
                UPDATE t_operating_sub
                SET phone=%s, name=%s
                WHERE id = %s
            '''
            cursor.execute(sql, (phone, name,id))
            conn.commit()
            updata_operating_sub_singer(phone)
            return 0

    except Exception as e:
        print(f"Error in edit_operating_sub: {e}")

    finally:
        conn.close()

#删除
def del_operating_sub(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 DELETE from t_operating_sub where id=%s
             '''
            cursor.execute(sql, (id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in del_operating_sub: {e}")
    finally:
        conn.close()
