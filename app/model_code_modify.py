import datetime

from app.db import get_db_connection, get_db_connection_w
from datetime import datetime
from base64 import b64encode

# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取数据转移申请列表
def get_code_modify_search(company_id,code):
    conn = get_db_connection_w()
    try:
        with conn.cursor() as cursor:
            # 构建 SQL 查询
            sql_conditions = ["1=1"]

            if company_id not in (None, ''):
                sql_conditions.append("id = %s")

            if code not in (None, ''):
                sql_conditions.append("from_code = %s")

            sql = '''
                select id,company_name,remark,offical_remark,from_code,create_time,
(select mod_value from company_config where  company_id=company.id and mod_name="END_DATE")end_date
 from company where '''+" AND ".join(sql_conditions)

            if company_id not in (None, '') or code not in (None, ''):
                query_params = tuple(
                    param for param in [company_id, code]
                    if param is not None and param != '')

            cursor.execute(sql,query_params)
            results= cursor.fetchall()
            return results
    except Exception as e:
        print(f"Error get_vip_refund: {e}")
    finally:
        conn.close()


def update_code(company_id=None,code=None):
    conn = get_db_connection_w();
    try:
        with conn.cursor() as cursor:

            if code not in (None, ''):
                sql = '''
                    UPDATE company  SET `from_code`=%s WHERE id=%s
                '''
                cursor.execute(sql, (code, company_id))
                conn.commit()
    except Exception as e:
        print(f"Error update_contact: {e}")
    finally:
        conn.close()
