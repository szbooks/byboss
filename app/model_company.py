import json

from flask import jsonify

from app.db import get_db_connection, get_db_connection_read
from datetime import datetime

current_time = datetime.now()
# 格式化为所需的字符串表示形式（年-月-日 时:分）
formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
formatted_data = current_time.strftime("%Y-%m-%d")


def get_companies_search(page, per_page, account_status=None, used_modules=None, expiry_month=None, company_id=None, category=None, start_value=0, end_value=999999999,api=None):
    # 计算起始记录
    start = (page - 1) * per_page

    # 创建数据库连接
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            # 构建 SQL 查询
            sql_conditions = ["1=1"]

            # 添加状态过滤条件
            if account_status not in (None, ''):
                sql_conditions.append("account_state = %s")

            # 添加功能使用过滤条件
            print(used_modules)
            if used_modules not in (None, ''):
                sql_conditions.append("used_modules LIKE %s")

            # 添加到期月份过滤条件
            if expiry_month not in (None, ''):
                sql_conditions.append("end_data = %s")

            if company_id not in (None, ''):
                sql_conditions.append("company_id = %s")

            if category not in (None, ''):
                sql_conditions.append("{} between %s and %s".format(category))

            # if self_code not in (None, ''):
            #     sql_conditions.append("{} between %s and %s".format(category))

            if start_value in (None, ''):
                start_value = 0

            if end_value in (None, ''):
                end_value = 999999999

            if api not in (None, ''):
                sql_conditions.append("api_config like %s")
                api = "%" + api + "%"


            # 构建最终的 SQL 查询
            # sql = "select c.*,api.channel from t_company c LEFT JOIN t_api_channel api on c.api_config=api.address  where " + " AND ".join(
            #     sql_conditions) + " LIMIT %s OFFSET %s"
            # print(sql)

            sql = "select * from t_company   where " + " AND ".join(sql_conditions) + " LIMIT %s OFFSET %s"
            print(sql)

            # 构建查询参数

            query_params = tuple(
                param for param in [account_status, used_modules, expiry_month, company_id,api]
                if param is not None and param != '')
            print(category, start_value, end_value)

            # 有查询条件用


            page_query_params = tuple(
                param for param in [account_status, used_modules, expiry_month, company_id, api,per_page, start]
                if param is not None and param != '')

            # 执行 SQL 查询
            cursor.execute(sql, page_query_params)

            # 获取查询结果
            items = cursor.fetchall()
            # utf8_item=""
            # for item in items:
            #     # 假设 item 是一个元组，其中包含可能出现 Unicode 字符的字符串
            #     utf8_item = item.encode('gbk', errors='ignore')
            #
            #     # 现在你可以处理 utf8_item，它应该是完全 UTF-8 编码的

            # 获取总记录数
            # total_count_sql = "SELECT COUNT(*) FROM t_company c LEFT JOIN t_api_channel api on c.api_config=api.address WHERE " + " AND ".join(sql_conditions)

            total_count_sql = "SELECT COUNT(*) FROM t_company  WHERE " + " AND ".join(sql_conditions)

            # 执行总记录数查询
            cursor.execute(total_count_sql, query_params)
            total_count = cursor.fetchone()['COUNT(*)']

            return items, total_count

    except Exception as e:
        print(f"Error get_companies_search: {e}")
    finally:
        conn.close()


# 获取账号列表
def get_companies(page, per_page):
    # 计算起始记录
    start = (page - 1) * per_page

    # 创建数据库连接
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            # 编写SQL查询，使用LIMIT进行分页
            # sql = """select * from t_company c LEFT JOIN (SELECT company_id, MAX(id)lastid,details FROM t_discount where status=3 GROUP BY company_id)a on c.company_id=a.company_id LIMIT %s OFFSET %s """
            sql="select c.*,api.channel from t_company c LEFT JOIN t_api_channel api on c.api_config=api.address LIMIT %s OFFSET %s;"
            cursor.execute(sql, (per_page, start))
            items = cursor.fetchall()

            # 获取总记录数
            sql = "SELECT COUNT(*) FROM t_company"
            cursor.execute(sql)
            total_count = cursor.fetchone()['COUNT(*)']

            return items, total_count
    except Exception as e:
        print(f"Error get_companies: {e}")
    finally:
        conn.close()


