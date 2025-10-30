import datetime
from contextlib import closing

from app.db import get_db_connection, get_db_connection_read
from datetime import datetime

# current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
# formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
# formatted_data = current_time.strftime("%Y-%m-%d")


# 读取数据转移申请列表
def get_coop_ex(partner=None,code=None,open=None,status_filter=None):
    conn = get_db_connection()
    connread = get_db_connection_read()
    params_partner=""
    params_code = ""
    try:
        with conn.cursor() as cursor:
            sql_conditions = ["1=1"]

            if partner not in (None, ''):
                params_partner = "%"+partner+"%"
                sql_conditions.append("name like %s")

            if code not in (None, ''):
                code="%"+code+"%"
                sql_conditions.append("code like %s")

            if open not in (None, ''):
                sql_conditions.append("isauthority = %s")

            if status_filter not in (None, ''):
                sql_conditions.append("isauthority = %s")

            sql = '''
                      select * from t_coop_ex where '''+" AND ".join(sql_conditions) + " ORDER BY id desc"

            if partner not in (None, '') or code not in (None, '') or open not in (None, '') or status_filter not in (None, ''):
                query_params = tuple(
                    param for param in [params_partner, code,open,status_filter]
                    if param is not None and param != '')
                print(sql)
                cursor.execute(sql, query_params)
                results = cursor.fetchall()
            else:
                cursor.execute(sql)
                results = cursor.fetchall()
            print(results)
            return results
    except Exception as e:
        print(f"Error get_coop_ex: {e}")
    finally:
        conn.close()
        connread.close()



def get_coop_updata():
    conn = get_db_connection()
    connread = get_db_connection_read()
    params_partner = ""
    params_code = ""
    try:
        with conn.cursor() as cursor:
            sql_conditions = ["1=1"]


            sql = '''
                          select * from t_coop_ex'''
            cursor.execute(sql)
            results = cursor.fetchall()


            for result in results:
                if result['code'] not in (None, ''):
                    with connread.cursor() as cursor:
                        sql = '''
                                             select count(*)num,group_concat(id)companys from company where from_code in (%s)'''
                        cursor.execute(sql, (result['code'],))
                        # cursor.execute(sql)
                        results_read = cursor.fetchone()
                        result.update(results_read)

                    with connread.cursor() as cursor:

                        sql = '''
                                                    select group_concat(DISTINCT user_id)bind_userid,sum(price_from)original_price,sum(price)promotion_fee,count(*)pay_num
                                                            ,(select group_concat(DISTINCT company_id) from payment_vip where company_id in (select id from company where from_code=%s) and company_id not in (SELECT c.id 
                                                            FROM company c 
                                                            LEFT JOIN spread_bonus sb ON c.id = sb.payment_vip_company_id 
                                                            LEFT JOIN spread_user su ON sb.user_id = su.user_id 
                                                            WHERE c.from_code IN  (%s)
                                                            AND sb.user_id IS not NULL))ungive,
                            																(select group_concat(DISTINCT id) from company where from_code=%s and id not in (select company_id from payment_vip where company_id in (select id from company where from_code=%s) GROUP BY company_id))unpay
                                                            from spread_bonus
                                                            where user_id in (select user_id from spread_user where self_code in (%s));
                                                    '''

                        cursor.execute(sql, (result['code'], result['code'], result['code'], result['code'], result['code']))
                        results_bonus = cursor.fetchone()
                        result.update(results_bonus)
                if result['add_company'] not in (None, ''):

                    with connread.cursor() as cursor:
                        add_company = result['add_company']
                        company_ids = add_company.split(',')
                        formatted_company_ids = [f'"{id}"' for id in company_ids]
                        company_ids_str = ', '.join(formatted_company_ids)
                        unpay_code_sql = f'''
                            SELECT company_id 
                            FROM payment_vip 
                            WHERE company_id IN ({company_ids_str})
                            GROUP BY company_id
                        '''
                        cursor.execute(unpay_code_sql)
                        unpay_code_result = cursor.fetchall()
                        print("已支付", len(unpay_code_result) )

                        final_dict = {}
                        add_company = result['add_company']
                        # 检查结果是否为 None 或空列表
                        if len(unpay_code_result) > 0:
                            for row in unpay_code_result:
                                exclude_id = str(row["company_id"])
                                values = add_company.split(',')
                                filtered_values = [value for value in values if value != exclude_id]
                                add_company = ','.join(filtered_values)
                            final_dict["add_company_unpay"] = add_company
                            result.update(final_dict)

            print(results)
            return results
    except Exception as e:
        print(f"Error get_coop_ex: {e}")
    finally:
        conn.close()
        connread.close()


