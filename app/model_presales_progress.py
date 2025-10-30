import datetime
from contextlib import closing

from flask import jsonify

from app.db import get_db_connection, get_db_connection_read
from datetime import datetime

from app.model_company import single_company_update
from app.utils import get_username, is_integer, get_username_byrole
from datetime import datetime, timedelta


# 售前跟进列表
def get_presales_progress(company_id=None, account_status=None, operator=None, btnradio=None, task_status=None, current_user_id=None, date_select=None, persaler=None, search_api=None,
                          operating_sub=None, star=None, room_num=None, api_channel=None, coo_name=None, search_tag=None,companyType=None):
    # 计算起始记录
    page_query_params = ""
    new_query_params = ""
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    formatted_data = current_time.strftime("%Y-%m-%d")
    data_search = "";

    # 创建数据库连接
    conn = get_db_connection()

    try:
        with (conn.cursor() as cursor):

            get_scale_sql = "select persaler_list from t_account where id=%s"
            cursor.execute(get_scale_sql, (current_user_id,))
            scale_result = cursor.fetchone()
            persaler_list_value = scale_result['persaler_list'] if scale_result else None
            if persaler_list_value is None:
                persaler_list_value = "all"

                # 获取处理人员
            presaler_sql = "select a.username,a.realname,pp.operator_id from t_presales_progress pp join t_account a on pp.operator_id=a.id GROUP BY pp.operator_id"
            cursor.execute(presaler_sql)
            operator_name = cursor.fetchall()

            # 获取售前人员
            persaler_names = get_username_byrole(4)

            # 所属运营群

            # 构建 SQL 查询
            sql_caccount_status = ["1=1"]
            sql_conditions_query = ["1=1"]
            sql_conditions = ["1=1"]

            # 添加状态过滤条件

            if company_id not in (None, ''):
                sql_conditions.append("c.company_id = %s")
                sql_conditions_query.append("company_id = %s")

                # 添加状态过滤条件
            if account_status not in (None, ''):
                if account_status == "3":
                    sql_conditions.append("(c.account_state = %s or c.account_state = '4')")
                    sql_conditions_query.append("(account_state = %s or account_state = '4')")
                else:
                    sql_conditions.append("c.account_state = %s")
                    sql_conditions_query.append("account_state = %s")

            if operator not in (None, ''):
                sql_conditions.append("a.operator_id = %s")
                sql_conditions_query.append("operator_id = %s")

            if persaler not in (None, '', 0):
                sql_conditions.append("a.presales_id = %s")
                sql_conditions_query.append("presales_id = %s")
            elif persaler == 0:
                sql_conditions.append("a.presales_id is null")
                sql_conditions_query.append("presales_id is null")
                persaler = None

            if btnradio == "w" or persaler_list_value == "w" or room_num == "2":
                sql_conditions.append("c.room_count <30 and c.room_count >=10")
                sql_conditions_query.append("room_count <30 and room_count >=10")

            if btnradio == "s" or persaler_list_value == "s" or room_num == "1":
                sql_conditions.append("c.room_count >=30")
                sql_conditions_query.append("room_count >=30")

            if btnradio == "o" or persaler_list_value == "o" or room_num == "3":
                sql_conditions.append("(c.room_count <10  or c.room_count is null)")
                sql_conditions_query.append("(room_count <10  or room_count is null)")

            if task_status not in (None, ''):
                sql_conditions.append("a.progress_state = %s")
                sql_conditions_query.append("progress_state = %s")

            if date_select not in (None, ''):
                start_date, end_date = date_select.split(' - ')
                sql_conditions.append("left(a.create_data,10) between '%s' and '%s'" % (start_date, end_date))
                sql_conditions_query.append("left(create_data,10) between '%s' and '%s'" % (start_date, end_date))
                data_search = date_select
            else:
                data_search = ""

            if search_api not in (None, ''):
                sql_conditions.append("c.api_config is not null")
                sql_conditions_query.append("api_config is not null")

            if operating_sub not in (None, ''):
                # sql_conditions.append("c.api_config is not null")
                sql_conditions_query.append("(operating_sub_phone =%s or operating_sub_name =%s)")

            if star not in (None, ''):
                sql_conditions.append("a.stars = %s")
                sql_conditions_query.append("stars = %s")

            if api_channel not in (None, ''):
                sql_conditions.append("api.channel like %s")
                sql_conditions_query.append("api_channel like %s")

            if coo_name not in (None, ''):
                sql_conditions.append("coo.name like %s")
                sql_conditions_query.append("coo_name like %s")

            if search_tag not in (None, ''):
                sql_conditions.append("tag.name = %s")
                sql_conditions_query.append("tag = %s")

            if companyType not in (None, ''):
                sql_conditions.append("c.regi_infor like %s")
                sql_conditions_query.append("regi_infor like %s")

                # sql_conditions.append("video_name LIKE %s")  # query_params.append(f"%{video_name_search}%")

            # if room_num not in (None, ''):
            #     if room_num=="1":
            #         sql_conditions.append("c.room_count = %s")
            #         sql_conditions_query.append("room_count = %s")
            #     elif room_num=="2":
            #         sql_conditions.append("c.room_count <30 and c.room_count >=10")
            #         sql_conditions_query.append("room_count = %s")

            # 构建最终的 SQL 查询
            sql = '''
                    select * from (
select a.taskid,a.company_id,left(c.active_time,10)active_time,c.end_data,c.room_count,c.account_state,c.from_code,a.progress_state,left(a.create_data,10)create_data,
(select username from t_account where id=a.operator_id)operator,
(select username from t_account where id=a.presales_id)presales,
(select name from t_coop_ex where code=c.source)coo_name,
(select group_concat(phone) from t_operating_sub where FIND_IN_SET(a.company_id, `company_id`) > 0)operating_sub_phone,
(select group_concat(name) from t_operating_sub where FIND_IN_SET(a.company_id, `company_id`) > 0)operating_sub_name,
(select channel from t_api_channel where address=c.api_config)api_channel,c.api_config,c.global_sync,a.presales_id,
IFNULL(
    (SELECT GROUP_CONCAT(tag.name) 
     FROM t_presales_progress_tags tt 
     JOIN t_tags tag ON tt.tag_id = tag.id 
     WHERE tt.presales_progress_id = a.taskid),
    ""
) AS tag,
a.remark,a.step_one,a.step_two,a.step_three,a.step_four,a.step_five,a.step_six,c.affiliated_company,yetai_remark,xin_remark,c.company_name,a.contact,c.platform_count,c.regi_infor,if(stars is null,0,stars)stars
from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id)a''' + " WHERE " + " AND ".join(sql_conditions_query) + "  ORDER BY create_data desc, room_count desc"
            #            "  ORDER BY create_data desc, presales_id desc"

            print("今天的时间：" + formatted_data)
            # 获取总记录数
            total_count_sql = '''
                    select count(DISTINCT a.taskid)总数 from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id
																		LEFT JOIN t_api_channel api on c.api_config=api.address
																	  LEFT JOIN t_coop_ex coo on coo.code=c.source
																		LEFT JOIN t_presales_progress_tags tpt on a.taskid=tpt.presales_progress_id 
																		LEFT JOIN t_tags tag on tpt.tag_id=tag.id''' + " WHERE " + " AND ".join(sql_conditions)

            # 新记录
            new_count_sql = '''
                    select count(DISTINCT a.taskid)总数 from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id
																		LEFT JOIN t_api_channel api on c.api_config=api.address
																	  LEFT JOIN t_coop_ex coo on coo.code=c.source
																		LEFT JOIN t_presales_progress_tags tpt on a.taskid=tpt.presales_progress_id 
																		LEFT JOIN t_tags tag on tpt.tag_id=tag.id''' + " WHERE " + " AND ".join(
                sql_conditions) + " and left(create_data,10)=\"" + formatted_data + "\""

            # 未认领
            unclaimed_count_sql = '''
                                select count(DISTINCT a.taskid)总数 from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id
																		LEFT JOIN t_api_channel api on c.api_config=api.address
																	  LEFT JOIN t_coop_ex coo on coo.code=c.source
																		LEFT JOIN t_presales_progress_tags tpt on a.taskid=tpt.presales_progress_id 
																		LEFT JOIN t_tags tag on tpt.tag_id=tag.id''' + " WHERE " + " AND ".join(sql_conditions) + " and  presales_id is null"

            # 初步沟通
            step_one_count_sql = '''
                                            select count(DISTINCT a.taskid)总数 from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id
																		LEFT JOIN t_api_channel api on c.api_config=api.address
																	  LEFT JOIN t_coop_ex coo on coo.code=c.source
																		LEFT JOIN t_presales_progress_tags tpt on a.taskid=tpt.presales_progress_id 
																		LEFT JOIN t_tags tag on tpt.tag_id=tag.id''' + " WHERE " + " AND ".join(sql_conditions) + " and  progress_state=\"1\""

            # 直连
            step_two_count_sql = '''
                                                        select count(DISTINCT a.taskid)总数 from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id
																		LEFT JOIN t_api_channel api on c.api_config=api.address
																	  LEFT JOIN t_coop_ex coo on coo.code=c.source
																		LEFT JOIN t_presales_progress_tags tpt on a.taskid=tpt.presales_progress_id 
																		LEFT JOIN t_tags tag on tpt.tag_id=tag.id''' + " WHERE " + " AND ".join(sql_conditions) + " and  progress_state=\"3\""

            # 转售后
            step_four_count_sql = '''
                                                                    select count(DISTINCT a.taskid)总数 from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id
																		LEFT JOIN t_api_channel api on c.api_config=api.address
																	  LEFT JOIN t_coop_ex coo on coo.code=c.source
																		LEFT JOIN t_presales_progress_tags tpt on a.taskid=tpt.presales_progress_id 
																		LEFT JOIN t_tags tag on tpt.tag_id=tag.id''' + " WHERE " + " AND ".join(sql_conditions) + " and  progress_state=\"4\""

            # 放弃
            step_six_count_sql = '''
                                                                                select count(DISTINCT a.taskid)总数 from t_presales_progress a LEFT JOIN t_company c on a.company_id=c.company_id
																		LEFT JOIN t_api_channel api on c.api_config=api.address
																	  LEFT JOIN t_coop_ex coo on coo.code=c.source
																		LEFT JOIN t_presales_progress_tags tpt on a.taskid=tpt.presales_progress_id 
																		LEFT JOIN t_tags tag on tpt.tag_id=tag.id''' + " WHERE " + " AND ".join(sql_conditions) + " and  progress_state=\"6\""

            print(sql)

            if operating_sub not in (None, ''):
                query_params_operating_sub = tuple(
                    param for param in [company_id, account_status, operator, persaler, task_status, operating_sub, operating_sub, star, f"%{api_channel}%", f"%{coo_name}%", search_tag,f"%{companyType}%"] if
                    param is not None and param != '' and param != '%%' and param != '%None%')

                cursor.execute(sql, query_params_operating_sub)
                results = cursor.fetchall()
                total_count = ""
                new_count = ""
                unclaimed_count = ""
                step_one_count = ""
                step_two_count = ""
                step_four_count = ""
                step_six_count = ""
            else:

                # 有查询条件用
                if company_id not in (None, '') or account_status not in (None, '') or operator not in (None, '') or task_status not in (None, '') or persaler not in (None, '', 0) or star not in (
                None, '', 0) or api_channel not in (None, '', 0) or coo_name not in (None, '', 0) or search_tag not in (None, '', 0) or companyType not in (None, '', 0):
                    query_params = tuple(
                        param for param in [company_id, account_status, operator, persaler, task_status, operating_sub, operating_sub, star, f"%{api_channel}%", f"%{coo_name}%", search_tag,f"%{companyType}%"] if
                        param is not None and param != '' and param != '%%' and param != '%None%')

                    cursor.execute(sql, query_params)
                    results = cursor.fetchall()

                    cursor.execute(total_count_sql, query_params)
                    total_count = cursor.fetchone()['总数']

                    cursor.execute(new_count_sql, query_params)
                    new_count = cursor.fetchone()['总数']

                    cursor.execute(unclaimed_count_sql, query_params)
                    unclaimed_count = cursor.fetchone()['总数']

                    cursor.execute(step_one_count_sql, query_params)
                    step_one_count = cursor.fetchone()['总数']

                    cursor.execute(step_two_count_sql, query_params)
                    step_two_count = cursor.fetchone()['总数']

                    cursor.execute(step_four_count_sql, query_params)
                    step_four_count = cursor.fetchone()['总数']

                    cursor.execute(step_six_count_sql, query_params)
                    step_six_count = cursor.fetchone()['总数']

                else:
                    cursor.execute(sql)
                    results = cursor.fetchall()

                    cursor.execute(total_count_sql)
                    total_count = cursor.fetchone()['总数']

                    cursor.execute(new_count_sql)
                    new_count = cursor.fetchone()['总数']

                    cursor.execute(unclaimed_count_sql)
                    unclaimed_count = cursor.fetchone()['总数']

                    cursor.execute(step_one_count_sql)
                    step_one_count = cursor.fetchone()['总数']

                    cursor.execute(step_two_count_sql)
                    step_two_count = cursor.fetchone()['总数']

                    cursor.execute(step_four_count_sql)
                    step_four_count = cursor.fetchone()['总数']

                    cursor.execute(step_six_count_sql)
                    step_six_count = cursor.fetchone()['总数']

            return results, total_count, new_count, persaler_list_value, operator_name, persaler_names, unclaimed_count, step_one_count, step_two_count, data_search, step_four_count, step_six_count

    except Exception as e:
        print(f"Error get_presales_progress: {e}")
    finally:
        conn.close()