# 未付费的记录
def get_unpay_companies(page, per_page):
    # 计算起始记录
    start = (page - 1) * per_page

    # 创建数据库连接
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            # 编写SQL查询，使用LIMIT进行分页
            sql = "select * from (SELECT * FROM t_unpay_task LIMIT %s OFFSET %s)a LEFT JOIN t_company on a.company_id=t_company.company_id order by create_data desc"
            # sql = "SELECT * FROM t_unpay_task LEFT JOIN t_company on t_unpay_task.company_id=t_company.company_id  where t_company.pay_count=0 LIMIT %s OFFSET %s"
            cursor.execute(sql, (per_page, start))
            items = cursor.fetchall()

            # 获取总记录数
            sql = "select count(*)总数 from (SELECT * FROM t_unpay_task)a LEFT JOIN t_company on a.company_id=t_company.company_id order by create_data desc"
            # sql = "SELECT COUNT(*) FROM t_unpay_task LEFT JOIN t_company on t_unpay_task.company_id=t_company.company_id"
            cursor.execute(sql)
            total_count = cursor.fetchone()['总数']

            return items, total_count
    except Exception as e:
        print(f"Error get_unpay_companies: {e}")
    finally:
        conn.close()


def get_unpay_companies_search(page, per_page, company_id=None):
    # 计算起始记录
    start = (page - 1) * per_page

    # 创建数据库连接
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            # 构建 SQL 查询
            sql_caccount_status = ["1=1"]
            sql_conditions = ["1=1"]

            # 添加状态过滤条件

            if company_id not in (None, ''):
                sql_conditions.append("a.company_id = %s")

            # 构建最终的 SQL 查询

            sql = "select * from (SELECT * FROM t_unpay_task LIMIT %s OFFSET %s)a LEFT JOIN t_company on a.company_id=t_company.company_id where " + " AND ".join(
                sql_conditions) + " order by create_data desc"
            print(sql)

            # 有查询条件用
            if company_id not in (None, ''):
                query_params = tuple(
                    param for param in [per_page, start, company_id]
                    if param is not None and param != '')

            # 构建查询参数
            if company_id not in (None, ''):
                page_query_params = tuple(
                    param for param in [company_id] if param is not None and param != '')

            # 执行 SQL 查询
            cursor.execute(sql, query_params)

            # 获取查询结果
            items = cursor.fetchall()

            # 获取总记录数
            total_count_sql = "select count(*)总数 from (SELECT * FROM t_unpay_task)a LEFT JOIN t_company on a.company_id=t_company.company_id WHERE " + " AND ".join(sql_conditions)

            # 执行总记录数查询
            cursor.execute(total_count_sql, page_query_params)
            total_count = cursor.fetchone()['总数']

            return items, total_count

    except Exception as e:
        print(f"Error get_unpay_companies_search: {e}")
    finally:
        conn.close()