# 读取数据
def get_coop_id(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_coop_ex
                WHERE id = %s
            '''
            cursor.execute(sql, id)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Error get_coop_id: {e}")
    finally:
        conn.close()


# 更新数据

def update_coop_ex(id, name, phone,wx_id,area, code,remark,discounts):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    sql=""
    try:
        # 使用 with 语句确保游标在使用完毕后被关闭
        with closing(conn.cursor()) as cursor:
            sql = '''
                    UPDATE t_coop_ex
                    SET name = %s, phone = %s,wx_id = %s, area = %s, code = %s, remark = %s,updata_date=%s ,discounts=%s WHERE id = %s
                '''

            # 在 with 语句块内执行 SQL
            cursor.execute(sql, (name, phone,wx_id, area, code, remark, formatted_time,discounts,id))

            # 提交事务
            conn.commit()

    except Exception as e:
        # 回滚事务以防数据不一致
        conn.rollback()
        print(f"Error update_coop_ex: {e}")

    finally:
        # 关闭数据库连接
        conn.close()


# 添加合作伙伴
def add_new_coop_ex(name, phone,wx_id,area, code,remark,discounts):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO `dh_support`.`t_coop_ex` (`name`, `phone`, `wx_id`,`area`, `code`, `remark`, `create_date`, `updata_date`,discounts) 
                VALUES (%s, %s, %s, %s, %s, %s, %s,%s,%s);
            '''

            cursor.execute(sql, (name, phone,wx_id,area,code, remark, formatted_time, formatted_time,discounts))
            conn.commit()
            # 获取插入记录的ID
            return cursor.lastrowid
    except Exception as e:
        print(f"Error add_new_account_deletion: {e}")
    finally:
        conn.close()


# 添加合作伙伴
def add_company_coop(id, add_company):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            if add_company not in (None, ''):
                sqlread= '''
                        select add_company,name from t_coop_ex where id=%s
                 '''
                cursor.execute(sqlread, (id))
                results_read = cursor.fetchone()

                if results_read is None:
                    # 如果没有找到记录，则提示或处理
                    print("No record found with the given ID.")
                else:
                    try:
                        old_add_company = results_read["add_company"]
                    except IndexError:
                        # 如果 results_read 是空的
                        print("Unexpected empty result.")

                    if old_add_company is None:
                        # 如果 add_company 字段为 NULL，则直接更新为新值
                        sql = '''
                                                         UPDATE `dh_support`.`t_coop_ex`  SET add_company =%s , `updata_date`=%s WHERE id =%s;
    
                                                    '''
                        cursor.execute(sql, (add_company, formatted_time, id))
                        conn.commit()
                    else:
                        # 如果 add_company 字段已有值，则追加新值
                        new_value = f"{old_add_company},{add_company}"
                        sql = '''
                                        UPDATE dh_support.t_coop_ex 
                                        SET add_company = %s,  updata_date = %s 
                                        WHERE id = %s
                                    '''
                        cursor.execute(sql, (new_value, formatted_time, id))
                        conn.commit()


    except Exception as e:
        print(f"Error add_new_account_deletion: {e}")
    finally:
        conn.close()

# 合作权限设置
def update_authority_db(id, status):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            sql = '''
                UPDATE `dh_support`.`t_coop_ex` SET `isauthority`=%s WHERE (`id`=%s)

            '''

            cursor.execute(sql, (status, id))
            conn.commit()
            return True

    except Exception as e:
        print(f"Error add_new_account_deletion: {e}")
    finally:
        conn.close()