# 读取数据
def get_presales_progress_id(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_presales_progress
                WHERE taskid = %s
            '''
            cursor.execute(sql, id)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Error get_presales_progress_id: {e}")
    finally:
        conn.close()


def get_presales_progress_id(id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                SELECT * FROM t_presales_progress
                WHERE taskid = %s
            '''
            cursor.execute(sql, id)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Error get_presales_progress_id: {e}")
    finally:
        conn.close()


def update_contact(company_id=None, contact=None, id=None, yetai_remark=None, xin_remark=None):
    conn = get_db_connection();

    try:
        with conn.cursor() as cursor:
            sql = '''
                      select taskid from t_presales_progress where company_id=%s      
                        '''
            cursor.execute(sql, (company_id))
            result = cursor.fetchone()
            # print(result['taskid'])
            # print(id)
            if result is not None:
                if result['taskid'] != int(id):
                    sql = '''
                           DELETE from t_presales_progress where taskid=%s  
                                            '''
                    cursor.execute(sql, (result['taskid']))
                    conn.commit()

            sql = '''
                UPDATE `dh_support`.`t_presales_progress` 
                SET `contact`=%s,company_id=%s,yetai_remark=%s,xin_remark=%s
                WHERE `taskid`=%s
            '''
            cursor.execute(sql, (contact, company_id, yetai_remark, xin_remark, id))
            conn.commit()
    except Exception as e:
        print(f"Error update_contact: {e}")
    finally:
        conn.close()


# 检查认领
def get_presales_by_taskid(taskid):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            search_claim_sql = '''
                select * from t_presales_progress a LEFT JOIN t_account b on a.presales_id=b.id where taskid=%s
            '''
            cursor.execute(search_claim_sql, (taskid))
            result = cursor.fetchone()
            presales = result['presales_id']
            username = result['username']
            return presales, username
    except Exception as e:
        print(f"Error in update_claim_presales: {e}")
    finally:
        conn.close()


# 认领
def update_claim_presales(presales_id, current_user_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = '''
                 UPDATE `dh_support`.`t_presales_progress` SET `presales_id`=%s WHERE `taskid`=%s;
             '''
            cursor.execute(sql, (current_user_id, presales_id))
            conn.commit()
            return "success"
    except Exception as e:
        print(f"Error in update_claim_presales: {e}")
    finally:
        conn.close()


# 批量认领
def batch_update_claim_presales(task_ids, current_user_id):
    # 获取数据库连接
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            # 检查 task_ids 是否为空
            if not task_ids:
                print("任务 ID 列表为空")
                return False

            # 构造 IN 子句的占位符 (%s)
            placeholders = ', '.join(['%s'] * len(task_ids))
            sql = f'''
                UPDATE `dh_support`.`t_presales_progress` 
                SET `presales_id` = %s 
                WHERE `taskid` IN ({placeholders});
            '''

            # 构造参数列表：[current_user_id, task_id1, task_id2, ...]
            params = [current_user_id] + task_ids

            # 执行 SQL 查询
            cursor.execute(sql, params)

            # 提交事务
            conn.commit()
            return True

    except Exception as e:
        # 捕获异常并打印错误信息
        print(f"Error in batch_update_claim_presales: {e}")
        conn.rollback()  # 回滚事务以确保数据一致性
        return False

    finally:
        # 确保关闭数据库连接
        if conn:
            conn.close()


# 更新数据

def update_presales_progress(id, progress_state, remark, current_user_id):
    conn = get_db_connection()
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    resultid = get_username(current_user_id)
    current_remark = ""

    time_line = resultid["username"] + "<br>" + formatted_time
    stateupadate = ""
    new_value = ""
    remark_add = ""
    if progress_state == "1":
        stateupadate = "step_one"
    elif progress_state == "2":
        stateupadate = "step_two"
    elif progress_state == "3":
        stateupadate = "step_three"
    elif progress_state == "4":
        stateupadate = "step_four"
    # elif progress_state == "5":
    #     stateupadate = "step_five"
    # elif progress_state == "6":
    #     stateupadate = "step_six"

    # if remark not in (None, ''):
    #     # remark_add=remark+"<br>"+"---"+"<b>"+resultid["username"]+"</b><br>"
    #     # remark_add = remark +"\n"

    try:
        # 使用 with 语句确保游标在使用完毕后被关闭
        with closing(conn.cursor()) as cursor:

            # get_progress_state_sql="select progress_state from t_presales_progress where taskid=%s"
            # cursor.execute(get_progress_state_sql, (id))
            # get_progress_state_result = cursor.fetchone()
            # old_progress_state = get_progress_state_result["progress_state"]
            # if progress_state!=old_progress_state:
            # sql = '''
            #                     select remark from t_presales_progress where taskid=%s
            #       '''
            # cursor.execute(sql, (id))
            # result =  cursor.fetchone()
            # old_remark=result["remark"]
            # new_remark = f"{old_remark}\n{remark_add}"
            if progress_state == "5" or progress_state == "6" or progress_state == "7":
                sql = '''
                     UPDATE t_presales_progress  SET progress_state = %s, remark = %s,updata_date = %s,operator_id=%s  WHERE taskid =%s
                '''
                cursor.execute(sql, (progress_state, remark, formatted_time, current_user_id, id))
            else:
                sql = '''
                    UPDATE t_presales_progress  SET progress_state = %s, remark = %s,updata_date = %s,operator_id=%s,''' + stateupadate + "=%s WHERE taskid =%s"

                # 在 with 语句块内执行 SQL
                cursor.execute(sql, (progress_state, remark, formatted_time, current_user_id, time_line, id))

            # 提交事务
            conn.commit()  # else:  #     sql = '''  #                                 UPDATE t_presales_progress  SET current_remark = %s,updata_date = %s,operator_id=%s WHERE taskid =%s'''  #  #     # 在 with 语句块内执行 SQL  #     cursor.execute(sql, (remark, formatted_time, current_user_id,id))  #  #     # 提交事务  #     conn.commit()

    except Exception as e:
        # 回滚事务以防数据不一致
        conn.rollback()
        print(f"Error update_coop_ex: {e}")

    finally:
        # 关闭数据库连接
        conn.close()


# 售前添加新公司
def presales_progress_add(company_id, current_user_id, remark="", contact="", yetai_remark="", xin_remark=""):
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M")
    mouth_time = current_time.strftime("%Y-%m")
    resultid = get_username(current_user_id)
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if is_integer(company_id):
                sql = '''
                    SELECT count(*)num FROM t_presales_progress
                    WHERE company_id = %s
                '''
                cursor.execute(sql, company_id)
                result = cursor.fetchone()
                if result["num"] > 0:
                    return 1

            step_one = resultid["username"] + "<br>" + formatted_time
            add_sql = '''
                    INSERT INTO `dh_support`.`t_presales_progress` (`company_id`, `operator_id`, `progress_state`, `remark`, `step_one`,`create_data`,idx_data,contact,yetai_remark,xin_remark) VALUES (%s,%s,"1",%s,%s,%s,%s,%s,%s,%s)
            '''

            cursor.execute(add_sql, (company_id, current_user_id, remark, step_one, formatted_time, mouth_time, contact, yetai_remark, xin_remark))
            conn.commit()
            if is_integer(company_id):
                with conn.cursor() as cursor:
                    sql = '''
                        select count(*)num from t_company where company_id =%s
                    '''
                    cursor.execute(sql, company_id)
                    result = cursor.fetchone()
                    if result["num"] > 0:
                        return cursor.lastrowid
                    else:
                        single_company_update(company_id)




    except Exception as e:
        print(f"Error add_presales_progress: {e}")
    finally:
        conn.close()


def uupdate_presales_scale_impl(current_user_id=None, selectedValue=None):
    conn = get_db_connection()
    persaler_list = None
    if selectedValue == "btnradio2":
        persaler_list = "w"
    elif selectedValue == "btnradio3":
        persaler_list = "s"
    elif selectedValue == "btnradio4":
        persaler_list = "o"
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

#售前统计
def get_stat_presales():
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "select * from t_stat_presales order by stat_day desc"
            cursor.execute(sql)
            results = cursor.fetchall()

            sum_sql='''
                 select CONCAT(b.start_day,"~",b.end_day) AS week,a.*,b.*  from (
                select stat_day,presales_id,claim,step_one,step_three,step_four,step_six,tag_replay,tag_track from t_stat_presales)a LEFT JOIN (
                SELECT 
                    DATE_ADD(MIN(stat_day), INTERVAL (6 - WEEKDAY(MIN(stat_day))) DAY) AS last_day_of_week,
                    MIN(stat_day) AS start_day,
                    MAX(stat_day) AS end_day,
                    presales_id,
                    name,
                    SUM(single_claim) AS single_claim,
                    SUM(single_step_three) AS single_step_three,
                    SUM(single_step_four) AS single_step_four,
                    SUM(single_step_six) AS single_step_six
                FROM 
                    t_stat_presales
                GROUP BY 
                    YEAR(stat_day),
                    WEEK(stat_day, 1),  -- 使用模式1表示周从周一开始
                    presales_id,
                    NAME
                ORDER BY 
                    last_day_of_week)b on a.presales_id = b.presales_id and a.stat_day=b.last_day_of_week where b.last_day_of_week is not null ORDER BY a.stat_day desc;
            '''
            cursor.execute(sum_sql)
            week_results = cursor.fetchall()

            stat_sql = '''
                        SELECT 
                        COUNT(*) AS stat_count,
                        SUM(CASE WHEN presales_id IS NOT NULL THEN 1 ELSE 0 END) AS stat_claim,
                        SUM(CASE WHEN presales_id IS NOT NULL AND progress_state = '1' THEN 1 ELSE 0 END) AS stat_step_one,
                        SUM(CASE WHEN presales_id IS NOT NULL AND progress_state = '3' THEN 1 ELSE 0 END) AS stat_step_three,
                        SUM(CASE WHEN presales_id IS NOT NULL AND progress_state = '4' THEN 1 ELSE 0 END) AS stat_step_four,
                        SUM(CASE WHEN presales_id IS NOT NULL AND progress_state = '6' THEN 1 ELSE 0 END) AS stat_step_six
                    FROM 
                        t_presales_progress;
            
            '''

            cursor.execute(stat_sql)
            count_results = cursor.fetchall()


            return results,week_results,count_results

    except Exception as e:
        print(f"Error get_stat_presales: {e}")
        return jsonify({"success": False, "message": str(e)})  # 返回错误信息
    finally:
        conn.close()




# 售前认领统计
# def get_stat_presales_claim(search_date=None):
#     conn = get_db_connection()
#     today = datetime.now().date().strftime("%Y-%m-%d")
#     try:
#         with conn.cursor() as cursor:
#             # 构建基础SQL条件
#             sql_conditions = ["1=1"]
#             if search_date not in (None, ''):
#                 if search_date == 'today':
#                     sql_conditions.append(f"left(create_data, 10) = '{today}'")
#                 elif search_date == 'week':
#                     week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
#                     sql_conditions.append(f"left(create_data, 10) BETWEEN '{week_ago}' AND '{today}'")
#                 elif search_date == 'month':
#                     month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
#                     sql_conditions.append(f"left(create_data, 10) BETWEEN '{month_ago}' AND '{today}'")
#
#             # 主查询：按日期分组统计
#             main_sql = f'''
#                 SELECT
#                     g.name,
#                     g.create_date,
#                     g.total,
#                     g.state1,
#                     g.state3,
#                     g.state4,
#                     g.state7,
#                     g.state5,
#                     g.state6,
#                     s.date_total AS total_all_records,
#                     s.date_null_presales AS total_null_presales
#                 FROM (
#                     -- 销售人员分组统计
#                     SELECT
#                         (SELECT realname FROM t_account WHERE id = p.presales_id) AS name,
#                         LEFT(create_data, 10) AS create_date,
#                         COUNT(*) AS total,
#                         SUM(CASE WHEN progress_state = 1 THEN 1 ELSE 0 END) AS state1,
#                         SUM(CASE WHEN progress_state = 3 THEN 1 ELSE 0 END) AS state3,
#                         SUM(CASE WHEN progress_state = 4 THEN 1 ELSE 0 END) AS state4,
#                         SUM(CASE WHEN progress_state = 7 THEN 1 ELSE 0 END) AS state7,
#                         SUM(CASE WHEN progress_state = 5 THEN 1 ELSE 0 END) AS state5,
#                         SUM(CASE WHEN progress_state = 6 THEN 1 ELSE 0 END) AS state6
#                     FROM t_presales_progress p
#                     WHERE {' AND '.join(sql_conditions)}
#                     AND presales_id IS NOT NULL
#                     GROUP BY name, LEFT(create_data, 10)
#                 ) g
#                 JOIN (
#                     -- 每日统计
#                     SELECT
#                         LEFT(create_data, 10) AS date,
#                         COUNT(*) AS date_total,
#                         SUM(CASE WHEN presales_id IS NULL THEN 1 ELSE 0 END) AS date_null_presales
#                     FROM t_presales_progress
#                     WHERE {' AND '.join(sql_conditions)}
#                     GROUP BY LEFT(create_data, 10)
#                 ) s ON g.create_date = s.date
#                 ORDER BY g.create_date DESC, g.total DESC
#             '''
#
#             cursor.execute(main_sql)
#             results = cursor.fetchall()
#
#             # 预处理数据，添加rowspan信息
#             processed_results = []
#             date_groups = {}
#
#             # 先按日期分组
#             for row in results:
#                 if row['create_date'] not in date_groups:
#                     date_groups[row['create_date']] = []
#                 date_groups[row['create_date']].append(row)
#
#             # 为每个日期组的行添加rowspan信息
#             for date, rows in date_groups.items():
#                 row_count = len(rows)
#                 for i, row in enumerate(rows):
#                     row['show_date'] = (i == 0)  # 只有每组的第一行显示日期
#                     row['rowspan'] = row_count if i == 0 else 0
#                     processed_results.append(row)
#
#             return processed_results
#     except Exception as e:
#         print(f"Error in get_stat_presales_claim: {e}")
#         return None
#     finally:
#         conn.close()


# 更新标签
def update_save_tags(taskid=None, tags=None):
    if taskid is None:
        print("Error: company_id cannot be None")
        return

    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            # 1. 删除原有标签记录
            delete_sql = "DELETE FROM t_presales_progress_tags WHERE presales_progress_id = %s"
            cursor.execute(delete_sql, (taskid,))

            # 2. 如果没有新标签，直接提交并返回
            if not tags or tags.strip() == '':
                conn.commit()
                return

            # 3. 分割标签字符串为列表
            tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]

            # 4. 插入新标签
            insert_sql = """
                INSERT INTO t_presales_progress_tags (presales_progress_id, tag_id)
                VALUES (%s, %s)
            """
            for tag_id in tag_list:
                cursor.execute(insert_sql, (taskid, tag_id))

            # 5. 提交事务
            conn.commit()

    except Exception as e:
        print(f"Error update_save_tags: {e}")
        conn.rollback()  # 出错回滚
    finally:
        conn.close()


def update_stat_presales():
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            # 1. 删除原有标签记录
            updata_sql = '''
                select  DATE(NOW() - INTERVAL 1 DAY) stat_day,presales_id,realname,认领,初步沟通,直连,转售后,放弃,复盘,重点跟踪,IFNULL(新增认领, 0) 新增认领,IFNULL(新增直连, 0) 新增直连,IFNULL(新增转售后, 0) 新增转售后,IFNULL(新增放弃, 0) 新增放弃 from (
                select * from (
                SELECT
                        a.presales_id,
                    b.realname,
                    COUNT(DISTINCT a.taskid) AS 认领,
                    SUM(CASE WHEN a.progress_state = '1' THEN 1 ELSE 0 END) AS 初步沟通,
                    SUM(CASE WHEN a.progress_state = '3' THEN 1 ELSE 0 END) AS 直连,
                    SUM(CASE WHEN a.progress_state = '4' THEN 1 ELSE 0 END) AS 转售后,
                    SUM(CASE WHEN a.progress_state = '6' THEN 1 ELSE 0 END) AS 放弃,
                    SUM(CASE WHEN tags.tag_id = '1' THEN 1 ELSE 0 END) AS 复盘,
                    SUM(CASE WHEN tags.tag_id = '2' THEN 1 ELSE 0 END) AS 重点跟踪		
                FROM 
                    t_presales_progress a
                LEFT JOIN 
                    t_account b ON a.presales_id = b.id
                LEFT JOIN (
                    SELECT DISTINCT presales_progress_id, tag_id
                    FROM t_presales_progress_tags
                ) AS tags ON a.taskid = tags.presales_progress_id
                WHERE 
                    a.presales_id IS NOT NULL and a.presales_id not in (3,8)
                GROUP BY 
                    a.presales_id)A LEFT JOIN 
                
                (SELECT 
                    a.user_id,
                -- 		a.operation_desc,
                --     b.username,
                        count(*) "新增认领"
                FROM 
                    t_operation_log a
                LEFT JOIN 
                    t_account b ON a.user_id = b.id
                INNER JOIN (
                    SELECT 
                        operation_id,
                        MAX(operation_time) AS max_time
                    FROM 
                        t_operation_log
                    WHERE 
                        operation_desc ="认领"
                        AND LEFT(operation_time, 10) = DATE(NOW() - INTERVAL 1 DAY)
                    GROUP BY 
                        operation_id
                ) latest
                ON a.operation_id = latest.operation_id AND a.operation_time = latest.max_time
                WHERE 
                    a.operation_desc ="认领"
                    AND LEFT(a.operation_time, 10) = DATE(NOW() - INTERVAL 1 DAY) GROUP BY operation_desc,username)B on A.presales_id=B.user_id
                
                LEFT JOIN
                
                (SELECT 
                    a.user_id Cuser_id,
                -- 		a.operation_desc,
                --     b.username,
                        count(*) "新增直连"
                FROM 
                    t_operation_log a
                LEFT JOIN 
                    t_account b ON a.user_id = b.id
                INNER JOIN (
                    SELECT 
                        operation_id,
                        MAX(operation_time) AS max_time
                    FROM 
                        t_operation_log
                    WHERE 
                        operation_desc ="直连"
                        AND LEFT(operation_time, 10) = DATE(NOW() - INTERVAL 1 DAY)
                    GROUP BY 
                        operation_id
                ) latest
                ON a.operation_id = latest.operation_id AND a.operation_time = latest.max_time
                WHERE 
                    a.operation_desc ="直连"
                    AND LEFT(a.operation_time, 10) = DATE(NOW() - INTERVAL 1 DAY) GROUP BY operation_desc,username)C on A.presales_id=C.Cuser_id
                LEFT JOIN
                
                (SELECT 
                    a.user_id Duser_id,
                -- 		a.operation_desc,
                --     b.username,
                        count(*) "新增转售后"
                FROM 
                    t_operation_log a
                LEFT JOIN 
                    t_account b ON a.user_id = b.id
                INNER JOIN (
                    SELECT 
                        operation_id,
                        MAX(operation_time) AS max_time
                    FROM 
                        t_operation_log
                    WHERE 
                        operation_desc ="转售后"
                        AND LEFT(operation_time, 10) = DATE(NOW() - INTERVAL 1 DAY)
                    GROUP BY 
                        operation_id
                ) latest
                ON a.operation_id = latest.operation_id AND a.operation_time = latest.max_time
                WHERE 
                    a.operation_desc ="转售后"
                    AND LEFT(a.operation_time, 10) = DATE(NOW() - INTERVAL 1 DAY) GROUP BY operation_desc,username)D on A.presales_id=D.Duser_id
                
                LEFT JOIN
                
                (SELECT 
                    a.user_id Euser_id,
                -- 		a.operation_desc,
                --     b.username,
                        count(*) "新增放弃"
                FROM 
                    t_operation_log a
                LEFT JOIN 
                    t_account b ON a.user_id = b.id
                INNER JOIN (
                    SELECT 
                        operation_id,
                        MAX(operation_time) AS max_time
                    FROM 
                        t_operation_log
                    WHERE 
                        operation_desc ="放弃"
                        AND LEFT(operation_time, 10) = DATE(NOW() - INTERVAL 1 DAY)
                    GROUP BY 
                        operation_id
                ) latest
                ON a.operation_id = latest.operation_id AND a.operation_time = latest.max_time
                WHERE 
                    a.operation_desc ="放弃"
                    AND LEFT(a.operation_time, 10) = DATE(NOW() - INTERVAL 1 DAY) GROUP BY operation_desc,username)E on A.presales_id=E.Euser_id
                
                )F           
            '''

            insert_sql = '''
                            INSERT INTO `dh_support`.`t_stat_presales` (`stat_day`,`presales_id`,`name`, `claim`, `step_one`, `step_three`, `step_four`, `step_six`, `tag_replay`, `tag_track`, `single_claim`, `single_step_three`, `single_step_four`, `single_step_six`) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                            
            cursor.execute(updata_sql)
            results = cursor.fetchall()

            if len(results) > 0:
               for result in results:
                   cursor.execute(insert_sql, (result['stat_day'], result['presales_id'], result['realname'], result['认领'], result['初步沟通'], result['直连'], result['转售后'], result['放弃'],
                                               result['复盘'], result['重点跟踪'], result['新增认领'], result['新增直连'], result['新增转售后'], result['新增放弃']))

            conn.commit()

            # 5. 提交事务


    except Exception as e:
        print(f"Error update_stat_presales: {e}")
        conn.rollback()  # 出错回滚
    finally:
        conn.close()


# def refresh_database_with_date(refresh_date=None):
#     conn = get_db_connection()
# 
#     try:
#         with conn.cursor() as cursor:
#             # 1. 删除原有标签记录
#             refresh_sql = "DELETE FROM t_presales_progress_tags WHERE presales_progress_id = %s"
#             cursor.execute(delete_sql, (taskid,))
# 
# 
#             # 3. 分割标签字符串为列表
#             tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
# 
#             # 4. 插入新标签
#             insert_sql = """
#                 INSERT INTO t_presales_progress_tags (presales_progress_id, tag_id)
#                 VALUES (%s, %s)
#             """
#             for tag_id in tag_list:
#                 cursor.execute(insert_sql, (taskid, tag_id))
# 
#             # 5. 提交事务
#             conn.commit()
# 
#     except Exception as e:
#         print(f"Error update_save_tags: {e}")
#         conn.rollback()  # 出错回滚
#     finally:
#         conn.close()