# 读取备注信息
def get_unpay_companies_remark(company_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 编写SQL查询

            sql = "select basic_info, period_target from t_unpay_task where company_id=%s"
            cursor.execute(sql, (company_id,))
            row = cursor.fetchone()
            if row:
                basic_info = row['basic_info']
                period_target = row['period_target']
                return basic_info, period_target
            else:
                # 没有匹配的结果
                return None, None
    except Exception as e:
        print(f"Error get_unpay_companies_remark: {e}")
    finally:
        conn.close()


# 更新备注相关
def update_unpay_companies_remark(company_id, basic_info=None, period_target=None, current_user_id=None, state=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:

            # 添加状态过滤条件
            if state not in (None, ''):
                sql = "update t_unpay_task set basic_info=%s,period_target=%s,state=%s,submit_time=%s,presales_id=%s where company_id=%s"
                cursor.execute(sql, (basic_info, period_target, state, formatted_time, current_user_id, company_id))
                conn.commit()
            else:
                sql = "update t_unpay_task set basic_info=%s,period_target=%s,submit_time=%s,presales_id=%s where company_id=%s"
                cursor.execute(sql, (basic_info, period_target, formatted_time, current_user_id, company_id))
                conn.commit()





    except Exception as e:
        print(f"Error update_unpay_companies_remark: {e}")
    finally:
        conn.close()


# 售前客服进度表
def get_followup_companies(page, per_page, current_user_id=None):
    # 计算起始记录
    start = (page - 1) * per_page

    # 创建数据库连接
    conn = get_db_connection()
    new_count = None

    try:
        with conn.cursor() as cursor:
            # 编写SQL查询，使用LIMIT进行分页
            # 全部数据

            get_scale_sql = "select persaler_list from t_account where id=%s"
            cursor.execute(get_scale_sql, (current_user_id,))
            scale_result = cursor.fetchone()

            persaler_list_value = scale_result['persaler_list'] if scale_result else None
            if persaler_list_value is None:
                persaler_list_value = "all"

            if persaler_list_value not in ("w", "s"):
                all_sql = (
                    # "select c.company_id,c.room_count,c.end_data,c.account_state,a.presales_id,a.customer_id,a.basic_info,a.period_target,a.progress_exec,a.progress_description,a.presales_remark,a.progress_data,c.used_modules,"
                    # "a.state,a.submit_time,(select username from t_account where id=a.presales_id)presaler,(select username from t_account where id=a.customer_id)customer,a.idx_data"
                    # 					" from t_unpay_task a LEFT JOIN t_company c on a.company_id=c.company_id  ORDER BY create_data desc LIMIT %s OFFSET %s"

                    "select c.*, a.presales_id, a.customer_id, a.basic_info, a.period_target, a.progress_exec, a.progress_description, a.presales_remark, a.progress_data,left(c.registration_date,10)company_creattime,"
                    "a.state, a.submit_time, (select username from t_account where id=a.presales_id) presaler, (select username from t_account where id=a.customer_id) customer, a.idx_data,left(a.create_data,10)create_data from t_unpay_task a "
                    "LEFT JOIN t_company c on a.company_id = c.company_id ORDER BY a.create_data desc LIMIT % s OFFSET % s"

                )

                print(all_sql)

                cursor.execute(all_sql, (per_page, start))
                items = cursor.fetchall()
            if persaler_list_value == "s":
                s_sql = (
                    "select c.*, a.presales_id, a.customer_id, a.basic_info, a.period_target, a.progress_exec, a.progress_description, a.presales_remark, a.progress_data,left(c.registration_date,10)company_creattime,"
                    "a.state, a.submit_time, (select username from t_account where id=a.presales_id) presaler, (select username from t_account where id=a.customer_id) customer, a.idx_data,left(a.create_data,10)create_data  from t_unpay_task a "
                    "LEFT JOIN t_company c on a.company_id = c.company_id where c.room_count >=30 ORDER BY a.create_data desc LIMIT %s OFFSET %s"
                )
                print(s_sql)
                cursor.execute(s_sql, (per_page, start))
                items = cursor.fetchall()
            if persaler_list_value == "w":
                w_sql = (
                    "select c.*, a.presales_id, a.customer_id, a.basic_info, a.period_target, a.progress_exec, a.progress_description, a.presales_remark, a.progress_data,left(c.registration_date,10)company_creattime,"
                    "a.state, a.submit_time, (select username from t_account where id=a.presales_id) presaler, (select username from t_account where id=a.customer_id) customer, a.idx_data,left(a.create_data,10)create_data  from t_unpay_task a "
                    "LEFT JOIN t_company c on a.company_id = c.company_id where c.room_count <30 and room_count >=10  ORDER BY a.create_data desc "
                    "LIMIT %s OFFSET %s"
                )

                print(w_sql)
                cursor.execute(w_sql, (per_page, start))
                items = cursor.fetchall()

            # 获取售前人员
            presaler_sql = "select id,realname,username from t_user_roles ur join t_account a on a.id=ur.user_id where role_id=3"
            cursor.execute(presaler_sql)
            presalers = cursor.fetchall()

            # 获取总记录数

            if persaler_list_value not in ("w", "s"):
                total_count_sql = "select count(*)总数 from (SELECT * FROM t_unpay_task )a LEFT JOIN t_company c on a.company_id=c.company_id "
                cursor.execute(total_count_sql)
                total_count = cursor.fetchone()['总数']

            if persaler_list_value == "s":
                s_total_count_sql = "select count(*)总数 from (SELECT * FROM t_unpay_task )a LEFT JOIN t_company c on a.company_id=c.company_id where c.room_count >=30"
                cursor.execute(s_total_count_sql)
                total_count = cursor.fetchone()['总数']
            if persaler_list_value == "w":
                w_total_count_sql = "select count(*)总数 from (SELECT * FROM t_unpay_task )a LEFT JOIN t_company c on a.company_id=c.company_id where c.room_count <30 and c.room_count >=10"
                cursor.execute(w_total_count_sql)
                total_count = cursor.fetchone()['总数']

            # 获取新增录数
            if persaler_list_value not in ("w", "s"):
                new_count_sql = "select count(*)总数 from (SELECT * FROM t_unpay_task where left(create_data,10)=%s)a LEFT JOIN t_company c on a.company_id=c.company_id"
                cursor.execute(new_count_sql, (formatted_data,))
                print("formatted_data:" + formatted_data)
                new_count = cursor.fetchone()['总数']

            if persaler_list_value == "s":
                s_total_count_sql = "select count(*)总数 from (SELECT * FROM t_unpay_task where left(create_data,10)=%s)a LEFT JOIN t_company c on a.company_id=c.company_id where c.room_count >=30"
                cursor.execute(s_total_count_sql, (formatted_data,))
                new_count = cursor.fetchone()['总数']
            if persaler_list_value == "w":
                w_total_count_sql = "select count(*)总数 from (SELECT * FROM t_unpay_task where left(create_data,10)=%s)a LEFT JOIN t_company c on a.company_id=c.company_id where c.room_count <30 and c.room_count >=10"
                cursor.execute(w_total_count_sql, (formatted_data,))
                new_count = cursor.fetchone()['总数']

            print("persaler_list_value:" + persaler_list_value)

            return items, total_count, new_count, presalers, persaler_list_value
    except Exception as e:
        print(f"Error get_followup_companies: {e}")
    finally:
        conn.close()


def get_followup_companies_search(page, per_page, company_id=None, account_status=None, presaler=None, btnradio=None, task_status=None, current_user_id=None):
    # 计算起始记录
    start = (page - 1) * per_page

    # 创建数据库连接
    conn = get_db_connection()

    try:
        with (conn.cursor() as cursor):
            # 构建 SQL 查询
            sql_caccount_status = ["1=1"]
            sql_conditions = ["1=1"]

            # 添加状态过滤条件

            if company_id not in (None, ''):
                sql_conditions.append("c.company_id = %s")

                # 添加状态过滤条件
            if account_status not in (None, ''):
                sql_conditions.append("c.account_state = %s")

            if presaler not in (None, ''):
                sql_conditions.append("a.presales_id = %s")

            if btnradio == "w":
                sql_conditions.append("c.room_count <30 and c.room_count >=10")

            if btnradio == "s":
                sql_conditions.append("c.room_count >=30")

            if task_status not in (None, ''):
                sql_conditions.append("a.state = %s")

            # get_scale_sql = "select persaler_list from t_account where id=%s"
            # cursor.execute(get_scale_sql, (current_user_id,))
            # scale_result = cursor.fetchone()
            #
            # persaler_list_value = scale_result['persaler_list'] if scale_result else None

            # 构建最终的 SQL 查询
            sql = (
                    "select c.company_id,c.room_count,c.end_data,c.account_state,a.presales_id,a.customer_id,a.basic_info,a.period_target,a.progress_exec,a.progress_description,a.presales_remark,a.progress_data,c.used_modules,"
                    "a.state,a.submit_time,(select username from t_account where id=a.presales_id)presaler,(select username from t_account where id=a.customer_id)customer,a.idx_data"
                    " from t_unpay_task a LEFT JOIN t_company c on a.company_id=c.company_id" + " WHERE " + " AND ".join(sql_conditions) + "  ORDER BY create_data" + " LIMIT %s OFFSET %s"
            )

            print(sql)

            # 有查询条件用
            if company_id not in (None, '') or account_status not in (None, '') or presaler not in (None, '') or task_status not in (None, ''):
                query_params = tuple(
                    param for param in [company_id, account_status, presaler, task_status, per_page, start]
                    if param is not None and param != '')
                # query_params = tuple(
                #     param for param in [company_id,per_page, start]
                #     if param is not None and param != '')

            # 构建查询参数
            if company_id not in (None, '') or account_status not in (None, '') or presaler not in (None, '') or task_status not in (None, ''):
                page_query_params = tuple(
                    param for param in [company_id, account_status, presaler, task_status] if param is not None and param != '')

            if company_id not in (None, '') or account_status not in (None, '') or presaler not in (None, '') or task_status not in (None, ''):
                new_query_params = tuple(
                    param for param in [formatted_data, company_id, account_status, presaler, task_status] if param is not None and param != '')

            # print("get_followup_companies_search: "+sql)

            # 执行 SQL 查询
            cursor.execute(sql, query_params)

            # 获取查询结果
            items = cursor.fetchall()

            # 获取总记录数
            total_count_sql = (
                    "select count(*)总数 from t_unpay_task a LEFT JOIN t_company c on a.company_id=c.company_id" + " WHERE " + " AND ".join(sql_conditions)
            )

            # 执行总记录数查询
            cursor.execute(total_count_sql, page_query_params)
            total_count = cursor.fetchone()['总数']

            new_count_sql = (
                    "select count(*)总数 from t_unpay_task a LEFT JOIN t_company c on a.company_id=c.company_id" + " WHERE " + " AND ".join(sql_conditions) + " and left(create_data,10)=%s "
            )

            # 执行总记录数查询
            print("查询新增数:" + new_count_sql)
            cursor.execute(new_count_sql, new_query_params)
            new_count = cursor.fetchone()['总数']

            return items, total_count, new_count

    except Exception as e:
        print(f"Error get_followup_companies_search: {e}")
    finally:
        conn.close()


# 读取售前目标完成情况
def get_followup_operdata(company_id):
    conn = get_db_connection()
    try:
        with (conn.cursor() as cursor):
            # 编写SQL查询
            sql = "select period_target,progress_exec,progress_description,presales_remark from t_unpay_task where company_id=%s"
            cursor.execute(sql, (company_id,))
            row = cursor.fetchone()
            if row:
                period_target = row['period_target']
                progress_exec = row['progress_exec']
                progress_description = row['progress_description']
                presales_remark = row['presales_remark']
                return period_target, progress_exec, progress_description, presales_remark
            else:
                # 没有匹配的结果
                return None, None
    except Exception as e:
        print(f"Error get_followup_operdata: {e}")
    finally:
        conn.close()


# 更新售前目标完成情况
def update_progress_exec_impl(company_id, progress_exec=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:

            print(f"formatted_time: {formatted_time}")
            sql = "update t_unpay_task set progress_exec=%s,progress_data=%s where company_id=%s"
            cursor.execute(sql, (progress_exec, formatted_time, company_id))
            conn.commit()

    except Exception as e:
        print(f"Error update_progress_exec_impl: {e}")
    finally:
        conn.close()


def update_progress_description_impl(company_id, progress_description=None, presales_remark=None):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:

            print(f"formatted_time: {formatted_time}")
            if progress_description is not None:
                sql = "update t_unpay_task set progress_description=%s where company_id=%s"
                cursor.execute(sql, (progress_description, company_id))
                conn.commit()
            if presales_remark is not None:
                sql = "update t_unpay_task set presales_remark=%s where company_id=%s"
                cursor.execute(sql, (presales_remark, company_id))
                conn.commit()

    except Exception as e:
        print(f"Error update_progress_description_impl: {e}")
    finally:
        conn.close()


def update_scale_impl(current_user_id=None, selectedValue=None):
    conn = get_db_connection()
    persaler_list = None
    if selectedValue == "btnradio2":
        persaler_list = "w"
    elif selectedValue == "btnradio3":
        persaler_list = "s"
    else:
        persaler_list = "all"

    try:
        with conn.cursor() as cursor:
            sql = "update t_account set persaler_list=%s where id=%s"
            cursor.execute(sql, (persaler_list, current_user_id))
            conn.commit()

    except Exception as e:
        print(f"Error update_scale_impl: {e}")
        return jsonify({"success": False, "message": str(e)})  # 返回错误信息
    finally:
        conn.close()


def update_customer_impl(current_user_id=None, company_id=None):
    # Check if company_id or current_user_id is None
    if company_id is None or current_user_id is None:
        print("Error: company_id or current_user_id cannot be None")
        return

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            sql = "update t_unpay_task set customer_id=%s,state=%s where company_id=%s"
            cursor.execute(sql, (current_user_id, "w", company_id))
            conn.commit()

    except Exception as e:
        print(f"Error update_customer_impl: {e}")
    finally:
        conn.close()


def get_bonus(userid=None, code=None):
    sql = ""
    # 计算起始记录

    # 创建数据库连接
    conn = get_db_connection_read()

    try:
        with conn.cursor() as cursor:
            if userid != "" and userid is not None and code == "" and code is not None:
                sql1 = """
                      select self_code from spread_user where user_id=%s;
                            """
                cursor.execute(sql1, (userid))
                code = cursor.fetchone()['self_code']

            sql = """
                                        select  u.company_id,spu.*,
                                            (select real_name from `user` where id=spu.user_id)user_name,
                                            (select price from payment_vip where company_id=u.company_id and step="E" and payment_type="D" ORDER BY id LIMIT 1)first_pay,
                                            (select CONCAT(price,"(",user_id,")") from spread_bonus where  payment_vip_company_id=u.company_id)bonus
                                             from spread_user spu join user u on spu.user_id=u.id where spu.self_code=%s or spu.from_code=%s
                                        """
            cursor.execute(sql, (code, code))
            results = cursor.fetchall()

            total_count_sql = """
                    select  count(*)总数 from spread_user spu join user u on spu.user_id=u.id where spu.self_code=%s or spu.from_code=%s;
            """

            # 执行总记录数查询
            cursor.execute(total_count_sql, (code, code))
            total_count = cursor.fetchone()['总数']

            return results, total_count
    except Exception as e:
        print(f"Error get_companies: {e}")
    finally:
        conn.close()


def get_contract(code=None):
    sql = ""
    # 计算起始记录

    # 创建数据库连接
    conn = get_db_connection_read()
    code = code
    baseresults = ""
    csxresults = ""

    try:
        with conn.cursor() as cursor:
            if code != "" and code is not None:
                if code.startswith('r_X') or code.startswith('d_X') or code.startswith('p_X'):
                    convertsql = """
                           select contract_id from csx_bank_pay_order where out_no=%s     
                    """
                    cursor.execute(convertsql, (code))
                    code = cursor.fetchone()['contract_id']
                elif code.startswith('42') and len(code) > 20:
                    ord_notsql = """
                          select contract_id from csx_bank_pay_order where ord_no=%s;       
                                        """
                    cursor.execute(ord_notsql, (code))
                    code = cursor.fetchone()['contract_id']

                sql1 = """
                         select a.id,a.company_id,a.create_time,a.channel,a.channel_order_id,a.info_realname,a.info_phone,a.unit_name,group_concat(a.room_no)room_no,a.Check_in,a.price
 from (
select c.id,c.company_id,c.create_time,c.channel,c.channel_order_id,c.info_realname,c.info_phone,
                        (select channel_unit_name from channel_unit where id=c.unit_id)unit_name,
                        (select group_concat(room_no) from room where id=prn.room_id)room_no,
                        c.price,concat(c.check_in,"至",c.check_out)Check_in
                         from contract c join product_room_night prn on c.id=prn.contract_id where c.id=%s)a GROUP BY a.id;
                            """
                cursor.execute(sql1, (code))
                baseresults = cursor.fetchall()

                # csxsql = """
                #         select out_no,ord_no,trade_amount,old_out_no,company_id,contract_id,night_id,state,(select trade_amount from csx_bank_pay_order where old_out_no=cpo.out_no)refund_amount
                #         from csx_bank_pay_order cpo where contract_id=%s and (out_no like "r_X%%" or out_no like "d_X%%" or out_no like "p_X%%")
                # """
                csxsql = """
                        select a.out_no,a.ord_no,(a.trade_amount/100)trade_amount,a.old_out_no,a.company_id,a.contract_id,a.night_id,a.state,if(a.refund_amount is null,"未退押或未退款",if(a.refund_amount=0,"全扣押",a.refund_amount/100))refund_amount,left(a.out_no,3)out_no_head from (
select out_no,ord_no,trade_amount,old_out_no,company_id,contract_id,night_id,state,(select trade_amount from csx_bank_pay_order where old_out_no=cpo.out_no)refund_amount
                        from csx_bank_pay_order cpo where contract_id=%s and state in ("1","8") and (out_no like "r_X%%" or out_no like "d_X%%" or out_no like "p_X%%"))a;

                """

                cursor.execute(csxsql, (code))
                csxresults = cursor.fetchall()

                total_count_sql = """
                         select count(*)总数  from contract c join product_room_night prn on c.id=prn.contract_id where c.id=%s
                """

                # 执行总记录数查询
                cursor.execute(total_count_sql, (code))
                total_count = cursor.fetchone()['总数']

            return baseresults, csxresults, total_count
    except Exception as e:
        print(f"Error get_companies: {e}")
    finally:
        conn.close()


def Batchget_contract(code=None):
    sql = ""
    # 计算起始记录

    # 创建数据库连接
    conn = get_db_connection_read()
    code = code
    baseresults = ""
    csxresults = ""
    finalcode = ""
    code_original = code.strip()
    code_split = code_original.split(',')

    try:
        with conn.cursor() as cursor:
            if code != "" and code is not None:
                for subcode in code_split:

                    if subcode.startswith('r_X') or subcode.startswith('d_X') or subcode.startswith('p_X'):
                        convertsql = """
                               select contract_id from csx_bank_pay_order where out_no=%s     
                        """
                        cursor.execute(convertsql, (subcode))
                        fist_code = cursor.fetchone()['contract_id']
                        finalcode = finalcode + str(fist_code) + ","
                    elif code.startswith('42') and len(code) > 20:
                        ord_notsql = """
                              select contract_id from csx_bank_pay_order where ord_no=%s;       
                                            """
                        results=cursor.execute(ord_notsql, (subcode))
                        if results:
                            second_code = cursor.fetchone()['contract_id']
                            finalcode = finalcode + str(second_code) + ","
                    else:
                        finalcode = finalcode + str(subcode) + ","

                finalcode = finalcode.rstrip(',')
                print("finalcode：" + finalcode)

                sql1 = '''
                 select a.id,a.company_id,a.create_time,a.channel,a.channel_order_id,a.info_realname,a.info_phone,a.unit_name,group_concat(a.room_no)room_no,a.Check_in,a.price 
                        from (select c.id,c.company_id,c.create_time,c.channel,c.channel_order_id,c.info_realname,c.info_phone,
                        (select channel_unit_name from channel_unit where id=c.unit_id)unit_name,
                        (select group_concat(room_no) from room where id=prn.room_id)room_no,c.price,CONCAT(c.check_in, "至", c.check_out) AS Check_in 
                         from contract c join product_room_night prn on c.id=prn.contract_id where c.id in (%s))a GROUP BY a.id
                '''
                cursor.execute(sql1, (finalcode))
                baseresults = cursor.fetchall()

                # csxsql = """
                #         select out_no,ord_no,trade_amount,old_out_no,company_id,contract_id,night_id,state,(select trade_amount from csx_bank_pay_order where old_out_no=cpo.out_no)refund_amount
                #         from csx_bank_pay_order cpo where contract_id=%s and (out_no like "r_X%%" or out_no like "d_X%%" or out_no like "p_X%%")
                # """
                csxsql = '''
                        select a.out_no,a.ord_no,(a.trade_amount/100)trade_amount,a.old_out_no,a.company_id,a.contract_id,a.night_id,a.state,if(a.refund_amount is null,"未退押或未退款",if(a.refund_amount=0,"全扣押",a.refund_amount/100))refund_amount,left(a.out_no,3)out_no_head from (
        select out_no,ord_no,trade_amount,old_out_no,company_id,contract_id,night_id,state,(select trade_amount from csx_bank_pay_order where old_out_no=cpo.out_no)refund_amount 
                        from csx_bank_pay_order cpo where contract_id in (%s) and state in ("1","8") and (out_no like "r_X%%" or out_no like "d_X%%" or out_no like "p_X%%"))a;
                '''

                cursor.execute(csxsql, (finalcode))
                csxresults = cursor.fetchall()

                total_count_sql = '''
                         select count(*)总数  from contract c join product_room_night prn on c.id=prn.contract_id where c.id in (%s)
                '''

                # 执行总记录数查询
                cursor.execute(total_count_sql, (finalcode))
                total_count = cursor.fetchone()['总数']

        return baseresults, csxresults, total_count
    except Exception as e:
        print(f"Error Batchget_contract: {e}")
    finally:
        conn.close()


def single_company_update(company_id):
    conn_read = get_db_connection_read()
    conn = get_db_connection()
    try:
        with conn_read.cursor() as cursor:
            sql = '''
                    select a.*,
CASE WHEN ISNULL(a.到期日)=1 then "5"
            WHEN a.到期日>=CURDATE() and a.付费次数=0 then "1"
WHEN (TO_DAYS(CURDATE())-TO_DAYS(a.到期日))>0 and (TO_DAYS(CURDATE())-TO_DAYS(a.到期日))<=7 then "3"
WHEN (TO_DAYS(CURDATE())-TO_DAYS(a.到期日))>7 then "4"
WHEN a.到期日="" then "6"
ELSE "2"
END as "账号状态"
from (
select id,company_name,city,
(select CONCAT(c1.from_code,"(",user.company_id,")") from spread_user u join company c1 on u.self_code=c1.from_code join user on u.user_id=user.id where c1.id=c.id)
from_code,create_time,
(select from_code from company where id not in (select company_id from company_config where mod_name = "LITE_FROM") and id=c.id)注册来源,
(select create_time from company_config where mod_name = "END_DATE" and company_id=c.id)激活时间,
(select mod_value from company_config where mod_name = "END_DATE" and company_id=c.id)到期日,
(select count(*) from room where company_id=c.id and state="S")房号数,
(select count(*) from (select count(*) from channel_account where state="S" and company_id=%s GROUP BY channel)a)平台数,
(select count(*) from payment_vip where company_id=c.id and step="E")付费次数
from company c where id=%s)a;
                                '''
            cursor.execute(sql, (company_id,company_id))
            company = cursor.fetchone()
        with conn.cursor() as cursor:
            sql = '''
                INSERT INTO `dh_support`.`t_company` (`company_id`, `company_name`, `city`,`from_code`, `account_state`,`source`, `active_time`, `end_data`, `room_count`, `platform_count`,`pay_count`,`create_time`)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ON DUPLICATE KEY UPDATE
                    company_name = VALUES(company_name),
                    city = VALUES(city),
                    from_code = VALUES(from_code),
                    account_state = VALUES(account_state),
                    source = VALUES(source),
                    active_time = VALUES(active_time),
                    end_data = VALUES(end_data),
                    room_count = VALUES(room_count),
                    platform_count = VALUES(platform_count),
                    pay_count = VALUES(pay_count),
                    create_time = VALUES(create_time);
            '''
            cursor.execute(sql, (company['id'], company['company_name'],company['city'],company['from_code'],company['账号状态'],company['注册来源'],company['激活时间'],company['到期日'],company['房号数'],company['平台数'],company['付费次数'],formatted_time))
            conn.commit()

    except Exception as e:
        print(f"Error single_company_update: {e}")
    finally:
        conn_read.close()
        conn.close()

    return




