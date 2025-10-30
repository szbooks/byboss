import datetime

from app.db import get_db_connection
from datetime import datetime

# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取数据转移申请列表
def get_special_apply():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT apply.*,t_account.username as todo_user_name FROM 
                (
                SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                ) AS apply 
                LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f"
                ORDER BY apply.create_datetime desc
            '''
            cursor.execute(sql)
            specials = cursor.fetchall()

            count_sql='''
                SELECT count(*)总数 FROM 
                (
                SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                ) AS apply 
                LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f"
                ORDER BY apply.create_datetime desc
            '''
            cursor.execute(count_sql)
            total_count = cursor.fetchone()['总数']

            status1_count_sql = '''
                            SELECT count(*)总数 FROM 
                (
                SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                ) AS apply 
                LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f" and apply.`status`=1
                ORDER BY apply.create_datetime desc
                        '''
            cursor.execute(status1_count_sql)
            status1_count = cursor.fetchone()['总数']

            status2_count_sql = '''
                                       SELECT count(*)总数 FROM 
                           (
                           SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                           LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                           ) AS apply 
                           LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f" and apply.`status`=2
                           ORDER BY apply.create_datetime desc
                                   '''
            cursor.execute(status2_count_sql)
            status2_count = cursor.fetchone()['总数']

            status3_count_sql = '''
                                                   SELECT count(*)总数 FROM 
                                       (
                                       SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                                       LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                                       ) AS apply 
                                       LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f" and apply.`status`=3
                                       ORDER BY apply.create_datetime desc
                                               '''
            cursor.execute(status3_count_sql)
            status3_count = cursor.fetchone()['总数']

            return specials,total_count,status1_count,status2_count,status3_count
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



def get_special_apply_search(status=None,company_id=None):
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
                LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f" and
                 '''+ " AND ".join(sql_conditions)+" ORDER BY apply.create_datetime desc"


            if company_id not in (None, '') or status not in (None, '') :
                query_params = tuple(
                    param for param in [company_id, status]
                    if param is not None and param != '')
            print(sql)
            # cursor.execute(sql,status)
            # receipts = cursor.fetchall()
            cursor.execute(sql, query_params)
            specials = cursor.fetchall()

            count_sql = '''
                            SELECT count(*)总数 FROM 
                            (
                            SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                            LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                            ) AS apply 
                            LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f" and
                 '''+ " AND ".join(sql_conditions)+" ORDER BY apply.create_datetime desc"


            cursor.execute(count_sql,query_params)
            total_count = cursor.fetchone()['总数']

            status1_count_sql = '''
                                        SELECT count(*)总数 FROM 
                            (
                            SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                            LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                            ) AS apply 
                            LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f" and apply.`status`=1 and
                 '''+ " AND ".join(sql_conditions)+" ORDER BY apply.create_datetime desc"

            cursor.execute(status1_count_sql,query_params)
            status1_count = cursor.fetchone()['总数']

            status2_count_sql = '''
                                                   SELECT count(*)总数 FROM 
                                       (
                                       SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                                       LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                                       ) AS apply 
                                       LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f" and apply.`status`=2 and
                 '''+ " AND ".join(sql_conditions)+" ORDER BY apply.create_datetime desc"

            cursor.execute(status2_count_sql,query_params)
            status2_count = cursor.fetchone()['总数']

            status3_count_sql = '''
                                                               SELECT count(*)总数 FROM 
                                                   (
                                                   SELECT t_special_apply.*,t_account.username as create_user_name FROM t_special_apply 
                                                   LEFT JOIN t_account ON t_account.id = t_special_apply.create_account_id
                                                   ) AS apply 
                                                   LEFT JOIN t_account ON t_account.id = apply.todo_account_id where apply.type="f" and apply.`status`=3 and
                 '''+ " AND ".join(sql_conditions)+" ORDER BY apply.create_datetime desc"

            cursor.execute(status3_count_sql,query_params)
            status3_count = cursor.fetchone()['总数']









            return specials,total_count,status1_count,status2_count,status3_count
    except Exception as e:
        print(f"Error get_discounts_search: {e}")
    finally:
        conn.close()


# 读取数据转移详情
def get_special(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_special_apply
                WHERE id = %s and type = "f"
            '''
            cursor.execute(sql, id)
            discount = cursor.fetchone()
            return discount
    except Exception as e:
        print(f"Error get_receipt: {e}")
    finally:
        conn.close()


# 更新数据转移

def update_special_status(id, status, todo_account_id, final_plan,todo_remark,company_id,phone):
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
        print(f"Error update_special_status {e}")
    finally:
        conn.close()


# 申请新转移
def add_new_transfer(company_id, phone,content, create_account_id, todo_account_id,type):
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
        print(f"Error add_new_transfer {e}")
    finally:
        conn.close()

#编辑转移
def edit_transfer_data(id, phone, content, company_id):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    sql = ""

    try:
        with conn.cursor() as cursor:
            sql = '''
                UPDATE t_special_apply
                SET phone=%s, company_id=%s, content=%s
                WHERE id = %s
            '''
            cursor.execute(sql, (phone, company_id, content,id))
            conn.commit()


    except Exception as e:
        print(f"Error in edit_discount_data: {e}")

    finally:
        conn.close()



#删除转移
def del_special_record(special_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 DELETE from t_special_apply where id=%s
             '''
            cursor.execute(sql, (special_id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()


#移动优惠到调整
def move_special_record(special_id):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    try:
        with conn.cursor() as cursor:
            special_sql = '''
                 select company_id,content,status,type,create_account_id,todo_account_id,todo_remark,phone from t_special_apply where id=%s;
             '''

            insert_discount='''INSERT INTO t_discount (company_id,status,create_userid,todo_userid,remark,create_datetime,details,phone) VALUES (%s,'1',%s,%s,%s,%s,%s,%s);'''
            cursor.execute(special_sql, (special_id,))
            move_special = cursor.fetchone()
            if move_special:
                cursor.execute(insert_discount, (move_special['company_id'],move_special['create_account_id'],move_special['todo_account_id'],move_special['content'],formatted_time,move_special['todo_remark'],move_special['phone']))
                conn.commit()
            del_special_record(special_id)
    except Exception as e:
        print(f"Error in move_special_record: {e}")
    finally:
        conn.close()
