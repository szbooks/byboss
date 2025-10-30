import datetime

from app.db import get_db_connection
from datetime import datetime

# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取数据转移申请列表
def get_account_deletion():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT apply.*,t_account.username as todo_user_name FROM 
                (
                SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                ) AS apply 
                LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="e"
                ORDER BY apply.create_datetime desc
            '''
            cursor.execute(sql)
            specials = cursor.fetchall()
            print(specials)
            return specials

    except Exception as e:
        print(f"Error get_discounts: {e}")
    finally:
        conn.close()


# 读取优惠申请列表
# def get_discount_by_status(status):
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             sql = '''
#                 SELECT discount.*,t_account.username as todo_user_name FROM
#                 (
#                 SELECT t_discount.*,t_account.username as create_user_name FROM t_discount
#                 LEFT JOIN t_account ON t_account.id = t_discount.create_userid
#                 ) AS discount
#                 LEFT JOIN t_account ON t_account.id = discount.todo_userid
#                 WHERE discount.status = %s
#                 ORDER BY discount.create_datetime desc
#             '''
#             cursor.execute(sql, status)
#             discounts = cursor.fetchall()
#             return discounts
#     except Exception as e:
#         print(f"Error get_discount_by_status: {e}")
#     finally:
#         conn.close()



def get_account_deletion_search(status=None,company_id=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_conditions = ["1=1"]

            if company_id not in (None, ''):
                sql_conditions.append("apply.company_id = %s")

            if status not in (None, ''):
                sql_conditions.append("apply.status = %s")

            sql = '''
                           SELECT apply.*,t_account.username as todo_user_name FROM 
                            (
                            SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                            LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                            ) AS apply 
                            LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="e" and
                             ''' + " AND ".join(sql_conditions) + " ORDER BY apply.create_datetime desc"


            if company_id not in (None, '') or status not in (None, '') :
                query_params = tuple(
                    param for param in [company_id, status]
                    if param is not None and param != '')
            print(sql)
            # cursor.execute(sql,status)
            # receipts = cursor.fetchall()
            cursor.execute(sql, query_params)
            discounts = cursor.fetchall()
            return discounts
    except Exception as e:
        print(f"Error get_discounts_search: {e}")
    finally:
        conn.close()


# 读取数据转移详情
def get_account_deletion_id(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_special_apply
                WHERE id = %s and type = "e"
            '''
            cursor.execute(sql, id)
            account_deletion = cursor.fetchone()
            return account_deletion
    except Exception as e:
        print(f"Error get_receipt: {e}")
    finally:
        conn.close()


# 更新数据转移

def update_account_deletion_status(id, status, todo_account_id, final_plan,todo_remark,company_id,phone):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    sql=""
    try:
        with conn.cursor() as cursor:
            if status == 2 or status == 3:
                sql = '''
                    UPDATE t_special_apply
                    SET status = %s, todo_remark = %s, todo_account_id = %s, todo_datetime = %s, final_plan = %s, company_id = %s, phone = %s
                    WHERE id = %s
                '''
                cursor.execute(sql, (status, todo_remark, todo_account_id, formatted_time, final_plan, company_id, phone, id))
                conn.commit()
            elif status == 8:
                sql = '''
                    UPDATE t_special_apply
                    SET todo_remark = %s, final_plan = %s, company_id = %s, phone = %s
                    WHERE id = %s
                '''
                cursor.execute(sql, (todo_remark, final_plan, company_id, phone, id))
                conn.commit()
            elif status == 4:
                sql = '''
                    UPDATE t_special_apply  SET todo_remark = %s  WHERE id = %s
                '''
                cursor.execute(sql, (todo_remark, id))  # 注意这里只传递两个参数
                conn.commit()


    except Exception as e:
        print(f"Error update_account_deletion_status: {e}")
    finally:
        conn.close()


# 申请新发票
def add_new_account_deletion(company_id, phone,content, create_account_id, todo_account_id,type):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO `dh_support`.`t_special_apply` (`company_id`, `phone`, `content`, `status`, `create_account_id`, `create_datetime`, `todo_account_id`,type) 
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s);
            '''
            if create_account_id==3:
                status = 2
            else:
                status = 1
            # current_time = datetime.datetime.now()
            cursor.execute(sql, (company_id, phone,content,status, create_account_id, formatted_time, todo_account_id,type))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_new_account_deletion: {e}")
    finally:
        conn.close()

#删除账号
def del_account_record(account_deletion_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 DELETE from t_special_apply where id=%s and type="e"
             '''
            cursor.execute(sql, (account_deletion_id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()


#编辑转移
def edit_account_data(id, phone, content, company_id):
    conn = get_db_connection()
    current_time = datetime.now()
    sql = ""

    try:
        with conn.cursor() as cursor:
            sql = '''
                UPDATE t_special_apply
                SET phone=%s, company_id=%s, content=%s
                WHERE id = %s and type="e"
            '''
            cursor.execute(sql, (phone, company_id, content,id))
            conn.commit()


    except Exception as e:
        print(f"Error in edit_discount_data: {e}")

    finally:
        conn.close()