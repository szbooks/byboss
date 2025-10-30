import datetime

from app.db import get_db_connection
from datetime import datetime


# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取优惠申请列表
def get_discounts():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                
select a.*,c.end_data,c.room_count from (
SELECT
	discount.*, t_account.username AS todo_user_name
FROM
	(
		SELECT
			t_discount.*, t_account.username AS create_user_name
		FROM
			t_discount
		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
	) AS discount
LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id
ORDER BY
	a.create_datetime DESC;
            '''
            cursor.execute(sql)
            discounts = cursor.fetchall()

#待处理
            status1_sql='''
                select count(*)总数 from (
SELECT	discount.*, t_account.username AS todo_user_name FROM
(SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
	) AS discount
LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=1
ORDER BY a.create_datetime DESC;
            '''

            cursor.execute(status1_sql)
            status1_count = cursor.fetchone()['总数']

# 已沟通
            status2_sql = '''
                            select count(*)总数 from (
            SELECT	discount.*, t_account.username AS todo_user_name FROM
            (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
            		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
            	) AS discount
            LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=2
            ORDER BY a.create_datetime DESC;
                        '''

            cursor.execute(status2_sql)
            status2_count = cursor.fetchone()['总数']
#4已提交books
            status4_sql = '''
                                        select count(*)总数 from (
                        SELECT	discount.*, t_account.username AS todo_user_name FROM
                        (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
                        		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
                        	) AS discount
                        LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=4
                        ORDER BY a.create_datetime DESC;
                                    '''

            cursor.execute(status4_sql)
            status4_count = cursor.fetchone()['总数']

# 5二次沟通
            status5_sql = '''
                                                    select count(*)总数 from (
                                    SELECT	discount.*, t_account.username AS todo_user_name FROM
                                    (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
                                    		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
                                    	) AS discount
                                    LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=5
                                    ORDER BY a.create_datetime DESC;
                                                '''

            cursor.execute(status5_sql)
            status5_count = cursor.fetchone()['总数']

            # 7继续跟踪
            status7_sql = '''
                                                                select count(*)总数 from (
                                                SELECT	discount.*, t_account.username AS todo_user_name FROM
                                                (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
                                                		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
                                                	) AS discount
                                                LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=7
                                                ORDER BY a.create_datetime DESC;
                                                            '''

            cursor.execute(status7_sql)
            status7_count = cursor.fetchone()['总数']

            return discounts,status1_count,status2_count,status4_count,status5_count,status7_count
    except Exception as e:
        print(f"Error get_discounts: {e}")
    finally:
        conn.close()




def get_discounts_search(status=None, company_id=None,contact=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql_conditions = ["1=1"]

            if company_id not in (None, ''):
                sql_conditions.append("a.company_id = %s")

            if status not in (None, ''):
                sql_conditions.append("a.status = %s")

            if contact not in (None, ''):
                sql_conditions.append("a.phone = %s")

            sql = '''
               select a.*,c.end_data,c.room_count from (
SELECT
	discount.*, t_account.username AS todo_user_name
FROM
	(
		SELECT
			t_discount.*, t_account.username AS create_user_name
		FROM
			t_discount
		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
	) AS discount
LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id
                 WHERE ''' + " AND ".join(sql_conditions) + " ORDER BY a.create_datetime desc"

            if company_id not in (None, '') or status not in (None, '') or contact not in (None, ''):
                query_params = tuple(param for param in [company_id, status,contact] if param is not None and param != '')
            print(sql)

            cursor.execute(sql, query_params)
            discounts = cursor.fetchall()

            # 待处理
            status1_sql = '''
                            select count(*)总数 from (
            SELECT	discount.*, t_account.username AS todo_user_name FROM
            (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
            		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
            	) AS discount
            LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=1 and
            ''' + " AND ".join(sql_conditions) + " ORDER BY a.create_datetime desc"


            cursor.execute(status1_sql,query_params)
            status1_count = cursor.fetchone()['总数']

            # 已沟通
            status2_sql = '''
                                        select count(*)总数 from (
                        SELECT	discount.*, t_account.username AS todo_user_name FROM
                        (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
                        		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
                        	) AS discount
                        LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=2 and
                        ''' + " AND ".join(sql_conditions) + " ORDER BY a.create_datetime desc"


            cursor.execute(status2_sql,query_params)
            status2_count = cursor.fetchone()['总数']
            # 4已提交books
            status4_sql = '''
                                                    select count(*)总数 from (
                                    SELECT	discount.*, t_account.username AS todo_user_name FROM
                                    (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
                                    		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
                                    	) AS discount
                                    LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=4 and
                                    ''' + " AND ".join(sql_conditions) + " ORDER BY a.create_datetime desc"

            cursor.execute(status4_sql,query_params)
            status4_count = cursor.fetchone()['总数']

            # 5二次沟通
            status5_sql = '''
                                                                select count(*)总数 from (
                                                SELECT	discount.*, t_account.username AS todo_user_name FROM
                                                (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
                                                		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
                                                	) AS discount
                                                LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=5 and
                                                ''' + " AND ".join(sql_conditions) + " ORDER BY a.create_datetime desc"

            cursor.execute(status5_sql,query_params)
            status5_count = cursor.fetchone()['总数']

            # 7继续跟踪
            status7_sql = '''
                                                                         select count(*)总数 from (
                                                         SELECT	discount.*, t_account.username AS todo_user_name FROM
                                                         (SELECT	t_discount.*, t_account.username AS create_user_name FROM	t_discount
                                                         		LEFT JOIN t_account ON t_account.id = t_discount.create_userid
                                                         	) AS discount
                                                         LEFT JOIN t_account ON t_account.id = discount.todo_userid)a LEFT JOIN t_company c on a.company_id=c.company_id where a.status=7 and
                                                         ''' + " AND ".join(sql_conditions) + " ORDER BY a.create_datetime desc"

            cursor.execute(status7_sql, query_params)
            status7_count = cursor.fetchone()['总数']

            return discounts,status1_count,status2_count,status4_count,status5_count,status7_count
    except Exception as e:
        print(f"Error get_discounts_search: {e}")
    finally:
        conn.close()


# 读取发票详情
def get_discount(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_discount
                WHERE id = %s
            '''
            cursor.execute(sql, id)
            discount = cursor.fetchone()
            return discount
    except Exception as e:
        print(f"Error get_receipt: {e}")
    finally:
        conn.close()


# 更新状态
def update_discount_status(id, status, details, todo_userid, final_plan, todo_remark, company_id,phone):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    sql = ""
    try:
        with conn.cursor() as cursor:
            if (status == 3 or status == 9):
                sql = '''
                    UPDATE t_discount
                    SET status = %s, todo_userid = %s, todo_datetime = %s, final_plan=%s,company_id=%s,phone=%s
                    WHERE id = %s
                '''
                cursor.execute(sql, (status, todo_userid, formatted_time, final_plan, company_id, phone,id))
                conn.commit()
            elif (status == 8):
                sql = '''
                    UPDATE t_discount
                    SET todo_userid = %s, todo_datetime = %s, final_plan=%s,company_id=%s,phone=%s
                    WHERE id = %s
                                '''
                cursor.execute(sql, (todo_userid, formatted_time, final_plan, company_id,phone, id))
                conn.commit()
            elif (status == 10):
                sql = '''
                               UPDATE t_discount
                               SET todo_userid = %s, todo_datetime = %s, details=%s,company_id=%s,phone=%s
                               WHERE id = %s
                                           '''
                cursor.execute(sql, (todo_userid, formatted_time, details, company_id, phone, id))
                conn.commit()
            else:
                sql = '''
                    UPDATE t_discount
                    SET status = %s, details = %s, todo_userid = %s, todo_datetime = %s,final_plan=%s,company_id=%s,phone=%s
                    WHERE id = %s
                                '''
                cursor.execute(sql, (status, details, todo_userid, formatted_time, final_plan, company_id,phone, id))
                conn.commit()
    except Exception as e:
        print(f"Error update_discount_status: {e}")
    finally:
        conn.close()

# 编辑发票
def edit_discount_data(id, remark, company_id,phone):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    sql = ""

    try:
        with conn.cursor() as cursor:
            sql = '''
                UPDATE t_discount
                SET remark=%s, company_id=%s ,phone=%s
                WHERE id = %s
            '''
            cursor.execute(sql, (remark, company_id,phone,id))
            conn.commit()


    except Exception as e:
        print(f"Error in edit_discount_data: {e}")

    finally:
        conn.close()


# 申请新发票
def add_new_discount(company_id, remark,phone,create_account_id, todo_account_id):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO `dh_support`.`t_discount` (`company_id`, `status`, `details`, `create_userid`, `create_datetime`, `todo_userid`, `todo_datetime`, `remark`, `final_plan`,phone) 
VALUES (%s, %s, NULL, %s, %s, %s, NULL,  %s, NULL,%s);
            '''
            if create_account_id == 3:
                status = 2
            else:
                status = 1
            # current_time = datetime.datetime.now()
            cursor.execute(sql, (company_id, status, create_account_id, formatted_time, todo_account_id, remark,phone))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_new_receipt: {e}")
    finally:
        conn.close()

#删除优惠
def del_discount_record(discount_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 DELETE from t_discount where id=%s
             '''
            cursor.execute(sql, (discount_id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()

#移动优惠到调整
def move_discount_record(discount_id):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    try:
        with conn.cursor() as cursor:
            discount_sql = '''
                 select company_id,create_userid,remark,todo_userid,details,phone from t_discount where id=%s;
             '''

            insert_special='''INSERT INTO t_special_apply (`company_id`, `content`, `status`, `type`, `create_account_id`,todo_account_id,create_datetime,todo_remark,phone) VALUES (%s,%s, '1', 'f',%s,%s,%s,%s,%s);'''
            cursor.execute(discount_sql, (discount_id,))
            move_discount = cursor.fetchone()
            if move_discount:
                cursor.execute(insert_special, (move_discount['company_id'],move_discount['remark'],move_discount['create_userid'],move_discount['todo_userid'],formatted_time,move_discount['details'],move_discount['phone']))
                conn.commit()
            del_discount_record(discount_id)
            # return "success"
    except Exception as e:
        print(f"Error in move_discount_record: {e}")
    finally:
        conn.close()


#继续跟踪
def tracking_discount_record(discount_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 UPDATE t_discount
                SET status=7
                WHERE id = %s
             '''
            cursor.execute(sql, (discount_id,))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()

#选择状态
def update_select_discount_state(id,newStatus):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                  UPDATE t_discount set status=%s where id=%s
             '''
            cursor.execute(sql, (newStatus,id))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in company_receipts_filter: {e}")
    finally:
        conn.close()

