import datetime
from contextlib import closing

from app.db import get_db_connection, get_db_connection_read, get_db_connection_w
from datetime import datetime

from app.utils import md5_encrypt


# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 子商户
def get_sub_merchant_list(company_id=None,channel=None):
    # conn = get_db_connection_read()
    connread = get_db_connection_read()

    try:
        with connread.cursor() as cursor:
            conditions = ["remark='子商户' and platform<>'jlpay' and need_settle=0"]

            if company_id not in (None, ''):
                conditions.append("company_id = %s")

            if channel not in (None, '',"None"):
                conditions.append("platform = %s")

            sql = f'''
select company_id,sub_mch_name,sub_mch_id,pay_channel_agent,state,create_time,platform
from wx_pay_sub_mch 
WHERE {" AND ".join(conditions)}
ORDER BY company_id desc
'''

            sql_count = f'''select count(*)total_count from wx_pay_sub_mch 
WHERE {" AND ".join(conditions)} ORDER BY id desc'''

            if company_id not in (None, '') or channel not in (None, '', 'None'):
                query_params = tuple(param for param in [company_id, channel] if param not in (None, '', 'None')  # 排除 None、空字符串和字符串 'None'
                )
                print(sql)
                cursor.execute(sql, query_params)
                results = cursor.fetchall()
                cursor.execute(sql_count, query_params)
                total_count = cursor.fetchone()['total_count']
            else:
                cursor.execute(sql)
                results = cursor.fetchall()
                cursor.execute(sql_count)
                total_count = cursor.fetchone()['total_count']
            # print(sql)
            # cursor.execute(sql)
            # results = cursor.fetchall()
            return results,total_count
    except Exception as e:
        print(f"Error get_coop_ex: {e}")
    finally:
        connread.close()
