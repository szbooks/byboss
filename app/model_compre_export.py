import datetime
import io

from flask import make_response, redirect, url_for, flash

from app.db import get_db_connection, get_db_connection_w, get_db_connection_read
from datetime import datetime
import urllib.parse  # 用于编码文件名
from base64 import b64encode

# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取数据转移申请列表
def get_compre_export():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 构建 SQL 查询
            sql_conditions = ["1=1"]

            # if company_id not in (None, ''):
            #     sql_conditions.append("id = %s")
            #
            # if code not in (None, ''):
            #     sql_conditions.append("from_code = %s")

            sql = '''
                    SELECT * FROM compre_export ORDER BY id desc;
                '''



            cursor.execute(sql)
            results= cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_compre_export: {e}")
    finally:
        conn.close()








def perio_export():
    try:
        # 获取当前时间
        current_time = datetime.now()
        formatted_data = current_time.strftime("%Y-%m-%d")

        # 获取数据库连接
        conn_read = get_db_connection_read()
        conn = get_db_connection()

        with conn.cursor() as cursor:
            # 查询 last_company
            sql = '''
                SELECT remark FROM compre_export WHERE id = 1
            '''
            cursor.execute(sql)
            last_company = cursor.fetchone()["remark"]

        with conn_read.cursor() as cursor:
            # 查询 companys
            result_sql = '''
                SELECT GROUP_CONCAT(CONCAT('P', id)) AS companys 
                FROM company 
                WHERE id NOT IN (SELECT company_id FROM company_config WHERE mod_name = "LITE_FROM") 
                AND id > %s;
            '''
            cursor.execute(result_sql, (last_company,))
            result = cursor.fetchone()

            if result and result["companys"]:
                # 获取所有公司 ID 字符串
                companys_str = result["companys"]

                # 更新 compre_export 表中的 last_company_id 和 last_data
                last_company_id = companys_str.split(',')[-1].lstrip('P')  # 获取最后一个公司 ID
                update_sql = '''
                    UPDATE compre_export SET remark = %s, last_data = %s WHERE id = 1
                '''
                with conn.cursor() as cursor:
                    cursor.execute(update_sql, (last_company_id, formatted_data))
                    conn.commit()

                # 创建一个 StringIO 对象来存储文本内容
                output = io.StringIO()
                output.write(companys_str)  # 写入所有公司 ID

                # 将 StringIO 对象转换为 bytes，使用 utf-8 编码
                output.seek(0)
                file_data = output.getvalue().encode('utf-8')

                # 创建响应对象
                response = make_response(file_data)

                # 设置 Content-Type 为 text/plain，确保浏览器以纯文本形式显示
                response.headers["Content-Type"] = "text/plain; charset=utf-8"

                return response
            else:
                flash('没有找到符合条件的公司', 'warning')
                return redirect(url_for('main.index'))

    except Exception as e:
        print(f"Error in perio_export: {e}")
        flash('导出失败，请稍后再试', 'danger')


    finally:
        # 确保关闭数据库连接
        if conn_read:
            conn_read.close()
        if conn:
            conn.close()
